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

## Core Agents (Design Registry)

These are the formal design-layer agent definitions. For operational agents in the running system, see **Cross-Repository Agent Inventory** below.

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

---

## Cross-Repository Agent Inventory

PCA agents span three repositories. This section maps all known agents and automation actors across the full system to eliminate blind spots in the registry.

### pca repo agents (jjuniper-dev/pca)

These are operational actors in the running system. See `pca/AGENTS.md` for the operational handbook (work dispatch, escalation, code agent capabilities).

| Agent | Type | Interface | Status |
|---|---|---|---|
| James (operator) | Human / Product Owner | Cowork, phone | Active |
| Cowork Claude | Orchestrator | Cowork desktop | Active |
| Claude Code | Code agent | `start_code_task` dispatch | Active |
| Codex | Code agent, PR-based | GitHub issues, `codex-task` label | Active |
| WF09 / Qwen3-Coder | Code agent, isolated snippets | `POST /webhook/pca/code` | Active |
| WF10 | Capture worker | `POST /webhook/pca/incident` | Active |
| WF12 | Memory worker | `POST /webhook/pca/memory` | Active |
| WF-Dispatch | Task dispatcher | `POST /webhook/pca/dispatch` | Active |
| WF-Ayla | Ayla persona chatbot | `POST /webhook/pca/ayla` | Pending (E-Ayla.1) |

### obsidian repo agents (jjuniper-dev/obsidian)

These define vault-level governance for agent behavior when writing to the Obsidian vault. See `obsidian/_System/agents/`.

| Agent | Type | Scope |
|---|---|---|
| Capture Agent | Vault write policy | What agents may write to Inbox |
| Reconciliation Agent | Vault write policy | What agents may update during reconciliation |

### Design → Implementation Mapping

How the design-layer agents (Core Agents section above) map to running implementations:

| Design Agent (this registry) | Operational Implementation (pca) | Gap |
|---|---|---|
| Ayla Orchestrator | Cowork Claude + WF-Ayla (pending E-Ayla.1) | WF-Ayla is Ollama-backed stepping stone; full Sonnet orchestrator is design target |
| Knowledge Query Worker | WF12 (GET mode) | Live |
| Memory Recall Worker | WF12 (GET mode, session context) | Live; session scoping is manual |
| Critical Review Agent | Not yet implemented | E1.3.x (contradiction detection) is the prerequisite |
| Capture Enrichment Worker | WF10 (partial — validation + auto-fill) | Full classification pending E4.1.1 |
| Observability Monitor | WF13 (polling), pca_health_check.ps1 | Polling-based; not event-triggered on failure |

### Capture Overlap Clarification

Three components claim "capture" ownership across repos. They are **complementary, not conflicting**:

| Component | Repo | What it actually is |
|---|---|---|
| WF10 | pca | **Running implementation** — validates and writes Obsidian + Qdrant + Neo4j |
| `agents/capture-worker.md` | personal-cognitive-architecture | **Design specification** for the capture worker role that WF10 implements |
| `_System/agents/capture-agent.md` | obsidian | **Vault write policy** — what any agent may and may not write to the vault |

WF10 implements the capture-worker design and must comply with the capture-agent write policy.

---

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
| Knowledge Lifecycle State Machine | `docs/KNOWLEDGE-LIFECYCLE.md` in this repo |
| Observability Architecture | Tracks operational metrics and failures |
| pca/AGENTS.md | Operational handbook: work dispatch and code agent procedures |

---

## Workflow Stack Reconciliation

The proposed workflow stack should be reconciled into the PCA registry by merging overlapping roles and adding only true capability gaps.

### Proposed Workflow Mapping

| Proposed Workflow Role | PCA-Aligned Disposition | Canonical PCA Role |
|---|---|---|
| Intake Agent | Merge and clarify | Capture Worker + Capture Enrichment Worker + Edge Policy Gate |
| Backlog Agent | Add as new bounded worker | Backlog Draft Worker |
| RAG Knowledge Agent | Merge | Knowledge Query Worker + Memory Recall Worker |
| DevOps Coordinator | Add as new bounded worker | DevOps Coordination Worker |
| Multi-Agent Research Team | Treat as orchestration pattern, not one agent | Research Orchestration Pattern |
| Knowledge Lifecycle Agent | Add as new reviewer/worker pair or single bounded worker | Knowledge Lifecycle Worker |
| Executive Briefing Agent | Add as new publisher | Executive Briefing Publisher |
| Agent Supervisor | Merge | Ayla Orchestrator + Observability Monitor + Runtime Policy Gate |

### Reconciliation Principles

- Do not create a new agent when the role is already covered by an existing orchestrator, worker, or monitor.
- Do not model governance layers such as the Runtime Policy Gate as free-standing autonomous agents.
- Treat "teams" as orchestration patterns unless a single runtime identity is actually required.
- Add new agents only when there is a distinct permission boundary, output target, or lifecycle responsibility.

### Recommended PCA-Aligned Workflow Stack

1. `Ayla Orchestrator`
2. `Capture Worker`
3. `Capture Enrichment Worker`
4. `Backlog Draft Worker`
5. `Knowledge Query Worker`
6. `Memory Recall Worker`
7. `Critical Review Agent`
8. `Knowledge Lifecycle Worker`
9. `Executive Briefing Publisher`
10. `DevOps Coordination Worker`
11. `Observability Monitor`

This stack preserves PCA control-plane discipline while still covering the intent of the proposed eight workflow roles.

## Added Canonical Agents for Current Gaps

The following agents fill real gaps in the current registry and are appropriate additions.

### Backlog Draft Worker

```yaml
agent_id: backlog-draft-worker
agent_type: worker
status: proposed
runtime: Claude Haiku or local model
execution_mode: semi-autonomous
allowed_tools:
  - backlog_schema_validation
  - draft_generation
  - obsidian_write
  - review_queue_write
allowed_output_targets:
  - obsidian_inbox
  - backlog_review_queue
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 2
policy_profile: backlog-draft-worker
```

Purpose:

- convert captures into draft backlog items
- preserve acceptance criteria and suggested ownership
- write only to draft or review destinations
- never create GitHub issues or external tracker items without approval

### DevOps Coordination Worker

```yaml
agent_id: devops-coordination-worker
agent_type: worker
status: proposed
runtime: Claude Sonnet
execution_mode: assisted
allowed_tools:
  - workflow_health
  - incident_lookup
  - config_diff
  - runbook_query
  - ci_status_query
allowed_output_targets:
  - ops_review_queue
  - incident_notes
  - remediation_plan
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 2
policy_profile: devops-worker
```

Purpose:

- coordinate infrastructure and workflow remediation
- assemble operational context for failures
- propose runbook actions and recovery sequences
- avoid direct destructive infrastructure changes without approval

### Knowledge Lifecycle Worker

```yaml
agent_id: knowledge-lifecycle-worker
agent_type: worker
status: proposed
runtime: Claude Haiku
execution_mode: semi-autonomous
allowed_tools:
  - metadata_review
  - relationship_lookup
  - reconciliation_trigger
  - archive_candidate_generation
allowed_output_targets:
  - lifecycle_review_queue
  - provisional_knowledge_updates
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 2
policy_profile: lifecycle-worker
```

Purpose:

- manage candidate promotion, challenge, stale marking, and archive proposals
- prepare lifecycle transitions for governed review
- trigger reconciliation when lifecycle state depends on contradiction analysis

### Executive Briefing Publisher

```yaml
agent_id: executive-briefing-publisher
agent_type: publisher
status: proposed
runtime: Claude Sonnet
execution_mode: assisted
allowed_tools:
  - memory_query
  - briefing_template
  - citation_builder
  - output_review
allowed_output_targets:
  - briefing_drafts
  - obsidian_reports
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 1
policy_profile: publisher-agent
```

Purpose:

- generate executive-ready summaries from governed source material
- preserve provenance and uncertainty
- publish drafts only, not final external communications

## Roles Not Added as New Agents

These proposed roles should not be added as independent runtime identities.

### Intake Agent

Use existing PCA roles:

- `Capture Worker` for intake and normalization
- `Capture Enrichment Worker` for classification and metadata extraction
- `Edge Policy Gate` for deterministic route control

Reason:

- intake is a pipeline segment, not one autonomous agent

### RAG Knowledge Agent

Use existing PCA roles:

- `Knowledge Query Worker`
- `Memory Recall Worker`

Reason:

- retrieval and recall are already separated appropriately by purpose

### Multi-Agent Research Team

Treat as:

- orchestrated workflow pattern under `Ayla Orchestrator`
- optionally composed from retrieval, review, and publishing agents

Reason:

- this is a coordination pattern, not a single permission boundary

### Agent Supervisor

Use existing PCA roles:

- `Ayla Orchestrator`
- `Observability Monitor`
- `Runtime Policy Gate`

Reason:

- supervision is already distributed across orchestration, observability, and governance
- introducing a separate supervisor agent would duplicate control-plane authority
