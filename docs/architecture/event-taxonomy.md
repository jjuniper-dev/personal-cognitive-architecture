# PCA Event Taxonomy

## Purpose

The Event Taxonomy defines the canonical events used by the Personal Cognitive Architecture (PCA) to coordinate capture, validation, reconciliation, memory updates, agent execution, workflow automation, observability, and human review.

The PCA should become event-centric rather than workflow-centric. Workflows may change, but events provide stable contracts across agents, n8n, Obsidian, Neo4j, Qdrant, dashboards, and future runtimes.

## Design Principles

1. Events describe something that happened, not a command to do something.
2. Event names are stable contracts.
3. Every event must include traceability metadata.
4. Events should be replayable where possible.
5. Events should not contain secrets.
6. Event payloads should be small, structured, and link to larger artifacts by reference.
7. Events should support human review and audit.

## Naming Convention

Use lowercase dot-separated names:

```text
<domain>.<entity_or_action>.<state>
```

Examples:

```text
capture.received
validation.scored
knowledge.reconciled
review.required
agent.execution.failed
```

## Required Event Envelope

Every event must include this envelope:

```yaml
event_id: uuid
event_type: string
event_version: string
timestamp: ISO-8601 UTC timestamp
producer: service | workflow | agent | user
trace_id: correlation identifier
causation_id: event_id that caused this event, if any
actor_id: user, agent, workflow, or system identifier
source_system: ios_shortcut | n8n | obsidian | neo4j | qdrant | fastapi | manual | other
domain: personal | work | mixed | system
sensitivity: public | personal | internal | confidential | restricted
payload_ref: optional URI/path/id for larger artifact
payload: structured event-specific content
policy_decision_id: optional link to Runtime Policy Gate decision
schema_version: string
```

## Event Domains

| Domain | Purpose |
|---|---|
| `capture` | Input acquisition |
| `validation` | Scoring and quality checks |
| `reconciliation` | Comparison with existing knowledge |
| `knowledge` | Memory lifecycle and graph updates |
| `agent` | Agent execution lifecycle |
| `workflow` | n8n or automation lifecycle |
| `policy` | Runtime Policy Gate decisions |
| `review` | Human-in-the-loop review |
| `artifact` | Generated outputs |
| `observability` | Health, metrics, and incidents |
| `security` | Secrets, access, and boundary events |
| `finance` | Personal finance ingestion and processing |

## Capture Events

| Event | Meaning |
|---|---|
| `capture.received` | A new input entered the PCA |
| `capture.normalized` | Input was transformed into standard format |
| `capture.enriched` | Metadata or context was added |
| `capture.failed` | Capture failed |
| `capture.duplicate_detected` | Input appears to duplicate existing content |

### Example: capture.received

```json
{
  "event_type": "capture.received",
  "payload": {
    "capture_type": "voice_note",
    "source_label": "ios_shortcut",
    "content_ref": "obsidian://Inbox/2026-05-27-voice-note.md",
    "media_type": "audio/m4a",
    "estimated_size_bytes": 1048576
  }
}
```

## Validation Events

| Event | Meaning |
|---|---|
| `validation.started` | Validation process began |
| `validation.scored` | Input received quality/relevance score |
| `validation.threshold_passed` | Input passed integration threshold |
| `validation.threshold_failed` | Input did not pass threshold |
| `validation.requires_review` | Validation result needs human review |
| `validation.failed` | Validation process failed |

## Reconciliation Events

| Event | Meaning |
|---|---|
| `reconciliation.started` | Reconciliation process began |
| `reconciliation.reinforced` | New input supports existing knowledge |
| `reconciliation.expanded` | New input adds meaningful detail |
| `reconciliation.challenged` | New input conflicts with existing knowledge |
| `reconciliation.replaced` | New input supersedes existing knowledge |
| `reconciliation.ignored` | New input was intentionally not integrated |
| `reconciliation.failed` | Reconciliation process failed |

## Knowledge Events

| Event | Meaning |
|---|---|
| `knowledge.created` | New knowledge object created |
| `knowledge.updated` | Existing knowledge object updated |
| `knowledge.linked` | Relationship created between knowledge objects |
| `knowledge.contested` | Knowledge object marked contested |
| `knowledge.promoted` | Knowledge moved to higher trust state |
| `knowledge.demoted` | Knowledge moved to lower trust state |
| `knowledge.archived` | Knowledge retained but removed from active use |
| `knowledge.rejected` | Knowledge explicitly excluded |
| `knowledge.deleted` | Knowledge removed; requires approval |

## Agent Events

| Event | Meaning |
|---|---|
| `agent.execution.requested` | Agent execution requested |
| `agent.execution.allowed` | Runtime Policy Gate allowed execution |
| `agent.execution.denied` | Runtime Policy Gate denied execution |
| `agent.execution.started` | Agent began work |
| `agent.execution.completed` | Agent completed work |
| `agent.execution.failed` | Agent failed |
| `agent.tool.requested` | Agent requested tool access |
| `agent.tool.allowed` | Tool access allowed |
| `agent.tool.denied` | Tool access denied |

## Workflow Events

| Event | Meaning |
|---|---|
| `workflow.triggered` | Automation workflow triggered |
| `workflow.started` | Workflow began execution |
| `workflow.completed` | Workflow completed successfully |
| `workflow.failed` | Workflow failed |
| `workflow.retry_scheduled` | Retry scheduled |
| `workflow.retry_exhausted` | Retry limit reached |
| `workflow.disabled` | Workflow disabled |
| `workflow.health_checked` | Workflow health check completed |

## Policy Events

| Event | Meaning |
|---|---|
| `policy.evaluation.requested` | Policy decision requested |
| `policy.allowed` | Request allowed |
| `policy.denied` | Request denied |
| `policy.approval_required` | Human approval required |
| `policy.sandbox_required` | Request constrained to sandbox |
| `policy.violation_detected` | Policy violation detected |

## Review Events

| Event | Meaning |
|---|---|
| `review.required` | Human review required |
| `review.assigned` | Review assigned to user/role |
| `review.approved` | Human approved action |
| `review.rejected` | Human rejected action |
| `review.deferred` | Review deferred |
| `review.expired` | Review not completed within expected window |

## Artifact Events

| Event | Meaning |
|---|---|
| `artifact.requested` | Output generation requested |
| `artifact.generated` | Output generated |
| `artifact.validated` | Output validated against requirements |
| `artifact.published` | Output published/shared |
| `artifact.failed` | Output generation failed |

## Observability Events

| Event | Meaning |
|---|---|
| `observability.metric.recorded` | Metric captured |
| `observability.health.degraded` | Component health degraded |
| `observability.health.restored` | Component health restored |
| `observability.incident.created` | Incident created |
| `observability.alert.sent` | Alert sent |
| `observability.daily_digest.generated` | Daily digest generated |

## Security Events

| Event | Meaning |
|---|---|
| `security.secret.requested` | Secret access requested |
| `security.secret.allowed` | Secret access allowed |
| `security.secret.denied` | Secret access denied |
| `security.boundary.crossed` | Data crossed a domain/execution boundary |
| `security.sensitivity.changed` | Sensitivity classification changed |
| `security.violation.detected` | Security violation detected |

## Finance Events

| Event | Meaning |
|---|---|
| `finance.transaction.ingested` | Transaction ingested |
| `finance.transaction.categorized` | Transaction categorized |
| `finance.transaction.review_required` | Transaction needs manual review |
| `finance.summary.generated` | Finance summary generated |
| `finance.processing.failed` | Finance processing failed |

## Minimum Viable Event Set

The MVP event backbone should support at least:

```text
capture.received
validation.scored
reconciliation.reinforced
reconciliation.expanded
reconciliation.challenged
knowledge.created
knowledge.updated
knowledge.promoted
review.required
review.approved
review.rejected
agent.execution.started
agent.execution.completed
agent.execution.failed
workflow.failed
policy.allowed
policy.denied
artifact.generated
observability.incident.created
```

## Storage Targets

| Target | Use |
|---|---|
| JSONL audit log | Append-only event history |
| Neo4j | Event relationships and lineage |
| Obsidian | Human-readable review and summaries |
| Dashboard | Health and operational visibility |
| n8n executions | Workflow-specific traces |

## Implementation Notes

Initial implementation can be a local JSONL event log:

```text
logs/events/pca-events-YYYY-MM-DD.jsonl
```

Each n8n workflow should emit at least:

- start event
- completion event
- failure event
- trace ID

Future implementation may include:

- event bus
- queue-backed processing
- replay tooling
- event schema validation
- event-driven dashboards
- event-to-graph projection

## Anti-Patterns

Avoid:

- workflow-specific event names that cannot be reused
- events without trace IDs
- embedding large content directly in event payloads
- storing credentials in events
- silent state transitions
- agent actions without policy event linkage

## Relationship to Other Artifacts

| Artifact | Relationship |
|---|---|
| Runtime Policy Gate | Consumes and emits policy events |
| Reconciliation Engine | Emits reconciliation and knowledge events |
| Agent Registry | Defines valid agent actors |
| Knowledge Lifecycle State Machine | Defines allowed knowledge state transitions |
| Observability Architecture | Aggregates event-derived operational signals |