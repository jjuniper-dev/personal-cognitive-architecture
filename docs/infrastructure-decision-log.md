---
type: governance
created: 2026-05-11
updated: 2026-05-11
tags: [pca, infrastructure, adr, decisions, governance]
status: active
---

# Infrastructure Decision Log

## 1. Purpose

This document records major infrastructure, runtime, orchestration, security, and platform decisions for the Personal Cognitive Architecture (PCA).

The objective is to:

- preserve architectural rationale
- prevent repeated re-evaluation of settled decisions
- document tradeoffs and constraints
- reduce architecture drift
- track rejected options and lessons learned
- support long-term maintainability

This document functions similarly to:

- Architecture Decision Records (ADRs)
- enterprise standards decisions
- platform governance records

---

# 2. Decision Format

Each decision should contain:

| Field | Purpose |
|---|---|
| Decision ID | Unique identifier |
| Status | Proposed / Accepted / Deferred / Rejected / Superseded |
| Date | Decision date |
| Context | Why the decision exists |
| Decision | What was chosen |
| Rationale | Why it was chosen |
| Tradeoffs | Downsides or constraints |
| Alternatives Considered | Other evaluated approaches |
| Follow-Up | Future reassessment triggers |

---

# 3. Decision Log

---

## PCA-INF-001 — Obsidian as Canonical Memory

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

The PCA requires:

- durable knowledge persistence
- human-readable storage
- portability
- sovereignty
- long-term maintainability
- graph-oriented linking

The architecture must avoid dependence on opaque proprietary memory systems.

### Decision

Obsidian markdown vaults are the canonical memory substrate.

### Rationale

Advantages:

- markdown durability
- local-first operation
- graph-friendly structure
- broad tooling compatibility
- vendor independence
- filesystem transparency
- Git compatibility

### Tradeoffs

- requires external indexing/retrieval services
- graph semantics remain partially implicit
- synchronization requires governance

### Alternatives Considered

- Notion
- Tana
- Logseq
- fully managed vector databases
- cloud-native proprietary memory systems

### Follow-Up

Future graph-layer augmentation may occur through Neo4j or similar services.

Canonical markdown remains authoritative.

---

## PCA-INF-002 — Local-First Runtime Direction

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

The PCA increasingly depends on:

- persistent workflows
- memory continuity
- agent orchestration
- automation
- runtime governance

Pure SaaS dependency creates risk:

- vendor lock-in
- transcript loss
- pricing instability
- degraded portability
- reduced sovereignty

### Decision

The PCA will follow a local-first, cloud-assisted runtime model.

### Rationale

Local-first enables:

- durable memory
- operational independence
- offline capability
- stronger privacy posture
- reduced recurring dependency risk

Cloud burst remains available for:

- frontier reasoning
- multimodal synthesis
- high-context processing

### Tradeoffs

- increased operational responsibility
- infrastructure management burden
- local security requirements
- backup/recovery responsibility

### Alternatives Considered

- fully cloud-hosted stack
- SaaS-only automation model
- managed orchestration platforms

### Follow-Up

Cloud usage patterns should be periodically reassessed against:

- cost
- capability
- sovereignty
- operational burden

---

## PCA-INF-003 — Dell Mini PC as Primary Runtime Node

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

The PCA requires:

- Docker runtime
- orchestration
- persistence
- observability
- lightweight local services
- potential local inference

Raspberry Pi-only infrastructure was evaluated.

### Decision

Dell Mini PCs / OptiPlex Micro systems are the preferred primary runtime substrate.

### Rationale

Advantages:

- stronger CPU performance
- more RAM
- virtualization support
- better Docker performance
- better storage flexibility
- easier runtime scaling
- stronger persistence capability

### Tradeoffs

- higher power usage than Raspberry Pi
- larger physical footprint
- reduced portability compared to single-board systems

### Alternatives Considered

- Raspberry Pi-only runtime
- NAS-first runtime
- cloud-only runtime
- gaming-PC-hosted runtime

### Follow-Up

Hardware selection should remain:

- modular
- replaceable
- cost-conscious

Avoid over-optimizing hardware before operational maturity.

---

## PCA-INF-004 — Raspberry Pi as Edge Runtime Node

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

Raspberry Pis remain valuable for:

- low-power execution
- edge sensing
- environmental monitoring
- event-driven automation

However, they are less suited for:

- heavy orchestration
- multi-service persistence
- high-throughput runtime operations

### Decision

Raspberry Pis are positioned as edge/event nodes rather than primary orchestration infrastructure.

### Rationale

Best-fit use cases:

- weather agents
- camera triggers
- home monitoring
- lightweight APIs
- automation satellites
- isolated experimentation

### Tradeoffs

- introduces distributed topology complexity
- requires additional network management
- limited local compute capability

### Alternatives Considered

- Pi-only cluster
- no edge nodes
- cloud-only sensors

### Follow-Up

Edge-node expansion should occur only after:

- orchestration stability
- secrets handling maturity
- observability baseline

---

## PCA-INF-005 — VPN-First Remote Access

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

The PCA runtime may eventually expose:

- orchestration endpoints
- remote administration
- APIs
- automation services

Direct public exposure creates unnecessary risk.

### Decision

Remote administrative access should use VPN-first patterns.

### Rationale

Advantages:

- authenticated access
- reduced public exposure
- stronger administrative boundary
- portability across networks
- reduced dependence on static IP restrictions

### Tradeoffs

- added configuration complexity
- additional operational maintenance
- dependency on VPN availability

### Alternatives Considered

- direct port forwarding
- IP allow lists only
- public web exposure

### Follow-Up

VPN implementation selection remains open.

Preference:

- simple
- observable
- recoverable
- low-maintenance

---

## PCA-INF-006 — Runtime Governance Before Autonomy

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-11 |

### Context

The PCA increasingly includes:

- workflows
- agents
- cloud routing
- memory promotion
- automation

Unrestricted autonomy creates:

- governance risk
- memory corruption risk
- accidental destructive behavior
- uncontrolled cloud usage

### Decision

The PCA requires runtime governance and policy gating before autonomous execution expansion.

### Rationale

This aligns with:

- human-in-the-loop philosophy
- enterprise governance patterns
- explainability requirements
- trust boundaries
- sovereignty principles

### Tradeoffs

- slower automation expansion
- increased implementation complexity
- additional review burden

### Alternatives Considered

- unrestricted autonomous agents
- direct model/tool invocation
- implicit trust architecture

### Follow-Up

Future implementation areas:

- Runtime Policy Gate
- agent permissions
- auditability
- approval workflows
- model routing

---

## PCA-INF-007 — Portable Edge Runtime Is a Future Deployment Pattern

| Field | Value |
|---|---|
| Status | Deferred |
| Date | 2026-05-11 |

### Context

There is strong interest in:

- portable AI runtime infrastructure
- transportable edge compute
- ruggedized deployment
- self-contained orchestration environments

However, operational requirements are not fully stabilized.

### Decision

Portable rack infrastructure is deferred until runtime requirements mature.

### Rationale

The PCA should avoid:

- premature hardware optimization
- infrastructure overbuild
- transport-focused design before runtime usefulness is proven

### Tradeoffs

- delays physical infrastructure experimentation
- limits short-term portability

### Alternatives Considered

- immediate rack build-out
- fully distributed cluster experimentation
- portable-first architecture

### Follow-Up

Portable runtime packaging should be revisited after:

- stable ingestion loop
- durable orchestration runtime
- secrets management maturity
- observability baseline
- local runtime recovery validation

---

# 4. Deferred Decisions

The following decisions remain open:

| Area | Status |
|---|---|
| Secrets management platform | Open |
| Local vector database | Open |
| VPN implementation | Open |
| Observability stack | Open |
| Local model serving | Deferred |
| Agent registry implementation | Deferred |
| Portable rack hardware | Deferred |
| Backup tooling strategy | Open |
| Runtime policy engine implementation | Open |

---

# 5. Decision Governance Rules

1. Decisions should be revisited only when conditions materially change.
2. Rejected options should remain documented.
3. Major runtime changes require rationale.
4. Governance and simplicity take precedence over novelty.
5. Local-first remains default unless strong justification exists.
6. Infrastructure should follow operational need, not curiosity.
7. Portability should not compromise maintainability.
8. Human oversight remains a core architectural principle.

---

# 6. Strategic Position

This decision log formalizes the PCA as:

> a governed cognitive infrastructure platform with explicit architectural reasoning, runtime constraints, and long-term operational accountability.

The goal is not merely to accumulate tooling.

The goal is:

> coherent, durable, sovereign cognitive infrastructure.
