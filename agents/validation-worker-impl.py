#!/usr/bin/env python3
"""
Validation Worker Implementation

Receives captures from n8n workflow, scores them, classifies them, and returns routing decisions.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Validation Worker", version="1.0.0")

# Load routing rules and confidence thresholds
ROUTING_RULES_PATH = Path.home() / "personal-cognitive-architecture" / "data" / "routing-rules.json"


class CaptureInput(BaseModel):
    """Input capture from ingestion pipeline"""
    type: str  # text, voice, article, signal
    content: str
    domain: Optional[str] = ""
    source: str  # webhook, file, rss, etc
    timestamp: str
    transcription: Optional[str] = None
    confidence_input: float = 0.5
    tags: List[str] = []
    sensitivity: str = "public"


class ScoringResult(BaseModel):
    """4D scoring model result"""
    credibility: float
    relevance: float
    novelty: float
    signal_strength: float
    overall_confidence: float


class RoutingDecision(BaseModel):
    """Final routing decision"""
    routing_action: str  # ADVANCE_TO_INTEGRATION, ROUTE_WITH_TAG, ESCALATE_FOR_REVIEW, QUARANTINE
    destination: str  # Project path or Inbox
    confidence: float
    reason: Optional[str] = None
    tags: List[str] = []
    requires_escalation: bool = False
    escalation_reason: Optional[str] = None


class ValidationResponse(BaseModel):
    """Response from validation worker"""
    scores: ScoringResult
    classification: str
    routing_decision: RoutingDecision
    timestamp: str


# Load LLM client (use OpenAI or other)
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    HAS_OPENAI = True
except:
    HAS_OPENAI = False
    logger.warning("OpenAI not available, using fallback scoring")


def score_content(content: str, source_type: str) -> ScoringResult:
    """
    Score content using 4D model:
    - Credibility: Is this trustworthy information?
    - Relevance: Does this relate to known projects/domains?
    - Novelty: Is this new information?
    - Signal strength: Is this actionable/important?
    """

    # Length heuristics
    content_lower = content.lower()
    word_count = len(content.split())

    # Base credibility by source type
    credibility_base = {
        "article": 0.80,
        "rss": 0.65,
        "voice": 0.70,
        "text": 0.60,
        "signal": 0.55
    }.get(source_type, 0.50)

    # Boost credibility for proper structure
    credibility = credibility_base
    if "source:" in content_lower or "url:" in content_lower:
        credibility += 0.10
    if word_count > 100:
        credibility += 0.05

    # Relevance: contains keywords related to known domains
    domain_keywords = {
        "AI-Safety": ["ai safety", "alignment", "risk", "threat", "control"],
        "Research": ["research", "study", "experiment", "data", "analysis"],
        "Projects": ["project", "initiative", "work", "task", "goal"]
    }

    relevance = 0.40  # Base
    for domain, keywords in domain_keywords.items():
        if any(kw in content_lower for kw in keywords):
            relevance = max(relevance, 0.75)
            break

    # Novelty: duplicate detection (simplified)
    # In production, check against knowledge graph
    novelty = min(0.90, 0.50 + (word_count / 500))  # More content = potentially more novel

    # Signal strength: urgency/importance indicators
    urgent_keywords = ["urgent", "critical", "immediate", "risk", "danger", "alert"]
    signal_strength = 0.40
    if any(kw in content_lower for kw in urgent_keywords):
        signal_strength = 0.85
    elif word_count > 50:
        signal_strength = 0.65

    # Normalize to 0-1
    overall = (credibility + relevance + novelty + signal_strength) / 4

    return ScoringResult(
        credibility=min(1.0, max(0.0, credibility)),
        relevance=min(1.0, max(0.0, relevance)),
        novelty=min(1.0, max(0.0, novelty)),
        signal_strength=min(1.0, max(0.0, signal_strength)),
        overall_confidence=min(1.0, max(0.0, overall))
    )


def classify_with_llm(content: str, scores: ScoringResult, source_type: str) -> Dict:
    """
    Use LLM to classify content.

    In production: Call OpenAI GPT-4 with zero-shot classification prompt
    For now: Rule-based fallback
    """

    if HAS_OPENAI:
        try:
            prompt = f"""Classify this {source_type} capture:

Content: {content[:500]}

Scores: credibility={scores.credibility:.2f}, relevance={scores.relevance:.2f}, novelty={scores.novelty:.2f}

Classify as: project (specific project task), inbox (general idea), archive (reference), signal (time-sensitive)
Return JSON: {{"classification": "...", "tags": ["..."], "reason": "..."}}
"""
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=100
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.warning(f"LLM classification failed: {e}, using fallback")

    # Fallback rule-based classification
    content_lower = content.lower()

    if any(kw in content_lower for kw in ["urgent", "critical", "alert", "breaking"]):
        classification = "signal"
        tags = ["urgent", "signal"]
    elif scores.relevance > 0.80:
        classification = "project"
        tags = ["structured"]
    elif scores.novelty > 0.75:
        classification = "inbox"
        tags = ["idea", "novel"]
    else:
        classification = "archive"
        tags = ["reference"]

    return {
        "classification": classification,
        "tags": tags,
        "reason": "Fallback rule-based classification"
    }


def route_capture(scores: ScoringResult, classification: str, source_type: str, sensitivity: str) -> RoutingDecision:
    """
    Route based on confidence and classification.

    Uses routing-rules.json for detailed routing logic.
    """

    overall_confidence = scores.overall_confidence

    # Safety check: never route sensitive data without approval
    if sensitivity == "sensitive":
        return RoutingDecision(
            routing_action="QUARANTINE",
            destination="40-Archive/sensitive",
            confidence=1.0,
            reason="Sensitive content requires manual review",
            tags=[],
            requires_escalation=True,
            escalation_reason="sensitive_content"
        )

    # Route based on confidence tiers
    if overall_confidence >= 0.85:
        if classification == "project":
            return RoutingDecision(
                routing_action="ADVANCE_TO_INTEGRATION",
                destination="10-Projects/[project_name]/Notes/",
                confidence=overall_confidence,
                reason="High confidence structured knowledge",
                tags=["auto-routed"],
                requires_escalation=False
            )
        elif classification == "signal":
            return RoutingDecision(
                routing_action="ESCALATE_FOR_REVIEW",
                destination="40-Escalations/signals/",
                confidence=overall_confidence,
                reason="Time-sensitive signal requiring review",
                tags=["signal", "urgent"],
                requires_escalation=True,
                escalation_reason="signal_requires_action"
            )
        else:
            return RoutingDecision(
                routing_action="ROUTE_WITH_TAG",
                destination="20-Ideas/Unstructured/",
                confidence=overall_confidence,
                reason="High confidence unstructured idea",
                tags=["inbox", "reviewed"],
                requires_escalation=False
            )

    elif overall_confidence >= 0.65:
        return RoutingDecision(
            routing_action="ROUTE_WITH_TAG",
            destination="20-Ideas/Unstructured/",
            confidence=overall_confidence,
            reason="Medium confidence, needs human review",
            tags=["requires-review", "medium-confidence"],
            requires_escalation=False
        )

    elif overall_confidence >= 0.40:
        return RoutingDecision(
            routing_action="ESCALATE_FOR_REVIEW",
            destination="40-Escalations/manual-review/",
            confidence=overall_confidence,
            reason="Low confidence, requires escalation",
            tags=["escalated"],
            requires_escalation=True,
            escalation_reason="low_confidence_escalation"
        )

    else:
        return RoutingDecision(
            routing_action="QUARANTINE",
            destination="40-Archive/quarantine/",
            confidence=overall_confidence,
            reason="Very low confidence, quarantined for review",
            tags=["quarantined", "review-needed"],
            requires_escalation=True,
            escalation_reason="very_low_confidence"
        )


@app.post("/validate", response_model=ValidationResponse)
async def validate_capture(capture: CaptureInput) -> ValidationResponse:
    """
    Main validation endpoint.

    Receives capture from n8n, scores, classifies, and routes.
    """

    try:
        logger.info(f"Validating capture: {capture.type} from {capture.source}")

        # Step 1: Score content
        scores = score_content(capture.content, capture.type)
        logger.info(f"Scores: credibility={scores.credibility:.2f}, relevance={scores.relevance:.2f}")

        # Step 2: Classify with LLM or rules
        classification_result = classify_with_llm(capture.content, scores, capture.type)
        classification = classification_result["classification"]
        tags = classification_result.get("tags", [])
        logger.info(f"Classification: {classification}, tags: {tags}")

        # Step 3: Route based on confidence
        routing = route_capture(scores, classification, capture.type, capture.sensitivity)
        logger.info(f"Routing: {routing.routing_action} to {routing.destination}")

        # Add input tags to routing tags
        all_tags = list(set(tags + routing.tags + capture.tags))
        routing.tags = all_tags

        # Return full response
        return ValidationResponse(
            scores=scores,
            classification=classification,
            routing_decision=routing,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/config")
async def config():
    """Return current configuration"""
    return {
        "model": "validation-worker-v1",
        "scoring_method": "4d-model",
        "has_llm": HAS_OPENAI,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("VALIDATION_WORKER_PORT", 8001))
    host = os.getenv("VALIDATION_WORKER_HOST", "127.0.0.1")

    logger.info(f"Starting Validation Worker on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
