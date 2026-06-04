#!/usr/bin/env python3
"""
PCA Orchestrator Agent - Control Plane

Manages workflow dispatch, routing decisions, escalations, and monthly calibration.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import json
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Orchestrator", version="1.0.0")

# Load routing rules and policies
ROUTING_RULES_PATH = Path.home() / "personal-cognitive-architecture" / "data" / "routing-rules.json"
CONFIG_PATH = Path.home() / "personal-cognitive-architecture" / "data"


class RoutingAction(str, Enum):
    ADVANCE_TO_INTEGRATION = "ADVANCE_TO_INTEGRATION"
    ROUTE_WITH_TAG = "ROUTE_WITH_TAG"
    ESCALATE_FOR_REVIEW = "ESCALATE_FOR_REVIEW"
    QUEUE_FOR_REVIEW = "QUEUE_FOR_REVIEW"
    QUARANTINE = "QUARANTINE"


class CaptureRequest(BaseModel):
    """Request to process a capture through the pipeline"""
    source_type: str  # voice, text, article, signal
    content: str
    domain: Optional[str] = ""
    tags: List[str] = []
    sensitivity: str = "public"
    confidence: float = 0.5
    timestamp: str


class RoutingPolicy(BaseModel):
    """Policy for routing decisions"""
    rule_id: str
    condition: str  # e.g., "confidence >= 0.85 AND source_type == 'article'"
    action: RoutingAction
    destination: str
    escalation_reason: Optional[str] = None
    priority: int = 0


class PCAOrchestrator:
    """
    Control plane for the PCA system.

    Responsibilities:
    - Load and apply routing policies
    - Dispatch captures to appropriate workers
    - Handle escalations
    - Manage monthly calibration
    - Track metrics for feedback loop
    """

    def __init__(self):
        self.routing_rules = self._load_routing_rules()
        self.policies = self._load_policies()
        self.escalation_queue = []
        self.monthly_metrics = {}

    def _load_routing_rules(self) -> Dict:
        """Load routing rules from routing-rules.json"""
        try:
            with open(ROUTING_RULES_PATH, 'r') as f:
                return json.load(f)
        except:
            logger.warning("Could not load routing rules, using defaults")
            return self._default_routing_rules()

    def _load_policies(self) -> List[RoutingPolicy]:
        """Load policies from configuration"""
        # In production, load from data/policies.json
        # For now, use built-in policies
        return self._default_policies()

    def _default_routing_rules(self) -> Dict:
        """Default routing rules"""
        return {
            "route-001": {
                "name": "High confidence structured",
                "condition": "confidence >= 0.85 AND type == 'article'",
                "action": "ADVANCE_TO_INTEGRATION",
                "destination": "10-Projects/[project]/Notes/"
            },
            "route-002": {
                "name": "Provisional structured",
                "condition": "0.65 <= confidence < 0.85 AND type == 'article'",
                "action": "ROUTE_WITH_TAG",
                "destination": "20-Ideas/Unstructured/"
            },
            "route-003": {
                "name": "Unstructured ideas",
                "condition": "type == 'text'",
                "action": "ROUTE_WITH_TAG",
                "destination": "20-Ideas/Unstructured/"
            },
            "route-004": {
                "name": "Critical signal",
                "condition": "type == 'signal' AND signal_strength >= 0.8",
                "action": "ESCALATE_FOR_REVIEW",
                "destination": "40-Escalations/signals/"
            },
            "route-005": {
                "name": "Moderate signal",
                "condition": "type == 'signal' AND 0.5 <= signal_strength < 0.8",
                "action": "ROUTE_WITH_TAG",
                "destination": "20-Ideas/Unstructured/"
            },
            "route-006": {
                "name": "Low signal",
                "condition": "type == 'signal' AND signal_strength < 0.5",
                "action": "ROUTE_WITH_TAG",
                "destination": "40-Archive/"
            },
            "route-007": {
                "name": "Sensitive content",
                "condition": "sensitivity == 'sensitive'",
                "action": "QUARANTINE",
                "destination": "40-Archive/sensitive/",
                "escalation_reason": "sensitive_content"
            },
            "route-008": {
                "name": "Contradictions detected",
                "condition": "has_contradictions == true",
                "action": "ESCALATE_FOR_REVIEW",
                "destination": "40-Escalations/contradictions/",
                "escalation_reason": "contradictions_detected"
            },
            "route-009": {
                "name": "Very low confidence",
                "condition": "confidence < 0.4",
                "action": "QUARANTINE",
                "destination": "40-Archive/quarantine/",
                "escalation_reason": "very_low_confidence"
            }
        }

    def _default_policies(self) -> List[RoutingPolicy]:
        """Default policies"""
        return []

    async def dispatch_capture(self, request: CaptureRequest) -> Dict:
        """
        Main orchestration logic.

        1. Receive capture from ingestion worker
        2. Send to validation worker for scoring
        3. Apply routing rules
        4. Dispatch to destination or escalate
        5. Log for feedback loop
        """
        logger.info(f"Dispatching capture: {request.source_type} from {request.domain}")

        try:
            # Step 1: Send to validation worker
            validation_result = await self._call_validation_worker(request)

            if not validation_result["success"]:
                return self._escalate_capture(request, "validation_failed")

            # Step 2: Extract routing decision
            routing = validation_result["routing_decision"]
            confidence = routing["confidence"]

            # Step 3: Apply escalation logic
            if routing["requires_escalation"]:
                return self._escalate_capture(request, routing["escalation_reason"])

            # Step 4: Route to destination
            return self._route_capture(request, routing)

        except Exception as e:
            logger.error(f"Orchestration error: {str(e)}")
            return self._escalate_capture(request, "orchestration_error")

    async def _call_validation_worker(self, request: CaptureRequest) -> Dict:
        """Call validation worker for scoring"""
        import aiohttp

        payload = {
            "type": request.source_type,
            "content": request.content,
            "domain": request.domain,
            "source": "orchestrator",
            "timestamp": request.timestamp,
            "tags": request.tags,
            "sensitivity": request.sensitivity,
            "confidence_input": request.confidence
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://127.0.0.1:8001/validate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        return {"success": True, "routing_decision": await resp.json()}
                    else:
                        return {"success": False, "error": f"Validation returned {resp.status}"}
        except Exception as e:
            logger.error(f"Validation worker error: {str(e)}")
            return {"success": False, "error": str(e)}

    def _route_capture(self, request: CaptureRequest, routing: Dict) -> Dict:
        """Route capture to final destination"""
        logger.info(f"Routing to: {routing['destination']} (action: {routing['routing_action']})")

        return {
            "success": True,
            "action": routing["routing_action"],
            "destination": routing["destination"],
            "confidence": routing["confidence"],
            "tags": routing.get("tags", []),
            "timestamp": datetime.now().isoformat()
        }

    def _escalate_capture(self, request: CaptureRequest, reason: str) -> Dict:
        """Escalate capture for human review"""
        logger.warning(f"Escalating capture: {reason}")

        escalation = {
            "id": f"escalation-{datetime.now().timestamp()}",
            "source_type": request.source_type,
            "content": request.content,
            "domain": request.domain,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "status": "pending_review"
        }

        self.escalation_queue.append(escalation)

        return {
            "success": True,
            "action": "ESCALATE_FOR_REVIEW",
            "destination": "40-Escalations/manual-review/",
            "escalation_id": escalation["id"],
            "reason": reason,
            "timestamp": escalation["timestamp"]
        }

    async def handle_escalation_resolution(self, escalation_id: str, user_action: str, feedback: str) -> Dict:
        """
        Handle user resolution of an escalated item.

        user_action: "approved" | "rejected" | "reclassified"
        feedback: User's classification or notes
        """
        logger.info(f"Resolving escalation {escalation_id}: {user_action}")

        # Find escalation
        escalation = next((e for e in self.escalation_queue if e["id"] == escalation_id), None)

        if not escalation:
            raise HTTPException(status_code=404, detail="Escalation not found")

        # Record feedback for monthly calibration
        self._record_feedback(escalation, user_action, feedback)

        # Update escalation status
        escalation["status"] = "resolved"
        escalation["user_action"] = user_action
        escalation["user_feedback"] = feedback
        escalation["resolved_at"] = datetime.now().isoformat()

        return escalation

    def _record_feedback(self, escalation: Dict, action: str, feedback: str):
        """Record feedback for monthly calibration cycle"""
        feedback_entry = {
            "type": "escalation_resolution",
            "escalation_id": escalation["id"],
            "source_type": escalation["source_type"],
            "user_action": action,
            "user_feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }

        # Append to feedback log
        feedback_log = Path.home() / "personal-cognitive-architecture" / "data" / "feedback-log.jsonl"
        with open(feedback_log, "a") as f:
            f.write(json.dumps(feedback_entry) + "\n")

        logger.info(f"Recorded feedback for calibration")

    async def monthly_calibration(self) -> Dict:
        """
        Monthly calibration cycle.

        1. Collect all feedback from past month
        2. Calculate accuracy by pattern
        3. Analyze weight sensitivity
        4. Recommend weight adjustments
        5. Apply changes with user approval
        """
        logger.info("Starting monthly calibration cycle")

        # Step 1: Collect feedback
        feedback = self._collect_monthly_feedback()

        # Step 2: Calculate accuracy
        accuracy_by_pattern = self._calculate_accuracy_by_pattern(feedback)

        # Step 3: Analyze sensitivity
        weight_sensitivity = self._analyze_weight_sensitivity(feedback)

        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(accuracy_by_pattern, weight_sensitivity)

        return {
            "month": datetime.now().strftime("%Y-%m"),
            "accuracy_by_pattern": accuracy_by_pattern,
            "weight_sensitivity": weight_sensitivity,
            "recommendations": recommendations,
            "requires_approval": True,
            "approval_deadline": (datetime.now() + timedelta(days=7)).isoformat()
        }

    def _collect_monthly_feedback(self) -> List[Dict]:
        """Collect feedback from past month"""
        feedback_log = Path.home() / "personal-cognitive-architecture" / "data" / "feedback-log.jsonl"
        cutoff_date = datetime.now() - timedelta(days=30)
        feedback = []

        if feedback_log.exists():
            with open(feedback_log, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    entry_date = datetime.fromisoformat(entry["timestamp"])
                    if entry_date >= cutoff_date:
                        feedback.append(entry)

        return feedback

    def _calculate_accuracy_by_pattern(self, feedback: List[Dict]) -> Dict:
        """Calculate accuracy by ingestion pattern"""
        patterns = {"voice": [], "article": [], "text": [], "signal": []}

        for entry in feedback:
            pattern = entry.get("source_type", "text")
            if pattern in patterns:
                # accuracy: 1.0 if approved, 0.0 if rejected, 0.5 if reclassified
                accuracy_score = {
                    "approved": 1.0,
                    "rejected": 0.0,
                    "reclassified": 0.5
                }.get(entry.get("user_action"), 0.5)

                patterns[pattern].append(accuracy_score)

        # Calculate means
        result = {}
        for pattern, scores in patterns.items():
            if scores:
                result[pattern] = {
                    "accuracy": sum(scores) / len(scores),
                    "count": len(scores)
                }

        return result

    def _analyze_weight_sensitivity(self, feedback: List[Dict]) -> Dict:
        """Analyze which scoring weights have most impact"""
        # Simplified: track what corrections users made most
        corrections = {}

        for entry in feedback:
            if entry.get("user_action") == "reclassified":
                feedback_text = entry.get("user_feedback", "")
                # Count mentions of different scoring factors
                if "credibility" in feedback_text.lower():
                    corrections["credibility"] = corrections.get("credibility", 0) + 1
                if "relevance" in feedback_text.lower():
                    corrections["relevance"] = corrections.get("relevance", 0) + 1
                if "novelty" in feedback_text.lower():
                    corrections["novelty"] = corrections.get("novelty", 0) + 1

        return corrections

    def _generate_recommendations(self, accuracy: Dict, sensitivity: Dict) -> List[Dict]:
        """Generate weight adjustment recommendations"""
        recommendations = []

        # Pattern-level recommendations
        for pattern, metrics in accuracy.items():
            if metrics["accuracy"] < 0.85:
                recommendations.append({
                    "type": "accuracy_improvement",
                    "pattern": pattern,
                    "current_accuracy": metrics["accuracy"],
                    "target_accuracy": 0.90,
                    "action": f"Review and retrain classification for {pattern} pattern"
                })

        # Weight recommendations
        if sensitivity.get("credibility", 0) > 5:
            recommendations.append({
                "type": "weight_adjustment",
                "weight": "credibility",
                "direction": "increase",
                "reason": "Users frequently corrected credibility assessments"
            })

        return recommendations

    async def apply_calibration_changes(self, recommendations: List[Dict], user_approval: bool) -> Dict:
        """Apply calibration changes with user approval"""
        if not user_approval:
            logger.info("Calibration changes not approved")
            return {"status": "rejected", "timestamp": datetime.now().isoformat()}

        logger.info(f"Applying {len(recommendations)} calibration changes")

        # In production: Update scoring weights, retrain models, etc.
        # For now: Log the changes
        calibration_log = Path.home() / "personal-cognitive-architecture" / "data" / "calibration-log.jsonl"

        with open(calibration_log, "a") as f:
            for rec in recommendations:
                rec["applied_at"] = datetime.now().isoformat()
                f.write(json.dumps(rec) + "\n")

        return {
            "status": "applied",
            "count": len(recommendations),
            "timestamp": datetime.now().isoformat()
        }


# Initialize orchestrator
orchestrator = PCAOrchestrator()


@app.post("/dispatch")
async def dispatch(request: CaptureRequest) -> Dict:
    """Main dispatch endpoint"""
    return await orchestrator.dispatch_capture(request)


@app.post("/escalation/{escalation_id}/resolve")
async def resolve_escalation(escalation_id: str, action: str, feedback: str) -> Dict:
    """Resolve an escalated item"""
    return await orchestrator.handle_escalation_resolution(escalation_id, action, feedback)


@app.get("/escalations")
async def get_escalations() -> List[Dict]:
    """Get pending escalations"""
    return [e for e in orchestrator.escalation_queue if e["status"] == "pending_review"]


@app.post("/calibration/monthly")
async def start_monthly_calibration() -> Dict:
    """Start monthly calibration cycle"""
    return await orchestrator.monthly_calibration()


@app.post("/calibration/apply")
async def apply_calibration(recommendations: List[Dict], user_approval: bool) -> Dict:
    """Apply calibration recommendations"""
    return await orchestrator.apply_calibration_changes(recommendations, user_approval)


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "role": "orchestrator",
        "escalations_pending": len([e for e in orchestrator.escalation_queue if e["status"] == "pending_review"]),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ORCHESTRATOR_PORT", 8003))
    host = os.getenv("ORCHESTRATOR_HOST", "127.0.0.1")

    logger.info(f"Starting PCA Orchestrator on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
