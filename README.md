# React Profile App

## Quick Start

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## ⚠️ Important: Database Scripts

The Neo4j population scripts (`scripts/populate-graph.js` and `scripts/populate-markov-states.js`) write to the database and require:
- `CONFIRM_NEO4J_WRITE=true` environment variable
- A secure `NEO4J_PASSWORD` (not the default "password")

These scripts will refuse to run without both conditions met.

---

# Personal Cognitive Architecture (PCA)

## One-Line Definition

A cognitive operating system that captures, evaluates, integrates, and activates knowledge to continuously improve human thinking and decision-making.

## What It Is

The PCA is **not** a note-taking system, chatbot interface, or productivity tool.

It is a designed system that transforms human cognition into a structured, augmentable, and continuously improving architecture.

The system actively evaluates and evolves knowledge through a Cognitive Reconciliation Engine that identifies reinforcement, contradictions, gaps, and novel contributions. It bridges personal knowledge management with enterprise AI transformation patterns.

## Core Objectives

- **Capture** inputs from multiple modalities (text, voice, web, video, documents)
- **Evaluate** information quality, credibility, and relevance
- **Integrate** knowledge into a structured knowledge graph (Obsidian)
- **Reconcile** new information against existing knowledge with confidence updates
- **Activate** knowledge to generate insights, drive decisions, and trigger actions
- **Output** high-quality structured artifacts (presentations, documents, dashboards)
- **Govern** critical decisions through human-in-the-loop validation
- **Comply** with GC/HC standards and Responsible AI principles

## Architectural Principles

| Principle | Meaning |
|-----------|---------|
| **System over Tools** | Architecture and flow prioritized over individual tools |
| **Human-in-the-Loop Governance** | Critical decisions and belief updates require human validation |
| **Structured Knowledge First** | All information normalized before integration |
| **Continuous Evolution** | System updates internal models over time |
| **Separation of Concerns** | Capture, Processing, Storage, Reasoning, Output remain modular |
| **Ethics by Design** | Privacy, bias detection, accountability embedded at each stage |

## End-to-End Flow

```
[Capture]
   ↓
[Validation & Scoring]
   ↓
[Cognitive Reconciliation Engine]
   ↓
[Knowledge Graph (Obsidian)]
   ↓
[Reasoning / Agents]
   ↓
[Execution Layer]
   ↓
[Multi-Modal Output Generation]
```

Each stage is governed, modular, and reversible.

## Key Capabilities

- **Knowledge Management**: Structured ingestion, graph-based linking, semantic retrieval
- **AI-Augmented Reasoning**: Pattern detection, cross-domain synthesis, insight generation
- **Agent Orchestration**: Modular agents performing specific tasks via n8n automation
- **Multi-Modal Processing**: Text, audio transcription, video summarization, web extraction
- **Decision Support**: Prioritization, risk identification, strategic alignment
- **Reconciliation**: Active contradiction detection and belief evolution
- **Output Generation**: Multi-modal artifacts meeting GC/HC compliance standards

## Current Phase

### Phase 1: MVP (Cloud Jumpstart)

**Objective**: Prove the first operational loop

```
n8n → Obsidian → structured note in vault
```

**Immediate Goals**:
- Obsidian vault operational
- VS Code workspace operational
- n8n in Docker operational
- One metadata-compliant note written to `/00 Inbox`
- Ingestion workflow validated
- Metadata integrity verified

**Timeline**: Establish memory and plumbing layer first.

### Phase 2: Self-Hosted Migration

- Local inference
- Self-hosted services
- Semantic indexing
- Structured session support
- Full observability

### Phase 3+: Enterprise Applicability

- Formal Cognitive Reconciliation Engine implementation
- GC/HC compliance integration
- Multi-modal output standardization
- Agent orchestration at scale

## Key Differentiators

1. **Cognitive Reconciliation** - Explicit handling of contradictions, model updates, and belief evolution
2. **System-Level Thinking** - Designed like enterprise architecture for the mind
3. **Not Passive Storage** - Actively evaluates and evolves knowledge
4. **Multi-Modal Output Engine** - Produces artifacts, not just responses
5. **Hybrid Personal + Enterprise** - Bridges personal cognition with enterprise patterns
6. **Governed Autonomy** - Human oversight required for consequential decisions

## Non-Negotiable Principles

- **Obsidian is canonical** — Vector indexes support recall, never replace source memory
- **Intake is not knowledge** — Unprocessed captures remain untrusted until validated
- **Human oversight matters** — High-impact decisions require review or approval
- **Governed not autonomous** — Reconciliation and synthesis are explicitly triggered
- **Least-complex architecture** — Simple, durable components over unnecessary infrastructure
- **Orchestrator-worker pattern** — Clear scope, routing, and escalation boundaries

## Documentation Structure

### Strategic & Vision
| Document | Purpose |
|----------|---------|
| **pca-north-star.md** | Vision, design position, and strategic direction |
| **pca-intent-and-build-direction.md** | Current build phase and immediate objectives |
| **pca-active-priorities.md** | Current focus and execution order |

### Architectural Foundations
| Document | Purpose |
|----------|---------|
| **ARCHITECTURE.md** | 9-layer system design, data flows, governance gates, 8-phase roadmap |
| **TECHNOLOGY_STACK.md** | Phase-based technology choices (Phase 1-3), component decisions, cost analysis |
| **ARCHITECTURE_RECONCILIATION.md** | 8-phase roadmap with sprint assignments, gate criteria, blocking dependencies |
| **pca-cognitive-reconciliation-engine.md** | Core differentiator: contradiction detection, Bayesian confidence updates |

### Core Runtime & Governance
| Document | Purpose |
|----------|---------|
| **pca-cognitive-control-plane.md** | Zero Trust Cognition: authorization layer, sensitivity classifier, policy gate, trust thresholds |
| **runtime-policy-gate.md** | Policy definition language (YAML), approval tiers (ROUTINE/SENSITIVE/CRITICAL), escalation workflows |
| **runtime-topology.md** | Deployment architecture: Phase 1-3 topologies, Docker Compose, networking, failover strategies |
| **homelab-reference-architecture.md** | Sovereign edge runtime: hardware specs, installation guide, tuning, maintenance, cost analysis |
| **agent-runtime-model.md** | Agent anatomy, execution semantics, autonomy boundaries, tool invocation, lifecycle management |
| **observability-and-audit.md** | Execution tracing, lineage tracking, compliance logging, monitoring, retention policies |

### Implementation & Planning
| Document | Purpose |
|----------|---------|
| **SPRINT_5_VALIDATION_LAYER.md** | Dual-agent scoring model, 4-dimension framework, agreement logic, routing decisions |
| **SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md** | 60-90 minute n8n implementation guide, 9-node workflow, system prompts, testing |
| **SPRINT_5_QUICKSTART.md** | 45-minute implementation path for Phase 1 validation layer |
| **ARCHITECTURAL_REVIEW_REQUEST_FOR_OPUS.md** | Architecture review package and questions for Claude Opus 4.7 |
| **pca-compliance-and-governance.md** | GC/HC alignment, ethics by design, responsible AI standards |
| **pca-readiness-assessment.md** | State vs intent gap analysis |

## Technology Stack

### Personal Stack (Phase 1)
- **Obsidian** — Knowledge graph and canonical memory
- **n8n** — Workflow orchestration and automation
- **VS Code** — Development and note editing
- **LLMs** — OpenAI, Mistral (API-based initially)

### Enterprise Alignment (Phase 3)
- **Azure ecosystem** — Cloud infrastructure
- **Microsoft Fabric** — Data and analytics platform
- **Power Platform** — Low-code automation
- **GC-compliant AI services** — Enterprise governance

## Strategic Positioning

This system represents the transition from:

**AI as a tool** → **AI as cognitive infrastructure**

It aligns with:
- Personal Knowledge Management evolution
- Agent-based system design patterns
- Enterprise AI transformation practices
- Responsible AI and GC policy frameworks

## Getting Started

1. Review **pca-north-star.md** for vision and principles
2. Read **pca-intent-and-build-direction.md** for current phase
3. Check **pca-active-priorities.md** for execution order
4. See **docs/** directory for complete architecture documentation

## Key Constraints (Phase 1)

- ✗ No new infrastructure before ingestion loop works
- ✗ No workers before orchestrator defined
- ✗ No indexing before memory is clean
- ✓ Priority: Memory and plumbing layer first

---

**Mantra**: Build memory and plumbing first.
