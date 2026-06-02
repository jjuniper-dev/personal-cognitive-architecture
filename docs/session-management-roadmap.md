# PCA Claude-Orchestrated Session Management Roadmap

> **Work Package:** PCA-WP-SESSION-HARNESS-001
> **Status:** Phase 1 and Phase 2 active — dispatched to Codex
> **Backlog reference:** `pca/BACKLOG.md` → PCA-WP-SESSION-HARNESS-001

## Objective

Create a governed session management architecture that ensures every Claude session:

- Starts with the correct context
- Uses approved architecture artifacts
- Loads relevant memory automatically
- Produces auditable outputs
- Updates backlog and knowledge consistently
- Can be resumed after interruption
- Improves future sessions through structured learning

---

## Phase 1 — Establish Session Control Plane

### Step 1: Standardize Session Lifecycle

Define a formal session lifecycle:

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

**Deliverables:**
- `docs/session-lifecycle.md`
- `schemas/session-state.schema.json`

---

### Step 2: Session Identity

Every session receives:

```yaml
session_id:
started_at:
initiator:
objective:
priority:
active_epic:
```

Example:

```yaml
session_id: pca-2026-06-02-001
objective: Context Harness Design
active_epic: PCA-WP-CONTEXT-HARNESS-001
```

---

### Step 3: Session Registry

Create:

```
/system/sessions/
```

Store:

```
active-session.md
session-log.md
handover.md
```

Claude must always update these artifacts.

---

## Phase 2 — Automated Context Assembly

### Step 4: Context Manifest

Create:

```
context/context-manifest.yaml
```

Used by Claude before execution.

Loads:
- PCA principles
- active backlog items
- relevant architecture docs
- workflow instructions
- memory retrieval

---

### Step 5: Context Harness

Build:

```
scripts/assemble_context.py
```

Responsibilities:

1. Identify task type
2. Retrieve relevant memory
3. Load required context
4. Apply runtime policy gate
5. Generate context pack

Output:

```
context-pack.json
```

---

### Step 6: Context Audit

Store:

```json
{
  "session_id": "...",
  "loaded_context": [],
  "memory_used": [],
  "policy_decision": "allow"
}
```

This creates explainability.

---

## Phase 3 — Backlog Governance

### Step 7: Session-to-Backlog Contract

Before work begins, Claude must determine which backlog item is being advanced.

Every session should map to:
- Epic
- Story
- Work Package

No orphan work.

---

### Step 8: Backlog Update Protocol

At session end, Claude must:
- Update status
- Record blockers
- Record decisions
- Record next actions

---

### Step 9: Architectural Drift Detection

Before creating new artifacts, Claude checks:
- existing architecture
- existing workflow
- existing schema

Goal: **Reuse before Create**

---

## Phase 4 — Knowledge Management

### Step 10: Session Capture

Every session produces:
- Session Summary
- Decisions
- Artifacts Created
- Risks
- Next Actions

Stored as:

```
knowledge/sessions/
```

---

### Step 11: Decision Registry

Create:

```
knowledge/decisions/
```

Store ADR-style decisions:

```
Decision:
Context:
Options:
Selected:
Consequences:
```

---

### Step 12: Learning Capture

Extract:
- preferences
- patterns
- architecture updates
- recurring issues

Store separately from canon. Nothing enters canon automatically.

---

## Phase 5 — Recovery and Continuity

### Step 13: Session Handover Generation

At session close generate:
- Current State
- Work Completed
- Outstanding Work
- Recommended Next Step

Output: `HANDOVER.md`

---

### Step 14: Session Recovery

A future Claude session should be able to start with:

```
Read:
- CLAUDE.md
- BACKLOG.md
- HANDOVER.md
- Active Context Pack
```

and continue immediately.

---

### Step 15: Interruption Recovery

Handle:
- Claude timeout
- phone disconnect
- branch conflict
- partial implementation

Every session should be resumable.

---

## Phase 6 — Multi-Agent Orchestration

> **Note:** This phase overlaps with pca GitHub Epic #30–40 (Agent Workflow Stack v1). Coordinate with that epic before implementing.

### Step 16: Agent Registry

Define:
- Intake Agent
- Backlog Agent
- Knowledge Agent
- Review Agent
- Architecture Agent
- Coding Agent

Each agent owns a bounded responsibility.

---

### Step 17: Agent Dispatch Rules

Context Harness determines:

```
Task
    ↓
Agent
    ↓
Context Pack
    ↓
Execution
```

---

### Step 18: Review Gate

Important outputs require:

```
Primary Agent
    ↓
Review Agent
    ↓
Approval
```

Supports disagreement-driven validation.

---

## Phase 7 — Operational Maturity

### Step 19: Session Dashboard

Expose:
- active session
- active epic
- blockers
- context pack
- memory usage
- model route

---

### Step 20: Session Metrics

Track:
- tasks completed
- backlog velocity
- context pack size
- memory retrieval effectiveness
- model cost
- model latency

---

### Step 21: Model Routing

Use Context Harness to select:
- Gemma
- Qwen
- Claude
- GPT

based on:
- sensitivity
- complexity
- cost
- latency

---

## End State

Claude becomes an orchestrated worker operating inside PCA rather than an isolated conversational assistant.

The system evolves into:

```
Backlog
    ↓
Context Harness
    ↓
Agent Dispatch
    ↓
Execution
    ↓
Review
    ↓
Knowledge Capture
    ↓
Handover
    ↓
Next Session
```

Result:
- Deterministic sessions
- Recoverable sessions
- Auditable sessions
- Continuously improving sessions
- Governed agent execution

---

## Implementation Sequence

| Phase | Steps | Status | Overlap |
|-------|-------|--------|----------|
| 1 — Session Control Plane | 1–3 | `active` — Codex PCA-WP-SESSION-HARNESS.1 | New work |
| 2 — Context Assembly | 4–6 | `active` — Codex PCA-WP-SESSION-HARNESS.2 | New work |
| 3 — Backlog Governance | 7–9 | `pending` | Procedural — no new files |
| 4 — Knowledge Management | 10–12 | `pending` | Overlaps E-Learn chain |
| 5 — Recovery + Continuity | 13–15 | `pending` | Overlaps HANDOVER.md |
| 6 — Multi-Agent Orchestration | 16–18 | `pending` | Overlaps pca #30–40 |
| 7 — Operational Maturity | 19–21 | `pending` | Overlaps E6.2.1 dashboard |
