---
type: architecture
created: 2026-04-24
updated: 2026-05-11
tags: [pca, technology, stack]
status: active
---

# PCA Technology Stack

## Overview

The PCA architecture is technology-agnostic at the conceptual level but requires specific implementations for each stage.

The stack is organized by phase and domain, with clear separation between personal (Phase 1-2) and enterprise (Phase 3+) components.

## Principles

- **Modular**: Components replaceable without breaking the system
- **Durable**: Choices support long-term operation and evolution
- **Local-first**: Personal stack prioritizes local operation where practical
- **Standards-based**: Enterprise stack aligns with GC/HC infrastructure

## Phase 1: Cloud Jumpstart (MVP)

### Purpose

Prove ingestion loop: **n8n → Obsidian → structured note**

### Technology Choices

| Component | Technology | Role | Rationale |
|-----------|-----------|------|--------|
| **Knowledge Store** | Obsidian | Canonical memory | Human-readable, version-controllable, local-first |
| **Automation Orchestration** | n8n (Docker) | Workflow engine | Low-code, flexible, self-hosted capable |
| **Development Environment** | VS Code | Coding & note editing | Integrated, extensible, markdown support |
| **LLM (Validation — Screening Agent)** | Claude Sonnet (Anthropic API) | Conservative scoring, consistent evaluation | High quality, cost-effective, reliable |
| **LLM (Validation — Critical Agent)** | Claude Haiku (Anthropic API) | Independent scoring with exploration | Fast, low-cost, asymmetric agent pair |
| **Data Storage** | Local filesystem + Git | Persistence | Version control, auditability |
| **API Gateway** | n8n built-in webhooks | External integrations | Capture from web, voice apps |

### Validation Architecture (Phase 1)

**Dual-Agent Screening:**

- **Screening Agent:** Claude Sonnet, Temperature 0.3 (conservative, consistent scoring across 4 dimensions)
- **Critical Agent:** Claude Haiku, Temperature 0.8 (exploratory, independent assessment)
- **Agreement Gate:** Both agents must align within 15 points per dimension
- **Per-Dimension Hard Floors:** Relevance ≥ 60 (non-negotiable); other dimensions to be tuned based on user feedback
- **Routing:** PROMOTE (>80), INBOX (60-80), ARCHIVE (<60)
- **Confidence Model:** Agents agree on all 4 dimensions = 95% confidence; partial disagreement = 40-70%; most disagree = 20%

### Architecture Diagram (Phase 1)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Capture Sources                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ iPhone   │ │ Web      │ │ Chat     │ │ Voice    │ │ Documents│ │
│  │ Shortcuts│ │ Capture  │ │ Interface│ │ Notes    │ │ Upload   │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
└───────┼────────────┼────────────┼────────────┼────────────┼────────┘
        └────────────┴────────────┴────────────┴────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   n8n Webhooks    │
                    │   (Event Router)  │
                    └─────────┬─────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼──────┐    ┌────────▼────────┐   ┌──────▼──────┐
    │ Validation │    │  Reconciliation │   │ Integration │
    │  & Scoring │    │   (Phase 2)     │   │   Worker    │
    │ (Dual      │    │                 │   │             │
    │ Claude     │    │                 │   │             │
    │ Agents)    │    │                 │   │             │
    └────┬──────┘    └────────┬────────┘   └──────┬──────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Obsidian Vault   │
                    │ (Canonical Memory)│
                    └───────────────────┘
```

### Deployment (Phase 1)

**Local Development**:

```
├── /home/user/obsidian-vault/     # Obsidian workspace
├── /docker/n8n/                   # n8n configuration
├── .env                           # Anthropic API keys
└── claude/workflows/              # Workflow automation scripts
```

**Storage**:

- Obsidian vault in Git repository
- n8n workflows in code version control
- Execution logs in local filesystem
- API keys in environment variables (.env, not committed)

**Cost Estimate (Phase 1)**:

- ~50 videos/day × 365 days = ~18,250 videos/year
- Claude Sonnet + Claude Haiku dual-agent scoring: ~CAD $0.018/video
- **Annual budget: ~CAD $330**

## Phase 2: Self-Hosted Migration

### Purpose

Local inference, semantic indexing, structured session support, observability

### Technology Additions

| Component | Technology | Role | Rationale |
|-----------|-----------|------|--------|
| **LLM (Local — Fast/Real-time)** | Qwen2.5-7B via Ollama | On-device reasoning, real-time chat | Low latency, privacy, cost reduction |
| **LLM (Local — Deep Synthesis)** | Qwen2.5-32B via Ollama | Deep analysis, reconciliation | Higher quality than 7B, still local |
| **Embedding Model** | BGE-M3 via Ollama | Semantic search, local embeddings | Privacy-first, multilingual, no external dependency |
| **Vector Store** | ChromaDB | Semantic indexing | Lightweight, no external dependency, always-local |
| **Observability** | Prometheus + Grafana | Monitoring | Standard open-source stack |
| **Logging** | PostgreSQL run logs | Session and execution history | Structured, queryable, ACID guarantees |
| **Session Management** | Redis | Short-term context cache | Fast in-context recall during agent runs |

### Architecture Additions (Phase 2)

```
Phase 1 Components + New Layer:

    ┌──────────────────────────────────┐
    │  Local LLM Inference (RTX 3090)  │
    │  ├─ Qwen2.5-7B (fast)            │
    │  ├─ Qwen2.5-32B (deep)           │
    │  ├─ BGE-M3 embeddings            │
    │  └─ Quantization: 4-bit          │
    └────────────┬─────────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │  ChromaDB Vector Store        │
    │  (Semantic Index, Ephemeral)  │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────────────────────┐
    │  Neo4j Graph Database                     │
    │  (Knowledge graph, reconciliation state)  │
    └────────────┬──────────────────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │  Reasoning & Reconciliation    │
    │  (Cognitive Reconciliation Engine)│
    └────────────┬──────────────────┘
                 │
              Obsidian (Canonical)
```

### Deployment (Phase 2)

```
Docker Compose:
├── n8n (container)
├── postgres (container — run logs)
├── redis (container — session cache)
├── chromadb (container — vector index)
├── ollama (container — Qwen2.5-7B, Qwen2.5-32B, BGE-M3 on RTX 3090)
├── prometheus (monitoring)
├── grafana (dashboards)
└── volumes for persistence
```

### Knowledge Store Layers (Phase 2)

| Layer | Technology | Role | Sync Direction |
|-------|-----------|------|----------------|
| Canonical (Human) | Obsidian | Source of truth | Primary |
| Semantic Graph | Neo4j | Relationship modeling, reconciliation | Obsidian → Neo4j (one-way) |
| Vector Index | ChromaDB | Semantic search, RAG retrieval | Neo4j → ChromaDB (derived) |

**Rule: Obsidian is always authoritative. Neo4j and ChromaDB are derived indices, rebuildable from Obsidian.**

## Phase 3+: Enterprise Applicability

### Purpose

GC/HC compliance, enterprise governance, multi-tenant orchestration, formal output engine

### Technology Stack

| Component | Technology | Role | Rationale |
|-----------|-----------|------|--------|
| **Cloud Platform** | Azure | Enterprise infrastructure | GC-approved, compliance-ready |
| **Data Lakehouse** | Microsoft Fabric | Analytics & integration | Enterprise-grade data management |
| **Automation Platform** | Power Automate | Enterprise workflows | Native Azure integration |
| **LLM Service** | Azure OpenAI (Claude Sonnet) | Compliant AI services | GC-aligned, audit-ready |
| **Identity** | Azure AD | Access control | Enterprise IAM |
| **Secrets Management** | Azure Key Vault | Credential management | Enterprise security |
| **Audit & Compliance** | Azure Purview | Data governance | Policy enforcement |
| **Output Engine** | Python + FastAPI | Template rendering | Structured artifact generation |
| **Report Server** | Power BI | Executive dashboards | Visual decision support |
| **Audio Output** | Kokoro TTS | Podcast-style summaries | High-quality, local audio generation |

### Multi-Tenant Architecture (Phase 3)

```
┌─────────────────────────────────────────────────┐
│          Azure Enterprise Tenant                 │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  Identity & Access (Azure AD)             │ │
│  └───────────────────┬───────────────────────┘ │
│                      │                         │
│  ┌───────────────────▼───────────────────────┐ │
│  │  Data Lakehouse (Microsoft Fabric)        │ │
│  │  ├─ Raw Data Lake                         │ │
│  │  ├─ Processed Knowledge Graph             │ │
│  │  └─ Policy-Governed Access Layers         │ │
│  └───────────────────┬───────────────────────┘ │
│                      │                         │
│  ┌───────────────────▼───────────────────────┐ │
│  │  Integration Layer                        │ │
│  │  ├─ Power Automate (Orchestration)        │ │
│  │  ├─ Azure OpenAI (Reasoning)              │ │
│  │  └─ Azure Purview (Governance)            │ │
│  └───────────────────┬───────────────────────┘ │
│                      │                         │
│  ┌───────────────────▼───────────────────────┐ │
│  │  Output Engine                            │ │
│  │  ├─ PowerPoint (Presentations)            │ │
│  │  ├─ Word (Reports)                        │ │
│  │  ├─ Power BI (Dashboards)                 │ │
│  │  └─ Audio (Summaries via Kokoro)          │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Component Decision Matrix

### Knowledge Store

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Obsidian** | Human-readable, version control, local-first | No native multi-user, limited enterprise features | ✓ Phase 1-2 |
| **Azure Data Lake** | Enterprise-grade, compliance-ready | Less human-readable, complex setup | ✓ Phase 3+ |
| **PostgreSQL** | Relational, mature | Less suitable for graph structure | - |

### Automation Orchestration

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **n8n** | Low-code, self-hosted, flexible | Limited enterprise features | ✓ Phase 1-2 |
| **Power Automate** | Enterprise-grade, Azure-native | Vendor lock-in, complex licensing | ✓ Phase 3+ |
| **Zapier** | Popular, easy setup | Limited control, expensive at scale | - |
| **Custom Python** | Full control, no vendor lock-in | High maintenance burden | - |

### LLM Service

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Claude Sonnet + Haiku (API)** | High quality, asymmetric agents, cost-effective | External dependency | ✓ Phase 1 |
| **Azure OpenAI** | GC-compliant, compliance-ready | Higher latency, compliance overhead | ✓ Phase 3+ |
| **Qwen2.5 (Local)** | Privacy, cost, no external dependency, strong reasoning | Requires GPU, inference time | ✓ Phase 2 |
| **Google Cloud AI** | Competitive quality | Less GC alignment | - |

### Embeddings

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **BGE-M3 (Local via Ollama)** | Privacy, multilingual, no external API | Local GPU required | ✓ Phase 2 |
| **OpenAI embeddings (API)** | Simple, reliable | API cost, external dependency | Phase 1 only |
| **all-MiniLM-L6-v2** | Lightweight | Monolingual, lower quality | - |

## Technology Migration Path

### Phase 1 → Phase 2

**No breaking changes** if designed properly:

1. Keep Obsidian as canonical memory
2. Introduce ChromaDB for semantic search (non-destructive, derived layer)
3. Stand up Neo4j for relationship modeling (one-way sync from Obsidian)
4. Add local LLM alongside Claude API (gradual cutover)
5. Introduce BGE-M3 embeddings in parallel with external embeddings
6. Migrate when ready; maintain dual-stack during transition

### Phase 2 → Phase 3

**Requires careful mapping**:

1. Migrate Obsidian knowledge graph to Azure Data Lake (retaining structure)
2. Map n8n workflows to Power Automate (conceptual equivalence)
3. Stand up Azure OpenAI in parallel with local LLM
4. Implement compliance layer (audit, access control)
5. Build output engine for GC/HC standards
6. Cutover in phases by capability, not all-at-once

## Principles for Technology Decisions

When evaluating new tools or changes:

1. **Does it preserve Obsidian as canonical memory?**
2. **Does it support the reconciliation engine?**
3. **Can we migrate away from it if needed?**
4. **Does it align with GC/HC frameworks?**
5. **Does it increase or decrease system complexity?**
6. **Can we operate it with available skill and resources?**

If you can't answer yes to most of these, reconsider.

## Revision History

- **2026-05-11:** Updated to Claude Sonnet + Haiku (Phase 1), Qwen2.5 (Phase 2), BGE-M3 embeddings, CAD pricing, one-way Obsidian→Neo4j sync, Kokoro TTS
- **2026-04-24:** Initial version