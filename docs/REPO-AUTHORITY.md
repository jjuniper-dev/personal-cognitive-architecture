# Repository Authority Model

**Last revised:** 2026-05-30

---

## Repository Roles

| Repository | Role | Authority |
|---|---|---|
| `jjuniper-dev/personal-cognitive-architecture` | System architecture, schemas, agent design, governance model, use cases | Canonical design and schema authority |
| `jjuniper-dev/pca` | Running system: n8n workflows, PowerShell scripts, operational backlog, Docker deployment | Canonical implementation and operations authority |
| `jjuniper-dev/obsidian` | Obsidian vault: captures, notes, vault governance, reference mirrors | Canonical human-readable memory surface |

No repository supersedes another **within its domain**. Architecture decisions live here; how they are implemented lives in pca; how they are read by humans lives in obsidian.

---

## Backlog Authority

**Single source of truth for the active operational task list:** `jjuniper-dev/pca/BACKLOG.md`

Other backlog-related documents exist for different purposes:

| Document | Location | Purpose |
|---|---|---|
| `BACKLOG.md` | `jjuniper-dev/pca` | Active task list — status, priority, acceptance criteria, implementation notes |
| `PCA Backlog Operating Model Alignment.md` | `jjuniper-dev/obsidian/_System/` | Meta-document: authority model decisions, vault-specific backlog items (PCA-BL-011 to PCA-BL-015) |
| Use case profiles (UC-01 to UC-34) | `jjuniper-dev/personal-cognitive-architecture/` | Design-space use cases — requirements, not tasks |

**Rule:** When a use case from this repo needs implementation, a task is created in `pca/BACKLOG.md`. The use case doc is the *why*; the backlog item is the *what to do*.

---

## Schema Authority

**Canonical schemas:** `jjuniper-dev/personal-cognitive-architecture/schemas/`

| Schema file | Governs |
|---|---|
| `canonical-metadata.schema.json` | All PCA knowledge objects — the master contract |
| `ingest-capture.schema.json` | Capture event payloads |
| `validation-result.schema.json` | Validation gate outputs |
| `signal-score.schema.json` | WF02 scoring results |
| `cognitive-cost-model.schema.json` | Cost tracking |
| `workload-compatibility.schema.json` | Model routing decisions |
| `personal-os-profile.schema.json` | User profile and preferences |

**`pca/knowledge-schema.md` (pending, E1.2.1):** This markdown prose document predates the JSON schemas. When written, it should be a human-readable companion to the JSON schemas — not an independent definition. The JSON schemas are the machine-enforceable contracts.

**WF10 current behavior (E1.2.3, done 2026-05-30):** Validates `type` and `source` using inline Code node logic. This is a working partial implementation of `ingest-capture.schema.json`. Full validation against `canonical-metadata.schema.json` is a future step.

---

## AGENTS.md Disambiguation

Both `pca/AGENTS.md` and `personal-cognitive-architecture/AGENTS.md` exist. They serve different purposes and are not duplicates.

| File | Audience | Content |
|---|---|---|
| `pca/AGENTS.md` | Operator and code agents working in the running system | Team structure, work dispatch flow, escalation procedures, what each code agent can/cannot do, PR checklist format |
| `personal-cognitive-architecture/AGENTS.md` | LLM coding bots working in this design repo | Coding discipline, architectural layer rules, canonical naming (PCA vs Ayla), event backbone rules, pre-edit checklist |

Neither file replaces the other. Read both when working across repositories.

---

## Capture Implementation vs Design

| Component | Location | What it is |
|---|---|---|
| WF10 | `jjuniper-dev/pca` | **The real capture implementation** — POST /webhook/pca/incident, validates schema, writes Obsidian + Qdrant + Neo4j |
| `agents/capture-worker.md` | `jjuniper-dev/personal-cognitive-architecture` | Design specification for the capture worker role |
| `_System/agents/capture-agent.md` | `jjuniper-dev/obsidian` | Vault-level governance: what the capture agent may and may not write |

These are complementary, not conflicting. WF10 is the implementation; capture-worker.md is the design contract it should satisfy; capture-agent.md is the vault write policy it must comply with.

---

## Ayla: Design vs Implementation

| Component | Location | Stage |
|---|---|---|
| Ayla Orchestrator | `agents/agent-registry.md` in this repo | Design: Claude Sonnet-based, policy-gated, formal YAML spec |
| WF-Ayla | `pca/BACKLOG.md` (E-Ayla.1, dispatched to Codex) | Implementation: Local Ollama chat endpoint with WF12 memory injection |

WF-Ayla is the immediate implementation and intentional stepping stone — it proves the persona and memory injection pattern before the full orchestrator design is warranted. When WF-Ayla is live and stable, evaluate whether the Ayla Orchestrator design adds further value or whether the running system has superseded it.

---

## Reference Mirror Policy

`jjuniper-dev/obsidian/40_Reference/PCA/` contains mirrors of architecture documents from this repo. These are **reference copies, not canonical source**.

| Mirror file | Canonical source |
|---|---|
| `40_Reference/PCA/ARCHITECTURE.md` | `jjuniper-dev/personal-cognitive-architecture/docs/ARCHITECTURE.md` |
| `40_Reference/PCA/ARCHITECTURE_RECONCILIATION.md` | `jjuniper-dev/personal-cognitive-architecture/docs/ARCHITECTURE_RECONCILIATION.md` (not yet created) |
| `40_Reference/PCA/SPRINT_5_QUICKSTART.md` | Historical — no active canonical source |

No active sync mechanism exists. Mirror files will drift unless manually updated. Until a sync workflow is built:
- Treat obsidian mirror files as read-only snapshots
- Update the canonical source first; mirror update is discretionary
- Mirror files should carry `source_of_truth: false` frontmatter per `obsidian/_System/Vault Schema.md` rules

---

## personal-cognitive-architecture App Code

The `src/` directory and related app code in this repo are the **GitHub Vault Connector** (PR #23, deployed). This is a live utility — not placeholder code. The repo intentionally contains both design documentation and this deployed UI feature. The two coexist because the Vault Connector directly serves the architecture design role (connecting Obsidian vault to the PCA system).
