from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from app.models.schemas import (
    CaptureConfidence,
    CaptureContent,
    CaptureReceipt,
    CaptureSourceMetadata,
    HealthResponse,
    IPhoneCaptureRequest,
    ProcessingNote,
    StagedCaptureRecord,
)
from app.services.capture_store import CaptureStore


app = FastAPI(
    title="PCA Capture API",
    version="0.1.0",
    description="Minimal intake service for iPhone-originated capture events.",
)
store = CaptureStore()


def _normalize_title(text: str) -> str:
    words = text.split()
    if not words:
        return "iPhone Capture"

    title = " ".join(words[:8])
    return title[:60].strip().rstrip(".,;:-") or "iPhone Capture"


def _render_markdown(record: StagedCaptureRecord) -> str:
    tags = ", ".join(record.source_metadata.tags)
    tag_value = f"[{tags}]" if tags else "[]"
    location_value = record.source_metadata.location or ""
    context_value = record.user_context or ""

    lines = [
        "---",
        "type: capture",
        f"source_type: {record.source_type}",
        f"captured_at: {record.captured_at.isoformat()}",
        f"capture_id: {record.capture_id}",
        "status: raw",
        "confidence: 1.0",
        "domain: personal",
        "sensitivity: personal",
        f"processing_state: {record.processing_state}",
        "validation_id: ~",
        "routing_action: ~",
        f"tags: {tag_value}",
        "---",
        "",
        f"# {record.title}",
        "",
        "## Raw Capture",
        "",
        record.content.raw_text,
        "",
        "## Source Metadata",
        "",
        f"- **Source Type**: {record.source_type}",
        f"- **Captured**: {record.captured_at.isoformat()}",
        f"- **Device/Location**: iPhone{f' / {location_value}' if location_value else ''}",
    ]

    if context_value:
        lines.extend(["- **Context**: " + context_value])

    if record.source_metadata.tags:
        lines.extend(["- **Tags**: " + ", ".join(record.source_metadata.tags)])

    lines.extend([
        "",
        "## Processing Notes",
        "",
        "### Needs Review?",
        "- [ ] No (appears clear)",
        "- [ ] Yes (ambiguous or requires verification)",
        "  - Reason: _specify_",
        "",
        "### Next Steps",
        "- [ ] Promote to knowledge base (decision made above)",
        "- [ ] Link to related note (specify: _______)",
        "- [ ] Archive (not actionable)",
        "- [ ] Hold in inbox (awaiting context)",
        "",
        "---",
        "",
        f"**Status**: Staged for triage",
        f"**Last Modified**: {record.captured_at.isoformat()}",
    ])

    return "\n".join(lines) + "\n"


def _build_record(payload: IPhoneCaptureRequest) -> StagedCaptureRecord:
    capture_id = str(uuid4())
    title = _normalize_title(payload.context_note or payload.text)
    content = CaptureContent(
        raw_text=payload.text,
        word_count=len(payload.text.split()),
        language="en",
    )
    processing_notes = [
        ProcessingNote(
            timestamp=datetime.now(timezone.utc),
            stage="webhook",
            note="Accepted iPhone text capture payload.",
        ),
        ProcessingNote(
            timestamp=datetime.now(timezone.utc),
            stage="staging",
            note="Capture staged for triage.",
        ),
    ]
    record = StagedCaptureRecord(
        capture_id=capture_id,
        source_type="text",
        source_metadata=CaptureSourceMetadata(
            device="iPhone",
            location=payload.location,
            tags=payload.tags,
        ),
        captured_at=payload.timestamp.astimezone(timezone.utc),
        content=content,
        confidence=CaptureConfidence(),
        user_context=payload.context_note,
        processing_notes=processing_notes,
        title=title,
        body_markdown="",
    )
    markdown = _render_markdown(record)
    if hasattr(record, "model_copy"):
        return record.model_copy(update={"body_markdown": markdown})
    return record.copy(update={"body_markdown": markdown})


@app.get("/")
def root():
    return {
        "service": "PCA Capture API",
        "status": "ready",
        "routes": [
            "/health",
            "/webhook/pca-ingest",
            "/webhook/pca-capture",
            "/captures/{capture_id}",
            "/captures/latest",
        ],
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="capture-api",
        capture_store=str(store.root),
        timestamp=datetime.now(timezone.utc),
    )


@app.post("/webhook/pca-ingest", response_model=CaptureReceipt)
@app.post("/webhook/pca-capture", response_model=CaptureReceipt)
def ingest_capture(payload: IPhoneCaptureRequest) -> CaptureReceipt:
    if payload.source.strip().lower() != "iphone":
        raise HTTPException(status_code=400, detail="source must be iphone for this POC slice")

    record = _build_record(payload)
    storage_paths = store.stage_capture(record)
    record = record.model_copy(update={"storage_paths": storage_paths}) if hasattr(record, "model_copy") else record.copy(update={"storage_paths": storage_paths})

    return CaptureReceipt(
        capture_id=record.capture_id,
        received_at=datetime.now(timezone.utc),
        storage_paths=storage_paths,
    )


@app.get("/captures/{capture_id}")
def get_capture(capture_id: str):
    capture = store.read_capture(capture_id)
    if capture is None:
        raise HTTPException(status_code=404, detail="capture not found")
    return capture


@app.get("/captures/latest")
def get_latest_capture():
    capture = store.latest_capture()
    if capture is None:
        raise HTTPException(status_code=404, detail="no captures have been staged yet")
    return capture


if __name__ == "__main__":
    import os
    import uvicorn

    host = os.getenv("CAPTURE_API_HOST", "0.0.0.0")
    port = int(os.getenv("CAPTURE_API_PORT", "8002"))
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
