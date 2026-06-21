from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, constr, validator


class IPhoneCaptureRequest(BaseModel):
    source: constr(min_length=1) = Field(
        ...,
        description="Capture source. For the POC webhook, this should be 'iphone'.",
    )
    capture_type: Literal["text"] = Field(
        "text",
        description="First POC slice accepts text payloads only.",
    )
    timestamp: datetime = Field(..., description="ISO-8601 capture timestamp")
    text: constr(strip_whitespace=True, min_length=1, max_length=20000)
    context_note: str | None = Field(
        default=None,
        description="Optional user context supplied with the capture.",
    )
    location: str | None = Field(
        default=None,
        description="Optional user location or place label.",
    )
    tags: list[str] = Field(default_factory=list)

    @validator("tags", pre=True)
    def _normalize_tags(cls, value):  # noqa: N805
        if value is None:
            return []
        if isinstance(value, list):
            return [str(tag).strip() for tag in value if str(tag).strip()]
        if isinstance(value, str):
            return [tag.strip() for tag in value.split(",") if tag.strip()]
        raise TypeError("tags must be a list or comma-separated string")


class CaptureConfidence(BaseModel):
    transcription_confidence: float = 1.0
    extraction_completeness: float = 1.0
    content_coherence: float = 1.0


class CaptureSourceMetadata(BaseModel):
    device: str = "iPhone"
    location: str | None = None
    tags: list[str] = Field(default_factory=list)


class CaptureContent(BaseModel):
    raw_text: str
    word_count: int
    language: str = "en"


class ProcessingNote(BaseModel):
    timestamp: datetime
    stage: str
    note: str


class StagedCaptureRecord(BaseModel):
    capture_id: str
    source_type: Literal["text"]
    source_metadata: CaptureSourceMetadata
    captured_at: datetime
    content: CaptureContent
    classification: Literal[
        "personal",
        "public",
        "work-unclassified",
        "work-protected-b",
        "work-confidential",
        "sensitive",
    ] = "personal"
    processing_state: Literal[
        "raw",
        "extracted",
        "normalized",
        "scored",
        "classified",
        "reconciled",
        "routed",
        "integrated",
        "triggered",
        "audited",
    ] = "raw"
    confidence: CaptureConfidence = Field(default_factory=CaptureConfidence)
    user_context: str | None = None
    ingestion_policy: str = "pca-mobile-poc-v1"
    processing_notes: list[ProcessingNote] = Field(default_factory=list)
    title: str
    body_markdown: str
    storage_paths: dict[str, str] = Field(default_factory=dict)


class CaptureReceipt(BaseModel):
    ok: bool = True
    capture_id: str
    received_at: datetime
    status: Literal["staged"] = "staged"
    storage_paths: dict[str, str]


class HealthResponse(BaseModel):
    status: str
    service: str
    capture_store: str
    timestamp: datetime
