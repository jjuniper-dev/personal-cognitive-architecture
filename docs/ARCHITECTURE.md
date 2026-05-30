# PCA Architecture

**Status:** Living document  
**Layer model version:** 1.1  
**Last revised:** 2026-05-30

This is the canonical architecture document for the Personal Cognitive Architecture (PCA).  
Referenced by `jjuniper-dev/obsidian/40_Reference/PCA/ARCHITECTURE.md` (mirror copy).

---

## Canonical Mental Model

```text
Capture → Reconcile → Activate
```

Implementation primitive chain:

```text
Input → Event → Validate → Route → Store → Retrieve → Act → Audit
```

---

## Layer Models

PCA uses two complementary layer models. They describe the same system from different angles and serve different purposes.

### Design Layer Model (5 layers)

Use this when reasoning about **where code belongs**, which component owns a capability, or how to scope a change.

| Layer | Name | Purpose | Typical Components |
|---|---|---|---|
| L1 | Knowledge & Control | Durable memory, vault, graph, governance | Obsidian, Neo4j, schemas, source register |
| L2 | Agent Runtime | Assistant and bounded workers | Ayla assistant, workers, model adapters |
| L3 | Workflow & Integration | Deterministic orchestration | n8n workflows, webhooks, routers |
| L4 | Infrastructure | Local/self-hosted runtime | Docker, Tailscale, host services |
| L5 | AI Models | Inference and transcription | Local models, cloud APIs, Whisper |

*Source of truth for this model: `AGENTS.md` in this repository.*

### Functional Decomposition Model (9 layers)

Use this when **tracing data flow**, designing a new capture path, or documenting system behavior end-to-end.

| # | Layer | Function |
|---|---|---|
| 1 | Input Sources | Voice, text, web, document, financial, image |
| 2 | Capture Layer | Ingest, normalize, stamp provenance |
| 3 | Validation Layer | Schema enforcement, classification, confidence |
| 4 | Cognitive Reconciliation Engine | Contradiction detection, tension resolution |
| 5 | Knowledge Integration Layer | Obsidian, Qdrant, Neo4j storage and indexing |
| 6 | Reasoning & Agents Layer | Ayla, workers, retrieval, synthesis |
| 7 | Execution & Automation Layer | n8n workflows, webhooks, approval gates |
| 8 | Output Generation Layer | Notes, reports, alerts, external actions |
| 9 | Infrastructure, Governance & Ethics | Docker, Vault, audit, policy gates |

### Layer Model Cross-Reference

| Functional Layer (9) | Design Layer (5) | Primary Components (current) |
|---|---|---|
| 1–2 Input & Capture | L3 (Workflow) + L1 (Knowledge) | WF10, WF15, WF16, WF11 |
| 3 Validation | L3 (Workflow) + L1 (Schema) | WF10 validation gate, JSON schemas |
| 4 Reconciliation | L2 (Agent) + L3 (Workflow) | E1.3.x (pending), Critical Review Agent |
| 5 Knowledge Integration | L1 (Knowledge) | Obsidian, Qdrant, Neo4j |
| 6 Reasoning & Agents | L2 (Agent) + L5 (AI Models) | Ayla, WF-Ayla, WF12, WF02 |
| 7 Execution | L3 (Workflow) | n8n, webhooks, WF-Dispatch |
| 8 Output | L2 (Agent) + L3 (Workflow) | WF10 notes, WF13 alerts, WF14 cost |
| 9 Infrastructure & Governance | L4 (Infra) + L1 (Control) | Docker, Vault, pca-architecture.md |

### pca Operational Tier Labels → Design Layers

`pca/BACKLOG.md` uses `Layer:` labels in task metadata as routing and grouping conventions. These are **not** a separate formal layer model — they map to the 5-layer design model as follows:

| `pca/BACKLOG.md` Layer label | Maps to Design Layer(s) |
|---|---|
| Capture Mesh | L3 + L1 |
| Observability / Event Bus | L3 |
| Cognitive System / Memory | L1 |
| Reconciliation Engine | L1 + L2 |
| Retrieval | L1 + L2 |
| Agentic Runtime | L2 + L5 |
| Human Experience | L2 + L3 |
| Governance | L1 |
| Infrastructure / GitOps / IaC | L4 |
| Financial Agent | L2 + L5 |
| Cost & Budget Governance | L1 |

`pca/pca-architecture.md` uses **Phases** (1–15) for implementation sequencing (Phase 1 topology, Phase 2 Docker, etc.). This is an **implementation roadmap** — orthogonal to the semantic layer hierarchy. It describes deployment order, not architectural structure.

---

## Repository Roles

See `docs/REPO-AUTHORITY.md` for the full authority model.

| Repository | Role |
|---|---|
| `jjuniper-dev/personal-cognitive-architecture` | Canonical architecture, schemas, agent design, governance model, use cases |
| `jjuniper-dev/pca` | Running system: n8n workflows, scripts, operational backlog, deployment config |
| `jjuniper-dev/obsidian` | Human-readable knowledge vault: captures, notes, vault governance |

---

## Data Flow Examples

### Knowledge Capture (Live — WF10)

```
User/Agent POST → /webhook/pca/incident
  → WF10 Validation Gate (type + source required; auto-fill timestamps, confidence, provenance)
  → Obsidian note written to 00_Inbox/
  → Qdrant embedding (pca_vault / pca_incidents)
  → Neo4j :Note node (idempotent on input_hash)
  → HTTP 200 response
```

### Voice Capture (Pending — WF15, E1.1.1)

```
Audio file → audio_temp/
  → WF15 schedule trigger (60s scan)
  → Faster-Whisper transcription (localhost:8010)
  → WF10 (type:voice, source:whisper)
  → Obsidian + Qdrant + Neo4j
  → File moved to audio_temp/processed/
```

### Retrieval (Live — WF12)

```
POST /webhook/pca/memory {action:"get", query:"..."}
  → Qdrant semantic search (pca_memory + pca_vault)
  → Neo4j graph expansion (1–2 hops from semantic hits)
  → Composite ranked context block
  → HTTP 200
```

### Contradiction Detection (Pending — E1.3.x)

```
WF10 receives new knowledge object
  → Qdrant top-5 search for similar content
  → If similarity > 0.85: Ollama contradiction check
  → If contradiction: state = "contested", Neo4j :CONTRADICTS edge
  → If clear: state = "reconciled"
```

---

## Implementation Status

| Functional Layer | Implementation Status |
|---|---|
| Input & Capture | Partial — WF10, WF11, WF16 live; WF15 voice pending (E1.1.1) |
| Validation | Live — WF10 schema gate, E1.2.3 merged 2026-05-30 |
| Reconciliation | Pending — E1.3.x in pca backlog |
| Knowledge Integration | Live — Obsidian, Qdrant, Neo4j all active |
| Reasoning & Agents | Partial — WF12 retrieval live; WF-Ayla pending (E-Ayla.1) |
| Execution & Automation | Live — n8n, 14+ workflows |
| Output | Live — WF10 notes, WF13 alerts, WF14 cost |
| Infrastructure | Live — Docker, HashiCorp Vault, Tailscale |

---

## Design Trade-offs

**Local-first over cloud-first:** Ollama handles routine inference; Anthropic/OpenRouter are fallbacks or specialized tasks. Avoids vendor lock-in and data exposure for sensitive content.

**Deterministic workflows over autonomous agents:** n8n orchestrates; agents advise, enrich, and retrieve. Human approval gates on irreversible actions. AI recommends; humans and workflows execute.

**HTTP webhook event model (current) vs async event broker (target):** Current system uses n8n webhooks — synchronous request/response. Simpler to operate, fully observable via n8n execution logs, and sufficient at current scale. Event backbone aspiration (async, schema-validatable, replayable) is documented in `docs/EVENT-BACKBONE-STATUS.md`.

**Obsidian as human interface, not canonical store:** Qdrant and Neo4j are the machine-queryable stores. Obsidian is the human-readable surface. Source of truth for vault governance is `jjuniper-dev/obsidian`; source of truth for architecture and schemas is this repository.
