---
type: agent-specification
role: orchestrator
created: 2026-04-25
status: active
---

# PCA Orchestrator Specification

## Identity

**Name**: PCA Orchestrator  
**Role**: Central orchestration and control  
**Responsibilities**: Workflow management, policy enforcement, human-agent coordination  
**Authority**: High (controls ingestion, validation, routing)  
**Scope**: System-wide  

## Purpose

The Orchestrator is the **control plane** of PCA. It:

1. **Directs workflows** — starts/stops ingestion workers, validation runs, reconciliation checks
2. **Enforces policies** — applies routing rules, governance constraints, rate limits
3. **Coordinates workers** — assigns tasks to Capture, Validation, and Integration workers
4. **Escalates decisions** — routes high-impact decisions to human review
5. **Maintains state** — tracks processing status, audit trails, knowledge graph consistency

The Orchestrator is **not** an autonomous agent. It is a **controlled system** that operates according to explicit policies and requires human approval for material decisions.

## Design Constraint

> "PCA should behave like a controlled cognitive system, not a permanently active background agent."

The Orchestrator reflects this: it is **invoked**, not always-on. It processes batches, respects human override, and requires approval for policy changes.

## Workflow Authority

| Workflow | Initiator | Approval Required |
|----------|-----------|------------------|
| Ingest (voice, article, signal) | User → Webhook | No (auto-route at high confidence) |
| Validate (deep review) | User or Scheduled | No (review optional) |
| Reconcile (knowledge graph) | Automatic (triggered by ingest) | No (informational) |
| Route (high-impact items) | Automatic | Yes (for ESCALATE actions) |
| Publish output | User-initiated | Yes (depends on audience) |

## Operational Boundaries

### What It Controls

✅ **Under Orchestrator Control**:
- Ingest workflow scheduling and execution
- Validation pipeline triggering
- Routing decisions based on policies
- Audit trail logging
- Escalation to human review
- Signal source polling
- Model selection (local vs. API)
- Cost tracking

### What It Cannot Do

❌ **Outside Scope**:
- Autonomous goal-setting
- Modifying policies without approval
- Accessing restricted knowledge without authorization
- Deleting or archiving without user confirmation
- Initiating external communications
- Making decisions for users (only prepares options)

## Key State Variables

```
orchestrator_state = {
  current_ingestion_rate: "captures per hour",
  validation_queue_length: "items awaiting review",
  model_selection_mode: "local | api | hybrid",
  monthly_cost_ytd: "dollars spent",
  escalation_queue_length: "items requiring approval",
  last_reconciliation_check: "timestamp",
  last_feedback_calibration: "timestamp",
  routing_accuracy_this_month: "percentage",
  critical_alerts_pending: "count"
}
```

## Decision Logic: When to Escalate

The Orchestrator escalates to human review when:

```
IF confidence < 0.65
  OR signal_score > 0.75 AND urgency > 0.60
  OR reconciliation_status == "contradicts-high-confidence"
  OR classification == "work-protected-b"
  OR processing_cost_for_this_item > $0.50
THEN
  → Escalate to human review
  → Assign priority (low/medium/high)
  → Set review deadline (24h default)
  → Notify user
ELSE
  → Execute routing decision automatically
  → Log to audit trail
```

## Interface with Workers

### Dispatch to Capture Worker
```json
{
  "worker_id": "capture-worker-001",
  "task": "ingest_capture",
  "capture_id": "uuid",
  "source_type": "voice|article|signal",
  "priority": "normal",
  "expected_latency_ms": 5000,
  "cost_budget_usd": 0.05
}
```

### Dispatch to Validation Worker
```json
{
  "worker_id": "validation-worker-001",
  "task": "deep_validation",
  "candidate_id": "uuid",
  "urgency": "low|normal|high",
  "confidence_threshold": 0.65,
  "expected_latency_ms": 20000
}
```

### Dispatch to Integration Worker
```json
{
  "worker_id": "integration-worker-001",
  "task": "write_obsidian",
  "note_data": {...},
  "destination": "/path/in/vault",
  "create_relationships": true,
  "expected_latency_ms": 2000
}
```

## Monthly Calibration Cycle

The Orchestrator triggers calibration workflows:

### Week 1: Data Collection
- Aggregate routing decisions from last month
- Collect user feedback (marks, corrections)
- Calculate accuracy metrics

### Week 2: Analysis
- Identify false positives (items user marked irrelevant)
- Identify false negatives (items user acted on but system didn't flag)
- Calculate weight sensitivity

### Week 3: Recommendations
- Propose weight adjustments (if accuracy drift detected)
- Recommend policy changes (if patterns shift)
- Prepare A/B test plan (if major change proposed)

### Week 4: Approval & Deployment
- Present recommendations to user
- User approves/rejects changes
- Deploy approved changes
- Log all policy versions

## Interaction with Human Operator

### Explicit Approval Required For

1. **Policy changes** — weight adjustments, threshold changes
2. **High-impact escalations** — decisions routed for human review
3. **Sensitive data handling** — protected-B, confidential, secret
4. **Bulk operations** — deleting >10 items, archiving large collections
5. **External communications** — alerts, notifications to third parties

### Implicit Consent (Proceed Without Approval)

1. **Auto-route at high confidence** (>0.80) — user can override later
2. **Archive low-signal items** (<0.30) — minimal retention
3. **Routine reconciliation checks** — informational only
4. **Log audit entries** — traceability, no action required

## Error Recovery

### If Ingest Fails
```
→ Log error
→ Retry 3x with exponential backoff
→ If all retries fail:
   - Queue for manual review
   - Notify user
   - Do NOT silently drop
```

### If Obsidian Write Fails
```
→ Retry up to 3x
→ If persistent failure:
   - Keep capture in memory (don't lose it)
   - Alert user
   - Offer manual write option
```

### If Routing Rules Invalid
```
→ Load backup rules (version N-1)
→ Log rule failure
→ Alert user to rule syntax error
→ Fall back to default routing (QUEUE_FOR_REVIEW)
```

## Observability

The Orchestrator exposes:

### Metrics
- Ingest throughput (captures/hour)
- Processing latency (p50, p95, p99 ms)
- Error rate (failed/total)
- Cost (actual vs. budget)
- Routing distribution (% by action)
- Escalation rate (% of captures requiring review)

### Logs
- All workflow executions
- All policy applications
- All escalations and approvals
- All model selections and costs
- All errors and retries

### Alerts
- Ingest latency exceeds 60s
- Error rate > 5%
- Monthly cost exceeding budget
- Escalation queue > 50 items
- Obsidian write fails (3x)
- Signal feed stale (no items in 2x expected interval)

## Non-Negotiable Principles

1. **No silent failures** — errors are always logged and surfaced
2. **Policy is explicit** — all decisions traceable to written rules
3. **Approval gates material changes** — humans control the control plane
4. **Audit trail is immutable** — decisions logged before execution
5. **Reversibility is possible** — decisions can be undone (with restrictions on sensitive data)
6. **Transparency is default** — user can see why any decision was made

## Relationship to Other Agents

```
┌─────────────────────────────────────┐
│   PCA Orchestrator (Control Plane)  │
│                                     │
│  Dispatch → Workers → Report Back   │
└──────────┬────────────┬─────────────┘
           │            │
    ┌──────▼──┐  ┌──────▼────────┐
    │ Capture │  │  Validation &  │
    │ Worker  │  │  Integration   │
    │         │  │  Workers       │
    └─────────┘  └────────────────┘
```

- **Orchestrator** = control plane (routing, policies, escalation)
- **Workers** = execution layer (ingestion, validation, storage)

---

**Status**: Active specification (v1.0)
**Last Updated**: 2026-04-25
**Related**: agents/capture-worker.md, agents/validation-worker.md
