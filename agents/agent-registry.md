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

## Agent Workflow Stack v1 — Slice 1

These four agents form the first governed workflow foundation. They are defined in
`agents/intake-agent.md`, `agents/backlog-agent.md`, `agents/rag-knowledge-agent.md`,
and `agents/knowledge-lifecycle-agent.md`. Implementations are in the corresponding
`-impl.py` files.

Related issues: pca#32, pca#33, pca#34, pca#35, pca#40  
Spec: `pca/docs/agent-workflow-slice-1-spec.md`

### Intake Agent

```yaml
agent_id: intake-agent
agent_type: worker
status: active
runtime: FastAPI / Python
execution_mode: semi-autonomous
allowed_tools:
  - request_parser
  - classification_rules
  - provenance_stamper
can_trigger_agents: false
can_write_trusted_knowledge: false
requires_human_approval: false
max_autonomy_level: 1
policy_profile: intake-worker
created: 2026-06-02
updated: 2026-06-02
```

Purpose: Normalize inbound requests into PCA intake objects. No downstream workflow acts on an un-normalized request. Routes to `backlog`, `rag`, `capture`, `operational`, `briefing`, or `manual_review`.

### Backlog Agent

```yaml
agent_id: backlog-agent
agent_type: worker
status: active
runtime: FastAPI / Python
execution_mode: semi-autonomous
allowed_tools:
  - backlog_reader
  - epic_matcher
  - work_item_shaper
can_trigger_agents: false
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 1
policy_profile: backlog-worker
created: 2026-06-02
updated: 2026-06-02
```

Purpose: Convert qualified intake into structured PCA work item proposals. Prefers linking to existing epics and sprints over creating new items. Outputs are `status=proposed` pending approval.

### RAG Knowledge Agent

```yaml
agent_id: rag-knowledge-agent
agent_type: retriever
status: active
runtime: FastAPI / Python
execution_mode: semi-autonomous
allowed_tools:
  - canonical_kb_search
  - repo_doc_search
  - memory_artifact_search
can_trigger_agents: false
can_write_trusted_knowledge: false
requires_human_approval: false
max_autonomy_level: 1
policy_profile: retrieval-worker
created: 2026-06-02
updated: 2026-06-02
```

Purpose: Assemble trusted context packs using canonical-first retrieval. Surfaces gaps rather than filling them with lower-trust material. Respects sensitivity and classification boundaries.

### Knowledge Lifecycle Agent

```yaml
agent_id: knowledge-lifecycle-agent
agent_type: reviewer
status: active
runtime: FastAPI / Python
execution_mode: semi-autonomous
allowed_tools:
  - kb_metadata_scanner
  - drift_detector
  - review_queue_writer
  - draft_proposal_generator
can_trigger_agents: false
can_write_trusted_knowledge: false
requires_human_approval: true
max_autonomy_level: 2
policy_profile: lifecycle-reviewer
created: 2026-06-02
updated: 2026-06-02
```

Purpose: Detect staleness, missing source refs, and ungrounded seeds in canonical KB. Produces durable review queues and draft proposals — never auto-applies changes to canon. Exposes lifecycle state to the RAG Knowledge Agent.

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
| Intake Agent | Workflow worker | `POST :8010/intake` | Active (slice-1, pca#32) |
| Backlog Agent | Workflow worker | `POST :8011/shape` | Active (slice-1, pca#33) |
| RAG Knowledge Agent | Workflow retriever | `POST :8012/retrieve` | Active (slice-1, pca#34) |
| Knowledge Lifecycle Agent | Workflow reviewer | `POST :8013/scan` | Active (slice-1, pca#35) |

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
| Intake Agent | `agents/intake-agent-impl.py` (slice-1) | Service deployment pending; spec complete |
| Backlog Agent | `agents/backlog-agent-impl.py` (slice-1) | Service deployment pending; spec complete |
| RAG Knowledge Agent | `agents/rag-knowledge-agent-impl.py` (slice-1) | Stub store; production wires into Qdrant/Neo4j/vault |
| Knowledge Lifecycle Agent | `agents/knowledge-lifecycle-agent-impl.py` (slice-1) | Stub pages; production scans Obsidian vault |

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
