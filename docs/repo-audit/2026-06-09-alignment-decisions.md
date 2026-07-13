# Repo Alignment Decisions — 2026-06-09

**Scope:** Judgment calls deferred from the 2026-06-03 root alignment review  
**Decided by:** Owner session, 2026-06-09  
**Issues:** Align.0 (#49), Align.1 (#50)  

---

## Align.0 — Undocumented directories and placeholder structure (#49)

| Item | Decision |
|---|---|
| `_agents/PAI-UC-AU-06-ayla/` | Merge into `agents/`; delete `_agents/` wrapper; update agent registry |
| `pca/context/` | Rename to `context/` at repo root; delete `pca/` wrapper; update GROUNDING.md |
| `tests/` (empty placeholder) | Delete — test artefacts belong in the implementation repo (`pca`) |
| `outputs/`, `prompts/`, `knowledge/` (empty) | Keep — map to the canonical PCA primitive flow; will be populated |
| Personal health docs (`ADHD_STATE_TRACKER_V2.md`, `STATE_TRACKER_GUIDE.md`, `meeting-anxiety-management.md`, `ADM_Accountability_Framework.pptx`) | Delete from repo immediately; move to Obsidian vault; tracked as risk R1 in `docs/security-posture.md` |
| Sprint planning docs (`SPRINT_5_*.md`) | Move to `docs/archive/`; not canonical architecture docs |

---

## Align.1 — Web app build files and src/ (#50)

| Item | Decision |
|---|---|
| `src/` (React/Vite dashboard, `personal-profile-quiz`) | Remove from this repo; copy to `jjuniper-dev/pca` or dedicated dashboard repo before deletion |
| `package.json`, `package-lock.json`, `vite.config.js`, `index.html` | Remove from this repo after web app is relocated |
| `agents/*-impl.py` (implementation files) | Move to `jjuniper-dev/pca/agents/`; agent contracts (`*.md`) remain here |
| `agents/agents-requirements.txt`, `agents/agents-deployment.md` | Move to `pca` repo with the implementations |

**Rationale:** `docs/REPO-AUTHORITY.md` defines this repo's authority as architecture, schemas, agent design, and governance. Running code belongs in `jjuniper-dev/pca`. The web app and Python implementations violate that boundary.

**Prerequisite before deletion:** Confirm all code is present in the destination repo. Do not delete from here until destination is verified.

---

## Sequencing

Execute Align.0 before Align.1. Align.0 items are all in-repo moves and deletes with no external dependency. Align.1 requires coordination with `jjuniper-dev/pca` (copy-then-delete pattern).

Personal health file deletion (R1) should happen immediately as a standalone action — it does not depend on sequencing with other align items.
