---
type: project
created: 2026-04-19
updated: 2026-04-19
tags: [pca, operating-model, governance]
status: active
---

# PCA Operating Model

## Purpose

This document defines how the PCA should operate at runtime and how control is maintained across capture, validation, orchestration, reconciliation, and action.

It exists to prevent drift into uncontrolled autonomy or ad hoc workflow sprawl.

## Operating model summary

The PCA operates through governed layers:

- capture
- validation
- canonical storage
- orchestration
- worker execution
- controlled reconciliation
- output generation

Not every layer is always active.

The PCA should behave like a controlled cognitive system, not a permanently active background agent.

## Core runtime pattern

The system uses an orchestrator-worker model.

### Orchestrator responsibilities

The orchestrator is responsible for:

- receiving validated or candidate inputs
- determining whether action is required
- routing tasks to the appropriate worker or holding for human review
- deciding whether reconciliation should be triggered
- managing scope, confidence, and escalation
- maintaining overall control of workflow state

### Worker responsibilities

Workers are responsible for bounded task execution.

Examples:

- summarization
- classification
- extraction
- cleanup
- formatting
- source analysis
- retrieval support

Workers do not redefine system rules or update trusted knowledge without orchestrator and/or human approval.

## Human oversight model

Human review is required when:

- a capture has high potential impact and low or medium confidence
- a reasoning step would change trusted knowledge
- contradictory information is detected against trusted memory
- a workflow touches work-sensitive or governance-sensitive content
- an action has financial, reputational, or strategic consequence
- the orchestrator cannot confidently determine the correct route

Human review is not a failure state. It is a design feature.

## Reconciliation model

Reconciliation is not always on.

### Allowed reconciliation triggers

Reconciliation may be triggered by:

- explicit human request
- defined periodic review
- contradiction detection on trusted material
- a named process that has authority to invoke it

### Reconciliation modes

#### Off
Capture, validation, tagging, and storage only.

#### Local
Bounded reconciliation using available local context and constrained scope.

#### Deep
Broader synthesis or contradiction analysis using expanded retrieval, additional models, or more extensive review controls.

Deep reconciliation requires stronger human oversight.

## Escalation model

Escalation should consider:

- confidence
- impact
- contradiction level
- action type
- domain sensitivity

### Example logic

- low confidence + low impact → hold in inbox
- high confidence + low impact → route to worker
- contradiction + trusted memory → flag for review
- high impact + uncertain recommendation → human review
- sensitive domain + any non-trivial action → human review

## Kill-switch model

The ecosystem should support three levels of control:

### Level 1 — Pause task
Stops the current task or flow.

### Level 2 — Pause agent
Stops one agent and its downstream worker activity.

### Level 3 — Halt ecosystem
Stops all orchestrated activity until manually resumed.

## Canonical memory rules

- Obsidian is the canonical long-term memory layer.
- Raw intake is not trusted knowledge.
- Templates and agent identity documents are separate from trusted memory.
- Retrieval indexes are support layers only.

No worker or retrieval system should overwrite canonical memory without governed routing.

## Output rules

Outputs must:

- be traceable to source material or structured knowledge
- be reproducible where practical
- avoid bypassing memory structure
- reflect confidence and uncertainty when relevant

Outputs are downstream products, not replacements for the memory model.

## Agent role boundary

### Personal orchestrator
Handles personal domain routing, capture review, memory shaping, and personal output workflows.

### Professional orchestrator
Handles work-domain reasoning and outputs under stricter review and domain controls.

### Workers
Perform bounded tasks delegated by an orchestrator.

The orchestrators may share patterns, but their domains and governance boundaries should remain separate.

## Anti-patterns to avoid

- workers acting without bounded scope
- implicit reconciliation
- uncontrolled memory mutation
- silent confidence inflation
- routing logic hidden in too many places
- agent overlap without clear responsibility
- “chat first” interaction replacing system structure

## Operating principle

The PCA should act deliberately, visibly, and reversibly.

If a behavior cannot be explained, paused, or redirected, it is too autonomous for the intended design.
