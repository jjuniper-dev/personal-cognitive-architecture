from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import StagedCaptureRecord


class CaptureStore:
    def __init__(self, root_dir: str | Path | None = None):
        default_root = Path(__file__).resolve().parents[4] / "data" / "capture-staging"
        self.root = Path(root_dir or os.getenv("CAPTURE_STAGING_DIR", default_root)).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def stage_capture(self, record: StagedCaptureRecord) -> dict[str, str]:
        capture_dir = self._capture_dir(record.capture_id, record.captured_at)
        capture_dir.mkdir(parents=True, exist_ok=True)

        json_path = capture_dir / "capture.json"
        markdown_path = capture_dir / "capture.md"
        index_path = self.root / "captures.jsonl"
        audit_path = self.root / "audit.jsonl"

        self._write_json(json_path, self._model_dump(record))
        self._write_text(markdown_path, record.body_markdown)
        self._append_jsonl(index_path, {
            "capture_id": record.capture_id,
            "captured_at": record.captured_at.isoformat(),
            "source_type": record.source_type,
            "title": record.title,
            "storage_path": str(capture_dir),
        })
        self._append_jsonl(audit_path, {
            "event": "capture_staged",
            "capture_id": record.capture_id,
            "captured_at": record.captured_at.isoformat(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "storage_path": str(capture_dir),
        })

        return {
            "directory": str(capture_dir),
            "json": str(json_path),
            "markdown": str(markdown_path),
            "index": str(index_path),
            "audit": str(audit_path),
        }

    def read_capture(self, capture_id: str) -> dict[str, Any] | None:
        matches = sorted(self.root.rglob("capture.json"), reverse=True)
        for path in matches:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if payload.get("capture_id") == capture_id:
                return payload
        return None

    def latest_capture(self) -> dict[str, Any] | None:
        index_path = self.root / "captures.jsonl"
        if not index_path.exists():
            return None

        lines = [line for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return None

        return json.loads(lines[-1])

    def _capture_dir(self, capture_id: str, captured_at: datetime) -> Path:
        return self.root / captured_at.strftime("%Y") / captured_at.strftime("%m") / captured_at.strftime("%d") / capture_id

    def _write_json(self, path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def _write_text(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

    def _append_jsonl(self, path: Path, payload: Any) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False))
            handle.write("\n")

    def _model_dump(self, model: Any) -> dict[str, Any]:
        if hasattr(model, "model_dump"):
            return model.model_dump()
        return model.dict()
