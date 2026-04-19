---
type: project
created: 2026-04-19
updated: 2026-04-19
tags: [pca, build, direction]
status: active
---

# PCA Intent and Build Direction

## Current build intent

The current objective is not to complete the full PCA.

The current objective is to prove the first operational loop:

n8n → Obsidian → structured note in the vault

## Why this comes first

The PCA depends on a working foundation before higher-order capabilities make sense.

Without reliable ingestion into canonical memory:

- validation has nowhere durable to land
- reconciliation has nothing trustworthy to act on
- orchestration becomes speculative
- outputs become disconnected from source structure

The memory and plumbing layer must exist before reasoning and indexing layers are added.

## Current phase

### Phase 1 — Cloud jumpstart / low-friction bootstrap

Focus:

- simple tooling
- low setup friction
- visible results
- fast iteration
- minimal operational overhead

### Phase 2 — Self-hosted migration

Focus:

- local inference
- self-hosted services
- semantic indexing
- structured session support
- observability

## Immediate implementation target

- Obsidian vault operational
- VS Code workspace operational
- n8n in Docker operational
- one metadata-compliant note written automatically into `/00 Inbox`

## Now

- build ingestion workflow
- verify metadata integrity

## Next

- webhook capture
- validation schema
- Ayla identity

## Later

- indexing
- local inference

## Current mantra

Build the memory and plumbing layer first.
