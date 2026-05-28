# PCA Agent Instructions

This file is the shared instruction surface for LLM code bots working in this repository.

Use this file for Claude Code, Codex, Cursor, local Qwen/Kimi-style coding agents, and any future PCA development bot.

For Claude-specific guidance, also read [`CLAUDE.md`](./CLAUDE.md).

---

## Repository Mission

Personal Cognitive Architecture (PCA) is governed personal AI infrastructure.

It is not just a chatbot, note app, or workflow collection.

The system exists to capture, validate, structure, retrieve, and activate knowledge over time while remaining inspectable, local-first where practical, and maintainable by one operator.

The durable system name is **PCA**.

The assistant/persona/interface name is **Ayla**.

---

## Canonical Mental Model

PCA should remain understandable as:

```text
Capture → Reconcile → Activate
```

The implementation primitive chain is:

```text
Input → Event → Validate → Route → Store → Retrieve → Act → Audit
```

Every new feature should fit somewhere in that chain.

If it does not, stop and document the ambiguity before coding.

---

## Required Pre-Work Before Editing

Before changing files:

1. Read the relevant local files first.
2. Identify the architectural layer being changed.
3. Identify the owner component.
4. Identify whether canonical memory, graph state, workflow state, model calls, or external action are affected.
5. Keep the change as small as possible.

Do not make broad refactors while completing a narrow request.

---

## Architectural Layers

Use these layers when reasoning about placement:

| Layer | Meaning | Typical Components |
|---|---|---|
| L1 Knowledge & Control | durable memory, vault, graph, governance | Obsidian, Neo4j, schemas, source register |
| L2 Agent Runtime | assistant and bounded workers | Ayla assistant, workers, model adapters |
| L3 Workflow & Integration | deterministic orchestration | n8n workflows, webhooks, routers |
| L4 Infrastructure | local/self-hosted runtime | Docker, Tailscale, host services |
| L5 AI Models | inference and transcription | local models, cloud APIs, Whisper |

When adding a file, its location should make the layer obvious.

---

## PCA vs Ayla Naming Rules

Use **PCA** for:

- architecture
- repository-level concepts
- runtime services
- capture APIs
- event backbone
- schemas
- vault and graph contracts
- governance and audit
- infrastructure
- inspection/review tooling

Use **Ayla** for:

- the assistant persona
- conversational UX
- user-facing orchestration voice
- assistant-specific prompts
- assistant-specific interaction memory

Rule:

> If the component would still exist after renaming the assistant, call it PCA.

---

## Agent / Worker / Tool / Workflow Discipline

Do not call everything an agent.

Use:

- **assistant** for user-facing conversational interface
- **workflow** for deterministic n8n orchestration
- **tool** for callable capability
- **worker** for bounded task execution
- **agent** only when autonomous planning or tool selection is actually present

This matters because PCA needs clear operational boundaries.

---

## Karpathy-Style Coding Discipline

Apply four rules:

### 1. Think Before Coding

Understand the mechanism before editing.

Ask:

- What is the input?
- What is the output?
- What state is read?
- What state is written?
- What event is emitted?
- What validates the change?
- What fails if this breaks?

### 2. Simplicity First

Prefer simple, inspectable code.

Avoid clever abstractions, speculative plugin systems, hidden global state, duplicate routers, and generated code that the operator cannot understand.

### 3. Surgical Changes

Only touch files required for the task.

If unrelated dead code or bloat is discovered, document it as a finding unless explicitly asked to remove it.

### 4. Goal-Driven Execution

A change is ready when this sentence can be completed:

```text
This change adds <primitive> to support <use case>.
It receives <input>.
It emits <output/event>.
It writes to <state target>.
It is owned by <component>.
It is verified by <test/check>.
It can be removed by <rollback/deletion path>.
```

---

## Canonical Memory Rules

Canonical memory is special.

Do not write to Obsidian, graph state, durable metadata, or source registers without an explicit validation path.

Any durable memory write should have:

- source identifier
- timestamp
- provenance
- classification/sensitivity when applicable
- validation status
- clear owner or producing component
- rollback/deletion story

Derived memory such as embeddings, summaries, indexes, and graph projections must not be treated as authoritative unless explicitly declared.

---

## Event Backbone Rules

Prefer event-shaped integration over hidden side effects.

Events should be:

- explicit
- schema-validatable
- timestamped
- source-linked
- traceable to the producing component
- safe to replay or ignore where practical

Do not create a new workflow path that bypasses the event model unless the task explicitly requires a temporary experiment.

Temporary bypasses must be documented.

---

## Local-First and Degraded Operation

PCA should avoid fragile cloud-only assumptions where practical.

When adding dependencies:

- prefer local/self-hosted paths where reasonable
- document cloud dependencies
- document credential/secrets requirements
- document degraded behaviour when a service is unavailable
- avoid hidden free-tier or vendor lock-in assumptions

---

## Security and Secrets

Never commit secrets, tokens, API keys, private credentials, or live personal data.

Use environment variables, local `.env` files excluded from git, or a secrets manager.

If a workflow requires secrets, document the variable names and expected purpose without real values.

---

## Testing and Verification

Prefer automated tests when the repo has a test harness.

When no test harness exists, provide a clear manual verification path.

A code bot must report:

- what was changed
- what was verified
- what was not verified
- what assumptions remain

Do not claim success for unrun tests.

---

## Bloat Detection

Flag likely bloat when a component has:

- no active caller
- no documented use case
- no test path
- no event boundary
- duplicate responsibility
- unclear owner
- inconsistent PCA/Ayla naming
- hidden state mutation
- direct canonical memory writes without validation
- cloud-only dependency without fallback or documentation

Do not delete bloat automatically unless the task is explicitly cleanup/removal.

---

## Preferred Output for Code Bots

For each completed task, respond with:

```md
## Summary
- what changed

## Files Changed
- path: why it changed

## Verification
- checks/tests run
- checks/tests not run

## Architecture Notes
- layer affected
- state affected
- risks or follow-up items
```

Keep this concise.

---

## Default Posture

PCA values maintainability over novelty.

When uncertain, choose the smaller, clearer, more inspectable change.
