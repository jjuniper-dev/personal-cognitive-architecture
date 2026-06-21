"""Optional graph integration for future capture routing.

This module is intentionally a no-op in the POC slice.
The first implementation step stages the iPhone capture locally and exposes it through HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Neo4jCapturePublisher:
    enabled: bool = False

    def publish(self, capture: dict[str, Any]) -> None:
        _ = capture
        return None
