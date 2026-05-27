# Observability Architecture

## Purpose

The Observability Architecture defines how the Personal Cognitive Architecture (PCA) measures, traces, monitors, audits, and explains its own operation.

The goal is not merely uptime monitoring.

The goal is cognitive operational awareness.

The PCA should be able to answer:

- what happened
- why it happened
- which agent performed it
- which workflow triggered it
- which knowledge changed
- whether policy was enforced
- whether contradictions increased
- whether confidence changed
- whether failures occurred
- whether human review was bypassed

## Core Principle

Every meaningful action within the PCA should be:

- traceable
- observable
- explainable
- attributable
- measurable
- replayable where possible

## Observability Domains

| Domain | Purpose |
|---|---|
| Infrastructure | Containers, hosts, services |
| Workflows | n8n execution health |
| Agents | Agent behavior and outcomes |
| Knowledge | Knowledge lifecycle and reconciliation |
| Policy | Runtime Policy Gate decisions |
| Retrieval | Query quality and memory behavior |
| Outputs | Artifact generation quality |
| Security | Secrets and boundary events |
| Finance | API costs and usage |

## Observability Pillars

### 1. Logs

Structured records of events and execution.

Examples:

- workflow failures
- policy denials
- reconciliation outcomes
- agent execution traces
- ingestion failures

### 2. Metrics

Numerical measurements over time.

Examples:

- workflow success rate
- capture volume
- contradiction frequency
- retrieval latency
- token consumption
- approval rate

### 3. Traces

End-to-end execution lineage.

Examples:

```text
capture.received
  → validation.scored
  → reconciliation.expanded
  → knowledge.created
  → artifact.generated
```

### 4. Events

Canonical state transitions emitted by the Event Taxonomy.

Events form the backbone of observability.

## Canonical Trace Model

Every execution path should include:

```yaml
trace_id:
causation_id:
actor_id:
workflow_id:
agent_id:
policy_decision_id:
start_timestamp:
end_timestamp:
status:
```

## Required Metrics

### Infrastructure Metrics

| Metric | Description |
|---|---|
| CPU usage | Host and container CPU |
| Memory usage | RAM consumption |
| Disk usage | Persistent storage utilization |
| Container restart count | Stability indicator |
| GPU utilization | Local inference monitoring |

### Workflow Metrics

| Metric | Description |
|---|---|
| Workflow success rate | Successful executions |
| Workflow failure rate | Failed executions |
| Retry count | Retry behavior |
| Queue depth | Backlog visibility |
| Execution duration | Latency monitoring |

### Agent Metrics

| Metric | Description |
|---|---|
| Agent execution count | Operational volume |
| Agent failure rate | Reliability |
| Tool denial rate | Policy interaction |
| Human approval rate | Governance dependency |
| Token usage | Consumption visibility |

### Knowledge Metrics

| Metric | Description |
|---|---|
| Knowledge objects created | Growth rate |
| Trusted promotions | Maturity signal |
| Contradiction count | Cognitive instability indicator |
| Archived objects | Lifecycle activity |
| Review backlog | Governance load |

### Retrieval Metrics

| Metric | Description |
|---|---|
| Retrieval latency | Query performance |
| Retrieval success rate | Search effectiveness |
| Empty query rate | Knowledge gaps |
| Similarity confidence | Retrieval quality |

### Policy Metrics

| Metric | Description |
|---|---|
| Policy approvals | Allowed actions |
| Policy denials | Blocked actions |
| Sandbox executions | Constrained executions |
| Approval wait time | Human governance latency |
| Boundary violations | Security concerns |

### Output Metrics

| Metric | Description |
|---|---|
| Artifact generation count | Output volume |
| Artifact failure rate | Output reliability |
| Validation pass rate | Quality assurance |
| Accessibility compliance rate | WCAG adherence |

## Log Structure

All logs should be structured.

Example:

```json
{
  "timestamp": "2026-05-27T12:00:00Z",
  "trace_id": "trace-123",
  "event_type": "workflow.failed",
  "workflow_id": "WF10",
  "agent_id": "observability-monitor",
  "severity": "error",
  "message": "Neo4j write timeout",
  "retryable": true
}
```

## Severity Levels

| Level | Meaning |
|---|---|
| debug | Diagnostic detail |
| info | Normal operation |
| warning | Elevated attention required |
| error | Execution failure |
| critical | System-level risk |

## Health States

| State | Meaning |
|---|---|
| healthy | Operating normally |
| degraded | Reduced functionality |
| impaired | Significant operational issues |
| failed | Non-operational |
| isolated | Intentionally disconnected/sandboxed |

## Dashboard Requirements

The PCA should eventually expose:

### Operational Dashboard

Displays:

- workflow health
- agent health
- active incidents
- queue depth
- failure rates
- recent alerts

### Cognitive Dashboard

Displays:

- trusted knowledge growth
- contradiction trends
- review backlog
- confidence changes
- active domains
- knowledge freshness

### Governance Dashboard

Displays:

- approvals vs denials
- restricted-domain activity
- boundary crossings
- policy violations
- external API usage

### Cost Dashboard

Displays:

- token consumption
- API costs
- model usage distribution
- local vs cloud inference ratio

## Incident Model

An incident should be created when:

- workflows repeatedly fail
- contradiction spikes occur
- policy violations occur
- storage systems become unavailable
- agent execution loops emerge
- trust-state corruption is detected
- secrets access anomalies occur

## Retention Strategy

| Data Type | Suggested Retention |
|---|---|
| Raw events | Long-term |
| Debug logs | Short-term |
| Metrics aggregates | Medium/long-term |
| Incident records | Long-term |
| Trace data | Medium-term |

## MVP Observability Stack

Initial lightweight implementation:

| Component | Purpose |
|---|---|
| JSONL logs | Event persistence |
| n8n execution history | Workflow traces |
| Obsidian operational journal | Human-readable operational record |
| Daily digest workflow | Summary reporting |
| Neo4j | Relationship and lineage inspection |

## Future Evolution

Potential future capabilities:

- distributed tracing
- OpenTelemetry
- Grafana dashboards
- anomaly detection
- self-healing workflows
- predictive failure analysis
- trust-drift detection
- operational replay tools
- cognitive heatmaps

## Anti-Patterns

Avoid:

- silent failures
- hidden retries
- unstructured logs
- missing trace IDs
- workflows without health monitoring
- agents without execution metrics
- irreversible operations without audit trails

## Relationship to Other Artifacts

| Artifact | Relationship |
|---|---|
| Event Taxonomy | Defines canonical observable events |
| Runtime Policy Gate | Emits policy decisions and violations |
| Agent Registry | Defines observable actors |
| Reconciliation Engine | Emits confidence and contradiction events |
| Knowledge Lifecycle State Machine | Produces lifecycle transitions |