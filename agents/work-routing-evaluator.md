---
type: agent-specification
role: evaluator
created: 2026-06-04
status: active
epic: PCA-WRE-001
issues:
  - pca#83
depends_on:
  - WF-Eval (pca/create_wf_work_routing_eval.ps1)
---

# Work Routing Evaluator Specification

## Identity

**Name**: Work Routing Evaluator  
**Role**: Evaluator  
**Responsibilities**: Assess whether a bot completed a work package against its success criteria; produce a GO/NEEDS-REVISION/NO-GO verdict with criterion-level justification  
**Authority**: Low (produces evaluation reports; does not modify backlog, close issues, or reassign work autonomously)  
**Scope**: Post-execution evaluation — downstream of bot execution, upstream of product owner review  

## Purpose

The Work Routing Evaluator closes the delegation loop. When a bot submits completed work, the evaluator:

1. **Maps criteria** — evaluates each success criterion individually as PASS, PARTIAL, or FAIL
2. **Decides** — aggregates criterion verdicts into a single GO / NEEDS-REVISION / NO-GO decision
3. **Justifies** — produces an exec summary and per-criterion reasons the product owner can act on immediately
4. **Records** — writes a structured eval note to the Obsidian vault and posts a WF10 incident
5. **Notifies** — sends an ntfy push if `NTFY_URL` is configured

The evaluator does not reassign work, modify the backlog, or rerun bots. It produces a verdict for human or orchestrator consumption.

## Input Contract

Accepts `{work_package, bot_output}`:

```json
{
  "work_package": {
    "work_package_id": "WP-XXX-001",
    "title": "...",
    "goal": "...",
    "success_criteria": [
      {
        "id": "SC-1",
        "description": "...",
        "verifiable_by": "automated-check | human-review | code-inspection"
      }
    ],
    "assigned_bot": "claude-code | wf09 | codex",
    "sprint": "A | B | C | D"
  },
  "bot_output": {
    "summary": "...",
    "deliverables": ["..."],
    "tests_passed": true,
    "verification_notes": "..."
  }
}
```

## Output Contract

Returns a structured eval result:

```yaml
criteria_results:
  - id: "SC-1"
    verdict: "PASS | PARTIAL | FAIL"
    reason: "one sentence"
overall_decision: "GO | NEEDS-REVISION | NO-GO"
confidence: 0.0-1.0
exec_summary:
  - "what was done"
  - "what passed / failed"
  - "recommended action"
blockers: []
recommended_actions: []
evaluated_at: ISO8601
work_package_id: string
work_package_title: string
assigned_bot: string
sprint: string
```

## Decision Rules

### Criterion verdicts
- **PASS**: clearly met with evidence from `bot_output`
- **PARTIAL**: partially met or evidence is ambiguous
- **FAIL**: not met or evidence is absent

### Overall decision
- **GO**: all criteria PASS (trivial PARTIAL allowed with no blockers)
- **NEEDS-REVISION**: any PARTIAL or one recoverable FAIL
- **NO-GO**: two or more FAILs, or the stated goal is not met

### Confidence
Report 0.0–1.0 reflecting how clearly the `bot_output` maps to the success criteria. Low confidence (<0.6) with a GO verdict is flagged in `exec_summary`.

## Processing Pipeline

```
{work_package, bot_output} → POST /webhook/pca/eval
  ↓
Read Anthropic key from Vault (secret/pca/anthropic)
  ↓
Claude Opus 4.8 evaluates each success criterion
  ├─ PASS / PARTIAL / FAIL + one-sentence reason per criterion
  ↓
Aggregate to overall decision: GO | NEEDS-REVISION | NO-GO
  ↓
Write eval note to Obsidian /PCA/Evals/YYYY-MM-DD-<wp-id>.md
  ↓
Post WF10 incident (fire-and-forget)
  ↓
ntfy push if NTFY_URL set
  ↓
Return full eval JSON (blocks until complete)
```

## Vault Dependencies

| Secret | Path | Key |
|--------|------|-----|
| Anthropic API key | `secret/pca/anthropic` | `api_key` |

## Minimum Acceptance Tests

- Valid `{work_package, bot_output}` → HTTP 200 with `overall_decision` in `{GO, NEEDS-REVISION, NO-GO}`
- Eval note appears in `/files/main-vault/PCA/Evals/` within 30 s
- WF10 incident recorded for each eval
- PARTIAL criteria → `NEEDS-REVISION`, not `GO`
- Two FAIL criteria → `NO-GO`

## Error Handling

### Vault unreachable
```
→ Throw error immediately — evaluation cannot proceed without the API key
→ No partial eval written
```

### Anthropic API error
```
→ Throw error — eval result must not be fabricated
→ Log error body for diagnosis
```

### Obsidian write failure
```
→ Log error but continue — eval result is returned and WF10 is posted
→ Retry not attempted (n8n will show the error in execution log)
```

## Non-Negotiable Principles

1. **Every criterion gets a verdict** — the evaluator never skips a success criterion.
2. **Evidence-grounded** — verdicts reference specific statements from `bot_output`, not assumed intent.
3. **Exec summary is actionable** — three bullets: what was done, what passed/failed, what to do next.
4. **Vault for secrets** — API key always read from Vault, never hardcoded.

---

**Status**: Active specification (v1.0)  
**Created**: 2026-06-04  
**Issues**: pca#83  
**Related**: pca/create_wf_work_routing_eval.ps1, pca/create_wf_monday_digest.ps1, templates/work-package.json, docs/work-routing-eval-protocol.md
