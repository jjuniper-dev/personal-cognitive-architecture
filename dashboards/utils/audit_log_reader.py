"""
Audit Log Reader - Parse and analyze PCA audit logs
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class AuditEntry:
    """Structured audit log entry"""

    timestamp: datetime
    candidate_id: str
    source_type: str
    stage: str
    routing_action: str
    processing_time_ms: int
    cost_usd: float
    confidence: float
    classification: Dict
    routing_decision: str
    destination: str
    status: str  # success, error, pending
    error_message: Optional[str] = None


class AuditLogReader:
    """Read and parse audit logs from JSONL files"""

    def __init__(self, audit_log_path: Path):
        self.audit_log_path = audit_log_path

    def read_logs(self, hours: int = 24) -> List[AuditEntry]:
        """Read audit logs from last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        entries = []

        if not self.audit_log_path.exists():
            return entries

        # Find log files in date range
        log_files = sorted(self.audit_log_path.glob("audit-*.jsonl"), reverse=True)

        for log_file in log_files:
            file_date_str = log_file.stem.replace("audit-", "")
            try:
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                if file_date < (cutoff_time - timedelta(days=1)):
                    continue  # Skip old files
            except ValueError:
                continue

            with open(log_file, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        entry_time = datetime.fromisoformat(
                            data.get("audit_timestamp", "")
                        )

                        if entry_time >= cutoff_time:
                            entries.append(self._parse_entry(data))
                    except (json.JSONDecodeError, ValueError):
                        continue

        return sorted(entries, key=lambda x: x.timestamp)

    def _parse_entry(self, data: Dict) -> AuditEntry:
        """Parse raw JSON entry to AuditEntry"""
        return AuditEntry(
            timestamp=datetime.fromisoformat(
                data.get("audit_timestamp", datetime.now().isoformat())
            ),
            candidate_id=data.get("candidate_id", "unknown"),
            source_type=data.get("source_type", "unknown"),
            stage=data.get("stage", "unknown"),
            routing_action=data.get("routing_action", "unknown"),
            processing_time_ms=data.get("processing_time_ms", 0),
            cost_usd=data.get("cost_usd", 0.0),
            confidence=data.get("confidence", 0.0),
            classification=data.get("classification", {}),
            routing_decision=data.get("routing_decision", "unknown"),
            destination=data.get("destination", ""),
            status=data.get("status", "unknown"),
            error_message=data.get("error_message"),
        )

    def get_entries_by_stage(self, entries: List[AuditEntry], stage: str) -> List[AuditEntry]:
        """Filter entries by pipeline stage"""
        return [e for e in entries if e.stage == stage]

    def get_entries_by_source_type(
        self, entries: List[AuditEntry], source_type: str
    ) -> List[AuditEntry]:
        """Filter entries by source type"""
        return [e for e in entries if e.source_type == source_type]

    def get_entries_by_action(
        self, entries: List[AuditEntry], action: str
    ) -> List[AuditEntry]:
        """Filter entries by routing action"""
        return [e for e in entries if action.upper() in e.routing_action.upper()]

    def get_failed_entries(self, entries: List[AuditEntry]) -> List[AuditEntry]:
        """Get entries with errors"""
        return [e for e in entries if e.status == "error"]

    def get_escalated_entries(self, entries: List[AuditEntry]) -> List[AuditEntry]:
        """Get entries that were escalated"""
        return [e for e in entries if "ESCALATE" in e.routing_action]


class MetricsCalculator:
    """Calculate metrics from audit entries"""

    @staticmethod
    def throughput(entries: List[AuditEntry], interval_minutes: int = 60) -> float:
        """Calculate captures per minute"""
        if not entries:
            return 0.0

        time_span = (entries[-1].timestamp - entries[0].timestamp).total_seconds() / 60
        if time_span == 0:
            return 0.0

        return len(entries) / time_span

    @staticmethod
    def average_latency(entries: List[AuditEntry]) -> float:
        """Calculate average processing latency in ms"""
        if not entries:
            return 0.0

        latencies = [e.processing_time_ms for e in entries if e.processing_time_ms > 0]
        return sum(latencies) / len(latencies) if latencies else 0.0

    @staticmethod
    def latency_percentiles(entries: List[AuditEntry]) -> Dict[str, float]:
        """Calculate latency percentiles"""
        latencies = sorted(
            [e.processing_time_ms for e in entries if e.processing_time_ms > 0]
        )

        if not latencies:
            return {"p50": 0, "p95": 0, "p99": 0}

        n = len(latencies)
        return {
            "p50": latencies[int(n * 0.5)],
            "p95": latencies[int(n * 0.95)],
            "p99": latencies[int(n * 0.99)],
        }

    @staticmethod
    def success_rate(entries: List[AuditEntry]) -> float:
        """Calculate success rate as percentage"""
        if not entries:
            return 0.0

        successful = sum(1 for e in entries if e.status == "success")
        return (successful / len(entries)) * 100

    @staticmethod
    def total_cost(entries: List[AuditEntry]) -> float:
        """Calculate total cost"""
        return sum(e.cost_usd for e in entries)

    @staticmethod
    def cost_by_operation(entries: List[AuditEntry]) -> Dict[str, float]:
        """Break down cost by operation type"""
        costs = {}
        for entry in entries:
            operation = entry.stage
            costs[operation] = costs.get(operation, 0.0) + entry.cost_usd

        return costs

    @staticmethod
    def routing_distribution(entries: List[AuditEntry]) -> Dict[str, int]:
        """Get distribution of routing actions"""
        distribution = {
            "auto_route": 0,
            "review": 0,
            "escalate": 0,
            "quarantine": 0,
        }

        for entry in entries:
            if "ADVANCE" in entry.routing_action:
                distribution["auto_route"] += 1
            elif "ROUTE" in entry.routing_action and "ESCALATE" not in entry.routing_action:
                distribution["review"] += 1
            elif "ESCALATE" in entry.routing_action:
                distribution["escalate"] += 1
            elif "QUARANTINE" in entry.routing_action:
                distribution["quarantine"] += 1

        return distribution

    @staticmethod
    def accuracy_by_pattern(entries: List[AuditEntry]) -> Dict[str, float]:
        """Estimate accuracy by ingestion pattern"""
        patterns = {
            "voice": [],
            "article": [],
            "rss": [],
        }

        for entry in entries:
            if entry.source_type in patterns:
                # Accuracy estimate: success rate - escalation rate
                is_success = entry.status == "success"
                is_escalated = "ESCALATE" in entry.routing_action
                accuracy_score = 1.0 if (is_success and not is_escalated) else 0.0
                patterns[entry.source_type].append(accuracy_score)

        result = {}
        for pattern, scores in patterns.items():
            if scores:
                result[pattern] = (sum(scores) / len(scores)) * 100
            else:
                result[pattern] = 0.0

        return result

    @staticmethod
    def error_analysis(entries: List[AuditEntry]) -> Dict[str, int]:
        """Analyze errors by type"""
        errors = {}
        for entry in entries:
            if entry.error_message:
                error_type = entry.error_message.split(":")[0]
                errors[error_type] = errors.get(error_type, 0) + 1

        return errors
