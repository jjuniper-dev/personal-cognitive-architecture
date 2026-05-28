# PCA Claude Code Guidance

This file adapts the `andrej-karpathy-skills` coding-agent discipline to the Personal Cognitive Architecture repository.

The base pattern is four principles:

1. Think Before Coding
2. Simplicity First
3. Surgical Changes
4. Goal-Driven Execution

For PCA, apply those principles to a governed personal AI system where architecture clarity matters more than feature velocity.

---

## 1. Think Before Coding

Do not silently pick an interpretation when PCA/Ayla/runtime/vault/graph boundaries are ambiguous.

Before changing code or docs, identify:

- the layer being changed
- the component owner
- the state being read
- the state being written
- whether the change affects canonical memory
- whether the change affects external action
- whether the change affects routing, orchestration, or model calls

If uncertain, surface the ambiguity.

### PCA Boundary Questions

Ask these before implementation:

- Is this PCA architecture, Ayla assistant UX, runtime infrastructure, vault memory, graph memory, workflow orchestration, or model execution?
- Is this component authoritative or derived?
- Is this a durable path or an experiment?
- Is this a real agent, a workflow, a script, a tool, or a function?

### Naming Rule

Use **PCA** for architecture, runtime, infrastructure, schemas, event backbone, governance, vault, graph, and inspection.

Use **Ayla** only for the assistant/persona/interface layer.

If the component would still exist after renaming the assistant, it belongs to PCA.

---

## 2. Simplicity First

Build the smallest thing that preserves the architecture.

Prefer:

- one clear path over multiple clever options
- plain functions over abstractions
- explicit schemas over implicit payloads
- deterministic workflows over vague autonomous behaviour
- readable names over branding
- small files over large generated constructions

Avoid:

- speculative plugin systems
- unnecessary configuration layers
- duplicate routing surfaces
- multiple interfaces that do the same thing
- generic agent frameworks before one stable flow works
- hidden writes to vault, graph, or workflow state

### PCA Primitive Flow

Every durable capability should map to:

```text
Input → Event → Validate → Route → Store → Retrieve → Act → Audit
```

If a feature cannot be mapped to that chain, do not add complexity until the primitive is clear.

---

## 3. Surgical Changes

Touch only what is necessary for the requested goal.

Do not:

- rename PCA/Ayla concepts opportunistically
- reformat unrelated files
- refactor adjacent code without request
- delete pre-existing dead code unless explicitly asked
- change workflow semantics while editing docs
- alter vault/graph contracts while editing API code

Do:

- remove imports, variables, functions, or files made unused by your own change
- document unrelated dead code as a review finding
- keep diffs small and reviewable
- preserve existing conventions unless the task is to change them

### Diff Test

Every changed line must be explainable as necessary for the user’s request.

---

## 4. Goal-Driven Execution

Convert implementation requests into verifiable goals.

Bad:

```text
Add validation.
```

Better:

```text
Add validation so invalid capture payloads are rejected with a clear error, valid payloads still pass, and both paths are covered by tests or a documented manual verification.
```

For non-trivial changes, state:

1. goal
2. files likely affected
3. verification path
4. rollback/deletion path if relevant

### PCA Acceptance Sentence

A change is ready when this can be completed:

```text
This change adds <primitive> to support <use case>.
It receives <input>.
It emits <output/event>.
It writes to <state target>.
It is owned by <component>.
It is verified by <test/check>.
It can be removed by <rollback/deletion path>.
```

If this sentence cannot be completed, the change is not ready.

---

## PCA-Specific Review Lens

### Flag likely bloat

Flag code or docs when they show:

- no active caller
- no documented use case
- no test path
- no event boundary
- duplicate responsibility
- vague agent naming
- inconsistent PCA/Ayla naming
- hidden state mutation
- canonical memory writes without validation
- cloud-only dependency where local/degraded operation is expected

### Preserve the core architecture

The repo should remain understandable as:

```text
Capture → Reconcile → Activate
```

Mechanically:

```text
Input → Event → Validation → Routing → Memory → Retrieval → Action → Audit
```

### Agent Naming Discipline

Use:

- **assistant** for user-facing conversational interface
- **workflow** for n8n deterministic orchestration
- **tool** for callable capability
- **worker** for bounded task execution
- **agent** only when the component performs autonomous planning/tool selection

Do not call everything an agent.

---

## Default Behaviour for Coding Agents

When working in this repo:

1. Read relevant existing files before editing.
2. State assumptions when ambiguity exists.
3. Prefer minimal diffs.
4. Do not invent architecture.
5. Do not expand scope.
6. Verify with tests or explicit checks where possible.
7. If verification cannot be run, say exactly what was not verified.
8. Leave unrelated cleanup as findings, not hidden edits.

The goal is not faster code. The goal is durable cognitive infrastructure that remains inspectable after AI-assisted development.
