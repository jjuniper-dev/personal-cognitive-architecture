# Branch Reconciliation

Status: working draft  
Created: 2026-05-28  
Purpose: identify useful work distributed across branches and define how it should be reconciled into the canonical PCA architecture/runtime direction.

---

## Operating Rule

Do not merge old branches wholesale.

Use:

```text
inspect → extract → normalize → PR → review → merge
```

Reason:

Many branches are significantly behind `main`. Valuable architecture and prototype work exists, but broad merges would also reintroduce stale assumptions and drift.

---

## Branch Classes

| Class | Meaning |
|---|---|
| Extract | Pull useful docs/concepts into canonical `main` through small PRs |
| Review | Requires targeted technical/security review before merge |
| Prototype | Preserve as experiment/future capability; do not merge into PCA V1 |
| Cherry-pick | Selective commit/file extraction only |
| Archive | Likely stale, superseded, or merged elsewhere |
| Separate Artifact | Valuable output but not core PCA architecture/runtime |

---

# Branch Inventory

## Extract

### `claude/browse-repo-mI0AZ`

Status vs `main`:

- ahead: +13 commits
- behind: -117 commits

Observed value:

High-value architecture documents.

Important files:

- `docs/ARCHITECTURAL_REVIEW_REQUEST_FOR_OPUS.md`
- `docs/ARCHITECTURE.md`
- `docs/ARCHITECTURE_RECONCILIATION.md`
- `docs/SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md`
- `docs/SPRINT_5_VALIDATION_LAYER.md`
- `docs/TECHNOLOGY_STACK.md`
- `docs/agent-runtime-model.md`
- `docs/homelab-reference-architecture.md`
- `docs/observability-and-audit.md`
- `docs/pca-cognitive-control-plane.md`
- `docs/runtime-policy-gate.md`
- `docs/runtime-topology.md`

Recommended action:

- extract architecture docs into `main`
- normalize naming to PCA/Ayla rules
- reduce duplication where overlapping docs exist
- preserve reasoning, not necessarily exact structure

Priority: HIGH

---

### `claude/phase-1-specification`

Status vs `main`:

- ahead: +2 commits
- behind: -163 commits

Observed value:

Strong Phase 1 discipline and validation concepts.

Important files:

- `docs/pca-ddv-disagreement-driven-validation.md`
- `docs/pca-phase-1-note-classification-arbitration.md`

Important conceptual signal:

```text
n8n → Obsidian → structured note in vault
```

Observed constraints:

- no new infrastructure before ingestion loop works
- no workers before orchestrator defined
- no indexing before memory is clean
- memory and plumbing first

Recommended action:

- extract validation/arbitration concepts
- preserve Phase 1 simplicity discipline
- use as grounding for PCA V1 definition

Priority: HIGH

---

### `claude/cre-agentic-logic`

Status vs `main`:

- ahead: +3 commits
- behind: -164 commits

Observed value:

Cognitive Reconciliation Engine (CRE) thinking.

Important files:

- `docs/pca-cognitive-reconciliation-engine.md`
- `docs/pca-cre-agentic-screening-logic.md`
- `docs/pca-phase-1-note-classification-arbitration.md`

Recommended action:

- extract CRE logic into architecture docs
- normalize terminology
- avoid overusing “agent” terminology where workflow/worker is more accurate

Priority: HIGH

---

### `feat/architectural-review-brief`

Status vs `main`:

- ahead: +1 commit
- behind: -116 commits

Observed value:

Architecture review framing artifact.

Important file:

- `docs/ARCHITECTURAL_REVIEW_REQUEST_FOR_OPUS.md`

Recommended action:

- extract into canonical review/governance docs

Priority: MEDIUM

---

### `claude/shortcut-build-instructions-W9SvT`

Status vs `main`:

- ahead: +2 commits
- behind: -132 commits

Observed value:

Practical iOS capture guidance.

Important file:

- `docs/ios-shortcut-build-guide.md`

Recommended action:

- extract into canonical capture docs
- align with PCA V1 capture loop

Priority: MEDIUM

---

## Review

### `feat/github-vault-connector`

Status vs `main`:

- ahead: +7 commits
- behind: -11 commits

Observed value:

Potentially important GitHub/vault integration.

Important files:

- `docs/GITHUB_VAULT_INTEGRATION.md`
- `src/ui-dashboard/server/github-connector.ts`
- `src/ui-dashboard/server/vault-router.ts`
- `src/ui-dashboard/server/_core/trpc.ts`

Questions requiring review:

- Is `vaultRouter` actually wired into root routing?
- Does runtime already support tRPC transport?
- Is `publicProcedure` exposure acceptable?
- How are GitHub tokens/secrets managed?
- Does connector respect canonical memory boundaries?

Recommended action:

- targeted technical/security review before merge
- do not merge automatically

Priority: HIGH

---

## Prototype

### `claude/personal-profile-graph-WakXd`

Status vs `main`:

- ahead: +10 commits
- behind: -133 commits

Observed value:

Large personal-profile/graph prototype.

Includes:

- React/Vite app
- Neo4j configuration/scripts
- profile graph concepts
- Markov cognitive states
- ADHD tracker components/docs

Recommended action:

- quarantine as prototype/future capability
- extract concepts only after PCA V1 stabilizes
- avoid merging into core architecture/runtime prematurely

Priority: LOW for V1

---

### `claude/setup-weak-signal-finder-OZ2OH`

Status vs `main`:

- ahead: +1 commit
- behind: -133 commits

Observed value:

Weak-signal discovery capability.

Includes:

- weak-signal worker
- n8n polling workflow
- RSS/weak-signal docs

Recommended action:

- preserve as future capability track
- not part of PCA V1 core loop

Priority: LOW for V1

---

### `stabilize-profile-app-after-pr14-16`

Status vs `main`:

- ahead: +6 commits
- behind: -130 commits

Observed value:

Profile-app cleanup/reduction branch.

Risk:

Contains aggressive deletions/reductions.

Recommended action:

- inspect before touching
- do not merge automatically

Priority: LOW

---

## Cherry-pick

### `fix/stabilization-clean`

Status vs `main`:

- ahead: +1 commit
- behind: -130 commits

Observed value:

Small stabilization/cleanup changes.

Files:

- `README.md`
- `docs/ios-shortcut-build-guide.md`
- graph scripts
- UI cleanup files

Recommended action:

- selective cherry-pick only after validating relevance

Priority: MEDIUM

---

## Separate Artifact

### `claude/adm-ai-accountability-mfOkU`

Status vs `main`:

- ahead: +1 commit
- behind: -129 commits

Observed value:

Presentation artifact:

- `docs/ADM_Accountability_Framework.pptx`

Recommended action:

- keep separate unless repo intentionally stores presentation outputs

Priority: N/A

---

## Archive Candidate

### `claude/personal-os-system-spec-vV3Wu`

Status vs `main`:

- ahead: +0 commits
- behind: -136 commits

Observed value:

No observed unique value relative to `main`.

Recommended action:

- likely archive candidate
- confirm no hidden work before deletion

Priority: LOW

---

# Current Strategic Interpretation

The PCA project is not missing capability.

The primary issue is distributed source-of-truth across:

- branches
- repos
- experiments
- runtime state
- architecture drafts

The current cleanup priority is:

```text
recover good thinking → normalize it → make canonical docs stable
```

Not:

```text
add more capabilities
```

---

# Canonicalization Targets

The following should become canonical in `main`:

- repo map
- branch reconciliation
- PCA V1 definition
- event/backbone direction
- runtime topology
- runtime policy gate
- observability/audit model
- agent/runtime model
- technology stack
- capture pipeline guidance
- disagreement-driven validation concepts
- CRE logic

---

# Immediate Rule

Until reconciliation is complete:

```text
No broad merges.
No destructive cleanup.
No new major capability tracks.
```

Small additive documentation and stabilization work is preferred.
