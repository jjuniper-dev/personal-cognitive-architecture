---
type: project
created: 2026-04-19
updated: 2026-04-19
tags: [pca, strategy, north-star]
status: active
---

# PCA North Star

## One-line definition

The Personal Cognitive Architecture (PCA) is a governed cognitive operating system that captures, evaluates, integrates, and activates knowledge to improve thinking, decision-making, and execution over time.

## Design position

PCA is a personal cognitive system, not a collection of productivity tools.

Its purpose is to create durable, governed cognitive infrastructure in which information is captured, validated, structured, remembered, and activated with human oversight.

The architecture privileges canonical memory, explicit control, and modular reasoning over convenience-driven automation.

## Why PCA exists

PCA exists to move beyond note-taking, chatbot interaction, and fragmented personal productivity tooling.

It is intended to provide a durable personal cognitive environment that can:

- capture information with low friction
- validate and structure it before it becomes trusted knowledge
- preserve canonical memory in human-readable form
- reconcile new information against existing knowledge when appropriate
- trigger actions, outputs, and agent workflows from structured memory

The aim is to move from AI as a tool to AI as personal cognitive infrastructure.

## End-state vision

In its mature form, PCA should function as:

- a personal memory system
- a reasoning support environment
- an orchestration layer for personal and professional agents
- a structured output engine for notes, briefings, dashboards, and artifacts
- a controlled environment for contradiction handling, belief revision, and deeper synthesis

PCA should feel like cognitive infrastructure, not a chatbot shell.

## Core capabilities

PCA is intended to:

- ingest from voice, web, files, chat, video, and manual notes
- score and route incoming information through validation layer
- keep low-confidence material out of trusted memory
- maintain canonical knowledge in Obsidian (human-readable, durable)
- actively reconcile new information against existing knowledge through the Cognitive Reconciliation Engine
- detect reinforcement, contradictions, gaps, and novel contributions
- update confidence levels and trigger belief evolution
- support semantic retrieval through indexing layers without replacing canonical memory
- orchestrate agents across personal and professional domains with governed scope
- produce high-quality artifacts meeting GC/HC standards where applicable
- support human-in-the-loop governance for consequential reasoning and actions
- generate structured outputs (presentations, documents, dashboards, audio) from integrated knowledge
- maintain compliance with Responsible AI principles and ethical frameworks

## Architectural posture

The backbone of the system is:

Capture → Validation → Reconciliation → Knowledge Store → Reasoning / Agents → Execution → Output

The architecture is designed around the following posture:

- local-first where practical
- modular rather than monolithic
- governed rather than always-on
- rebuildable rather than brittle
- architecture-led rather than tool-led

Reconciliation is an invoked mode, not a background service.

Deep synthesis, contradiction handling, confidence restructuring, and graph-wide reinterpretation are governed operations that must be explicitly triggered or routed through defined controls.

## Non-negotiable principles

### Obsidian is canonical memory
Obsidian is the source of truth for long-term human-readable knowledge.

### Indexes are not truth
Vector stores and retrieval indexes may support recall and reasoning, but they never replace canonical memory.

### Intake is not knowledge
Unprocessed captures remain untrusted until they are validated, structured, and intentionally integrated.

### Human oversight matters
Higher-impact reasoning, belief updates, and actions require human review or approval.

### Least-complex architecture that works
The system should prefer simple, durable components over unnecessarily complex infrastructure.

### Orchestrator-worker pattern
The system should use orchestrator-worker patterns for agent behavior, with clear scope, routing, and escalation.

### Tools are replaceable
Tools are secondary to architecture. Any component may be replaced if canonical memory, operating principles, and clean interfaces are preserved.

### Outputs are not memory
Outputs are products of structured memory, not substitutes for it.

## Design tests for future changes

When evaluating a new component, workflow, or pattern, ask:

- Does this preserve Obsidian as canonical memory?
- Does this reduce or increase hidden complexity?
- Does this create unnecessary lock-in?
- Does this make reconciliation safer or noisier?
- Does this improve human-readable durable memory?
- Does this preserve rebuildability?
- Does this support governed orchestration instead of unmanaged autonomy?

If the answer is negative on multiple points, the change should be challenged or deferred.

## Constraints and optimization goals

PCA is optimized for:

- low-friction capture
- durable markdown-based memory
- reversible architecture decisions
- low operational overhead
- local-first operation where practical
- governed reasoning over constant autonomy
- cognitive usefulness over feature breadth

## What PCA is not

PCA is not:

- a generic note-taking vault
- a chatbot-first system
- a bloated enterprise platform at home
- a permanently active autonomous reasoning engine
- a random collection of AI tools
- infrastructure for its own sake

## Failure modes to avoid

The system should explicitly avoid:

- inbox becoming permanent storage
- vector indexes becoming de facto truth
- agents bypassing human review
- reconciliation becoming noisy and always-on
- tool sprawl outrunning architecture
- outputs becoming ad hoc and untraceable
- maintenance burden overwhelming cognitive value

## Success conditions

PCA succeeds when:

- raw inputs reliably become structured notes without heavy manual cleanup
- trusted memory remains durable, readable, and reusable
- retrieval layers improve recall without replacing source memory
- agent workflows produce traceable outputs tied to structured knowledge
- reconciliation remains deliberate, bounded, and human-governed
- the system reduces cognitive friction rather than increasing operational drag

## Relationship to current phase

The current build phase is focused on establishing the memory and plumbing layer first.

Immediate objective:

n8n → Obsidian → structured note in the vault

This proves the architecture is operational.

Current implementation emphasis:

- Obsidian as source of truth
- VS Code as working environment
- n8n in Docker as orchestration layer

Later phases may add:

- capture pipelines
- agent workflows
- semantic indexing
- local model execution
- controlled reconciliation
