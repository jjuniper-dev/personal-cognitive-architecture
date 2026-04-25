---
type: architecture
created: 2026-04-24
updated: 2026-04-24
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
|-----------|-----------|------|-----------|
| **Knowledge Store** | Obsidian | Canonical memory | Human-readable, version-controllable, local-first |
| **Automation Orchestration** | n8n (Docker) | Workflow engine | Low-code, flexible, self-hosted capable |
| **Development Environment** | VS Code | Coding & note editing | Integrated, extensible, markdown support |
| **LLM (Validation)** | OpenAI API (GPT-4) | Scoring, validation | High quality, fast iteration |
| **LLM (Reasoning)** | OpenAI API (GPT-4) | Synthesis, tagging | Established reliability |
| **Data Storage** | Local filesystem + Git | Persistence | Version control, auditability |
| **API Gateway** | n8n built-in webhooks | External integrations | Capture from web, voice apps |

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
    │  & Scoring │    │   (Future)      │   │   Worker    │
    │ (GPT-4)    │    │                 │   │             │
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
├── .env                           # OpenAI API keys
└── claude/workflows/              # Workflow automation scripts
```

**Storage**:
- Obsidian vault in Git repository
- n8n workflows in code version control
- Execution logs in local filesystem
- API keys in environment variables (.env, not committed)

## Phase 2: Self-Hosted Migration

### Purpose
Local inference, semantic indexing, structured session support, observability

### Technology Additions

| Component | Technology | Role | Rationale |
|-----------|-----------|------|-----------|
| **LLM (Local)** | Mistral 7B or Llama 2 | Reasoning on-device | Reduced API costs, privacy |
| **Embedding Model** | all-MiniLM-L6-v2 | Semantic search | Lightweight, fast inference |
| **Vector Store** | ChromaDB | Semantic indexing | Lightweight, no external dependency |
| **Observability** | Prometheus + Grafana | Monitoring | Standard open-source stack |
| **Logging** | ELK (Elasticsearch) | Centralized logs | Search and analysis capability |
| **Session Management** | Custom layer | State tracking | Workflow continuity |

### Architecture Additions (Phase 2)

```
Phase 1 Components + New Layer:

    ┌─────────────────────────────────┐
    │  Local LLM Inference Cluster     │
    │  ├─ Mistral 7B                  │
    │  ├─ Embedding: all-MiniLM-L6-v2 │
    │  └─ Quantization: 4-bit         │
    └────────────┬────────────────────┘
                 │
    ┌────────────▼────────────┐
    │  ChromaDB Vector Store  │
    │  (Semantic Index)       │
    └─────────────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │  Reasoning & Reconciliation    │
    │  (Cognitive Reconciliation)    │
    └────────────┬──────────────────┘
                 │
              Obsidian
```

### Deployment (Phase 2)

```
Docker Compose:
├── n8n (container)
├── mistral-7b-inference (container)
├── chromadb (container)
├── prometheus (monitoring)
├── grafana (dashboards)
└── volumes for persistence
```

## Phase 3+: Enterprise Applicability

### Purpose
GC/HC compliance, enterprise governance, multi-tenant orchestration, formal output engine

### Technology Stack

| Component | Technology | Role | Rationale |
|-----------|-----------|------|-----------|
| **Cloud Platform** | Azure | Enterprise infrastructure | GC-approved, compliance-ready |
| **Data Lakehouse** | Microsoft Fabric | Analytics & integration | Enterprise-grade data management |
| **Automation Platform** | Power Automate | Enterprise workflows | Native Azure integration |
| **LLM Service** | Azure OpenAI | Compliant AI services | GC-aligned, audit-ready |
| **Identity** | Azure AD | Access control | Enterprise IAM |
| **Secrets Management** | Azure Key Vault | Credential management | Enterprise security |
| **Audit & Compliance** | Azure Purview | Data governance | Policy enforcement |
| **Output Engine** | Python + FastAPI | Template rendering | Structured artifact generation |
| **Report Server** | Power BI | Executive dashboards | Visual decision support |

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
│  │  └─ Audio (Summaries)                     │ │
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
| **OpenAI API** | High quality, fastest iteration | API costs, external dependency | ✓ Phase 1 |
| **Azure OpenAI** | GC-compliant, compliance-ready | Higher latency, compliance overhead | ✓ Phase 3+ |
| **Local Mistral** | Privacy, cost, no external dependency | Lower quality, requires GPU | ✓ Phase 2 |
| **Google Cloud AI** | Competitive quality | Less GC alignment | - |

## Technology Migration Path

### Phase 1 → Phase 2

**No breaking changes** if designed properly:

1. Keep Obsidian as canonical memory
2. Introduce ChromaDB for semantic search (non-destructive)
3. Stand up local LLM alongside OpenAI API (gradual cutover)
4. Add observability without changing core flow
5. Migrate when ready; maintain dual-stack during transition

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
