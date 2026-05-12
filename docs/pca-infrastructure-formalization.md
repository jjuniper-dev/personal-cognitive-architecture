# PCA Infrastructure Formalization

## Purpose

The PCA is evolving from a knowledge and reasoning architecture into a sovereign personal cognitive platform with a local runtime, governed automation, durable persistence, and optional cloud augmentation.

This document formalizes the infrastructure direction:

> Modeled after enterprise architecture, but compressed into a personal-scale, portable, self-governed edge stack.

The goal is not infrastructure for its own sake. The infrastructure exists to support:

- durable memory
- local orchestration
- secure execution
- governed automation
- observability
- resilience
- selective cloud augmentation

## Core Principle

> Build memory and plumbing first; scale infrastructure only when the operational loop demands it.

Primary operational loop:

```text
Voice / Chat / File / Web Input
→ n8n Workflow
→ Structured Markdown
→ Obsidian Inbox
→ Metadata Validation
→ Human Review
```

## Infrastructure Layers

| Layer | Role |
|---|---|
| Device Access Layer | Capture and interaction |
| Orchestration Layer | Workflow automation |
| Cognitive Runtime Layer | Agent execution and reasoning |
| Knowledge Persistence Layer | Canonical memory |
| Secure Operations Layer | VPN, secrets, monitoring |
| Cloud Burst Layer | Frontier reasoning and hosted inference |

## Runtime Direction

### Primary Compute

Preferred:

- Dell Mini PC / OptiPlex Micro

Responsibilities:

- Docker runtime
- n8n
- local APIs
- vector/index services
- observability
- secrets management
- lightweight local inference

### Edge Nodes

Preferred:

- Raspberry Pi 5 nodes

Responsibilities:

- sensors
- lightweight automation
- event triggers
- home monitoring
- edge capture

Avoid using Raspberry Pi as the primary orchestration runtime.

## Security Position

Minimum security posture:

- VPN-first remote access
- avoid exposed ports where possible
- no secrets in GitHub or markdown
- separate admin and runtime credentials
- logging for automation activity
- isolated testing where practical

## Secrets Management

Requirements:

- secrets separated from notes/code
- scoped credentials
- rotation capability
- local-first preference
- documented dependencies

Candidate approaches:

- environment variables
- Docker secrets
- local vault
- Azure Key Vault

## Observability Requirements

Minimum:

- workflow execution logs
- failed run visibility
- note creation audit trail
- backup/recovery documentation

Future:

- agent execution logs
- model routing logs
- reconciliation event history
- token/cost telemetry
- policy gate audit records

## Local vs Cloud

| Workload | Preferred Location |
|---|---|
| Canonical memory | Local |
| Workflow orchestration | Local-first |
| Sensitive capture | Local where possible |
| Frontier reasoning | Cloud burst |
| Large multimodal synthesis | Cloud burst |

## Runtime Guardrails

1. No uncontrolled public exposure.
2. No service without ownership and shutdown path.
3. No cloud dependency without fallback understanding.
4. No irreversible automation without HITL approval.
5. No unrestricted agents.
6. No secrets in markdown or repo.
7. No infrastructure scaling before ingestion loop stability.

## Phased Infrastructure Roadmap

### Phase 1 — Minimal Runtime Foundation

Focus:

- Obsidian
- n8n
- structured ingestion
- metadata validation
- manual review

### Phase 1.5 — Local Runtime Stabilization

Focus:

- Docker persistence
- backups
- logging
- local access control
- initial secrets handling

### Phase 2 — Sovereign Edge Runtime

Focus:

- Dell mini PC runtime
- VPN
- observability
- local retrieval/indexing
- optional Pi edge nodes

### Phase 3 — Portable Edge Stack

Focus:

- transportable runtime
- cooling/networking integration
- degraded/offline operation
- headless management

### Phase 4 — Governed Agent Runtime

Focus:

- runtime policy gate
- agent permissions
- approval thresholds
- execution audit logs
- local/cloud routing

## Reference Runtime Pattern

```text
[Human Devices]
        |
        v
[Capture + Access Layer]
        |
        v
[Local Orchestration Layer]
        |
        v
[Runtime Policy Boundary]
        |
   +----+----+
   |         |
   v         v
[Knowledge] [Cloud Burst]
   |
   v
[Review + Reconciliation]
   |
   v
[Trusted Memory + Action]
```

## Strategic Position

The PCA infrastructure direction is:

> minimal first, local-first, governed always, portable later.
