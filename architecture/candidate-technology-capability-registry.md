# Candidate Technology & Capability Registry

## Purpose

The Candidate Technology & Capability Registry (CTCR) is a governed holding area for external tools, GitHub repositories, platforms, architectural patterns, reference implementations, reusable code assets, and technical resources that may support the Personal Cognitive Architecture (PCA), but require validation before becoming experiments, backlog items, or integrated capabilities.

The registry prevents useful discoveries from being lost while also preventing premature adoption into the solution architecture.

## Operating Principle

Promising technologies and patterns enter the CTCR first. Nothing becomes part of the PCA solution until it has been assessed, reconciled against the target architecture, and promoted through an explicit decision.

## Placement in PCA Flow

```text
[Capture Layer]
   ↓
[Candidate Technology & Capability Registry]
   ↓
[Validation & Scoring]
   ↓
[Cognitive Reconciliation Engine]
   ↓
[Knowledge Graph / Architecture Repository]
   ↓
[Experiment / Backlog / Roadmap]
   ↓
[Integrated Solution]
```

## Scope

The CTCR may include:

- Open-source repositories
- Commercial or open-source platforms
- Automation tools
- AI runtimes and model-serving tools
- Agent frameworks
- Observability and evaluation tools
- Self-hosting and platform-engineering resources
- Reference architectures
- Docker Compose, Terraform, or deployment templates
- Integration accelerators
- Governance, policy, and assurance patterns
- Reusable architectural decisions or implementation patterns

## Out of Scope

The CTCR is not:

- A delivery backlog by itself
- An approved technology list
- A software bill of materials
- A procurement catalogue
- A commitment to adopt any listed item

## Lifecycle States

| State | Meaning |
|---|---|
| Captured | Identified and recorded, but not assessed. |
| Candidate | Appears relevant to PCA and is worth assessment. |
| Under Assessment | Being reviewed for fit, maturity, risk, and effort. |
| Experiment | Approved for sandbox testing or proof of concept. |
| Reference Pattern | Useful as an architectural or design pattern, even if not adopted. |
| Promote to Backlog | Ready to become an actionable delivery, research, or experiment item. |
| Adopt | Approved as part of the solution or supporting toolchain. |
| Defer | Potentially useful, but not timely or aligned enough for current work. |
| Reject | Not suitable due to fit, risk, duplication, immaturity, or other constraint. |
| Retire | Previously useful, but no longer relevant or superseded. |

## Candidate Record Template

```yaml
id: CTCR-000
name: Example Technology or Repository
category: Tool | Platform | Framework | Pattern | Reference | Accelerator | Governance
source_type: GitHub | Article | Documentation | Product | Internal Note | Other
source_url: https://example.com
status: Captured
owner: TBD
date_captured: YYYY-MM-DD
last_reviewed: YYYY-MM-DD

capability_domains:
  - TBD

strategic_relevance:
  - TBD

potential_pca_use:
  - TBD

assessment:
  strategic_relevance: TBD # 1-5
  capability_fit: TBD # 1-5
  maturity: TBD # 1-5
  integration_potential: TBD # 1-5
  governance_fit: TBD # 1-5
  implementation_effort: TBD # 1-5, lower is easier
  risk: TBD # 1-5, lower is safer
  reusability: TBD # 1-5

mining_priority: TBD
next_action: TBD
decision_notes: TBD
```

## Scoring Model

Each candidate should be assessed using a 1-5 scale.

| Dimension | Guiding Question |
|---|---|
| Strategic relevance | Does it support the PCA target architecture or strategic direction? |
| Capability fit | Does it map to a real PCA capability or architecture gap? |
| Maturity | Is it maintained, documented, stable, and credible? |
| Integration potential | Can it connect to the PCA stack or enterprise-aligned patterns? |
| Governance fit | Can it be controlled, audited, secured, and human-governed? |
| Implementation effort | How difficult would it be to test, operate, or integrate? |
| Risk | Are there licensing, security, privacy, operational, or dependency concerns? |
| Reusability | Can it be reused across multiple workflows, agents, or platform layers? |

Suggested lightweight prioritization formula:

```text
Mining Priority = Strategic Relevance + Capability Fit + Reusability + Integration Potential + Governance Fit - Implementation Effort - Risk
```

The formula is a triage aid, not an automatic decision mechanism.

## Promotion Rules

A candidate may be promoted to the backlog only when:

1. It maps to a defined PCA capability or architecture gap.
2. It has a clear use case.
3. It has an identified next action.
4. Its risks are understood enough for the next decision.
5. The promotion is explicit, not implicit.

## Registry Buckets

### Candidate Tools

Technologies that may be tested or adopted.

### Reference Patterns

Resources that inform architecture, even if not implemented directly.

### Integration Accelerators

Templates, connectors, scripts, or reusable implementation assets.

### Evaluation Targets

Candidates selected for sandbox testing or proof of concept.

### Strategic Signals

Resources that indicate ecosystem movement or future architectural direction.

## Initial Seed Entries

| ID | Name | Type | Source | Status | PCA Relevance | Next Action |
|---|---|---|---|---|---|---|
| CTCR-001 | awesome-selfhosted | Reference Pattern | GitHub | Candidate | Ecosystem discovery catalogue for self-hosted capabilities. | Mine for relevant PCA capability domains. |
| CTCR-002 | Self-Hosting-Guide | Reference Pattern | GitHub | Candidate | Operational reference for self-hosting, networking, runtime, and infrastructure fundamentals. | Review for PCA platform foundation patterns. |
| CTCR-003 | Coolify | Platform | GitHub | Candidate | Self-hosted PaaS and developer self-service control-plane pattern. | Assess as PCA deployment/runtime management experiment. |
| CTCR-004 | Dokploy | Platform | GitHub | Candidate | Alternative self-hosted deployment platform. | Compare against Coolify for platform control-plane fit. |
| CTCR-005 | n8n | Tool / Platform | GitHub | Candidate | Automation, workflow orchestration, and agent workflow execution. | Promote likely experiment for PCA action and orchestration layer. |
| CTCR-006 | Ollama | Tool / Runtime | GitHub | Candidate | Local model runtime for self-hosted AI execution. | Assess for local PCA inference and private experimentation. |
| CTCR-007 | Open WebUI | Tool / Interface | GitHub | Candidate | Local AI interaction layer for self-hosted models. | Assess as optional UI layer for local model interaction. |
| CTCR-008 | Langfuse | Tool / Observability | GitHub | Candidate | LLM observability, tracing, evaluation, and prompt management. | Assess as observability/evaluation pattern for PCA agents. |
| CTCR-009 | NVIDIA NIM / API Catalog Free Developer Access | Cloud AI API / Model Serving | NVIDIA Developer Program | Candidate | Free prototyping access to NVIDIA-hosted NIM endpoints and downloadable NIM microservices; useful for model experimentation, OpenAI-compatible API testing, and agent/runtime comparison. | Validate current limits, data handling terms, model catalogue, and suitability for non-sensitive PCA experiments. |
| CTCR-010 | NVIDIA LaunchPad | Cloud Lab / Reference Environment | NVIDIA | Candidate | Free short-term hands-on labs for AI, data science, infrastructure, and NVIDIA enterprise software patterns. Useful for learning, reference architecture review, and platform capability exploration. | Identify relevant labs for AI runtime, data science, model serving, and enterprise platform patterns. |
| CTCR-011 | Obsidian | Tool / Knowledge Store | Internal Note | Candidate | Canonical human-readable memory substrate for PCA; supports local-first knowledge capture, durable markdown storage, and controlled promotion from personal notes to structured architecture artifacts. | Maintain as core canonical-memory pattern; assess vault governance, synchronization, backup, and separation between personal and work contexts. |
| CTCR-012 | Neo4j | Platform / Graph Database | Internal Note | Candidate | Graph substrate for semantic topology, relationship modeling, contradiction tracking, confidence propagation, and Cognitive Reconciliation Engine state. | Assess schema patterns for claims, evidence, contradictions, decisions, sources, and reconciliation status. |
| CTCR-013 | ChromaDB | Tool / Vector Store | Internal Note | Candidate | Lightweight local vector index for semantic retrieval and provisional RAG memory. | Validate as derived index from Obsidian and Neo4j; compare against hybrid retrieval alternatives. |
| CTCR-014 | OpenSearch | Platform / Search | Internal Note | Candidate | Candidate hybrid retrieval engine for keyword, metadata, and vector search fusion across PCA memory. | Assess whether OpenSearch should complement or supersede ChromaDB for mature retrieval architecture. |
| CTCR-015 | LM Studio | Tool / Runtime | Internal Note | Candidate | Local desktop model experimentation and runtime abstraction layer for testing open-weight models. | Evaluate as optional local experimentation interface alongside Ollama. |
| CTCR-016 | LlamaIndex | Framework | Internal Note | Candidate | Data and retrieval framework for structured RAG pipelines, context composition, and memory-aware agent access. | Assess fit for PCA retrieval orchestration versus custom n8n/Python implementation. |
| CTCR-017 | Whisper | Tool / Model | Internal Note | Candidate | Speech-to-text capability for voice-first cognition, ambient capture, mobile ingestion, and conversational memory persistence. | Validate local transcription workflow and integration with iPhone Shortcuts, n8n, and Obsidian note generation. |
| CTCR-018 | Playwright | Tool / Automation | Internal Note | Candidate | Browser automation and web extraction capability for agentic capture, structured scraping, and repeatable source collection. | Assess governance controls for web capture, rate limits, robots.txt respect, and provenance logging. |
| CTCR-019 | Cognitive Reconciliation Engine | Pattern / Capability | Internal Note | Candidate | Core reasoning-control capability for contradiction detection, evidence arbitration, relationship typing, confidence propagation, and reconciliation health. | Promote to architecture backlog after Phase 1 produces sufficient INBOX, disagreement, and validation data. |
| CTCR-020 | Disagreement-Driven Validation | Pattern / Governance | Internal Note | Reference Pattern | Multi-agent validation pattern using a primary assessment, critical opposition, agreement scoring, arbitration, and human escalation. | Preserve as validation and assurance pattern for PCA agent workflows. |
| CTCR-021 | Runtime Policy Gate | Pattern / Governance | Internal Note | Candidate | Policy-aware control point for classify, sanitize, route, enforce, and audit decisions before execution or persistence. | Define minimum viable policy gate for sensitive capture, model routing, and cloud/local execution decisions. |
| CTCR-022 | Cognitive Health Layer | Pattern / Observability | Internal Note | Candidate | Observability layer for reasoning quality, confidence, reconciliation status, review flags, validation score, and decision health. | Translate into metrics model for Prometheus/Grafana or Langfuse-style tracing. |
| CTCR-023 | Attention-Based Routing | Pattern / Runtime | Internal Note | Candidate | Priority-aware routing pattern for scoped reasoning, selective compute, bounded cognition, and least-capable-model-required execution. | Assess routing dimensions: sensitivity, latency, cost, task complexity, confidence, and escalation threshold. |
| CTCR-024 | Keycloak | Platform / Identity | Internal Note | Candidate | Open-source identity and access management pattern for role-aware cognition, Zero Trust boundaries, and authorization-aware workflows. | Compare with Azure AD for personal/self-hosted versus enterprise-aligned identity patterns. |
| CTCR-025 | Open Policy Agent | Tool / Policy Engine | Internal Note | Candidate | Runtime authorization and policy decision engine for governed AI execution and auditable control-plane decisions. | Assess as implementation option for Runtime Policy Gate. |
| CTCR-026 | Prometheus + Grafana | Tool / Observability | Internal Note | Candidate | Metrics and dashboard stack for execution monitoring, cognitive telemetry, validation analytics, and runtime health. | Define initial PCA metrics: validation volume, confidence distribution, disagreement rate, routing outcomes, and backlog age. |
| CTCR-027 | Docker + Docker Compose | Platform / Deployment | Internal Note | Candidate | Portable self-hosting foundation for reproducible PCA infrastructure and local runtime composition. | Maintain as baseline deployment pattern for Phase 1-2 services. |
| CTCR-028 | GitLab | Platform / DevOps | Internal Note | Candidate | Versioned operational governance spine for CI/CD, audit trails, issue tracking, promotion workflows, and knowledge lifecycle management. | Compare with current GitHub repository workflow before introducing additional DevOps platform complexity. |
| CTCR-029 | TurboQuant | Pattern / Optimization | Internal Note | Strategic Signal | Experimental quantization and compression signal involving polar encoding, Johnson-Lindenstrauss-style transforms, and aggressive local model optimization. | Track as frontier signal for edge/local cognition; do not adopt until implementation maturity and reproducibility are validated. |
| CTCR-030 | Per-Layer Embeddings | Pattern / Frontier AI | Internal Note | Strategic Signal | Experimental memory-injection concept for deeper context control through per-layer or internal-model representation hooks. | Track as research signal only; assess later if practical tooling emerges. |
| CTCR-031 | Gemma / Open-Weight Apache-2.0 Models | Model Ecosystem | Internal Note | Strategic Signal | Open-weight permissively licensed model ecosystem relevant to sovereign, auditable, local, and governed cognition. | Track candidate models for local runtime evaluation alongside Qwen2.5. |
| CTCR-032 | Model Context Protocol | Standard / Integration Pattern | Internal Note | Candidate | Integration pattern for tool, data, and context access across model runtimes and agent workflows. | Assess as possible interoperability layer for PCA connectors and enterprise-aligned context access. |
| CTCR-033 | Microsoft Fabric | Platform / Enterprise Data | Internal Note | Candidate | Enterprise lakehouse and analytics platform relevant to Phase 3+ architecture, data integration, governance, and reporting. | Keep as enterprise applicability pattern; map PCA graph and memory concepts to Fabric-compatible data products. |
| CTCR-034 | Azure AI / Azure OpenAI | Platform / Enterprise AI | Internal Note | Candidate | Enterprise-aligned cloud AI service pattern for compliant model access, auditability, and integration with Azure governance controls. | Assess only for enterprise or non-sensitive cloud-burst scenarios; preserve local-first pattern for personal PCA. |
| CTCR-035 | Power Automate | Platform / Enterprise Automation | Internal Note | Candidate | Enterprise workflow automation analogue to n8n for Phase 3+ mapping into Microsoft/Azure environments. | Map n8n workflow concepts to Power Automate patterns for future enterprise transition. |

## Backlog Translation Examples

A registry entry becomes a backlog item only after a use case is defined.

Example backlog items:

- Evaluate n8n as the PCA automation and agent orchestration layer.
- Deploy Coolify in a sandbox and assess whether it can support PCA application deployment.
- Mine awesome-selfhosted for capture, processing, storage, reasoning, and output-generation candidates.
- Assess Langfuse as a traceability and evaluation layer for PCA agent workflows.
- Test NVIDIA NIM/API Catalog free developer access as a non-sensitive model experimentation endpoint.
- Review NVIDIA LaunchPad labs for reference architectures relevant to PCA runtime and AI platform patterns.
- Assess OpenSearch as a hybrid retrieval layer across Obsidian, Neo4j, and vector-derived memory.
- Define the minimum viable Runtime Policy Gate for sensitive capture and model-routing decisions.
- Design the Cognitive Health metrics model for confidence, disagreement, routing, and reconciliation status.
- Evaluate Whisper-based voice capture into the n8n → Obsidian ingestion pipeline.
- Compare MCP-style context access with custom PCA connector patterns.

## Governance Notes

The CTCR supports human-in-the-loop governance. Registry inclusion does not imply approval. Each candidate must be assessed for privacy, security, licensing, operational resilience, maintainability, and alignment with PCA principles before promotion.

Cloud-hosted free tiers require additional scrutiny before use with any sensitive or personal data. Confirm terms, logging behavior, data retention, usage limits, and production restrictions before moving beyond experimentation.

Frontier techniques, model-runtime optimizations, and emerging protocol patterns must remain candidates or strategic signals until they have reproducible implementations, clear operational controls, and a defined PCA use case.

## Review Cadence

Recommended cadence:

- Weekly: review newly captured candidates.
- Monthly: reassess high-potential candidates.
- Quarterly: retire stale, duplicated, or superseded entries.

## Minimal Intake Checklist

Before adding an item, capture:

- Name
- Source URL
- Type
- Why it matters
- PCA capability domain
- Initial status
- Suggested next action

## Decision Rule

Great repository does not equal backlog item.

Great repository equals candidate capability.

Candidate capability plus clear use case equals backlog item.
