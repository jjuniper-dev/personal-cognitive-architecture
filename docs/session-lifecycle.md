# Session Lifecycle

**Version:** 0.1  
**Owner:** PCA runtime  
**Status:** Draft  
**Roadmap reference:** PCA-WP-SESSION-HARNESS-001 Phase 1 Step 1  

---

## Purpose

This document defines the canonical lifecycle of a PCA session. Every Claude Code session, agent session, or governed work session must map to these stages. The lifecycle exists to make sessions deterministic, recoverable, and auditable.

---

## Lifecycle Stages

```
Session Start
    ↓
Context Assembly
    ↓
Task Selection
    ↓
Execution
    ↓
Validation
    ↓
Knowledge Capture
    ↓
Backlog Update
    ↓
Session Handover
```

### 1. Session Start

**Input:** Session trigger (human-initiated, scheduled, or agent-dispatched)  
**Output:** Populated `session_state` record with identity fields  
**Actions:**
- Assign `session_id`
- Record `started_at`, `initiator`, `objective`
- Set `status: active`
- Write `system/sessions/active-session.md`

**Transition:** → Context Assembly

---

### 2. Context Assembly

**Input:** `session_id`, `objective`, `active_epic`  
**Output:** Context pack (active backlog items, relevant architecture docs, memory retrieval results)  
**Actions:**
- Load `CLAUDE.md`, `BACKLOG.md`, `HANDOVER.md` if present
- Retrieve relevant memory
- Apply runtime policy gate
- Record loaded context in `context_loaded[]`

**Transition:** → Task Selection

---

### 3. Task Selection

**Input:** Context pack, backlog  
**Output:** Confirmed `active_task` mapped to an epic, story, or work package  
**Actions:**
- Select the highest-priority backlog item that matches the session objective
- Confirm no orphan work — every task must map to a backlog item
- Record `active_task` in session state

**Transition:** → Execution

---

### 4. Execution

**Input:** `active_task`, context pack  
**Output:** Artifacts (code, docs, schemas, commits)  
**Actions:**
- Perform the task
- Record `artifacts_produced[]`
- Surface blockers immediately rather than silently

**Transition:** → Validation (on completion) | → Execution (if blocked, document and loop)

---

### 5. Validation

**Input:** Artifacts from Execution  
**Output:** Validation result (pass / fail / partial)  
**Actions:**
- Run applicable checks (tests, schema validation, word counts, linting)
- If checks cannot run, state explicitly what was not verified
- Record outcome in `validation_result`

**Transition:** → Knowledge Capture (pass/partial) | → Execution (fail — fix and retry)

---

### 6. Knowledge Capture

**Input:** Session artifacts, decisions made, learning signals  
**Output:** Session summary note, decision records, learning candidates  
**Actions:**
- Produce session summary (decisions, artifacts, risks, next actions)
- Flag learning candidates for review (per self-learning contract)
- Store in `knowledge/sessions/`

**Transition:** → Backlog Update

---

### 7. Backlog Update

**Input:** Session summary, validation result  
**Output:** Updated backlog items  
**Actions:**
- Update status of the active backlog item
- Record blockers, decisions, and next actions
- Close issues where acceptance criteria are met

**Transition:** → Session Handover

---

### 8. Session Handover

**Input:** Session summary, updated backlog  
**Output:** `HANDOVER.md`  
**Actions:**
- Write current state, work completed, outstanding work, and recommended next step
- Update `system/sessions/session-log.md`
- Set `status: completed` or `status: interrupted`
- Archive `active-session.md` → `session-log.md`

**Transition:** Terminal — session ends

---

## Session State Machine

| Status | Meaning | Terminal |
|---|---|---|
| `active` | Session in progress | No |
| `completed` | All stages finished cleanly | Yes |
| `interrupted` | Session ended before Handover | Yes |
| `blocked` | Execution paused — blocker recorded | No |

A session that reaches `interrupted` must produce at minimum a partial `HANDOVER.md` recording where it stopped and what is outstanding.

---

## Session Identity Fields

See `schemas/session-state.schema.json` for the canonical field definitions.

| Field | Required | Description |
|---|---|---|
| `session_id` | Yes | Unique identifier — format: `pca-YYYY-MM-DD-NNN` |
| `started_at` | Yes | ISO 8601 UTC timestamp |
| `initiator` | Yes | `human`, `scheduled`, or `agent:<id>` |
| `objective` | Yes | One-sentence description of the session goal |
| `priority` | Yes | `high`, `normal`, or `low` |
| `active_epic` | No | Work package or epic ID if applicable |
| `active_task` | No | Backlog item being worked — set during Task Selection |
| `status` | Yes | Current lifecycle status |

---

## Resumability Rule

Any future session can resume from an interrupted session by reading:

```
CLAUDE.md → BACKLOG.md → HANDOVER.md → active context pack
```

No tribal knowledge. No silent assumptions. The handover document is the contract.

---

## Out of Scope

- Session registry file management → PCA-WP-SESSION-HARNESS-001 Phase 1 Step 3
- Context harness script → Phase 2
- Agent dispatch rules → Phase 6
- Session dashboard → Phase 7
