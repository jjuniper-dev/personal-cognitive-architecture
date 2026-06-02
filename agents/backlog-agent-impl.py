#!/usr/bin/env python3
"""
Backlog Agent Implementation

Converts qualified PCA intake objects into structured work item proposals
aligned to existing planning structures. Implements pca/docs/agent-workflow-slice-1-spec.md § Agent B.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, timezone
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Backlog Agent", version="1.0.0")

WorkType = Literal["epic", "sprint", "backlog_item", "incident", "research_task", "deferred_item"]
WorkStatus = Literal["proposed", "queued", "merged", "deferred", "rejected"]
Classification = Literal["public", "internal", "confidential", "restricted"]

INCIDENT_SIGNALS = [
    "incident", "broken", "down", "failed", "regression",
    "outage", "bug", "error", "critical failure",
]
EPIC_SIGNALS = ["epic", "multi-sprint", "multiple sprints", "large scope", "phase"]
RESEARCH_SIGNALS = ["research", "investigate", "explore", "evaluate", "compare", "spike", "discovery"]
DEFERRED_SIGNALS = ["blocked", "waiting for", "depends on", "pending", "deferred", "later"]


class SourceInfo(BaseModel):
    actor: str = "human"
    channel: str = "chat"


class IntakeProvenance(BaseModel):
    created_at: str
    created_by: str
    source_refs: List[str] = []


class IntakeObject(BaseModel):
    intake_id: str
    request_type: str
    summary: str
    description: str
    source: SourceInfo
    priority: str
    classification: Classification
    requires_approval: bool
    provenance: IntakeProvenance
    confidence: float
    next_route: str


class WorkItemProvenance(BaseModel):
    intake_id: str
    shaped_at: str
    source_refs: List[str] = []


class WorkItemProposal(BaseModel):
    work_item_id: str
    work_type: WorkType
    title: str
    summary: str
    acceptance_criteria: List[str]
    dependencies: List[str]
    related_epics: List[str]
    related_docs: List[str]
    classification: Classification
    provenance: WorkItemProvenance
    status: WorkStatus
    reason: str


def determine_work_type(summary: str, description: str, priority: str) -> WorkType:
    text = (summary + " " + description).lower()
    if any(kw in text for kw in INCIDENT_SIGNALS):
        return "incident"
    if any(kw in text for kw in EPIC_SIGNALS):
        return "epic"
    if any(kw in text for kw in RESEARCH_SIGNALS):
        return "research_task"
    if any(kw in text for kw in DEFERRED_SIGNALS):
        return "deferred_item"
    if priority in ("critical", "high"):
        return "sprint"
    return "backlog_item"


def generate_acceptance_criteria(
    work_type: WorkType, summary: str, description: str
) -> List[str]:
    criteria: List[str] = []

    if work_type == "incident":
        criteria.extend([
            "Root cause is identified and documented.",
            "Regression test or preventive measure is added.",
            "Affected workflows are verified as restored.",
        ])
    elif work_type == "epic":
        criteria.extend([
            "All child issues are defined with acceptance criteria.",
            "Dependencies across child issues are documented.",
            "Exit criteria for the epic are approved.",
        ])
    elif work_type == "research_task":
        criteria.extend([
            "Research findings are captured in a canonical KB page or repo doc.",
            "Recommendations are actionable and traceable to sources.",
        ])
    else:
        criteria.extend([
            "Implementation matches the stated intent in the summary.",
            "Tests or verification steps confirm the change works as expected.",
        ])

    first_sentence = next(
        (s.strip() for s in description.split(".") if len(s.strip()) > 20),
        None,
    )
    if first_sentence:
        criteria.append(f"Addresses: {first_sentence[:120]}.")

    return criteria


def infer_related_docs(summary: str, description: str) -> List[str]:
    text = (summary + " " + description).lower()
    docs: List[str] = []
    if any(kw in text for kw in ["backlog", "sprint", "epic", "task"]):
        docs.append("BACKLOG.md")
    if any(kw in text for kw in ["architecture", "stack", "design", "system"]):
        docs.append("pca-architecture.md")
    if any(kw in text for kw in ["workflow", "agent", "pipeline", "intake", "rag", "lifecycle"]):
        docs.append("docs/agent-workflow-slice-1-spec.md")
    if any(kw in text for kw in ["claude", "codex", "code agent", "dispatch"]):
        docs.append("CLAUDE.md")
    if any(kw in text for kw in ["epic", "v1", "phase"]):
        docs.append("PCA_V1_EPIC.md")
    return list(dict.fromkeys(docs))


@app.post("/shape", response_model=WorkItemProposal)
async def shape_work_item(intake: IntakeObject) -> WorkItemProposal:
    if intake.next_route != "backlog":
        raise HTTPException(
            status_code=400,
            detail=f"next_route is '{intake.next_route}', expected 'backlog'.",
        )

    logger.info(f"Shaping work item from intake {intake.intake_id}")

    work_type = determine_work_type(intake.summary, intake.description, intake.priority)
    criteria = generate_acceptance_criteria(work_type, intake.summary, intake.description)
    related_docs = infer_related_docs(intake.summary, intake.description)

    return WorkItemProposal(
        work_item_id=str(uuid.uuid4()),
        work_type=work_type,
        title=intake.summary[:80],
        summary=intake.summary,
        acceptance_criteria=criteria,
        dependencies=[],
        related_epics=[],
        related_docs=related_docs,
        classification=intake.classification,
        provenance=WorkItemProvenance(
            intake_id=intake.intake_id,
            shaped_at=datetime.now(timezone.utc).isoformat(),
            source_refs=intake.provenance.source_refs,
        ),
        status="proposed",
        reason=(
            f"Shaped from intake {intake.intake_id} ({work_type}). "
            "Verify against existing backlog before creating a new issue."
        ),
    )


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "backlog-agent", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("BACKLOG_AGENT_PORT", 8011))
    host = os.getenv("BACKLOG_AGENT_HOST", "127.0.0.1")
    logger.info(f"Starting Backlog Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
