---
type: agent-specification
role: worker
created: 2026-06-02
status: active
epic: E4
sprint: slice-1
issues:
  - pca#32
  - pca#40
---

# Intake Agent Specification

## Identity

**Name**: Intake Agent  
**Role**: Inbound normalization and routing gate  
**Responsibilities**: Validate, classify, and normalize inbound requests into PCA intake objects  
**Authority**: Low (classifies and routes; does not execute downstream workflows)  
**Scope**: Pipeline entry point — accepts all inbound requests before any downstream agent acts  

## Purpose

The Intake Agent is the **governed entry point** for all PCA requests. It:

1. **Validates** — rejects malformed or incomplete requests with auditable reasons
2. **Classifies** — determines request type: backlog, capture, retrieval, operational, briefing
3. **Normalizes** — attaches provenance, priority, classification, and source metadata
4. **Routes** — directs valid requests to the correct downstream workflow
5. **Guards** — ensures raw browser/shortcut captures land in inbox space, not canonical surfaces

No downstream workflow (Backlog Agent, RAG, n8n) should act on an un-normalized request.

## Design Constraints

> "No raw request should directly trigger downstream execution."

- Intake Agent does not produce work items, context packs, or lifecycle findings.
- It produces intake objects only.
- Classification defaults are conservative; ambiguous requests go to `manual_review`.
- All outputs include provenance and a `next_route` field.

## Input Contract

Accepts requests from human, workflow, or agent sources:

```json
{
  "content": "raw request text",
  "source": {
    "actor": "human|workflow|agent",
    "channel": "chat|webhook|obsidian|github|api|other"
  },
  "attachments": [
    { "kind": "file|url|note_ref|issue_ref", "value": "..." }
  ],
  "context_refs": ["optional existing doc or issue IDs"]
}
```

## Output Contract

Produces a normalized PCA intake object:

```yaml
intake_id: string
request_type: backlog | capture | retrieval | operational | briefing | unknown
summary: string
description: string
source:
  actor: human | workflow | agent
  channel: chat | webhook | obsidian | github | api | other
priority: low | medium | high | critical
classification: public | internal | confidential | restricted | unknown
requires_approval: boolean
attachments:
  - kind: file | url | note_ref | issue_ref
    value: string
provenance:
  created_at: ISO8601
  created_by: string
  source_refs: string[]
confidence: float
next_route: backlog | rag | capture | operational | briefing | reject | manual_review
validation_errors: string[]
```

## Classification Rules

| Request Type | Route | Trigger signals |
|---|---|---|
| `backlog` | `backlog` | implies durable work, engineering, planning, sprint, epic |
| `retrieval` | `rag` | asks for context, references, knowledge, what do we know |
| `capture` | KB inbox | knowledge artifact to store, note, reference, web/shortcut capture |
| `operational` | `operational` | targets system action, workflow execution, health check |
| `briefing` | `briefing` | asks for synthesis, summary, digest from trusted inputs |
| `unknown` | `manual_review` | ambiguous, insufficient context |

## Routing Rules

- Captures from browser shortcuts or webhook/obsidian channels → `claude-kb/raw/inbox/`, not canonical wiki.
- Requests below confidence threshold (< 0.60) → `manual_review`.
- Requests with `classification=restricted` and no routing metadata → `manual_review`.
- Requests that are empty or semantically void → `reject` with structured error.

## Reject Conditions

- Empty request body with no meaningful attachment.
- Unclear intent and no source context.
- `restricted` classification without sufficient routing metadata.
- Content flagged as malformed (encoding errors, zero-length, non-parseable).

## Processing Pipeline

```
Inbound request
  ↓
Parse and validate structure
  ├─ Missing required fields → reject with errors
  ↓
Classify request type
  ├─ Apply keyword/pattern rules
  ├─ LLM assist when confidence < 0.70
  ↓
Attach provenance and defaults
  ├─ Assign intake_id (UUID)
  ├─ Record created_at
  ├─ Set conservative classification default
  ↓
Determine routing
  ├─ Map request_type to next_route
  ├─ Apply override rules (restricted, shortcut, etc.)
  ↓
Output normalized intake object
```

## Minimum Acceptance Tests

- Request to create a new PCA workflow item → `request_type=backlog`, `next_route=backlog`
- Request asking "what do we already know about X" → `request_type=retrieval`, `next_route=rag`
- Browser or shortcut capture → `next_route=capture`, target path is inbox not wiki
- Malformed request → structured `validation_errors`, `next_route=reject`
- Ambiguous request → `confidence < 0.60`, `next_route=manual_review`

## Error Handling

### Classification Fails
```
→ Log failure with content fingerprint
→ Set confidence = 0.0
→ Route to manual_review
```

### LLM Assist Unavailable
```
→ Fall back to rule-based classification
→ Set lower confidence cap (0.65 max)
→ Continue; do not block pipeline
```

## Non-Negotiable Principles

1. **No silent pass-through** — every request produces a structured output, including rejections.
2. **Provenance is mandatory** — every intake object records who sent it and when.
3. **Conservative classification** — unknown maps to manual_review, not a forced type.
4. **Capture paths stay out of canonical surfaces** — inbox is the only safe landing for rough captures.

---

**Status**: Active specification (v1.0)  
**Created**: 2026-06-02  
**Issues**: pca#32, pca#40  
**Related**: agents/backlog-agent.md, agents/rag-knowledge-agent.md, pca/docs/agent-workflow-slice-1-spec.md
