---
type: architecture
created: 2026-05-11
updated: 2026-06-01
tags: [pca, governance, runtime, policy, orchestration, security]
status: draft
---

# Runtime Policy Gate

## 1. Purpose

The Runtime Policy Gate is the primary governance and execution control boundary for the Personal Cognitive Architecture (PCA).

It governs:

- what cognition is allowed to execute
- which models may be used
- which tools may be invoked
- when cloud escalation is permitted
- when human approval is required
- what information may persist into memory
- how automation actions are authorized

The Runtime Policy Gate exists because:

> cognition is activated, not assumed.

The PCA does not treat:

- reasoning
- memory updates
- agent execution
- automation
- cloud access
- synthesis
- decision generation

as automatically trusted.

All consequential operations must pass through a governed runtime boundary.

---

# 1.1 Gate Hierarchy

The Runtime Policy Gate is the canonical PCA governance model.

Specialized gates may exist for particular execution paths, but they inherit from this model rather than replacing it.

Current specialization:

- `Edge Policy Gate`: governs phone-originated capture events after local inference and before downstream routing

The relationship is:

```text
Runtime Policy Gate
└── Edge Policy Gate
    └── capture -> validate -> govern -> route
```

The edge gate is therefore a scoped implementation of runtime governance for intake, not a separate architecture.

---

# 2. Architectural Position

The Runtime Policy Gate functions similarly to:

| Enterprise Pattern | PCA Equivalent |
|---|---|
| API Gateway | Runtime Policy Gate |
| Zero Trust Access Layer | Cognitive Execution Authorization |
| Service Mesh Policy Layer | Agent Execution Governance |
| Data Governance Enforcement | Memory and Knowledge Governance |
| Workflow Approval Engine | HITL Escalation Framework |
| Cloud Routing Layer | Burst Control and Model Routing |

The Runtime Policy Gate is effectively:

> Zero Trust for cognition and automation.

---

# 3. Core Responsibilities

The Runtime Policy Gate is responsible for:

## 3.1 Execution Authorization

Determine whether:

- an agent may execute
- a workflow may run
- a tool may be invoked
- a memory update may occur
- a model escalation may occur

The default posture is:

> deny by default unless policy conditions are satisfied.

---

## 3.2 Model Routing and Burst Control

Select appropriate execution location:

| Workload | Preferred Location |
|---|---|
| Sensitive/private reasoning | Local |
| Lightweight automation | Local |
| Canonical memory operations | Local |
| High-context reasoning | Cloud burst |
| Large multimodal synthesis | Cloud burst |
| Cost-sensitive recurring workflows | Local-first |

Routing factors:

- sensitivity
- latency
- cost
- context size
- confidence
- required capability
- availability of local runtime
- offline status

The gate enforces:

> least-capable-model-required.

---

## 3.3 Human-in-the-Loop Governance

The gate determines whether human review is required.

Approval triggers may include:

- irreversible actions
- memory promotion
- deletion
- external communications
- credential changes
- system modifications
- high-confidence contradiction detection
- cloud escalation for sensitive material
- autonomous task execution

The PCA philosophy is:

> governed autonomy, not unrestricted autonomy.

---

## 3.4 Knowledge Governance

The gate governs movement between knowledge lifecycle states.

Example lifecycle:

```text
Inbox
→ Provisional
→ Reviewed
→ Trusted
→ Challenged
→ Archived
```

The gate controls:

- promotion
- rejection
- contradiction escalation
- confidence updates
- provenance tracking
- reconciliation triggers

The gate enforces:

> intake is not knowledge.

---

## 3.5 Tool and Agent Permissions

Agents must not receive unrestricted tool access.

The Runtime Policy Gate controls:

- permitted tools
- execution scope
- data access boundaries
- filesystem permissions
- network permissions
- API access
- cloud escalation rights
- persistence rights

Principle:

> every agent should have the minimum permissions required for its role.

---

# 4. Runtime Decision Inputs

The Runtime Policy Gate evaluates:

| Input Type | Example |
|---|---|
| Sensitivity | personal/private/work-related |
| Source Trust | verified vs weak signal |
| Confidence Score | low/moderate/high |
| Action Risk | reversible vs irreversible |
| Runtime Availability | local runtime online/offline |
| Cost State | token or API budget |
| Memory State | inbox/provisional/trusted |
| Human Presence | available/unavailable |
| Agent Identity | allowed capabilities |
| Environmental Context | connected/disconnected/travel mode |

---

# 5. Runtime Decision Outputs

The Runtime Policy Gate may:

| Output | Meaning |
|---|---|
| Allow | operation proceeds |
| Deny | operation blocked |
| Escalate | requires human review |
| Downgrade | route to simpler/local model |
| Burst | allow cloud escalation |
| Sandbox | execute in isolated mode |
| Log Only | permit but audit heavily |
| Hold | defer until conditions improve |

For implementation consistency, specialized gates should map their decisions back to this shared vocabulary even when they expose narrower routing semantics such as `review_queue` or `local_only`.

---

# 5.1 Shared Decision Record

All policy gate implementations should emit a decision record with a stable minimum shape:

```json
{
  "decision": "allow|deny|escalate|sandbox|hold|log_only",
  "reason": "short_policy_reason",
  "route": "obsidian|backlog|review_queue|local_only|discard|null",
  "requires_human_approval": true,
  "policy_version": "string",
  "trace_id": "string"
}
```

Notes:

- `decision` is the canonical governance outcome
- `route` is the execution-path selection when routing is relevant
- `requires_human_approval` may be true even when the immediate decision is `hold` or `escalate`
- capture-specific gates may add fields, but should not omit these baseline outputs

---

# 6. Operational Modes

## 6.1 Reconciliation OFF

Minimal governance.

Used for:

- exploratory thinking
- temporary scratch reasoning
- low-consequence experimentation

Characteristics:

- no durable memory promotion
- lightweight logging
- minimal automation authority

---

## 6.2 Reconciliation LOCAL

Default operational mode.

Characteristics:

- local-first execution
- controlled memory promotion
- standard validation
- standard audit logging
- cloud escalation restricted

---

## 6.3 Reconciliation BURST

Escalated cognition mode.

Characteristics:

- cloud model escalation allowed
- larger context windows
- multimodal synthesis
- enhanced reasoning capability
- higher audit requirement
- stronger HITL expectations

Burst mode should be:

- intentional
- observable
- explainable
- cost-aware

---

# 7. Runtime Zones

The Runtime Policy Gate should eventually distinguish execution zones.

| Zone | Characteristics |
|---|---|
| Trusted Local | canonical memory and core workflows |
| Sandbox | experimental agents and testing |
| Edge Runtime | sensor/event nodes |
| Cloud Burst | hosted inference |
| Restricted | sensitive/private workflows |

Zones may have different:

- network access
- tool access
- persistence rights
- logging requirements
- cloud escalation rights

---

# 8. Policy Categories

Policies should eventually include:

| Policy Type | Purpose |
|---|---|
| Execution Policies | who/what can run |
| Memory Policies | what may persist |
| Routing Policies | local vs cloud |
| Cost Policies | budget thresholds |
| Security Policies | access control |
| Escalation Policies | when HITL required |
| Agent Policies | allowed capabilities |
| Retention Policies | archive/delete behavior |
| Audit Policies | logging requirements |

---

# 9. Audit and Observability

Every consequential runtime decision should be observable.

Minimum audit requirements:

- timestamp
- initiating workflow/agent
- requested action
- routing decision
- approval decision
- cloud escalation event
- model used
- confidence score if available
- memory promotion/rejection event
- failure reason if denied

Future capability:

- explainable policy decisions
- runtime replay
- reconciliation audit history
- decision lineage
- policy simulation/testing

---

# 10. Relationship to Cognitive Reconciliation Engine

The Runtime Policy Gate and Cognitive Reconciliation Engine are complementary.

| Component | Primary Role |
|---|---|
| Cognitive Reconciliation Engine | truth management and belief evolution |
| Runtime Policy Gate | execution governance and authorization |

Relationship:

```text
Capture
→ Validation
→ Runtime Policy Gate
→ Reconciliation Engine
→ Memory Promotion / Action
```

The Runtime Policy Gate determines:

> whether cognition may proceed.

The Reconciliation Engine determines:

> how cognition changes trusted knowledge.

---

# 11. Reference Runtime Flow

```text
[Capture/Input]
        |
        v
[Validation & Signal Scoring]
        |
        v
[Runtime Policy Gate]
        |
   +----+----+
   |         |
Allow     Escalate/HITL
   |         |
   v         v
[Execution / Agent / Model]
        |
        v
[Reconciliation Engine]
        |
        v
[Knowledge Lifecycle Decision]
        |
        v
[Trusted Memory / Action]
```

---

# 12. Non-Negotiable Runtime Principles

1. No unrestricted autonomous agents.
2. No automatic trust of captured information.
3. No cloud escalation without policy evaluation.
4. No irreversible automation without approval.
5. No secrets exposure through logs, markdown, or GitHub.
6. No memory promotion without provenance.
7. No persistence without lifecycle state.
8. No tool access broader than necessary.
9. No execution without observability.
10. Governance before autonomy.

---

# 13. Future Evolution

Potential future capabilities:

- policy simulation
- dynamic trust scoring
- adaptive routing
- agent reputation scoring
- cognitive load-aware throttling
- emotional/context-aware escalation
- multi-agent consensus validation
- runtime anomaly detection
- sovereign offline mode enforcement

---

# 14. Strategic Position

The Runtime Policy Gate is the core governance boundary that transforms the PCA from:

- a collection of AI tools

into:

- a governed cognitive runtime platform.

It operationalizes the PCA principle:

> cognition must be governed before it is operationalized.
