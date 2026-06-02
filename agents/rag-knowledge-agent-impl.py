#!/usr/bin/env python3
"""
RAG Knowledge Agent Implementation

Assembles trusted, source-grounded context packs using canonical-first retrieval policy.
Implements pca/docs/agent-workflow-slice-1-spec.md § Agent C.

The stub knowledge store in build_stub_knowledge_store() is replaced in production
by calls to Qdrant, Neo4j, and the Obsidian vault via WF10/WF12.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional
from datetime import datetime, timezone
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA RAG Knowledge Agent", version="1.0.0")

SourceType = Literal["canonical", "repo_doc", "reviewed_memory", "inbox", "incident"]
ReviewStatus = Literal["canonical", "reviewed", "draft", "raw"]
Classification = Literal["public", "internal", "confidential", "restricted"]
TierCeiling = Literal["canonical", "repo_doc", "reviewed_memory", "inbox"]
Audience = Literal["internal", "public", "mixed"]
PublishLevel = Literal["none", "internal", "public"]

CLASSIFICATION_RANK: Dict[str, int] = {
    "public": 0, "internal": 1, "confidential": 2, "restricted": 3
}
TIER_RANK: Dict[str, int] = {
    "canonical": 1, "repo_doc": 2, "reviewed_memory": 3, "inbox": 4, "incident": 4
}
CEILING_RANK: Dict[str, int] = {
    "canonical": 1, "repo_doc": 2, "reviewed_memory": 3, "inbox": 4
}


class DateRange(BaseModel):
    after: Optional[str] = None
    before: Optional[str] = None


class RetrievalFilters(BaseModel):
    tags: List[str] = []
    date_range: Optional[DateRange] = None
    sensitivity: Optional[Classification] = None
    audience: Optional[Audience] = None


class RetrievalRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    source_tier_ceiling: TierCeiling = "reviewed_memory"
    filters: RetrievalFilters = Field(default_factory=RetrievalFilters)
    max_results: int = 10
    include_gaps: bool = True
    requester_classification: Classification = "internal"


class RetrievalResult(BaseModel):
    source_id: str
    title: str
    source_type: SourceType
    review_status: ReviewStatus
    confidence: float
    classification: Classification
    sensitivity: Classification
    audience: Audience
    publish: PublishLevel
    reason_included: str
    provenance_refs: List[str]
    excerpt: str


class ContextPack(BaseModel):
    context_pack_id: str
    request_id: str
    query: str
    results: List[RetrievalResult]
    open_questions: List[str]
    gaps_or_uncertainties: List[str]
    assembled_at: str


def classification_allowed(source: Classification, requester: Classification) -> bool:
    return CLASSIFICATION_RANK.get(requester, 0) >= CLASSIFICATION_RANK.get(source, 0)


def tier_allowed(source_type: SourceType, ceiling: TierCeiling) -> bool:
    return TIER_RANK.get(source_type, 5) <= CEILING_RANK.get(ceiling, 4)


def build_stub_knowledge_store() -> List[RetrievalResult]:
    """
    Stub store for offline testing.
    In production: query Qdrant (semantic), Neo4j (graph), Obsidian vault (canonical pages).
    """
    return [
        RetrievalResult(
            source_id="canon-001",
            title="PCA Agent Workflow Slice 1 Spec",
            source_type="repo_doc",
            review_status="canonical",
            confidence=0.95,
            classification="internal",
            sensitivity="internal",
            audience="internal",
            publish="internal",
            reason_included="Primary specification for agent workflow stack slice 1.",
            provenance_refs=["pca/docs/agent-workflow-slice-1-spec.md"],
            excerpt="Implementation contract for the first governed agent workflow slice...",
        ),
        RetrievalResult(
            source_id="canon-002",
            title="PCA V1 Epic",
            source_type="repo_doc",
            review_status="canonical",
            confidence=0.92,
            classification="internal",
            sensitivity="internal",
            audience="internal",
            publish="internal",
            reason_included="Top-level epic defining PCA V1 scope and agent priorities.",
            provenance_refs=["pca/PCA_V1_EPIC.md"],
            excerpt="V1 Epic: governed intake, backlog management, retrieval-augmented knowledge...",
        ),
        RetrievalResult(
            source_id="inbox-001",
            title="Rough capture: agent workflow notes",
            source_type="inbox",
            review_status="raw",
            confidence=0.40,
            classification="internal",
            sensitivity="internal",
            audience="internal",
            publish="none",
            reason_included="Supplementary raw material — not canonical. Included only when tier ceiling permits.",
            provenance_refs=["claude-kb/raw/inbox/agent-notes.md"],
            excerpt="Notes on intake agent routing logic (unreviewed draft)...",
        ),
    ]


@app.post("/retrieve", response_model=ContextPack)
async def retrieve(request: RetrievalRequest) -> ContextPack:
    logger.info(f"Retrieval {request.request_id}: {request.query[:80]}")

    all_results = build_stub_knowledge_store()
    filtered: List[RetrievalResult] = []
    gaps: List[str] = []
    questions: List[str] = []
    canonical_found = False

    for result in all_results:
        if not tier_allowed(result.source_type, request.source_tier_ceiling):
            continue
        if not classification_allowed(result.classification, request.requester_classification):
            gaps.append(
                f"'{result.title}' excluded: classification '{result.classification}' "
                f"exceeds requester level '{request.requester_classification}'."
            )
            continue
        filtered.append(result)
        if result.source_type in ("canonical", "repo_doc") and result.review_status in ("canonical", "reviewed"):
            canonical_found = True

    filtered.sort(key=lambda r: (TIER_RANK.get(r.source_type, 5), -r.confidence))
    filtered = filtered[:request.max_results]

    if request.include_gaps and not canonical_found:
        gaps.append(
            f"No canonical or reviewed material found for '{request.query}'. "
            "Results may reflect lower-trust sources only."
        )

    if not filtered:
        gaps.append(
            f"No results for '{request.query}' within tier '{request.source_tier_ceiling}' "
            f"and classification '{request.requester_classification}'."
        )
        questions.append("Is the relevant knowledge captured in the canonical KB?")

    return ContextPack(
        context_pack_id=str(uuid.uuid4()),
        request_id=request.request_id,
        query=request.query,
        results=filtered,
        open_questions=questions,
        gaps_or_uncertainties=gaps,
        assembled_at=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "rag-knowledge-agent", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("RAG_AGENT_PORT", 8012))
    host = os.getenv("RAG_AGENT_HOST", "127.0.0.1")
    logger.info(f"Starting RAG Knowledge Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
