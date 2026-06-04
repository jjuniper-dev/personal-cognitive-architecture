# Work Routing & Evaluation Protocol

**Status:** active  
**Version:** 1.0  
**Created:** 2026-06-04  
**Owner:** PCA Runtime (L2/L3)  
**Epic:** PCA-WRE-001

---

## Purpose

This protocol closes the bot delegation loop in PCA. It defines:
- how work packages are formatted and routed to bots
- how bots report completed work
- how the evaluator maps outcomes to GO / NEEDS-REVISION / NO-GO
- how eval results are stored and surfaced to the product owner

---

## Work Package Format

See `templates/work-package.json` for the canonical template.

A work package has two sections:

### `work_package` — assigned by the product owner before delegation

| Field | Type | Description |
|-------|------|-------------|
| `work_package_id` | string | Unique ID — e.g., `WP-E6.2.1-001` |
| `title` | string | Short human-readable label |
| `goal` | string | One sentence: what the bot must accomplish |
| `success_criteria` | array | List of verifiable outcomes (see below) |
| `assigned_bot` | string | `claude-code`, `wf09`, `codex` |
| `sprint` | string | Sprint label from the active campaign |

Each success criterion:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `SC-1`, `SC-2`, … |
| `description` | string | Specific, observable outcome |
| `verifiable_by` | enum | `automated-check`, `code-inspection`, `human-review` |

**Writing good criteria:** A criterion is good when a reviewer can say PASS or FAIL from the `bot_output` alone without running the code. Prefer outcomes over actions ("webhook returns 200" not "deploy the script").

### `bot_output` — submitted by the bot when work is complete

| Field | Type | Description |
|-------|------|-------------|
| `summary` | string | One paragraph describing what was done |
| `deliverables` | string[] | Files, scripts, or artifacts produced |
| `tests_passed` | boolean | Whether automated tests passed |
| `verification_notes` | string | How the bot verified its own work |

---

## Delegation Flow

```
Product owner writes work package
  ↓
Assigns to bot (claude-code / wf09 / codex)
  ↓
Bot executes the work
  ↓
Bot POSTs {work_package, bot_output} to /webhook/pca/eval
  ↓
Evaluator (WF-Eval) maps each SC → PASS/PARTIAL/FAIL
  ↓
Aggregates to overall_decision: GO | NEEDS-REVISION | NO-GO
  ↓
Writes eval note to Obsidian /PCA/Evals/
Posts WF10 incident
Sends ntfy notification (if NTFY_URL set)
  ↓
Product owner reviews at Monday strategy session (WF-MondayDigest)
```

---

## Evaluation Webhook

**Endpoint:** `POST /webhook/pca/eval`  
**Blocking:** Yes — returns eval JSON when complete (up to 60 s)  
**Deploy:** `. "C:\Users\client\Documents\PCA\create_wf_work_routing_eval.ps1"`

### Request
```json
{
  "work_package": { "..." : "..." },
  "bot_output": { "..." : "..." }
}
```

### Response
```json
{
  "criteria_results": [
    { "id": "SC-1", "verdict": "PASS", "reason": "..." }
  ],
  "overall_decision": "GO",
  "confidence": 0.9,
  "exec_summary": ["...", "...", "..."],
  "blockers": [],
  "recommended_actions": [],
  "evaluated_at": "2026-06-04T10:00:00Z",
  "work_package_id": "WP-XXX-001",
  "work_package_title": "...",
  "assigned_bot": "claude-code",
  "sprint": "A"
}
```

---

## Decision Criteria

| Verdict | Criterion |
|---------|-----------|
| **PASS** | Criterion clearly met; evidence present in `bot_output` |
| **PARTIAL** | Partially met or evidence ambiguous |
| **FAIL** | Not met or evidence absent |

| Decision | Rule |
|----------|------|
| **GO** | All criteria PASS (trivial PARTIAL with no blockers allowed) |
| **NEEDS-REVISION** | Any PARTIAL or one recoverable FAIL |
| **NO-GO** | Two or more FAILs, or the stated goal is not met |

---

## Eval Note in Obsidian

Each eval produces a Markdown note at:
```
/files/main-vault/PCA/Evals/YYYY-MM-DD-<work_package_id>.md
```

Frontmatter:
```yaml
type: pca-eval
work_package_id: "WP-XXX-001"
decision: GO
confidence: 0.9
sprint: A
evaluated_at: "2026-06-04T10:00:00Z"
tags: [pca-eval, work-routing, go]
```

---

## Monday Digest

**Workflow:** WF-MondayDigest  
**Schedule:** Every Monday at 08:00  
**Deploy:** `. "C:\Users\client\Documents\PCA\create_wf_monday_digest.ps1"`

On Monday morning, WF-MondayDigest:
1. Reads all eval notes from `/PCA/Evals/` created in the past 7 days
2. Sends them to Claude Opus 4.8 as a single prompt
3. Synthesises an exec digest structured as:
   - **Sprint Status** — 1–2 sentences on overall health
   - **Work Package Results** — table: Title | Bot | Decision | Key Action
   - **Decisions Required** — items needing human input (omitted if none)
   - **Architecture Risks** — real risks only (omitted if none)
   - **Next Sprint Recommendation** — 1 sentence
4. Writes the digest to `/PCA/Digests/YYYY-MM-DD-monday-digest.md`
5. Sends ntfy push (if `NTFY_URL` set)
6. Posts WF10 incident

The digest is designed to be read in 5 minutes at the Monday strategy session.

---

## CLI Evaluator

For local evaluation without the n8n webhook:

```bash
# stdlib only — no install required for basic CLI
python work-routing-evaluator-impl.py --eval eval-payload.json

# Or split files
python work-routing-evaluator-impl.py \
  --work-package work-package.json \
  --bot-output bot-output.json

# JSON output
python work-routing-evaluator-impl.py --eval eval-payload.json --json

# Pipe
cat eval-payload.json | python work-routing-evaluator-impl.py --stdin
```

Exit code: `0` for GO, `1` for NEEDS-REVISION or NO-GO.

See `agents/work-routing-evaluator.md` for the full agent spec.  
See `agents/work-routing-evaluator-impl.py` for the CLI implementation.  
See `templates/work-package.json` for the canonical template.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VAULT_TOKEN` | Yes (n8n) | HashiCorp Vault token — read `secret/pca/anthropic` |
| `NTFY_URL` | No | ntfy base URL — skipped silently if unset |
| `PCA_EVAL_URL` | No | Override WF-Eval URL for CLI (default: `http://localhost:5678/webhook/pca/eval`) |
| `PCA_EVAL_TIMEOUT` | No | Request timeout in seconds for CLI (default: `60`) |

---

## Deployment Checklist

```powershell
# 1. Ensure Anthropic key in Vault
vault kv put secret/pca/anthropic api_key=<key>

# 2. Deploy WF-Eval
. "C:\Users\client\Documents\PCA\create_wf_work_routing_eval.ps1"

# 3. Deploy WF-MondayDigest
. "C:\Users\client\Documents\PCA\create_wf_monday_digest.ps1"

# 4. Smoke test
. "C:\Users\client\Documents\PCA\test_wf_work_routing_eval.ps1"
# Expected: [PASS] WF-Eval working correctly.
```
