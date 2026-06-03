# PCA Grounding — Required Reading Order for Agents

Before touching any file in this repo, read in this order.

## For work in personal-cognitive-architecture (this repo)

1. `README.md` — project overview, design philosophy
2. `AGENTS.md` — coding discipline, PCA vs Ayla naming, primitive chain, layer model
3. `CLAUDE.md` — Claude Code discipline adapted to PCA
4. `docs/REPO-AUTHORITY.md` — what this repo owns vs what `pca` owns
5. `docs/ARCHITECTURE.md` — canonical 5-layer design model + 9-layer functional decomposition
6. Relevant `schemas/`, `agents/`, or `docs/uc-profiles/` for the task
7. `docs/repo-audit/` — latest root alignment review (check the newest file before making structural changes to either repo)

## For cross-repo work

See `pca/GROUNDING.md` — the operational repo is the execution entry point.
Active task queue lives in `pca/BACKLOG.md`.

For cross-repo work involving Codex agents, also read `pca/CODEX.md`.

## Naming rule

- **PCA** — architecture, runtime, infrastructure, everything that would exist if you renamed the assistant
- **Ayla** — user-facing assistant persona and interface only

## Layer model

| Layer | Meaning |
|---|---|
| L1 | Knowledge & Control |
| L2 | Agent Runtime |
| L3 | Workflow & Integration |
| L4 | Infrastructure |
| L5 | AI Models |

## Schema authority

This repo (`personal-cognitive-architecture/schemas/`) is the **machine-readable schema authority** for all PCA knowledge objects, capture events, and agent contracts.
