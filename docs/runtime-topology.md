---
type: architecture
created: 2026-05-11
updated: 2026-05-11
tags: [pca, topology, runtime, infrastructure, orchestration, homelab]
status: draft
---

# Runtime Topology

## 1. Purpose

This document defines the runtime topology for the Personal Cognitive Architecture (PCA).

It describes:

- execution locations
- service boundaries
- node responsibilities
- storage boundaries
- orchestration flows
- network zones
- cloud integration points
- persistence and recovery expectations

The topology is designed around:

> local-first, governed execution with optional cloud burst.

The topology is intentionally phased and modular.

The PCA should remain functional:

- on a single machine
- in degraded/offline mode
- before expansion into portable edge infrastructure

---

# 2. Topology Philosophy

The PCA runtime is not intended to become:

- a hyperscale homelab
- a fragile distributed cluster
- a permanently online exposed service mesh
- an infrastructure-heavy experimentation environment

The runtime exists to support:

- governed cognition
- durable memory
- workflow orchestration
- controlled automation
- selective intelligence augmentation
- resilient personal-scale execution

Core posture:

> simple first, distributed only when justified.

---

# 3. High-Level Runtime Topology

```text
                ┌──────────────────────┐
                │ Human Access Layer   │
                │ iPhone / Mac / PC    │
                └──────────┬───────────┘
                           │
                           v
                ┌──────────────────────┐
                │ Capture & Intake     │
                │ Voice / Files / Web  │
                └──────────┬───────────┘
                           │
                           v
                ┌──────────────────────┐
                │ Orchestration Layer  │
                │ n8n / Webhooks       │
                └──────────┬───────────┘
                           │
                           v
                ┌──────────────────────┐
                │ Runtime Policy Gate  │
                │ Governance Boundary  │
                └───────┬───────┬──────┘
                        │       │
             ┌──────────┘       └──────────┐
             v                             v
┌────────────────────────┐     ┌────────────────────────┐
│ Local Runtime Services │     │ Cloud Burst Services   │
│ Local agents / APIs    │     │ OpenAI / Azure / APIs  │
└──────────┬─────────────┘     └──────────┬─────────────┘
           │                              │
           └──────────────┬───────────────┘
                          v
               ┌──────────────────────┐
               │ Reconciliation Layer │
               │ Validation / HITL    │
               └──────────┬───────────┘
                          │
                          v
               ┌──────────────────────┐
               │ Canonical Memory     │
               │ Obsidian Vault       │
               └──────────────────────┘
```

---

# 4. Runtime Node Roles

## 4.1 Primary Runtime Node

Preferred implementation:

- Dell Mini PC
- OptiPlex Micro
- equivalent small-form-factor compute node

Role:

> primary orchestration and runtime substrate.

Primary responsibilities:

- Docker runtime
- n8n orchestration
- local APIs
- local automation
- lightweight databases
- vector/index services
- secrets runtime
- observability stack
- local retrieval
- runtime logging
- backup coordination

Characteristics:

- always-on preferred
- headless operation
- persistent storage
- recoverable runtime
- local-first execution

This node becomes:

> the PCA control/runtime hub.

---

## 4.2 Edge Nodes

Preferred implementation:

- Raspberry Pi 5
- lightweight ARM edge devices

Role:

> event and environmental execution.

Primary responsibilities:

- sensor collection
- weather agents
- camera triggers
- local event detection
- lightweight APIs
- automation satellites
- isolated testing
- edge telemetry

Edge nodes should avoid:

- heavyweight orchestration
- large vector stores
- high-throughput indexing
- primary persistence responsibility

---

## 4.3 Human Access Devices

Primary devices:

- iPhone
- MacBook Pro
- home PC

Role:

> human interaction and capture layer.

Responsibilities:

- conversational capture
- Obsidian access
- workflow initiation
- review and reconciliation
- HITL approvals
- operational monitoring
- emergency runtime management

---

# 5. Runtime Service Topology

## 5.1 Core Runtime Services

Expected minimum service inventory:

| Service | Purpose |
|---|---|
| n8n | orchestration and workflow runtime |
| Obsidian vault | canonical memory |
| Docker | service isolation and deployment |
| Local APIs | workflow interfaces |
| Vector/index service | semantic retrieval |
| Secrets service | runtime credential access |
| Logging service | observability |
| Backup process | persistence protection |

---

## 5.2 Future Runtime Services

Potential future additions:

| Service | Purpose |
|---|---|
| Local model server | lightweight inference |
| Agent registry | capability management |
| Runtime policy engine | execution governance |
| Event bus | inter-agent messaging |
| Sensor aggregation service | environmental intelligence |
| Monitoring dashboard | operational visibility |
| Knowledge graph service | graph traversal and reasoning |

These should only be added when justified by operational need.

---

# 6. Persistence Topology

## 6.1 Canonical Memory

Canonical memory location:

> Obsidian vault.

Rules:

- markdown remains canonical
- vector indexes support retrieval only
- generated artifacts require provenance
- intake is not automatically trusted
- reconciliation determines promotion

Persistence expectations:

- local storage first
- backup required
- portable/recoverable
- vendor-independent where practical

---

## 6.2 Runtime Persistence

Persistent runtime data may include:

- n8n workflows
- workflow state
- runtime logs
- vector indexes
- metadata stores
- local databases
- audit history

Requirements:

- persistent Docker volumes
- documented backup paths
- restart survivability
- corruption recovery strategy

---

# 7. Network Topology

## 7.1 Baseline Network Position

The runtime assumes:

- home-network deployment initially
- local-first service access
- VPN for remote administration
- minimal public exposure

Preferred posture:

> services should not be publicly reachable unless intentionally exposed.

---

## 7.2 Network Zones

### Trusted Zone

Contains:

- primary runtime node
- canonical memory
- secrets services
- orchestration runtime

Characteristics:

- highest trust
- strongest persistence
- administrative access only

---

### Edge Zone

Contains:

- Raspberry Pi nodes
- sensors
- lightweight edge agents

Characteristics:

- lower trust than core runtime
- event-oriented
- restricted permissions

---

### Sandbox Zone

Contains:

- experimental services
- test agents
- temporary tooling
- security testing environments

Characteristics:

- isolated where possible
- disposable
- restricted persistence rights

---

### Cloud Burst Zone

Contains:

- OpenAI
- Azure-hosted AI
- hosted APIs
- frontier reasoning services

Characteristics:

- elastic capability
- external dependency
- policy-governed access
- audit-required interactions

---

# 8. Secrets Flow

Secrets must not be:

- stored in markdown
- committed to GitHub
- embedded in screenshots
- exposed in logs

Preferred flow:

```text
Workflow / Agent
        |
        v
Runtime Policy Gate
        |
        v
Secrets Runtime
        |
        v
Scoped Credential Delivery
```

Goals:

- scoped access
- least privilege
- auditability
- revocation capability
- local-first handling

---

# 9. Runtime Access Model

## Administrative Access

Preferred:

- SSH
- VPN-protected access
- headless administration

Avoid:

- direct internet exposure
- weak passwords
- shared admin accounts

---

## Human Approval Access

Used for:

- memory promotion
- runtime escalation
- cloud burst approval
- workflow overrides
- destructive actions

This reinforces:

> governed autonomy.

---

# 10. Observability Placement

Observability should exist at:

| Layer | Observability Need |
|---|---|
| Workflow Layer | success/failure tracking |
| Runtime Layer | service health |
| Policy Layer | routing and approval decisions |
| Memory Layer | promotion/reconciliation history |
| Agent Layer | execution traceability |
| Cloud Layer | token/cost visibility |

Minimum logging targets:

- workflow execution
- runtime failures
- cloud escalation events
- memory writes
- agent execution events
- backup success/failure

---

# 11. Backup and Recovery Topology

Critical backup targets:

- Obsidian vault
- n8n workflows
- runtime configuration
- secrets configuration metadata
- vector/index metadata
- infrastructure decision logs

Requirements:

- local backup
- recoverable restore path
- documented recovery process
- restart after power interruption

Portable runtime implications:

- runtime must tolerate transport
- storage corruption risk must be considered
- restart procedures should be documented

---

# 12. Portable Edge Runtime Direction

Long-term direction:

> portable AI edge runtime.

Potential implementation:

- compact half-rack
- Dell mini PC core runtime
- optional Raspberry Pi cluster
- active cooling
- integrated networking
- headless operation
- transport-safe mounting
- degraded/offline mode

The portable stack is:

- a deployment pattern
- not the architectural starting point.

The runtime must prove operationally useful before physical packaging is optimized.

---

# 13. Runtime Constraints

## Non-Negotiable Constraints

1. Obsidian remains canonical.
2. No unrestricted autonomous agents.
3. No uncontrolled public exposure.
4. No irreversible automation without HITL.
5. No infrastructure sprawl before ingestion stability.
6. No secrets in repo or markdown.
7. No dependency on a single cloud provider.
8. No runtime component without observability.
9. No service without documented ownership.
10. No scaling before operational justification.

---

# 14. Near-Term Topology Priorities

## Immediate Focus

Priority order:

1. stable ingestion loop
2. local Docker runtime
3. Obsidian persistence
4. secrets handling
5. backup/recovery
6. VPN access
7. lightweight observability

Avoid prematurely optimizing:

- clustering
- distributed agents
- large local inference
- complex service meshes
- high-availability infrastructure

---

# 15. Strategic Position

The PCA runtime topology represents:

> a sovereign cognitive runtime platform designed for governed memory, local orchestration, controlled automation, and resilient personal-scale AI execution.

The runtime philosophy is:

> local-first, observable, governed, portable when justified.
