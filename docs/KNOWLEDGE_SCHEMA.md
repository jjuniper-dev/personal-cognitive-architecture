---
type: specification
created: 2026-05-28
updated: 2026-05-28
tags: [pca, schema, knowledge, metadata, wf10]
status: active
---

# PCA Knowledge Schema

## Purpose

This document defines the canonical metadata contract for PCA knowledge objects. WF10 and all downstream workflows should validate against this schema before writing durable knowledge to vault, graph, or derived stores.

## Scope

This schema applies to normalized knowledge objects, not raw capture payloads. It is the contract for objects that have crossed the capture boundary and are ready for validation, routing, storage, and retrieval.

## Contract Summary

The task spec references eight fields, but the listed contract contains nine top-level metadata fields:

1. `type`
2. `source`
3. `confidence`
4. `status`
5. `tags`
6. `relationships`
7. `created_at`
8. `updated_at`
9. `provenance`

This document specifies all nine listed fields so WF10 has an unambiguous target.

## Canonical Field Definitions

| Field | Type | Required | Default | Validation Rules | Examples |
| --- | --- | --- | --- | --- | --- |
| `type` | `string` | Yes | None | Must be one of the `type` enum values. Lowercase snake-safe string. One primary type only. | `note`, `decision` |
| `source` | `string` | Yes | None | Must be one of the `source` enum values. Represents the ingress or authoring surface, not the storage destination. | `obsidian`, `voice` |
| `confidence` | `number` | Yes | `0.5` for machine-created objects when omitted upstream; no default for human-authored objects | Decimal in range `0.0` to `1.0`. Human-entered values should use at most two decimal places. | `0.82`, `1.0` |
| `status` | `string` | Yes | `raw` | Must be one of the `status` enum values. Status advances through the pipeline; downstream systems should not silently downgrade without audit. | `raw`, `validated` |
| `tags` | `array<string>` | No | `[]` | Each tag must be a non-empty lowercase string after normalization. No `null` entries. Deduplicate before write. | `["pca", "workflow"]`, `[]` |
| `relationships` | `array<object>` | No | `[]` | Each relationship object must include `type` and `target`. Optional `direction` and `confidence` must validate if present. | `[{"type":"supports","target":"decision:ddr-v1"}]` |
| `created_at` | `string` | Yes | None | Must be ISO8601 with timezone offset or `Z`. Immutable after first durable write. | `2026-05-23T18:12:30.271-04:00` |
| `updated_at` | `string` | Yes | `created_at` on first write | Must be ISO8601 with timezone offset or `Z`. Must be greater than or equal to `created_at`. Update on every durable mutation. | `2026-05-28T10:15:00Z` |
| `provenance` | `object` | Yes | None | Must include `workflow`, `model`, and `version`. Use explicit `"manual"` values when no model or workflow executed. | `{"workflow":"WF10","model":"claude-3-7-sonnet","version":"2026-05-28"}` |

## Enum Definitions

### `type`

Canonical `type` values:

- `note`
- `incident`
- `research`
- `decision`
- `task`
- `reference`
- `conversation`
- `voice`

Guidance:

- Use `note` for general durable textual knowledge that does not justify a more specific type.
- Use `voice` only when the knowledge object remains primarily an audio-derived artifact rather than a normalized note.
- Do not create ad hoc values such as `reflection`, `text`, or `schema` in WF10 output.

### `source`

The task spec says six values, but it lists seven. This document preserves the listed set so the implementation target is explicit.

Canonical `source` values:

- `obsidian`
- `telegram`
- `voice`
- `web`
- `pdf`
- `agent`
- `manual`

Guidance:

- `source` describes where the object entered PCA.
- Do not overload `source` with device names or transport labels such as `iphone` or `api`.
- Map technical ingress details into provenance or capture metadata, not the canonical `source` field.

### `status`

Canonical `status` values:

- `raw`
- `validated`
- `reconciled`
- `stale`
- `archived`

Guidance:

- `raw`: captured or normalized, not yet accepted into canonical memory.
- `validated`: passes schema and minimum quality gates.
- `reconciled`: linked, deduplicated, and aligned with existing memory.
- `stale`: retained for traceability but no longer trusted as current.
- `archived`: intentionally retained but removed from active reasoning paths.

## Temporal Field Format

`created_at` and `updated_at` must use ISO8601 timestamps with an explicit timezone:

- Accept: `2026-05-23T18:12:30.271-04:00`
- Accept: `2026-05-28T10:15:00Z`
- Reject: `2026/05/28 10:15`
- Reject: `2026-05-28`

Rules:

- Preserve source precision if known.
- Normalize missing timezone information before durable write.
- Never rewrite `created_at` during downstream enrichment.

## Provenance Structure

`provenance` is required for all canonical knowledge objects.

```json
{
  "workflow": "WF10",
  "model": "claude-3-7-sonnet",
  "version": "2026-05-28"
}
```

Rules:

- `workflow`: the workflow or process that produced the canonical object, for example `WF10` or `manual`.
- `model`: the primary model used for extraction, classification, or validation. Use `manual` if no model participated.
- `version`: the workflow export version, schema version, prompt version, or release tag used to produce the object.

Recommended optional extensions for later phases:

- `run_id`
- `prompt_id`
- `operator`
- `capture_id`

These are intentionally not required for E1.2.1 so the base contract stays narrow.

## Relationships Structure

`relationships` is an array of typed edges to other PCA objects.

```json
[
  {
    "type": "supports",
    "target": "decision:ddr-v1",
    "direction": "outbound",
    "confidence": 0.88
  }
]
```

Required fields per relationship object:

- `type`: edge label such as `supports`, `contradicts`, `derived_from`, `references`, `related_to`
- `target`: stable object identifier or resolvable external reference

Optional fields:

- `direction`: `outbound` or `inbound`
- `confidence`: decimal in range `0.0` to `1.0`

Rules:

- `target` must not be free text.
- Relationship labels should remain small and controlled.
- Unknown or unresolved links should be held out of canonical `relationships` until a stable target exists.

## Valid Example Payload

```json
{
  "type": "note",
  "source": "manual",
  "confidence": 0.91,
  "status": "validated",
  "tags": ["pca", "capture", "workflow"],
  "relationships": [
    {
      "type": "references",
      "target": "workflow:wf10",
      "direction": "outbound",
      "confidence": 0.95
    }
  ],
  "created_at": "2026-05-28T10:15:00-04:00",
  "updated_at": "2026-05-28T10:15:00-04:00",
  "provenance": {
    "workflow": "WF10",
    "model": "claude-3-7-sonnet",
    "version": "2026-05-28"
  }
}
```

## Anti-Patterns

Avoid these patterns in WF10 output and downstream writes:

- Using transport or device labels as `source`, for example `iphone` or `api`
- Using ad hoc `type` values such as `reflection`, `text`, or `capture`
- Writing `tags: [null]`
- Omitting `updated_at`
- Storing free-form prose in `relationships.target`
- Using `status: inbox` in canonical metadata
- Emitting canonical objects without `provenance`
- Mixing raw capture metadata into the canonical schema instead of keeping it in capture-specific payloads

## Validation Against Existing Vault Notes

Five existing notes from `050926_vault` style inbox captures were reviewed as migration test cases for this schema.

### 1. `2026-05-23-first-iphone-capture-test.md`

Observed fields:

- has `source`, `tags`, `status`, `created_at`
- missing `type`, `confidence`, `relationships`, `updated_at`, `provenance`
- uses `source: iphone`
- uses `status: inbox`
- uses `capture_type: reflection` rather than canonical `type`

Schema mapping:

- `type` should normalize from `capture_type: reflection` to `note`
- `source` should normalize from `iphone` to `manual` or `voice` depending on actual capture path
- `status` should normalize from `inbox` to `raw`

### 2. `2026-05-23-quick-capture.md`

Observed fields:

- same missing canonical fields as above
- casing and whitespace are inconsistent: `Reflection`, `General`, `iPhone `
- `tags` contains `null`

Schema mapping:

- normalize `type` to `note`
- normalize `source` to `manual` or `voice`
- normalize tags to `[]`
- strip whitespace and lowercase controlled enum values

### 3. `2026-05-23-untitled-capture.md`

Observed fields:

- missing `confidence`, `relationships`, `updated_at`, `provenance`
- uses `capture_type: text`
- uses `source: api`
- uses `status: inbox`

Schema mapping:

- normalize `type` from `text` to `note`
- map `source: api` to the true canonical ingress source, likely `agent` or `manual`
- map `status` to `raw`

### 4. `test-from-container.md`

Observed fields:

- empty file

Schema mapping:

- reject at WF10 validation
- emit an audit event with reason `empty_content`

### 5. `test-pca-capture.md`

Observed fields:

- has `source`, `status`, `created_at`
- missing `type`, `confidence`, `tags`, `relationships`, `updated_at`, `provenance`
- uses `status: inbox`

Schema mapping:

- normalize `type` from `capture_type: reflection` to `note`
- normalize `source: manual` directly
- map `status` to `raw`

## Validation Gaps Identified

The five example notes show the same structural gaps:

- capture-oriented frontmatter is being written instead of canonical knowledge metadata
- canonical timestamps are incomplete because `updated_at` is missing
- provenance is not recorded
- current status values are inbox lifecycle states, not canonical knowledge states
- current source values reflect transport details rather than the canonical enum
- relationship metadata does not exist yet

These gaps are expected for pre-schema captures and should drive the WF10 validation and normalization rules in E1.2.3.

## Implementation Notes For WF10

WF10 should enforce this schema in four stages:

1. **Parse**
   - Read frontmatter or JSON payload
   - Reject empty content and malformed metadata early

2. **Normalize**
   - Map legacy fields such as `capture_type` into canonical `type`
   - Map legacy `status: inbox` to canonical `status: raw`
   - Map transport labels such as `iphone` or `api` into canonical `source`
   - Normalize tags, casing, whitespace, and timestamps

3. **Validate**
   - Enforce required fields
   - Enforce enum membership
   - Enforce timestamp format and ordering
   - Enforce provenance object shape
   - Enforce relationship object shape

4. **Emit**
   - Write canonical metadata to durable storage
   - Record validation failures as audit events
   - Preserve pre-normalization payloads for traceability

Recommended implementation behavior for E1.2.3:

- treat missing `confidence` on human-authored notes as fillable by workflow default rather than a hard reject
- treat missing `provenance` as fillable only when WF10 itself is the writer
- hard-reject empty content, invalid timestamps, and unknown enum values after normalization
- keep legacy field mappings explicit in code, not implicit in prompts

## Review Checklist

- All canonical fields are documented
- Enum values are explicit and closed
- Timestamp and provenance rules are implementable
- Example payload is machine-usable
- Legacy vault-note gaps are documented for WF10 migration logic
