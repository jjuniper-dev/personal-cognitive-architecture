#!/usr/bin/env python3
"""
Knowledge Lifecycle Agent Implementation

Detects staleness, missing source refs, expired reviews, and ungrounded seeds in canonical KB.
Produces durable review queues and audit artifacts. Never mutates canon directly.
Implements pca/docs/agent-workflow-slice-1-spec.md § Agent D.

The stub page store in build_stub_pages() is replaced in production
by a scan of the Obsidian vault and claude-kb/ via the MCP filesystem tools.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Callable, List, Literal, Optional
from datetime import datetime, timezone, timedelta
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Knowledge Lifecycle Agent", version="1.0.0")

IssueType = Literal["stale", "missing_source_ref", "invalid_source_ref", "review_expired", "ungrounded_seed"]
Severity = Literal["low", "medium", "high"]
RecommendedAction = Literal["refresh", "validate", "link_source", "archive", "escalate"]
ReviewItemStatus = Literal["open", "proposed", "approved", "dismissed"]
TargetType = Literal["canonical_page", "kb_page", "summary", "workflow_doc"]
LifecycleStatus = Literal["fresh", "review_due", "stale", "missing_ref", "ungrounded"]
PageStatus = Literal["draft", "canonical", "reviewed", "stale", "archived"]


class CanonicalPageMetadata(BaseModel):
    page_id: str
    title: str
    target_type: TargetType
    source_ref: Optional[str] = None
    owner: Optional[str] = None
    status: PageStatus = "draft"
    review_after: Optional[str] = None
    updated_at: Optional[str] = None
    sensitivity: str = "internal"
    audience: str = "internal"
    publish: str = "none"
    linked_by_active_workflow: bool = False


class MetadataContract(BaseModel):
    required_fields: List[str] = ["source_ref", "owner", "review_after", "status", "sensitivity"]
    max_stale_days: int = 90


class LifecycleScanRequest(BaseModel):
    scan_scope: Literal["full", "incremental", "targeted"] = "full"
    target_ids: List[str] = []
    metadata_contract: MetadataContract = Field(default_factory=MetadataContract)
    context_pack_ref: Optional[str] = None


class ReviewItem(BaseModel):
    review_item_id: str
    target_id: str
    target_type: TargetType
    issue_type: IssueType
    severity: Severity
    summary: str
    recommended_action: RecommendedAction
    source_refs: List[str]
    proposed_patch_ref: Optional[str]
    created_at: str
    status: ReviewItemStatus


class AuditSummary(BaseModel):
    stale_count: int
    missing_source_ref_count: int
    review_expired_count: int
    ungrounded_seed_count: int


class AuditArtifact(BaseModel):
    audit_id: str
    scan_scope: str
    scan_completed_at: str
    total_pages_scanned: int
    findings: List[ReviewItem]
    summary: AuditSummary
    artifact_path: str


class PageLifecycleState(BaseModel):
    page_id: str
    lifecycle_status: LifecycleStatus
    last_reviewed: Optional[str]
    open_review_items: int
    has_pending_draft: bool


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def check_stale(
    page: CanonicalPageMetadata, max_stale_days: int, now: datetime
) -> Optional[ReviewItem]:
    if page.status == "archived":
        return None
    review_dt = _parse_dt(page.review_after)
    if review_dt and review_dt < now:
        severity: Severity = "high" if page.status == "canonical" else "medium"
        return ReviewItem(
            review_item_id=str(uuid.uuid4()),
            target_id=page.page_id,
            target_type=page.target_type,
            issue_type="stale",
            severity=severity,
            summary=f"Page '{page.title}' review_after date has passed ({page.review_after}).",
            recommended_action="refresh",
            source_refs=[page.source_ref] if page.source_ref else [],
            proposed_patch_ref=None,
            created_at=now.isoformat(),
            status="open",
        )
    updated_dt = _parse_dt(page.updated_at)
    if updated_dt and (now - updated_dt).days > max_stale_days:
        severity = "high" if page.status == "canonical" else "medium"
        return ReviewItem(
            review_item_id=str(uuid.uuid4()),
            target_id=page.page_id,
            target_type=page.target_type,
            issue_type="stale",
            severity=severity,
            summary=(
                f"Page '{page.title}' not updated in {(now - updated_dt).days} days "
                f"(threshold: {max_stale_days})."
            ),
            recommended_action="refresh",
            source_refs=[page.source_ref] if page.source_ref else [],
            proposed_patch_ref=None,
            created_at=now.isoformat(),
            status="open",
        )
    return None


def check_missing_source_ref(
    page: CanonicalPageMetadata, now: datetime
) -> Optional[ReviewItem]:
    if not page.source_ref or not page.source_ref.strip():
        severity: Severity = "high" if page.status == "canonical" else "low"
        return ReviewItem(
            review_item_id=str(uuid.uuid4()),
            target_id=page.page_id,
            target_type=page.target_type,
            issue_type="missing_source_ref",
            severity=severity,
            summary=f"Page '{page.title}' has no source_ref — deterministic drift checks are not possible.",
            recommended_action="link_source",
            source_refs=[],
            proposed_patch_ref=None,
            created_at=now.isoformat(),
            status="open",
        )
    return None


def check_ungrounded_seed(
    page: CanonicalPageMetadata, now: datetime
) -> Optional[ReviewItem]:
    missing_ref = not page.source_ref or not page.source_ref.strip()
    missing_owner = not page.owner or not page.owner.strip()
    if not (missing_ref and missing_owner and page.status == "draft"):
        return None
    updated_dt = _parse_dt(page.updated_at)
    if updated_dt and (now - updated_dt).days < 30:
        return None
    return ReviewItem(
        review_item_id=str(uuid.uuid4()),
        target_id=page.page_id,
        target_type=page.target_type,
        issue_type="ungrounded_seed",
        severity="low",
        summary=(
            f"Page '{page.title}' is an ungrounded seed: "
            "no source_ref, no owner, stale draft."
        ),
        recommended_action="validate",
        source_refs=[],
        proposed_patch_ref=None,
        created_at=now.isoformat(),
        status="open",
    )


def build_stub_pages() -> List[CanonicalPageMetadata]:
    """Stub KB pages for offline testing."""
    now = datetime.now(timezone.utc)
    return [
        CanonicalPageMetadata(
            page_id="page-001",
            title="Agent Workflow Architecture",
            target_type="canonical_page",
            source_ref="pca/docs/agent-workflow-slice-1-spec.md",
            owner="jjuniper-dev",
            status="canonical",
            review_after=(now - timedelta(days=5)).isoformat(),
            updated_at=(now - timedelta(days=95)).isoformat(),
        ),
        CanonicalPageMetadata(
            page_id="page-002",
            title="RAG Retrieval Policy",
            target_type="kb_page",
            source_ref=None,
            owner="jjuniper-dev",
            status="draft",
            updated_at=(now - timedelta(days=10)).isoformat(),
        ),
        CanonicalPageMetadata(
            page_id="page-003",
            title="Abandoned draft note",
            target_type="kb_page",
            source_ref=None,
            owner=None,
            status="draft",
            updated_at=(now - timedelta(days=45)).isoformat(),
        ),
    ]


CHECK_FNS: List[Callable] = [check_stale, check_missing_source_ref, check_ungrounded_seed]


def run_checks(
    page: CanonicalPageMetadata, max_stale_days: int, now: datetime
) -> List[ReviewItem]:
    findings: List[ReviewItem] = []
    for fn in CHECK_FNS:
        if fn.__name__ == "check_stale":
            result = fn(page, max_stale_days, now)
        else:
            result = fn(page, now)
        if result:
            findings.append(result)
    return findings


@app.post("/scan", response_model=AuditArtifact)
async def scan(request: LifecycleScanRequest) -> AuditArtifact:
    logger.info(f"Lifecycle scan: scope={request.scan_scope}")
    now = datetime.now(timezone.utc)

    pages = build_stub_pages()
    if request.target_ids:
        pages = [p for p in pages if p.page_id in request.target_ids]

    all_findings: List[ReviewItem] = []
    for page in pages:
        all_findings.extend(run_checks(page, request.metadata_contract.max_stale_days, now))

    summary = AuditSummary(
        stale_count=sum(1 for f in all_findings if f.issue_type == "stale"),
        missing_source_ref_count=sum(1 for f in all_findings if f.issue_type == "missing_source_ref"),
        review_expired_count=sum(1 for f in all_findings if f.issue_type == "review_expired"),
        ungrounded_seed_count=sum(1 for f in all_findings if f.issue_type == "ungrounded_seed"),
    )
    artifact_path = f"claude-kb/audit/lifecycle-{now.strftime('%Y%m%d-%H%M%S')}.md"
    logger.info(f"Scan complete: {len(all_findings)} findings across {len(pages)} pages")

    return AuditArtifact(
        audit_id=str(uuid.uuid4()),
        scan_scope=request.scan_scope,
        scan_completed_at=now.isoformat(),
        total_pages_scanned=len(pages),
        findings=all_findings,
        summary=summary,
        artifact_path=artifact_path,
    )


@app.get("/lifecycle-state", response_model=List[PageLifecycleState])
async def lifecycle_state() -> List[PageLifecycleState]:
    """Lifecycle state endpoint — consumed by RAG Knowledge Agent to adjust retrieval confidence."""
    now = datetime.now(timezone.utc)
    pages = build_stub_pages()
    states: List[PageLifecycleState] = []

    for page in pages:
        findings = run_checks(page, 90, now)
        if not findings:
            status: LifecycleStatus = "fresh"
        elif any(f.issue_type == "stale" for f in findings):
            status = "stale"
        elif any(f.issue_type in ("missing_source_ref", "invalid_source_ref") for f in findings):
            status = "missing_ref"
        elif any(f.issue_type == "ungrounded_seed" for f in findings):
            status = "ungrounded"
        else:
            status = "review_due"

        states.append(PageLifecycleState(
            page_id=page.page_id,
            lifecycle_status=status,
            last_reviewed=None,
            open_review_items=len(findings),
            has_pending_draft=False,
        ))

    return states


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "knowledge-lifecycle-agent", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("LIFECYCLE_AGENT_PORT", 8013))
    host = os.getenv("LIFECYCLE_AGENT_HOST", "127.0.0.1")
    logger.info(f"Starting Knowledge Lifecycle Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
