#!/usr/bin/env python3
"""
Intake Agent Implementation

Normalizes inbound PCA requests into validated intake objects before any downstream
workflow acts on them. Implements pca/docs/agent-workflow-slice-1-spec.md § Agent A.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from datetime import datetime, timezone
import uuid
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Intake Agent", version="1.0.0")

RequestType = Literal["backlog", "capture", "retrieval", "operational", "briefing", "unknown"]
NextRoute = Literal["backlog", "rag", "capture", "operational", "briefing", "reject", "manual_review"]
Classification = Literal["public", "internal", "confidential", "restricted", "unknown"]
Priority = Literal["low", "medium", "high", "critical"]

BACKLOG_SIGNALS = [
    "add", "build", "create", "implement", "develop", "fix", "refactor",
    "deploy", "update", "workflow", "epic", "sprint", "backlog", "issue",
    "task", "feature", "requirement", "ticket", "story",
]
RETRIEVAL_SIGNALS = [
    "what", "how", "why", "find", "search", "look up", "retrieve", "know",
    "context", "reference", "recall", "tell me", "summarize", "explain",
    "documentation", "docs", "what do we know",
]
OPERATIONAL_SIGNALS = [
    "run", "start", "stop", "restart", "deploy", "health", "check",
    "status", "monitor", "alert", "schedule", "trigger", "execute", "ping",
]
BRIEFING_SIGNALS = [
    "brief", "briefing", "digest", "report", "overview",
    "synthesis", "weekly", "daily", "update me", "what happened",
]
CAPTURE_SIGNALS = [
    "capture", "save", "note", "record", "store", "bookmark",
    "article", "link", "reading", "file", "pdf", "page",
]
RESTRICTED_MARKERS = ["secret", "classified", "top secret", "protected-b", "eyes only"]
INBOX_CHANNELS = {"webhook", "obsidian", "api"}


class AttachmentItem(BaseModel):
    kind: Literal["file", "url", "note_ref", "issue_ref"]
    value: str


class SourceInfo(BaseModel):
    actor: Literal["human", "workflow", "agent"] = "human"
    channel: Literal["chat", "webhook", "obsidian", "github", "api", "other"] = "chat"


class IntakeRequest(BaseModel):
    content: str
    source: SourceInfo = Field(default_factory=SourceInfo)
    attachments: List[AttachmentItem] = []
    context_refs: List[str] = []
    requesting_agent: Optional[str] = None


class ProvenanceInfo(BaseModel):
    created_at: str
    created_by: str
    source_refs: List[str] = []


class IntakeObject(BaseModel):
    intake_id: str
    request_type: RequestType
    summary: str
    description: str
    source: SourceInfo
    priority: Priority
    classification: Classification
    requires_approval: bool
    attachments: List[AttachmentItem]
    provenance: ProvenanceInfo
    confidence: float
    next_route: NextRoute
    validation_errors: List[str]


def _keyword_score(text: str, keywords: List[str], weight: float = 0.15) -> float:
    return sum(weight for kw in keywords if re.search(rf'\b{re.escape(kw)}\b', text))


def classify_request(
    content: str, source: SourceInfo, attachments: List[AttachmentItem]
) -> tuple[RequestType, float]:
    text = content.lower()

    if source.channel in INBOX_CHANNELS and (attachments or len(content) < 200):
        return "capture", 0.75

    scores: Dict[str, float] = {
        "backlog": _keyword_score(text, BACKLOG_SIGNALS),
        "retrieval": _keyword_score(text, RETRIEVAL_SIGNALS),
        "operational": _keyword_score(text, OPERATIONAL_SIGNALS),
        "briefing": _keyword_score(text, BRIEFING_SIGNALS, weight=0.20),
        "capture": _keyword_score(text, CAPTURE_SIGNALS),
    }

    best_type = max(scores, key=lambda k: scores[k])
    best_score = scores[best_type]

    if best_score < 0.15:
        return "unknown", 0.30

    confidence = min(0.92, 0.50 + best_score)
    return best_type, confidence  # type: ignore[return-value]


def infer_classification(content: str, source: SourceInfo) -> Classification:
    text = content.lower()
    if any(m in text for m in RESTRICTED_MARKERS):
        return "restricted"
    return "internal"


def infer_priority(content: str, request_type: RequestType) -> Priority:
    text = content.lower()
    if any(kw in text for kw in ["urgent", "critical", "production down", "outage"]):
        return "critical"
    if any(kw in text for kw in ["asap", "today", "immediately", "blocking"]):
        return "high"
    if request_type == "operational":
        return "medium"
    return "low"


def route_from_type(
    request_type: RequestType, classification: Classification, confidence: float
) -> NextRoute:
    if confidence < 0.60 or classification == "restricted":
        return "manual_review"
    routing: Dict[str, NextRoute] = {
        "backlog": "backlog",
        "retrieval": "rag",
        "capture": "capture",
        "operational": "operational",
        "briefing": "briefing",
        "unknown": "manual_review",
    }
    return routing[request_type]


def validate_request(content: str) -> List[str]:
    errors: List[str] = []
    if not content or not content.strip():
        errors.append("content is empty or whitespace only")
    elif len(content.strip()) < 5:
        errors.append("content is too short to classify (< 5 chars)")
    return errors


@app.post("/intake", response_model=IntakeObject)
async def intake(request: IntakeRequest) -> IntakeObject:
    logger.info(f"Intake: {request.source.actor} via {request.source.channel}")

    errors = validate_request(request.content)
    now = datetime.now(timezone.utc).isoformat()
    provenance = ProvenanceInfo(
        created_at=now,
        created_by=request.requesting_agent or request.source.actor,
        source_refs=request.context_refs,
    )

    if errors and not request.attachments:
        return IntakeObject(
            intake_id=str(uuid.uuid4()),
            request_type="unknown",
            summary="Rejected: invalid request",
            description=request.content[:200],
            source=request.source,
            priority="low",
            classification="unknown",
            requires_approval=False,
            attachments=request.attachments,
            provenance=provenance,
            confidence=0.0,
            next_route="reject",
            validation_errors=errors,
        )

    request_type, confidence = classify_request(request.content, request.source, request.attachments)
    classification = infer_classification(request.content, request.source)
    priority = infer_priority(request.content, request_type)
    next_route = route_from_type(request_type, classification, confidence)
    requires_approval = classification in ("restricted", "confidential") or next_route == "manual_review"

    summary = request.content[:120].strip()
    if len(request.content) > 120:
        summary += "…"

    return IntakeObject(
        intake_id=str(uuid.uuid4()),
        request_type=request_type,
        summary=summary,
        description=request.content,
        source=request.source,
        priority=priority,
        classification=classification,
        requires_approval=requires_approval,
        attachments=request.attachments,
        provenance=provenance,
        confidence=round(confidence, 3),
        next_route=next_route,
        validation_errors=errors,
    )


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "intake-agent", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("INTAKE_AGENT_PORT", 8010))
    host = os.getenv("INTAKE_AGENT_HOST", "127.0.0.1")
    logger.info(f"Starting Intake Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
