# Root Files Alignment Review — 2026-06-03

**Scope:** Root-level files in `jjuniper-dev/personal-cognitive-architecture` and `jjuniper-dev/pca`  
**Reviewed by:** Claude Code session, 2026-06-03  
**Branch:** `claude/root-files-alignment-review-AjD2Y`

How to use this file: on each review, create `docs/repo-audit/YYYY-MM-DD-<scope>.md`. `GROUNDING.md` in both repos now points here so agents load the latest review at session start without redoing the scan.

---

## Fixes applied in the review PR

| Repo | File | Issue | Action |
|------|------|-------|--------|
| personal-cognitive-architecture | `PR_DESCRIPTION.md` | PR body committed as a repo file | Deleted |
| personal-cognitive-architecture | `GROUNDING.md` | No pointer to review artifacts; CODEX.md missing from cross-repo section | Updated |
| pca | `claude-knowledge-base-schema.md` | Tool name embedded in PCA schema filename; violates naming rule and CLAUDE.md schema placement rule | Deleted |
| pca | `GROUNDING.md` | `CODEX.md` missing from required reading order | Updated (added at step 4) |
| pca | `BACKLOG.md` | No tracking entry for alignment findings | Added PCA-REPO-ALIGN-001 |

---

## personal-cognitive-architecture — Requires Decision

| File / Path | Issue | Decision needed |
|-------------|-------|-----------------|
| `_agents/` | Undocumented directory alongside canonical `agents/`; contains only `PAI-UC-AU-06-ayla/`; UC code `PAI-UC-AU-06` does not map to the README cluster scheme (UC 01–34, 8 clusters); underscore-prefix convention is not documented anywhere | Merge content into `agents/` or document the `_agents/` convention explicitly in GROUNDING.md |
| `pca/context/` | A directory named `pca/` inside `personal-cognitive-architecture/` creates a namespace collision with the sibling repo; contains only a `context/` subdirectory; not mentioned in GROUNDING.md; likely the Phase 2 context harness from PCA-WP-SESSION-HARNESS-001 placed here by Codex | Rename to `context/` at repo root, or add an explicit note to GROUNDING.md explaining the placement |
| `docs/ADHD_STATE_TRACKER_V2.md` | Personal health content in a public architecture repo | Move to Obsidian vault and delete from repo |
| `docs/ADM_Accountability_Framework.pptx` | Personal work file (binary) in a public architecture repo | Move to Obsidian vault and delete from repo |
| `docs/STATE_TRACKER_GUIDE.md` | Personal health content | Move to Obsidian vault and delete from repo |
| `docs/meeting-anxiety-management.md` | Personal health content | Move to Obsidian vault and delete from repo |
| `docs/SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md`, `docs/SPRINT_5_QUICKSTART.md`, `docs/SPRINT_5_VALIDATION_LAYER.md` | Sprint planning artifacts masquerading as permanent docs; create noise alongside canonical architecture docs | Move to `docs/archive/` or delete |
| `docs/ARCHITECTURE_RECONCILIATION.md` | Looks like a planning reconciliation doc rather than canonical architecture | Audit and archive or delete |
| `package.json`, `package-lock.json`, `vite.config.js`, `index.html` | Web app build configuration in the architecture/design repo; per REPO-AUTHORITY this repo should own schemas, agent contracts, and architecture docs — not a running application | Decide if this repo is the intended home for the dashboard UI; if not, move to `pca` or a dedicated repo |
| `src/` directory | Likely holds dashboard implementation code — same authority boundary issue as the build files above | Same decision as above |
| `outputs/`, `prompts/`, `tests/`, `knowledge/` | All empty placeholder directories (`.gitkeep` only; all share the same git tree SHA); aspirational structure with no content | Populate or remove |
| `agents/*-impl.py` files | Executable Python implementation files in the architecture repo; REPO-AUTHORITY states this repo owns contracts and specs, not running code | Confirm whether this is intentional or whether the implementations should move to `pca` |

---

## pca — Requires Decision

| File / Path | Issue | Decision needed |
|-------------|-------|-----------------|
| `wf04_v2.json` – `wf04_v6.json` (5 files), `wf04_entity_neo4j.json`, `wf02_current.json`, `wf05_obsidian_neo4j.json`, `wf09_inspect.json` | Versioned and debug workflow JSON files in root; `wf0*.json` is already in `.gitignore` but these files are tracked (committed before the ignore rule was added) | Confirm which version is current; run `git rm --cached wf04_v*.json wf02_current.json wf05_obsidian_neo4j.json wf09_inspect.json` and delete stale copies |
| `vault_embed_state.json` | Explicitly listed in `.gitignore` but is a tracked committed file (committed before the ignore line was added); will continue to appear in git history | Run `git rm --cached vault_embed_state.json` to untrack; the file remains on disk |
| `budget.json` | Purpose unclear; potentially regenerable operational state | Clarify purpose; if regenerable, add to `.gitignore` and untrack |
| `knowledge-schema.md` (root) vs `docs/KNOWLEDGE_SCHEMA.md` | Two schema companion documents in one repo; CLAUDE.md says only one human-readable companion is permitted; neither is machine-readable (that authority lives in `personal-cognitive-architecture/schemas/`) | Decide which is the companion doc, delete the other; cross-check content against `personal-cognitive-architecture/docs/KNOWLEDGE_SCHEMA.md` |
| `data-classification.md` | Deliverable for BACKLOG E5.1.1 (status `pending`), but the file already exists in root; suggests partial completion: doc created but WF10 classification-routing integration not yet done | Update E5.1.1 BACKLOG status to clarify: doc complete, WF10 integration is the remaining acceptance criterion |
| `restart_n8n_v3.ps1`, `restart_n8n_v4.ps1`, `restart_final.ps1`, `restart_ollama.ps1`, `restart_ollama_clean.ps1` | Five restart variants in root; only one canonical version is needed | Identify current canonical restart script; delete the rest |
| `install_ollama.ps1`, `install_ollama2.ps1` | Two versions of the same install script | Delete stale version |
| `find_emdash.ps1`, `find_emdash2.ps1`, `docker_check2.ps1`, `ping_test.ps1`, `hexdump.ps1`, `read_test_file.ps1`, `timing_test.ps1` | One-off diagnostic and debug scripts that were never cleaned up | Delete or move to `scripts/diagnostics/` |
| `test_payload.json` | Test fixture in root | Move to `tests/` |
| `branch-reconciliation.md` | Temporary planning document in root | Resolve and delete, or move to `docs/` |

---

## Cross-repo status

| Item | Status |
|------|--------|
| `personal-cognitive-architecture/docs/REPO-AUTHORITY.md` — cited in both GROUNDING files; file exists | OK |
| `personal-cognitive-architecture/docs/ARCHITECTURE.md` — cited in GROUNDING; file exists | OK |
| `pca/docs/ARCHITECTURE-ALIGNMENT.md` — cited in pca GROUNDING; file exists | OK |
| `pca/BACKLOG.md` is the sole backlog authority; no shadow backlog in `personal-cognitive-architecture` | OK |
| `agents/agent-registry.md` exists in `personal-cognitive-architecture/agents/` | OK |
| README sprint badge in `personal-cognitive-architecture` shows "Sprint 5" — likely stale | Low priority; update when sprint state changes |
