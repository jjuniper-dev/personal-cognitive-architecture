# ChatGPT → Claude Handoff Log

Date: 2026-05-28

Purpose: preserve the repo/reconciliation context from the ChatGPT session so Claude or another LLM code bot can continue without rediscovering the same state.

---

## Summary

The PCA project is currently split across two GitHub repositories and multiple branches. The key issue is not missing ideas; it is distributed source-of-truth.

The working interpretation established in this session is:

```text
jjuniper-dev/personal-cognitive-architecture
= architecture, planning, design decisions, epics/use cases, branch reconciliation, bot instructions

jjuniper-dev/pca
= private local runtime implementation: Docker, n8n, Qdrant, Neo4j, Vault, Ollama/Whisper, dashboards, runbooks
```

Claude should treat these as a paired system:

```text
Architecture repo defines.
Runtime repo implements.
```

Do not treat the repos as competing PCA truths.

---

## Repositories Inspected

### 1. `jjuniper-dev/personal-cognitive-architecture`

Visibility: public  
Default branch: `main`  
Observed role: architecture/docs/planning repo with many design and experiment branches.

Files added during this session:

- `CLAUDE.md`
- `AGENTS.md`

Purpose of added files:

- provide Claude/code-bot operating rules
- adapt the `andrej-karpathy-skills` discipline to PCA
- enforce PCA/Ayla naming discipline
- require small, inspectable changes
- define architecture-aware bot behaviour
- prevent autonomous drift and hidden state mutation

Important existing `main` README signal:

- PCA described as a cognitive operating system
- stack includes n8n, Neo4j, Obsidian, Tailscale, Claude Sonnet/Haiku, OpenClaw, Whisper
- 34 use cases across 8 clusters
- critical path listed as:
  1. iOS capture pipeline
  2. UC-07 Zapier → n8n migration
  3. UC-16 bank connectivity decision
  4. UC-01 stable
  5. UC-06 Ayla routing layer

### 2. `jjuniper-dev/pca`

Visibility: private  
Default branch: `master`  
Observed role: local runtime implementation repo.

Observed `docker-compose.yml` services:

- `n8n`
- `faster-whisper`
- `qdrant`
- `neo4j`
- `rss-bridge`
- `vault`
- `dashboard`
- `homepage`
- `syncthing`

Important runtime finding:

- `docker-compose.yml` contains hardcoded Neo4j credential:

```yaml
NEO4J_AUTH=neo4j/pca-neo4j-2026
```

Recommended fix:

```yaml
NEO4J_AUTH=${NEO4J_AUTH}
VAULT_TOKEN=${VAULT_TOKEN}
```

and add `.env.example` with placeholder values.

---

## Branches Inspected in `personal-cognitive-architecture`

The user supplied visible branch names by screenshot. The following branches were inspected using GitHub compare/fetch operations.

### High-value architecture branches to extract into `main`

#### `claude/browse-repo-mI0AZ`

Status vs `main`: diverged, +13 commits, -117 behind.

Unique/high-value files include:

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

Recommendation: extract architecture documents into canonical `main`. Do not blindly merge branch because it is far behind.

#### `claude/phase-1-specification`

Status vs `main`: diverged, +2 commits, -163 behind.

Unique/high-value files:

- `docs/pca-ddv-disagreement-driven-validation.md`
- `docs/pca-phase-1-note-classification-arbitration.md`

Additional README observed on this branch framed Phase 1 as:

```text
n8n → Obsidian → structured note in vault
```

Phase 1 constraints observed:

- no new infrastructure before ingestion loop works
- no workers before orchestrator defined
- no indexing before memory is clean
- priority is memory and plumbing first

Recommendation: extract Phase 1 discipline and validation docs into `main`.

#### `claude/cre-agentic-logic`

Status vs `main`: diverged, +3 commits, -164 behind.

Unique/high-value files:

- modified `docs/pca-cognitive-reconciliation-engine.md`
- added `docs/pca-cre-agentic-screening-logic.md`
- added `docs/pca-phase-1-note-classification-arbitration.md`

Recommendation: extract CRE logic into architecture docs, but normalize terminology. Avoid making everything an “agent.”

#### `feat/architectural-review-brief`

Status vs `main`: diverged, +1 commit, -116 behind.

Unique file:

- `docs/ARCHITECTURAL_REVIEW_REQUEST_FOR_OPUS.md`

Recommendation: extract. Low merge risk.

#### `claude/shortcut-build-instructions-W9SvT`

Status vs `main`: diverged, +2 commits, -132 behind.

Unique file:

- `docs/ios-shortcut-build-guide.md`

Recommendation: extract into canonical capture/iOS docs.

---

### Integration branch requiring careful review

#### `feat/github-vault-connector`

Status vs `main`: diverged, +7 commits, -11 behind.

Files:

- `PR_DESCRIPTION.md`
- `docs/GITHUB_VAULT_INTEGRATION.md`
- modified `package.json`
- `src/ui-dashboard/server/_core/trpc.ts`
- `src/ui-dashboard/server/github-connector.test.ts`
- `src/ui-dashboard/server/github-connector.ts`
- `src/ui-dashboard/server/vault-router.ts`

Recommendation: high-value but security-sensitive. Review before merge.

Questions to resolve:

- Is `vaultRouter` imported into the app/server root router?
- Does the dashboard runtime already support tRPC transport?
- Is exposing vault content through `publicProcedure` acceptable?
- How are GitHub tokens/secrets handled?
- Does the connector respect canonical memory boundaries?

---

### Prototype / later capability branches

#### `claude/personal-profile-graph-WakXd`

Status vs `main`: diverged, +10 commits, -133 behind.

Large prototype branch containing:

- React/Vite app
- Neo4j config/scripts
- Markov cognitive states
- ADHD tracker dashboards/docs
- profile graph data
- multiple UI components

Recommendation: do not merge directly. Quarantine as prototype or future capability. Extract concepts selectively after PCA V1 loop is stable.

#### `claude/setup-weak-signal-finder-OZ2OH`

Status vs `main`: diverged, +1 commit, -133 behind.

Files:

- `agents/weak-signal-worker-requirements.txt`
- `agents/weak-signal-worker.md`
- `agents/weak-signal-worker.py`
- `docs/WEAK_SIGNAL_FINDER_SETUP.md`
- `docs/weak-signal-finder-integration.md`
- `docs/weak-signal-finder-quickstart.md`
- `workflows/n8n/weak-signal-polling.json`

Recommendation: useful later capability, but not MVP-core. Quarantine as future capability/prototype until Capture → Validate → Store → Retrieve → Act → Audit loop is stable.

#### `stabilize-profile-app-after-pr14-16`

Status vs `main`: diverged, +6 commits, -130 behind.

Contains aggressive deletions/reductions to profile app files and docs.

Recommendation: inspect carefully. Possible cleanup branch for profile prototype, but destructive. Do not merge blindly.

---

### Cleanup / candidate cherry-pick

#### `fix/stabilization-clean`

Status vs `main`: diverged, +1 commit, -130 behind.

Files changed:

- `README.md`
- `docs/ios-shortcut-build-guide.md`
- `scripts/populate-graph.js`
- `scripts/populate-markov-states.js`
- `src/components/SchemaOutput.jsx`
- `src/markov/StateTracker.js`

Recommendation: candidate cherry-pick only after verifying current relevance. Do not merge whole branch.

---

### Separate artifact / not PCA-core

#### `claude/adm-ai-accountability-mfOkU`

Status vs `main`: diverged, +1 commit, -129 behind.

File:

- `docs/ADM_Accountability_Framework.pptx`

Recommendation: likely work-product artifact. Keep separate unless the architecture repo is intentionally storing presentation outputs.

---

### Likely stale / archive candidate

#### `claude/personal-os-system-spec-vV3Wu`

Status vs `main`: behind, +0 commits, -136 behind.

Recommendation: likely stale, merged, or superseded. Archive candidate.

---

## Decisions Established in Session

### Repo role decision

`personal-cognitive-architecture` should be the canonical architecture and planning repo.

`pca` should be the canonical local runtime repo.

### Branch decision

Do not merge old branches wholesale.

Use:

```text
inspect → extract → normalize → PR → review → merge
```

### MVP decision

PCA V1 should be one complete loop:

```text
Capture → Validate → Store → Retrieve → Act → Audit
```

A concrete V1 form:

```text
iOS/manual capture
→ n8n intake
→ metadata validation
→ Obsidian canonical note
→ optional graph/vector indexing
→ retrieval by assistant/workflow
→ summary/action output
→ audit/log entry
```

Out of scope until V1 loop is stable:

- finance automation
- weak signal finder
- profile graph app
- ADHD/Markov cognitive model
- full autonomous agents
- multi-modal publishing system

### Naming decision

Use **PCA** for architecture, runtime, infrastructure, schemas, event backbone, governance, vault, graph, and inspection.

Use **Ayla** only for assistant/persona/interface layer.

Rule:

```text
If the component would still exist after renaming the assistant, call it PCA.
```

---

## Recommended Next Steps for Claude

### Step 1 — Create canonical repo map

In `jjuniper-dev/personal-cognitive-architecture`, create:

```text
docs/repo-map/pca-repository-map.md
```

Include:

- two-repo split
- source-of-truth responsibilities
- architecture-to-runtime traceability
- what each repo should not own

### Step 2 — Create branch reconciliation doc

In `jjuniper-dev/personal-cognitive-architecture`, create:

```text
docs/repo-audit/branch-reconciliation.md
```

Use the branch findings in this handoff log.

### Step 3 — Create PCA V1 delivery map

In `jjuniper-dev/personal-cognitive-architecture`, create:

```text
docs/delivery/pca-v1-delivery-map.md
docs/delivery/mvp-definition.md
```

Use the V1 loop:

```text
Capture → Validate → Store → Retrieve → Act → Audit
```

### Step 4 — Bootstrap runtime repo docs

In `jjuniper-dev/pca`, create:

```text
README.md
AGENTS.md
.env.example
docs/runbooks/local-startup.md
docs/runbooks/health-checks.md
docs/runbooks/secrets-and-vault.md
docs/runtime/runtime-component-map.md
```

### Step 5 — Secrets hygiene PR

In `jjuniper-dev/pca`, externalize hardcoded credentials from `docker-compose.yml`.

Known issue:

```yaml
NEO4J_AUTH=neo4j/pca-neo4j-2026
```

Recommended replacement:

```yaml
NEO4J_AUTH=${NEO4J_AUTH}
```

Do not commit real `.env` values.

---

## Claude Operating Guidance

Claude should operate in two modes.

### Architecture repo mode

Optimize for:

- clarity
- canonical docs
- branch reconciliation
- epic/use-case mapping
- decision records
- naming discipline
- bot handoff

Do not casually add runtime code here.

### Runtime repo mode

Optimize for:

- Docker/runtime stability
- secrets hygiene
- runbooks
- workflow exports
- service health checks
- local-first operation

Do not invent architecture here.

### Shared rule

If architecture and runtime disagree, do not silently choose. Raise the mismatch and propose reconciliation.

---

## Open Questions

1. Where is the authoritative six-epic / 44-story backlog?
2. Should `ADM_Accountability_Framework.pptx` live in PCA architecture repo or a separate work-output repo?
3. Should profile graph / ADHD / Markov model become a future capability or remain outside PCA V1?
4. Should weak signal finder be represented as future capability track rather than active MVP work?
5. Should the architecture docs from `claude/browse-repo-mI0AZ` be extracted as-is or normalized into a smaller canonical set?
6. Should `pca` eventually use `main` instead of `master`, or leave default branch unchanged for now?

---

## Immediate Principle

For the next cleanup cycle:

```text
No new capability work until repo roles, runtime hygiene, branch reconciliation, and PCA V1 definition are canonical.
```

This is a control-plane cleanup step, not a feature sprint.
