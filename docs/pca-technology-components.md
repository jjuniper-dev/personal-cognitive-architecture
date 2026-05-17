---
type: architecture
created: 2026-05-11
updated: 2026-05-11
tags: [pca, technology-stack, components, runtime, infrastructure, tools]
status: draft
---

# PCA Technology Components

## 1. Purpose

This document identifies the technology components that support the Personal Cognitive Architecture (PCA).

It maps tools, platforms, and infrastructure components to the PCA capability model, runtime topology, and governance architecture.

The intent is not to lock the PCA into a fixed tool stack. The intent is to make technology choices explicit, explain their architectural role, and prevent tool sprawl.

The PCA technology position is:

> tools are replaceable; architectural roles are stable.

---

# 2. Technology Architecture Position

The PCA uses technology components to support:

- capture
- orchestration
- memory
- reconciliation
- retrieval
- automation
- governance
- observability
- secure execution
- local-first runtime
- optional cloud burst

The stack should remain:

- modular
- local-first where practical
- auditable
- portable
- low-dependency
- cost-aware
- simple before complex

---

# 3. Component Categories

| Category | Role |
|---|---|
| Canonical Memory | durable human-readable knowledge store |
| Orchestration | workflow execution and automation routing |
| Runtime Substrate | local execution environment |
| Capture Interfaces | voice, chat, web, files, and mobile capture |
| Retrieval & Indexing | semantic and graph-based recall |
| Agent Runtime | controlled task execution |
| Governance & Policy | approvals, routing, lifecycle, and control |
| Secrets & Security | credential protection and secure access |
| Observability | logging, telemetry, audit trails |
| Cloud Burst | frontier reasoning and hosted inference |
| Development & Versioning | repo, documentation, and implementation control |
| Edge/Event Compute | sensors, triggers, and environmental context |

---

# 4. Core Technology Components

## 4.1 Obsidian

| Field | Value |
|---|---|
| Architectural Role | Canonical memory substrate |
| Capability Alignment | KG-01, KG-02, IN-42 |
| Current Status | Core / Accepted |

### Purpose

Obsidian is the canonical memory layer for the PCA.

It stores:

- structured notes
- captured reflections
- decision artifacts
- architecture documents
- knowledge lifecycle states
- linked concepts
- human-readable source memory

### Architectural Rationale

Obsidian is preferred because it is:

- markdown-based
- local-first
- graph-oriented
- portable
- transparent
- compatible with Git
- independent of proprietary memory systems

### Key Principle

> Obsidian is canonical. Indexes and AI summaries support memory; they do not replace it.

---

## 4.2 n8n

| Field | Value |
|---|---|
| Architectural Role | Workflow orchestration and automation runtime |
| Capability Alignment | AR-48, IN-40, IF-01 |
| Current Status | Core / Preferred |

### Purpose

n8n is the primary orchestration layer for PCA workflows.

It supports:

- webhooks
- scheduled workflows
- API integrations
- capture routing
- note creation
- task automation
- agent-triggered workflows
- local/self-hosted execution

### Example PCA Flows

```text
Voice Capture
→ Webhook
→ n8n Workflow
→ Transform to Markdown
→ Write to Obsidian Inbox
→ Log Execution
```

```text
External Feed
→ n8n Polling Workflow
→ Signal Filter
→ AI Summary
→ Review Queue
```

### Architectural Rationale

n8n is attractive because it is:

- self-hostable
- API-friendly
- flexible
- visible
- workflow-oriented
- less dependent on SaaS-only automation patterns

### Key Principle

> n8n is the PCA nervous system, not the knowledge store.

---

## 4.3 Docker

| Field | Value |
|---|---|
| Architectural Role | Local service runtime and deployment substrate |
| Capability Alignment | IF-01, AR-48, OB-01 |
| Current Status | Core / Preferred |

### Purpose

Docker provides a repeatable local runtime for PCA services.

It may host:

- n8n
- databases
- vector stores
- local APIs
- monitoring services
- lightweight model servers
- supporting automation services

### Architectural Rationale

Docker supports:

- repeatable deployment
- service isolation
- portability
- simpler recovery
- local-first runtime
- future migration to mini PC infrastructure

### Guardrail

Docker should not become uncontrolled service sprawl. Every container requires:

- purpose
- owner
- data persistence model
- backup expectation
- shutdown path

---

## 4.4 GitHub

| Field | Value |
|---|---|
| Architectural Role | Version control, architecture repository, decision history |
| Capability Alignment | CP-38, OB-02, IF governance |
| Current Status | Core / Accepted |

### Purpose

GitHub stores and versions PCA architecture documents, implementation code, decision records, and supporting scripts.

It supports:

- version control
- change history
- architecture documentation
- decision traceability
- issue tracking
- future CI/CD validation

### Architectural Rationale

GitHub provides:

- transparent history
- collaboration-ready structure
- markdown-native documentation
- automation potential
- alignment with software delivery practices

### Guardrail

No secrets, tokens, API keys, credentials, or sensitive personal data should be committed to GitHub.

---

## 4.5 VS Code

| Field | Value |
|---|---|
| Architectural Role | Development and structured editing environment |
| Capability Alignment | IF-01, KP-51, KG-01 |
| Current Status | Supporting / Preferred |

### Purpose

VS Code supports editing, scripting, repo management, Markdown authoring, and lightweight development.

It supports:

- markdown editing
- repo work
- script development
- local configuration
- terminal-based operations
- future devcontainer support

---

# 5. Capture and Input Components

## 5.1 iPhone

| Field | Value |
|---|---|
| Architectural Role | Mobile capture and voice-first interaction device |
| Capability Alignment | IN-40, CO-45 |
| Current Status | Core capture device |

### Purpose

The iPhone is the primary ambient capture device for:

- voice reflections
- conversational capture
- mobile notes
- screenshots
- quick ideas
- task triggers
- contextual capture

### Architectural Rationale

The PCA is increasingly voice-first. The iPhone acts as the always-available capture surface.

---

## 5.2 ChatGPT / Voice AI Interface

| Field | Value |
|---|---|
| Architectural Role | Conversational reasoning and reflection interface |
| Capability Alignment | CO-45, IN-40, KP-50 |
| Current Status | Core external reasoning interface |

### Purpose

ChatGPT supports:

- conversational brainstorming
- reflection capture
- synthesis
- architecture drafting
- decision support
- executive narrative generation

### Constraint

Chat transcripts should not be treated as durable memory unless exported, summarized, or captured into Obsidian.

### Key Principle

> conversational cognition is transient until persisted.

---

## 5.3 Web, RSS, Reddit, GitHub, News APIs

| Field | Value |
|---|---|
| Architectural Role | External intelligence ingestion sources |
| Capability Alignment | IN-43, IN-41 |
| Current Status | Candidate / Emerging |

### Purpose

These sources support external signal acquisition from:

- AI newsletters
- Reddit technical communities
- GitHub trends
- Hacker News
- RSS feeds
- news APIs
- platform release notes

### Guardrail

The PCA should not archive raw internet exhaust. It should ingest selectively, score signal, and persist synthesized intelligence only when useful.

---

# 6. Retrieval and Knowledge Components

## 6.1 Vector Store / Semantic Index

| Field | Value |
|---|---|
| Architectural Role | Semantic retrieval support |
| Capability Alignment | IN-42 |
| Current Status | Candidate / Not yet canonical |

### Candidate Technologies

- Chroma
- Qdrant
- Weaviate
- FAISS
- OpenSearch vector search

### Purpose

Vector search supports:

- semantic recall
- similarity search
- retrieval augmentation
- memory lookup
- context assembly

### Guardrail

Vector indexes are derived retrieval aids. They are not canonical memory.

---

## 6.2 Knowledge Graph

| Field | Value |
|---|---|
| Architectural Role | Relationship and concept graph layer |
| Capability Alignment | IN-42, KG-02, CP-35 |
| Current Status | Candidate / Emerging |

### Candidate Technologies

- Obsidian graph
- Neo4j
- lightweight local graph store
- markdown link graph

### Purpose

The knowledge graph supports:

- concept relationships
- decision lineage
- contradiction mapping
- dependency mapping
- architecture visualization
- retrieval enrichment

### Guardrail

A graph database should not be introduced before clean memory and metadata patterns exist.

---

# 7. Runtime and Infrastructure Components

## 7.1 Dell Mini PC / OptiPlex Micro

| Field | Value |
|---|---|
| Architectural Role | Primary local runtime node |
| Capability Alignment | IF-01, AR-48, OB-01 |
| Current Status | Preferred target runtime |

### Purpose

The Dell mini PC is the preferred primary compute node for:

- Docker
- n8n
- local APIs
- vector indexes
- logs
- lightweight databases
- local automation
- possible small-model serving

### Rationale

Better suited than Raspberry Pi for Docker-heavy workloads because of:

- CPU performance
- RAM capacity
- storage flexibility
- virtualization support
- operational stability

---

## 7.2 Raspberry Pi

| Field | Value |
|---|---|
| Architectural Role | Edge/event compute node |
| Capability Alignment | IF-02 |
| Current Status | Candidate / Edge role |

### Purpose

Raspberry Pi nodes support:

- sensor agents
- weather monitoring
- camera triggers
- home monitoring
- lightweight APIs
- low-power event detection

### Guardrail

Raspberry Pis should not be the primary PCA orchestration or persistence substrate.

---

## 7.3 Portable Edge Rack

| Field | Value |
|---|---|
| Architectural Role | Future deployment pattern |
| Capability Alignment | IF-01, IF-02 |
| Current Status | Deferred / Future-state |

### Purpose

A future portable rack may contain:

- Dell mini PC
- Raspberry Pi nodes
- active cooling
- networking
- storage
- power management
- transport-safe mounting

### Guardrail

Physical packaging should follow runtime maturity. Do not optimize the rack before the operational loop is stable.

---

# 8. Security and Access Components

## 8.1 VPN

| Field | Value |
|---|---|
| Architectural Role | Secure remote access boundary |
| Capability Alignment | IF-03, CP-36 |
| Current Status | Preferred access pattern |

### Candidate Technologies

- Tailscale
- WireGuard
- ZeroTier
- router-based VPN

### Purpose

VPN provides secure remote access to local PCA services without exposing them publicly.

### Principle

> VPN-first access is preferred over direct port exposure.

---

## 8.2 Secrets Manager

| Field | Value |
|---|---|
| Architectural Role | Runtime credential protection |
| Capability Alignment | IF-03, CP-36 |
| Current Status | Open decision |

### Candidate Technologies

- Docker secrets
- environment variables for early MVP
- 1Password for human credential management
- local vault service
- Azure Key Vault

### Purpose

Secrets management supports:

- API keys
- webhook secrets
- model provider keys
- GitHub tokens
- workflow credentials
- runtime service credentials

### Guardrail

No secrets in:

- GitHub
- markdown notes
- screenshots
- chat transcripts
- unprotected logs

---

# 9. Cloud Burst Components

## 9.1 OpenAI / ChatGPT

| Field | Value |
|---|---|
| Architectural Role | Cloud reasoning and synthesis service |
| Capability Alignment | CP-37, KP-50, KP-51 |
| Current Status | Core external AI service |

### Purpose

Supports:

- high-quality reasoning
- architecture drafting
- synthesis
- multimodal interpretation
- executive narrative generation

### Guardrail

Cloud reasoning outputs should be captured into Obsidian only after review or distillation.

---

## 9.2 Azure / Microsoft AI Services

| Field | Value |
|---|---|
| Architectural Role | Optional cloud platform and experimentation environment |
| Capability Alignment | CP-37, IF-01, OB-01 |
| Current Status | Candidate / Experimental |

### Candidate Services

- Azure AI Foundry
- Azure Key Vault
- Azure Monitor
- Microsoft Fabric
- Defender / Sentinel-like patterns

### Purpose

Azure may support experimentation with:

- hosted inference
- secrets
- monitoring
- governance patterns
- data/AI platform concepts

### Guardrail

Avoid hidden costs, lock-in, and post-trial dependency breakage.

---

## 9.3 Local or Hosted Open Models

| Field | Value |
|---|---|
| Architectural Role | Optional local or hosted model capability |
| Capability Alignment | CP-37, AR-48 |
| Current Status | Candidate / Deferred |

### Candidate Families

- Qwen
- Gemma
- Llama-family models
- Mistral-family models

### Purpose

Potential future use cases:

- local summarization
- offline reasoning
- lightweight classification
- privacy-sensitive inference
- fallback cognition

### Guardrail

Do not prioritize model hosting before ingestion, memory, retrieval, and governance loops are stable.

---

# 10. Observability Components

## 10.1 Logging and Monitoring Stack

| Field | Value |
|---|---|
| Architectural Role | Runtime visibility and audit support |
| Capability Alignment | OB-01, OB-02 |
| Current Status | Emerging |

### Candidate Technologies

- n8n execution logs
- Docker logs
- lightweight log files
- Uptime Kuma
- Grafana
- Prometheus
- Loki
- Azure Monitor for cloud experiments

### Purpose

Observability supports:

- workflow debugging
- runtime health
- failure visibility
- model/API usage tracking
- policy decision records
- memory promotion audit

### Guardrail

Start lightweight. Avoid enterprise observability complexity before basic workflows are stable.

---

# 11. Component-to-Capability Mapping

| Component | Primary Capability | Secondary Capabilities |
|---|---|---|
| Obsidian | KG-01 | IN-42, KG-02 |
| n8n | AR-48 | IN-40, IF-01 |
| Docker | IF-01 | AR-48, OB-01 |
| GitHub | CP-38 | OB-02, KG-02 |
| VS Code | IF-01 | KG-01 |
| iPhone | IN-40 | CO-45 |
| ChatGPT | KP-50 | CP-37, CO-45 |
| Vector Store | IN-42 | KG-02 |
| Neo4j / Graph Store | IN-42 | CP-35, KG-02 |
| Dell Mini PC | IF-01 | AR-48, OB-01 |
| Raspberry Pi | IF-02 | IN-40 |
| VPN | IF-03 | CP-36 |
| Secrets Manager | IF-03 | CP-36 |
| Azure | CP-37 | IF-01, OB-01 |
| Monitoring Stack | OB-01 | OB-02 |

---

# 12. Current Stack View

## Phase 1 — Minimal Runtime Foundation

| Role | Component |
|---|---|
| Canonical memory | Obsidian |
| Orchestration | n8n |
| Runtime | Docker / local machine |
| Editing | VS Code |
| Version control | GitHub |
| Reasoning | ChatGPT / external LLMs |

## Phase 2 — Local Runtime Stabilization

| Role | Component |
|---|---|
| Primary runtime | Dell mini PC |
| Remote access | VPN |
| Runtime isolation | Docker |
| Workflow persistence | n8n volumes |
| Secrets | Docker secrets / local vault pattern |
| Retrieval | vector store candidate |
| Logs | n8n + Docker logs |

## Phase 3 — Sovereign Edge Runtime

| Role | Component |
|---|---|
| Edge nodes | Raspberry Pi |
| Event sensors | weather/camera/home monitoring |
| Local retrieval | vector + graph layer |
| Observability | lightweight monitoring stack |
| Runtime policy | Runtime Policy Gate implementation |
| Agent control | Agent registry / sandbox |

## Phase 4 — Portable Cognitive Runtime

| Role | Component |
|---|---|
| Portable compute | Dell mini PC + optional Pi cluster |
| Enclosure | portable rack / rugged case |
| Cooling | active fan/cooling setup |
| Networking | VPN + controlled internal network |
| Offline mode | local memory + local workflows |
| Cloud burst | policy-governed external AI services |

---

# 13. Open Technology Decisions

| Decision | Status | Notes |
|---|---|---|
| Vector database | Open | Chroma/Qdrant/OpenSearch/FAISS candidates |
| Secrets manager | Open | Need local-first pattern |
| VPN implementation | Open | Prefer simple and low-maintenance |
| Observability stack | Open | Start with n8n/Docker logs |
| Local model server | Deferred | Not needed before ingestion/retrieval maturity |
| Graph database | Deferred | Obsidian links first, Neo4j later if justified |
| Portable rack hardware | Deferred | Physical build follows runtime maturity |
| Event bus | Deferred | Only needed when agent/event complexity increases |

---

# 14. Technology Selection Principles

1. Prefer simple and durable tools.
2. Prefer local-first where practical.
3. Avoid hidden recurring costs.
4. Avoid unnecessary cloud dependency.
5. Avoid adding infrastructure before the operational loop requires it.
6. Keep canonical memory human-readable.
7. Ensure every runtime component has a shutdown path.
8. Do not introduce agents before governance exists.
9. Use cloud burst for capability, not dependency.
10. Treat technology as replaceable implementation, not architecture.

---

# 15. Strategic Position

The PCA technology stack is not a tool collection.

It is a set of replaceable components assigned to stable architectural roles.

The correct posture is:

> stable architecture, replaceable tools, governed runtime.
