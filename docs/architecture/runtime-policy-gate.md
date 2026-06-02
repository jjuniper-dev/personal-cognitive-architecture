# Runtime Policy Gate

## Purpose

The Runtime Policy Gate is the control layer that determines whether an agent, workflow, model, or tool invocation is allowed to execute within the Personal Cognitive Architecture (PCA).

It exists to prevent agent sprawl, uncontrolled data access, accidental disclosure, unsafe automation, and untraceable execution.

The Runtime Policy Gate is the PCA equivalent of an enterprise AI control plane.

## Gate Hierarchy

This is the canonical governance model for PCA execution.

Specialized gates can exist for narrower flows, but they inherit from this policy model.

Current specialization:

- `Edge Policy Gate` for phone-originated capture events after local inference and before routing

That relationship is:

```text
Runtime Policy Gate
└── Edge Policy Gate
```

The edge gate is therefore a scoped intake implementation, not a different control-plane concept.

## Scope

The gate applies to:

- agent execution
- model selection
- tool calls
- external API calls
- file system access
- vault writes
- Neo4j writes
- Qdrant writes
- workflow triggers
- secrets access
- human approval requirements
- output publication

## Core Principle

No agent or workflow should execute merely because it is technically possible.

Execution must be authorized based on:

- actor identity
- requested capability
- data sensitivity
- destination
- reversibility
- risk level
- confidence level
- auditability
- human approval status

## Policy Decision Model

Every execution request should be evaluated as a policy decision.

```text
Request → Evaluate Context → Apply Policy → Allow | Deny | Require Approval | Sandbox
```

## Required Policy Inputs

Each request should include:

```yaml
request_id: unique identifier
actor_type: user | agent | workflow | system
actor_id: stable actor identifier
capability_requested: capture | classify | reconcile | write | delete | publish | execute | notify
tool_requested: tool or API being invoked
data_sources: list of input sources
data_sensitivity: public | personal | internal | confidential | restricted
action_risk: low | medium | high | critical
reversibility: reversible | partially_reversible | irreversible
requires_external_call: true | false
requires_secret: true | false
human_approval_status: not_required | pending | approved | denied
trace_id: correlation id
```

## Default Decision Rules

| Condition | Decision |
|---|---|
| Missing actor identity | Deny |
| Missing trace ID | Deny |
| Restricted data + external API | Deny unless explicitly approved |
| Confidential data + write to public repo | Deny |
| Agent requests secret access | Require approval unless allow-listed |
| Agent requests file deletion | Require approval |
| Agent writes to Obsidian Inbox | Allow if traceable |
| Agent writes to Trusted knowledge state | Require reconciliation approval |
| Low-risk capture event | Allow |
| Contradiction detected | Route to review |
| Output publication | Require approval |

## Execution Modes

### 1. Allow

The request can proceed immediately.

### 2. Deny

The request is blocked and logged.

### 3. Require Approval

The request is paused until the user explicitly approves.

### 4. Sandbox

The request can execute only in a constrained environment with no durable writes.

Specialized gates may expose narrower routing results such as `review_queue` or `local_only`, but those should still map back to these canonical execution outcomes.

## Policy Domains

### Personal Domain

Used for personal notes, projects, finance, lifestyle, learning, and household workflows.

### Work Domain

Used for enterprise architecture, Health Canada / PHAC context, government policy, decks, and work-related knowledge.

### Mixed Domain

Used when personal infrastructure is used to reason about work concepts without storing sensitive work information.

### Restricted Domain

Used for secrets, credentials, tokens, protected information, or material that should not be processed by external services.

## Human Approval Gates

Approval is required when:

- a trusted knowledge node would be modified
- a contradiction would change an existing belief or conclusion
- an agent would delete, archive, or overwrite content
- data would leave the local machine
- a secret would be accessed
- a workflow would send email, post externally, or notify others
- a generated artifact would be published or shared

## Audit Requirements

Every policy decision should log:

```yaml
trace_id:
request_id:
timestamp:
actor_id:
capability_requested:
tool_requested:
data_sensitivity:
decision:
reason:
policy_version:
human_approval_id:
```

Minimum shared decision shape:

```yaml
decision: allow | deny | require_approval | sandbox | hold
reason: short_policy_reason
route: obsidian | backlog | review_queue | local_only | discard | null
policy_version: string
trace_id: correlation id
```

## Implementation Targets

Initial implementation may be lightweight:

- YAML policy file
- n8n function node validation
- local JSONL audit log
- manual approval via Obsidian task, notification, or n8n form

Future implementation may include:

- FastAPI policy service
- signed approval records
- policy-as-code
- Open Policy Agent
- Neo4j policy graph
- dashboard view of denied/approved executions

## Minimum Viable Gate

The MVP must enforce:

1. all durable writes include a trace ID
2. all external API calls declare data sensitivity
3. trusted knowledge writes require approval
4. destructive operations require approval
5. restricted data cannot leave local execution
6. all denials and approvals are logged

## Relationship to Other PCA Components

| Component | Relationship |
|---|---|
| Agent Registry | Defines who can request execution |
| Event Taxonomy | Defines trigger and trace events |
| Trust & Classification Model | Provides sensitivity and trust labels |
| Reconciliation Engine | Determines whether knowledge updates require review |
| Observability Architecture | Monitors policy decisions and failures |
| Cognitive Memory Architecture | Enforces safe memory writes |
