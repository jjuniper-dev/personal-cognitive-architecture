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

## Backlog Translation Examples

A registry entry becomes a backlog item only after a use case is defined.

Example backlog items:

- Evaluate n8n as the PCA automation and agent orchestration layer.
- Deploy Coolify in a sandbox and assess whether it can support PCA application deployment.
- Mine awesome-selfhosted for capture, processing, storage, reasoning, and output-generation candidates.
- Assess Langfuse as a traceability and evaluation layer for PCA agent workflows.

## Governance Notes

The CTCR supports human-in-the-loop governance. Registry inclusion does not imply approval. Each candidate must be assessed for privacy, security, licensing, operational resilience, maintainability, and alignment with PCA principles before promotion.

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
