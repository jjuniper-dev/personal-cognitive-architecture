---
type: project
created: 2026-04-19
updated: 2026-04-19
tags: [pca, readiness, assessment]
status: active
---

# PCA Readiness Assessment

## Purpose

Tracks current state vs intended architecture and identifies critical path.

## State vs intent

| Domain | Intended | Current | Gap |
|---|---|---|---|
| Capture | Multi-source ingestion | Partial | Routing not stable |
| Validation | Scored and routed | Inbox only | No schema yet |
| Knowledge Store | Structured Obsidian | Defined | Not fully operational |
| Index | ChromaDB | Planned | Deferred |
| Orchestration | n8n + Ayla | Partial | Ayla not complete |
| Workers | Task agents | Defined | Not implemented |
| Output | Structured artifacts | Ad hoc | Not templated |
| Observability | Full stack | Planned | Not wired |

## Critical path

n8n → Obsidian → structured note

## Immediate goal

Prove ingestion loop with metadata intact.

## Risks

- premature complexity
- memory drift
- governance gaps

## Recommendation

Do not expand stack until ingestion is stable.
