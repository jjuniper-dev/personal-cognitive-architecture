---
type: agent-specification
role: reviewer
created: 2026-06-02
status: active
epic: E4
sprint: slice-1
issues:
  - pca#35
  - pca#40
depends_on:
  - rag-knowledge-agent
---

# Knowledge Lifecycle Agent Specification

## Identity

**Name**: Knowledge Lifecycle Agent  
**Role**: Canon freshness governance and drift detection  
**Responsibilities**: Detect staleness, missing source refs, expired reviews; generate durable review queues and draft proposals  
**Authority**: Low (proposes, does not mutate; all changes are pending human approval)  
**Scope**: Knowledge governance layer — monitors canonical KB and feeds review queues for the Librarian workflow  

## Purpose

The Knowledge Lifecycle Agent continuously governs knowledge freshness and source alignment. It:

1. **Detects** — stale pages, missing `source_ref`, expired review windows, ungrounded seed pages
2. **Queues** — durable review items rather than silent inline edits
3. **Drafts** — source-grounded update proposals for human approval
4. **Reports** — audit artifacts for downstream retrieval and briefing workflows
5. **Exposes** — lifecycle state as a signal available to the RAG Knowledge Agent

This agent is the primary bridge between the new agent workflow stack and the existing Librarian / AI knowledge-ops direction.

## Design Constraint

> "Lifecycle workflows propose changes; they do not silently mutate canon."

- No direct overwrite of canonical content.
- No promotion of rough captures into canon.
- No suppression of lifecycle warnings because a draft patch exists.
- Public promotion requires explicit metadata and approval policy — slice 1 always blocks this path.

## Input Contract

Accepts lifecycle scan requests and RAG-identified gaps:

```json
{
  "scan_scope": "full|incremental|targeted",
  "target_ids": ["optional list of specific page IDs or paths"],
  "metadata_contract": {
    "required_fields": ["source_ref", "owner", "review_after", "status", "sensitivity"],
    "max_stale_days": 90
  },
  "context_pack_ref": "optional context_pack_id from RAG agent"
}
```

## Output Contracts

### Lifecycle review item

```yaml
review_item_id: string
target_id: string
target_type: canonical_page | kb_page | summary | workflow_doc
issue_type: stale | missing_source_ref | invalid_source_ref | review_expired | ungrounded_seed
severity: low | medium | high
summary: string
recommended_action: refresh | validate | link_source | archive | escalate
source_refs: string[]
proposed_patch_ref: string | null
created_at: ISO8601
status: open | proposed | approved | dismissed
```

### Audit artifact

```yaml
audit_id: string
scan_scope: full | incremental | targeted
scan_completed_at: ISO8601
total_pages_scanned: int
findings:
  - review_item_id: string
    target_id: string
    issue_type: string
    severity: string
    recommended_action: string
summary:
  stale_count: int
  missing_source_ref_count: int
  review_expired_count: int
  ungrounded_seed_count: int
artifact_path: string
```

## Detection Rules

### Stale detection
- Page `review_after` date has passed.
- Page `updated_at` is older than `max_stale_days` without a review event.
- Severity: `high` if `status=canonical`, `medium` otherwise.

### Missing source_ref
- `source_ref` field is null, empty, or contains only placeholder text.
- `source_ref` present but refers to a deleted or unreachable artifact.
- Severity: `high` for canonical pages, `low` for drafts.

### Review expired
- `review_after` is in the past and no review record exists.
- Severity: `medium` by default; `high` if page is linked by active workflows.

### Ungrounded seed
- Page has no `source_ref`, no `owner`, `status=draft`, and has not been touched in 30+ days.
- Severity: `low` unless linked from canonical content.

## Draft proposal generation

When a finding has high severity and a `source_ref` is resolvable:
1. Retrieve current source document.
2. Generate a diff-style draft update grounded in the source.
3. Store draft as a proposal in KB draft space (not the canonical page).
4. Populate `proposed_patch_ref` in the review item.
5. Draft is never applied without explicit approval.

## Processing Pipeline

```
Lifecycle scan request
  ↓
Load canonical page metadata
  ↓
Evaluate each page against detection rules
  ├─ Stale check
  ├─ source_ref presence/validity check
  ├─ Review expiry check
  ├─ Ungrounded seed detection
  ↓
For each finding: create review_item
  ├─ Assign severity
  ├─ Recommend action
  ├─ Generate source-grounded draft if applicable
  ↓
Emit audit artifact to KB audit space
  ↓
Expose lifecycle state for RAG Knowledge Agent
```

## Lifecycle State Exposure

For each scanned page, the agent exposes:

```yaml
page_id: string
lifecycle_status: fresh | review_due | stale | missing_ref | ungrounded
last_reviewed: ISO8601 | null
open_review_items: int
has_pending_draft: boolean
```

This is consumed by the RAG Knowledge Agent to downgrade confidence for pages with open lifecycle issues.

## Minimum Acceptance Tests

- Stale canonical page → `review_item` with `issue_type=stale`, `severity=high`.
- Page with `source_ref=null` → `review_item` with `issue_type=missing_source_ref`.
- Generated update remains a proposal (`status=proposed`), not applied to canon.
- Drift report audit artifact is produced under KB audit space.
- No workflow path writes from inbox capture directly to wiki publish output.

## Error Handling

### Knowledge store scan fails
```
→ Emit partial audit with count: "X pages scanned, scan aborted at Y"
→ Flag incomplete scan in audit artifact
→ Do not suppress findings already collected
```

### Draft generation fails
```
→ Create review item without proposed_patch_ref
→ Flag: "draft generation failed — manual review required"
→ Continue; do not block review queue output
```

## Non-Negotiable Principles

1. **Detect, don't mutate** — lifecycle findings feed review queues, not auto-fixes.
2. **Proposals are proposals** — no draft is applied to canon without explicit approval.
3. **Findings are durable** — review items persist until dismissed or resolved.
4. **Audit trail always emitted** — every scan produces a structured artifact.
5. **RAG agent sees lifecycle state** — retrieval confidence degrades for stale or ungrounded pages.

---

**Status**: Active specification (v1.0)  
**Created**: 2026-06-02  
**Issues**: pca#35, pca#40  
**Related**: agents/rag-knowledge-agent.md, pca/docs/agent-workflow-slice-1-spec.md, pca/BACKLOG.md
