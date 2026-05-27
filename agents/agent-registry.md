# PCA Agent Registry

## Purpose

The Agent Registry defines all approved agents, workers, orchestrators, automation roles, and runtime identities within the Personal Cognitive Architecture (PCA).

It exists to:

- prevent uncontrolled agent sprawl
- define execution boundaries
- establish capability ownership
- support Runtime Policy Gate enforcement
- improve observability and traceability
- document orchestration topology

No agent should exist without explicit registration.

## Design Principles

1. Agents are specialized.
2. Agents should have minimal required permissions.
3. Agents should not self-authorize.
4. Agents are runtime actors, not personalities.
5. Agents should emit observable execution events.
6. Agents should remain replaceable.
7. Deterministic workflows should be preferred over autonomous behavior when possible.

## Agent Types

| Type | Purpose |
|---|---|
| Orchestrator | Coordinates workflows and delegates work |
| Worker | Performs narrow scoped tasks |
| Reviewer | Validates outputs or identifies issues |
| Retriever | Retrieves information from memory systems |
| Enricher | Adds metadata or context |
| Publisher | Produces artifacts or notifications |
| Monitor | Observability and operational analysis |
| System | Infrastructure-level operations |

## Canonical Agent Record

Each agent should have a canonical definition.

```yaml
agent_id:
agent_name:
agent_type:
description:
owner:
status:
runtime:
model:
execution_mode:
allowed_tools:
allowed_data_domains:
allowed_output_targets:
requires_human_approval:
can_trigger_agents:
can_write_trusted_knowledge:
max_autonomy_level:
observability_level:
policy_profile:
created:
updated:
```

## Agent Status Values

| Status | Meaning |
|---|---|
| Proposed | Design-stage only |
| Experimental | Limited testing |
| Active | Approved for use |
| Restricted | Special controls required |
| Disabled | Temporarily unavailable |
| Retired | No longer used |

## Execution Modes

| Mode | Meaning |
|---|---|
| Manual | Human-triggered only |
| Assisted | Human initiates; agent executes |
| Semi-Autonomous | Event-triggered with policy controls |
| Autonomous | Executes without direct human initiation |

## Autonomy Levels

| Level | Description |
|---|---|
| 0 | Read-only analysis |
| 1 | Suggest actions only |
| 2 | Perform reversible actions |
| 3 | Trigger workflows |
| 4 | Write trusted knowledge |
| 5 | High-impact execution; requires strong governance |

## Core Agents

### Ayla Orchestrator

```yaml
agent_id: ayla-orchestrator
agent_type: orchestrator
status: active
runtime: Claude Sonnet
execution_mode: assisted
allowed_tools:
  - workflow_router
  - memory_query
  - capture_pipeline
  - web_search
can_trigger_agents: true
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 2
policy_profile: orchestrator-default
```

Purpose:

- coordinate workflows
- route tasks
- determine delegation
- maintain traceability
- invoke Runtime Policy Gate

### Knowledge Query Worker

```yaml
agent_id: knowledge-query-worker
agent_type: worker
status: active
runtime: Claude Haiku
execution_mode: semi-autonomous
allowed_tools:
  - qdrant_query
  - neo4j_query
  - obsidian_search
can_write_trusted_knowledge: false
max_autonomy_level: 1
policy_profile: retrieval-worker
```

Purpose:

- semantic retrieval
- graph retrieval
- context assembly

### Memory Recall Worker

```yaml
agent_id: memory-recall-worker
agent_type: retriever
status: active
runtime: Claude Haiku
execution_mode: semi-autonomous
allowed_tools:
  - qdrant_query
  - neo4j_query
can_write_trusted_knowledge: false
max_autonomy_level: 1
policy_profile: retrieval-worker
```

Purpose:

- retrieve contextual memory
- identify related knowledge
- support conversational continuity

### Critical Review Agent

```yaml
agent_id: critical-review-agent
agent_type: reviewer
status: active
runtime: Claude Haiku
execution_mode: assisted
allowed_tools:
  - contradiction_analysis
  - confidence_review
  - output_review
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 1
policy_profile: review-agent
```

Purpose:

- identify contradictions
- evaluate confidence
- challenge assumptions
- support reconciliation

### Capture Enrichment Worker

```yaml
agent_id: capture-enrichment-worker
agent_type: enricher
status: experimental
runtime: local model
execution_mode: semi-autonomous
allowed_tools:
  - metadata_extraction
  - tagging
  - transcript_processing
can_write_trusted_knowledge: false
max_autonomy_level: 2
policy_profile: enrichment-worker
```

Purpose:

- metadata extraction
- tagging
- title generation
- semantic enrichment

### Observability Monitor

```yaml
agent_id: observability-monitor
agent_type: monitor
status: active
runtime: n8n workflow
execution_mode: autonomous
allowed_tools:
  - workflow_health
  - log_analysis
  - incident_generation
can_write_trusted_knowledge: false
max_autonomy_level: 2
policy_profile: observability-agent
```

Purpose:

- monitor workflow health
- detect failures
- emit alerts
- produce operational summaries

## Runtime Separation

Agents should be separated by:

- purpose
- permissions
- trust domain
- model class
- execution environment

Avoid one general-purpose super-agent.

## Human Governance Rules

Human approval is required when:

- trusted knowledge would be modified
- sensitive data would leave the local environment
- external publication occurs
- secrets would be accessed
- destructive actions occur

## Tool Access Model

Agents should receive explicit allow-listed tools only.

Example:

```yaml
allowed_tools:
  - obsidian_search
  - qdrant_query
```

Avoid wildcard access.

## Identity & Traceability

Every agent execution must emit:

```yaml
trace_id:
agent_id:
execution_id:
workflow_id:
policy_decision_id:
start_time:
end_time:
status:
```

## Observability Expectations

Agents should expose:

- execution count
- success rate
- failure rate
- latency
- retry count
- approval rate
- contradiction rate
- token usage

## Future Agent Categories

Potential future agents:

- visual diagram interpreter
- architecture synthesis agent
- podcast ingestion worker
- YouTube semantic extractor
- financial anomaly detector
- relationship mapper
- graph maintenance agent
- lifecycle archival agent
- memory decay evaluator

## Anti-Patterns

Avoid:

- agents with unrestricted tool access
- self-modifying agents
- agents bypassing policy gates
- hidden workflow execution
- untraceable orchestration
- giant monolithic agents
- permanent autonomous write access

## Relationship to Other Artifacts

| Artifact | Relationship |
|---|---|
| Runtime Policy Gate | Controls agent execution permissions |
| Event Taxonomy | Defines agent execution events |
| Reconciliation Engine | Reviewer agents participate in reconciliation |
| Knowledge Lifecycle State Machine | Determines valid knowledge transitions |
| Observability Architecture | Tracks operational metrics and failures |