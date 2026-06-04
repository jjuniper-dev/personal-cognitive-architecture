# Work Routing & Evaluation Protocol

**Version**: 1.0  
**Created**: 2026-06-04  
**Owner**: PCA Orchestrator  
**Layer**: L2 Agent Runtime + L3 Workflow & Integration

---

## Purpose

Defines the complete loop for delegating bounded work to a bot, evaluating its output against explicit success criteria, and delivering an executive digest to the product owner for the Monday strategy session.

---

## The Loop

```
Product Owner
    |
    | 1. Fill out work package (templates/work-package.json)
    |
    v
Bot Assignment
    |
    | 2. Route work package to assigned bot (Claude Code, WF09, Codex)
    | 3. Bot executes, records output
    |
    v
POST /webhook/pca/eval
    |  { work_package: {...}, bot_output: {...} }
    |
    v
Work Routing Evaluator (Claude Opus 4.8)
    |
    | 4. Maps each success criterion -> PASS / PARTIAL / FAIL
    | 5. Makes GO / NEEDS-REVISION / NO-GO decision
    | 6. Writes eval note to Obsidian /PCA/Evals/
    | 7. Posts to WF10 (knowledge capture)
    | 8. Sends ntfy notification (if NTFY_URL configured)
    |
    v
Weekly Aggregation (Monday 08:00)
    |
    | 9. WF-MondayDigest scans /PCA/Evals/ (past 7 days)
    | 10. Synthesizes exec digest via Claude Opus 4.8
    | 11. Writes /PCA/Digests/{date}-monday-digest.md
    | 12. Sends ntfy + posts to WF10
    |
    v
Product Owner - Monday Strategy Session
```

---

## Work Package Fields

| Field | Required | Description |
|-------|----------|-------------|
| `work_package_id` | Yes | Unique ID (e.g. WP-2026-001) |
| `title` | Yes | Short title (< 60 chars) |
| `goal` | Yes | One sentence: what must be true when done |
| `context` | No | Relevant background for the bot |
| `inputs.files` | No | Files the bot needs |
| `inputs.references` | No | URLs, docs, related work |
| `inputs.constraints` | No | Hard limits (time, scope, style) |
| `success_criteria` | Yes | At least 1 criterion with verifiable_by |
| `assigned_bot` | Yes | `claude-code`, `wf09`, or `codex` |
| `target_repo` | No | GitHub repo if applicable |
| `target_branch` | No | Branch for the bot to work on |
| `callback_webhook` | Yes | URL to POST result to (default: /webhook/pca/eval) |
| `deadline_iso` | No | ISO 8601 datetime |
| `sprint` | Yes | Sprint letter (A / C / D) |
| `owner` | Yes | Who requested this (default: product-owner) |
| `created_at` | Yes | ISO 8601 datetime |

---

## Bot Output Format

When a bot completes a work package, it POSTs to `callback_webhook`:

```json
{
  "work_package": { /* original work package */ },
  "bot_output": {
    "summary": "One paragraph: what was done, what was not done",
    "deliverables": ["file path or PR URL"],
    "pr_url": "https://github.com/...",
    "tests_passed": true,
    "verification_notes": "How verification was performed or why skipped"
  }
}
```

---

## Evaluation Decisions

| Decision | Meaning | Required Action |
|----------|---------|------------------|
| GO | All criteria met | Merge / ship / mark done in BACKLOG |
| NEEDS-REVISION | Partial completion | Bot revisits with specific feedback |
| NO-GO | Goal not met | Rescope, re-spec, or reassign |

---

## Notification Flow

| Channel | When | Content |
|---------|------|---------|
| Obsidian `/PCA/Evals/` | Every eval | Full eval note with frontmatter + criteria + exec summary |
| WF10 | Every eval | Title + exec summary bullets |
| ntfy `/pca-eval` | Every eval (if NTFY_URL set) | Decision + exec summary |
| Obsidian `/PCA/Digests/` | Monday 08:00 | Full weekly digest |
| ntfy `/pca-digest` | Monday 08:00 (if NTFY_URL set) | Eval count + pointer to digest note |

---

## Deployment

```powershell
# 1. Store Anthropic API key in Vault (once)
vault kv put secret/pca/anthropic api_key=<your-key>

# 2. Deploy eval webhook
. "C:\Users\client\Documents\PCA\create_wf_work_routing_eval.ps1"

# 3. Deploy Monday digest scheduler
. "C:\Users\client\Documents\PCA\create_wf_monday_digest.ps1"

# 4. Smoke test
. "C:\Users\client\Documents\PCA\test_wf_work_routing_eval.ps1"
```

Requires: `N8N_API_KEY` env var set.

---

## Success Criteria for This Protocol

1. `POST /webhook/pca/eval` with a valid payload returns `overall_decision` in `{GO, NEEDS-REVISION, NO-GO}`
2. A `.md` file appears in `/PCA/Evals/` in the Obsidian vault for each eval
3. WF10 records the eval as an incident
4. Monday 08:00: a digest appears in `/PCA/Digests/`
5. ntfy notification fires on eval (if `NTFY_URL` is set)
