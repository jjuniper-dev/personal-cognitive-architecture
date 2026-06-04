# PCA Event Backbone — Per-Class Payload Contracts

This document defines the `payload` shape for each `event_class` in the PCA event schema (`schemas/pca-event.schema.json`).

Every workflow, tool, or agent that emits a durable event must populate `payload` according to its class contract below. Payload fields not listed here are allowed only if they are documented in the emitting workflow's own spec.

---

## 1. `capture` — Knowledge Ingestion

Emitted when raw input enters the PCA system. Always the first event in a processing chain.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `input_hash` | string | SHA256 prefix of raw input. Used for deduplication. |
| `mime_type` | string | MIME type of captured content (`text/plain`, `audio/wav`, `image/png`, etc.). |
| `source_channel` | string | Entry point: `telegram`, `obsidian`, `voice`, `web`, `shortcut`, `api`. |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `transcription` | string | For `capture.voice` — Whisper-produced text. |
| `url` | string | For `capture.url` — the source URL. |
| `filename` | string | For `capture.file` or `capture.image` — original filename. |
| `byte_size` | integer | Size of raw input in bytes. |
| `language` | string | Detected language code (e.g., `en`). |
| `obsidian_path` | string | Destination path in the Obsidian vault, if already written. |

### Example — `capture.voice` (WF15)

```json
{
  "input_hash": "3f7a2b9c",
  "mime_type": "audio/wav",
  "source_channel": "shortcut",
  "transcription": "Note to self: check the Vault unseal procedure.",
  "filename": "2026-06-03-voice.wav",
  "byte_size": 184320
}
```

### Example — `capture.image` (WF16)

```json
{
  "input_hash": "9a1b2c3d",
  "mime_type": "image/png",
  "source_channel": "api",
  "filename": "diagram-2026-06-03.png",
  "byte_size": 98304,
  "obsidian_path": "08_Media/2026-06-03_9a1b2c3d.png"
}
```

---

## 2. `classify` — Schema Tagging and Routing

Emitted when a knowledge object is assigned `type`, `tags`, `classification`, and `confidence`. Produced by WF10 classification step or WF-Classify.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `object_id` | string | ID of the knowledge object being classified. |
| `assigned_type` | string | The `type` enum value assigned (`note`, `incident`, `research`, etc.). |
| `assigned_tags` | array[string] | Tags assigned by the classifier. |
| `confidence` | number | 0.0–1.0 confidence score. |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `classification_level` | string | `public`, `internal`, `confidential`, or `restricted`. |
| `reasoning` | string | Short explanation of the classification decision. |
| `previous_type` | string | The `type` before reclassification, if this is an override. |
| `override_by` | string | Actor ID if a human overrode an automated classification. |

### Example — `classify.auto` (WF10)

```json
{
  "object_id": "note_3f7a2b9c",
  "assigned_type": "note",
  "assigned_tags": ["vault", "infra", "procedure"],
  "confidence": 0.82,
  "classification_level": "internal",
  "reasoning": "Content discusses internal infrastructure configuration."
}
```

---

## 3. `reconcile` — Contradiction and Staleness Resolution

Emitted when the system detects a conflict between knowledge objects, or marks an object as stale. Produced by WF10 contradiction detection (E1.3.1) or the reconciliation engine.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `object_id` | string | The primary knowledge object involved. |
| `reconcile_reason` | string | `contradiction`, `merge`, or `stale` — mirrors `event_type` subtype. |

### Optional fields — contradiction

| Field | Type | Description |
|-------|------|-------------|
| `conflict_with` | array[string] | IDs of objects that contradict `object_id`. |
| `similarity_score` | number | Qdrant cosine similarity that triggered the check. |
| `contradiction_reason` | string | Human-readable explanation of the contradiction. |
| `neo4j_edge` | string | Cypher edge created (e.g., `CONTRADICTS(note_abc, note_xyz)`). |

### Optional fields — stale

| Field | Type | Description |
|-------|------|-------------|
| `last_validated_at` | string | ISO 8601 timestamp when object was last validated. |
| `staleness_days` | integer | Days since last validation that triggered the stale flag. |

### Optional fields — merge

| Field | Type | Description |
|-------|------|-------------|
| `merged_into` | string | ID of the object this one was merged into. |
| `merged_fields` | array[string] | Field names that were merged. |

### Example — `reconcile.contradiction` (WF10)

```json
{
  "object_id": "note_abc",
  "reconcile_reason": "contradiction",
  "conflict_with": ["note_xyz"],
  "similarity_score": 0.91,
  "contradiction_reason": "Conflicting claim about Vault unseal procedure.",
  "neo4j_edge": "CONTRADICTS(note_abc, note_xyz)"
}
```

---

## 4. `retrieve` — Memory Lookup

Emitted when an agent or workflow queries stored knowledge. Produced by WF12 or any retrieval path (semantic, graph, hybrid).

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | The query string submitted. |
| `retrieval_method` | string | `semantic`, `graph`, or `hybrid`. |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `collection` | string | Qdrant collection queried (`pca_vault`, `pca_memory`). |
| `top_k` | integer | Number of results requested. |
| `results_returned` | integer | Number of results actually returned. |
| `top_score` | number | Highest similarity score in result set. |
| `graph_hops` | integer | Neo4j traversal depth used (for `graph` or `hybrid`). |
| `filters` | object | Metadata filters applied (e.g., `{"type": "incident", "status": "validated"}`). |
| `result_ids` | array[string] | IDs of returned knowledge objects. |
| `caller` | string | Workflow or agent that triggered this retrieval. |

### Example — `retrieve.semantic` (WF12)

```json
{
  "query": "Vault unseal procedure",
  "retrieval_method": "semantic",
  "collection": "pca_vault",
  "top_k": 5,
  "results_returned": 3,
  "top_score": 0.87,
  "caller": "WF09",
  "result_ids": ["note_abc", "note_def", "note_ghi"]
}
```

---

## 5. `execute` — Workflow, Agent, or Tool Invocation

Emitted when a workflow, agent, or tool is invoked for a consequential action. Produced by WF-Dispatch, WF09, or any orchestrator.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | The workflow ID, agent name, or tool name being invoked. |
| `action` | string | The action requested (`restart`, `generate-code`, `deploy`, etc.). |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `input_summary` | string | Brief description of the input. |
| `input_hash` | string | Hash of the full input for deduplication/replay. |
| `container_name` | string | For `execute.tool` against WF-Docker — container being acted on. |
| `allowed_actions` | array[string] | For WF-Docker: whitelist of permitted actions. |
| `timeout_ms` | integer | Execution timeout in milliseconds. |
| `triggered_by` | string | The upstream event or actor that caused this execution. |

### Example — `execute.tool` (WF-Docker)

```json
{
  "target": "WF-Docker",
  "action": "restart",
  "container_name": "qdrant",
  "allowed_actions": ["restart", "inspect", "logs"],
  "triggered_by": "pca_health_check.ps1"
}
```

### Example — `execute.workflow` (WF-Dispatch → WF09)

```json
{
  "target": "WF09",
  "action": "generate-code",
  "input_summary": "Write a Cypher query for blast-radius lookup",
  "input_hash": "a1b2c3d4",
  "triggered_by": "WF-Dispatch"
}
```

---

## 6. `alert` — Threshold, Failure, and Approval Notifications

Emitted when a monitored condition is breached, a workflow fails, or a human approval is required. Produced by WF13 (failure alerting), the health check, or the runtime policy gate.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `alert_reason` | string | Human-readable description of what triggered the alert. |
| `severity` | string | `info`, `warning`, `error`, or `critical`. |

### Optional fields — threshold

| Field | Type | Description |
|-------|------|-------------|
| `metric` | string | The metric that breached threshold (`token_cost_usd`, `container_restarts`). |
| `threshold` | number | The threshold value. |
| `actual_value` | number | The observed value that triggered the alert. |

### Optional fields — failure

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | The n8n workflow ID that failed. |
| `error_message` | string | Error text from n8n or the script. |
| `execution_id` | string | n8n execution ID for lookup. |

### Optional fields — approval-required

| Field | Type | Description |
|-------|------|-------------|
| `approval_gate` | string | Gate name: `publish-gate`, `cloud-call-gate`, `consequential-action-gate`. |
| `pending_action` | string | Description of the action awaiting approval. |
| `approver` | string | Expected approver identity. |
| `expires_at` | string | ISO 8601 timestamp after which the approval request expires. |

### Example — `alert.failure` (WF13)

```json
{
  "alert_reason": "WF10 execution failed at embedding step",
  "severity": "error",
  "workflow_id": "t55Sd3ZV5xFj9vIT",
  "error_message": "Qdrant connection refused at localhost:6333",
  "execution_id": "n8n-exec-00471"
}
```

### Example — `alert.approval-required` (runtime policy gate)

```json
{
  "alert_reason": "Publish action requires approval — content classification: confidential",
  "severity": "warning",
  "approval_gate": "publish-gate",
  "pending_action": "Publish note_abc to public wiki",
  "approver": "james",
  "expires_at": "2026-06-03T20:00:00Z"
}
```

---

## 7. `audit` — Access, Publish, Approval, and Lifecycle Records

Emitted for durable compliance records: who accessed what, when content was published, what was approved, and knowledge lifecycle state transitions. These events are append-only and must never be modified after emission.

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | string | The ID of the object this audit event concerns. |
| `audit_action` | string | What happened: `read`, `write`, `publish`, `approve`, `reject`, `archive`, `delete`. |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `previous_state` | string | Prior lifecycle state of the subject (for lifecycle transitions). |
| `new_state` | string | New lifecycle state after the transition. |
| `publication_target` | string | For `audit.publish` — where content was published (`wiki`, `obsidian`, `external-api`). |
| `approval_reference` | string | ID of the approval event that authorized this action. |
| `policy_decision_id` | string | ID of the runtime policy gate decision that governed this event. |
| `reason` | string | Human-readable reason for the action (especially for rejection). |

### Example — `audit.publish`

```json
{
  "subject_id": "note_abc",
  "audit_action": "publish",
  "publication_target": "wiki",
  "approval_reference": "evt_approval_9a1b",
  "policy_decision_id": "policy-2026-06-03-001",
  "new_state": "reconciled"
}
```

### Example — `audit.lifecycle`

```json
{
  "subject_id": "note_xyz",
  "audit_action": "archive",
  "previous_state": "stale",
  "new_state": "archived",
  "reason": "Content superseded by note_abc after contradiction resolution."
}
```

---

## Correlation chain example

A single voice capture session produces correlated events sharing `correlation_id: corr_voice_session_001`:

```
capture.voice (WF15) → classify.auto (WF10) → reconcile.contradiction (WF10)
  → retrieve.semantic (WF12) → execute.workflow (WF-Dispatch) → audit.lifecycle
```

All events in the chain carry the same `correlation_id`. Use it to reconstruct the full processing chain for any given input.

---

## Schema relationship

A `capture.*` event's `payload` describes the raw input. After WF10 processes it, the output conforms to `schemas/canonical-metadata.schema.json`. The `correlation_id` links the capture event to the resulting knowledge object.

For WF10 specifically:
- Capture event `payload.input_hash` = canonical metadata `provenance.input_hash`
- Capture event `source_channel` maps to canonical metadata `source`
- `outcome.artifacts` contains the Obsidian path of the written note
