# EPIC: PCA Experience Learning Layer

## Goal

Enable PCA to learn from outcomes, not just remember facts.

The system should capture decisions, actions, workflow executions, agent outputs, user feedback, and real outcomes, then convert them into reusable lessons that improve future routing, recommendations, prompts, and governance decisions.

---

## Architectural Position

This epic adds an experience-learning layer across the existing PCA flow.

Current PCA flow:

```text
Capture -> Validate -> Govern -> Route -> Store -> Retrieve -> Reuse
```

Target learning flow:

```text
Capture -> Validate -> Govern -> Store -> Retrieve -> Act -> Observe -> Reflect -> Learn -> Adapt
```

The important shift is from memory learning to experience learning.

Memory learning answers:

```text
What do I know?
```

Experience learning answers:

```text
What happened when I acted on what I knew?
What should change next time?
```

---

## Integration Points

### 1. Capture Layer

Sources:

- ChatGPT conversations
- Voice captures
- iPhone shortcut captures
- Obsidian notes
- GitHub PRs, issues, comments, and reviews
- n8n workflow runs
- Manual reflections
- Completed backlog items

Required output:

```yaml
capture_id:
source_type:
source_uri:
timestamp:
actor:
project:
raw_content:
```

Purpose:

- Preserve traceability from raw event to learned lesson.
- Allow later audit, reprocessing, or rollback.
- Avoid untraceable memory writes.

---

### 2. Knowledge Lifecycle

Connect to:

- WF10 knowledge validation
- Knowledge schema
- Lifecycle state machine
- Obsidian frontmatter
- PostgreSQL knowledge table
- Neo4j entities and relationships

New requirement:

Every durable knowledge object should be linkable to one or more experience records.

Example:

```yaml
knowledge_id: K-001
related_experience_ids:
  - EXP-001
  - EXP-002
```

Purpose:

- Link claims and decisions to evidence of what happened later.
- Allow confidence adjustments based on observed outcomes.
- Support provenance beyond initial capture.

---

### 3. Backlog System

Backlog items should support outcome tracking.

Add fields:

```yaml
backlog_id:
epic:
story:
status:
owner_agent:
expected_outcome:
actual_outcome:
success_score:
rework_required:
lesson_ids:
related_prs:
related_decisions:
```

Purpose:

- Track what was attempted.
- Compare expected outcomes against actual outcomes.
- Learn which agents and workflows perform well.
- Identify repeated failure modes.

---

### 4. GitHub Integration

Capture from:

- PR opened
- PR reviewed
- PR merged
- PR converted to draft
- PR comments
- Review comments
- Failed checks
- Merge conflicts
- Issue completion

Experience record example:

```yaml
type: experience
source_type: github_pr
source_uri: https://github.com/jjuniper-dev/personal-cognitive-architecture/pull/31
event: pr_converted_to_draft
expected_outcome: prevent accidental schema merge
actual_outcome: merge risk reduced
lesson: canonical schemas need lifecycle and provenance reconciliation before becoming enforceable
confidence: 0.9
```

Purpose:

- Make engineering activity part of the learning substrate.
- Allow PCA to learn from PR reviews, failed checks, rework, and successful merges.
- Support agent performance assessment across real development work.

---

### 5. n8n Integration

Capture from:

- Workflow started
- Workflow completed
- Workflow failed
- Retry occurred
- Human approval required
- Validation failed
- Output accepted or rejected

Required fields:

```yaml
workflow_id:
workflow_name:
run_id:
input_object_ids:
output_object_ids:
status:
error_type:
duration:
human_review_required:
lesson_candidate:
```

Purpose:

- Track operational effectiveness of workflows.
- Identify brittle automations.
- Convert failures and approval events into learning signals.

---

### 6. Agent Registry

Each agent should have performance history.

Add fields:

```yaml
agent_id:
agent_role:
tasks_completed:
success_rate:
common_failure_modes:
best_task_types:
requires_human_review_for:
last_reviewed:
```

Use for routing:

```text
If task = schema reconciliation, prefer architecture-review agent over code-generation agent.
```

Purpose:

- Route work based on observed agent performance.
- Reduce repeated rework.
- Distinguish good code generation from good architecture judgement.

---

### 7. Reflection Agent

New agent:

```yaml
agent_id: reflection-agent
role: Experience Learning and Retrospective Agent
```

Responsibilities:

- Review completed work.
- Compare expected and actual outcomes.
- Extract lessons.
- Identify repeated failure patterns.
- Recommend backlog updates.
- Recommend schema, policy, or workflow changes.
- Update agent performance metadata.

Inputs:

- Backlog items
- GitHub events
- n8n runs
- Knowledge objects
- User feedback

Outputs:

- Experience records
- Lessons learned
- Agent performance updates
- Backlog improvement recommendations

---

### 8. Experience Store

New durable object type:

```yaml
type: experience
id:
capture_id:
related_knowledge_ids:
related_backlog_ids:
related_pr_ids:
related_agent_ids:
event_type:
expected_outcome:
actual_outcome:
assessment:
success_score:
failure_mode:
lesson:
recommendation:
confidence:
created_at:
reviewed_by:
lifecycle_state:
```

Initial lifecycle states:

```text
captured
reviewed
lesson_extracted
applied
archived
```

Purpose:

- Provide durable evidence of outcomes.
- Separate raw knowledge from experience-based learning.
- Support retrospective analysis and confidence adjustment.

---

### 9. Lessons Learned Store

Lessons should be promoted from experience records.

```yaml
type: lesson
id:
title:
summary:
applies_to:
evidence:
source_experience_ids:
recommended_change:
confidence:
status:
created_at:
last_validated:
```

Example:

```yaml
title: Schema PRs require lifecycle reconciliation before merge
applies_to:
  - knowledge_schema
  - runtime_policy_gate
  - lifecycle_state_machine
recommended_change: require schema-impact checklist before merge
confidence: 0.9
status: trusted
```

Purpose:

- Promote repeated or high-value experience findings into reusable guidance.
- Let lessons inform future decisions, routing, and review gates.

---

### 10. Runtime Policy Gate

Experience learning should feed governance.

New policy trigger:

```text
If a PR changes canonical schema, lifecycle states, policy decisions, or agent contracts:
  require architecture review
  prevent auto-merge
  require reconciliation checklist
```

Canonical policy decision outputs:

```text
allow
deny
require_approval
downgrade
burst
defer
quarantine
```

Purpose:

- Prevent schema drift from becoming enforceable technical debt.
- Use lessons learned to strengthen future controls.
- Keep governance lightweight but explicit.

---

## Stories

### Story 1: Define Experience Record Schema

Create:

```text
docs/EXPERIENCE_RECORD_SCHEMA.md
```

Acceptance criteria:

- Defines required fields.
- Links to knowledge schema.
- Links to backlog model.
- Includes examples for GitHub, n8n, and manual reflection.

---

### Story 2: Extend Backlog Metadata

Update backlog schema to include:

- Expected outcome
- Actual outcome
- Success score
- Lesson IDs
- Related PRs
- Responsible agent

Acceptance criteria:

- Backlog items can be reviewed retrospectively.
- Completed items can generate experience records.

---

### Story 3: Add GitHub Experience Capture

Capture PR events into experience records.

Initial events:

- PR opened
- PR reviewed
- PR converted to draft
- PR merged
- Review comment added

Acceptance criteria:

- PR #31 can be represented as an experience record.
- Schema-related PRs are flagged for architecture review.

---

### Story 4: Add n8n Workflow Outcome Capture

Capture workflow run outcomes.

Acceptance criteria:

- Workflow success or failure is stored.
- Failed workflows generate lesson candidates.
- Human approval events are tracked.

---

### Story 5: Create Reflection Agent Contract

Create:

```text
docs/agents/reflection-agent.md
```

Acceptance criteria:

- Defines inputs.
- Defines outputs.
- Defines review cadence.
- Defines when lessons are promoted.

---

### Story 6: Create Lessons Learned Register

Create:

```text
docs/LESSONS_LEARNED_REGISTER.md
```

Acceptance criteria:

- Lessons link back to experience records.
- Lessons have confidence and status.
- Lessons can drive backlog changes.

---

### Story 7: Add Schema Impact Checklist

Create:

```text
docs/SCHEMA_IMPACT_CHECKLIST.md
```

Checklist includes:

- Knowledge schema impact
- Lifecycle state impact
- Runtime policy impact
- Agent contract impact
- Event taxonomy impact
- Obsidian frontmatter impact
- PostgreSQL impact
- Neo4j impact

Acceptance criteria:

- Required for any PR changing canonical fields, enums, or object contracts.

---

## Definition of Done

This epic is complete when PCA can answer:

1. What did we try?
2. Why did we try it?
3. What did we expect to happen?
4. What actually happened?
5. What did we learn?
6. What should change next time?
7. Which agent, workflow, or source should we trust more or less as a result?

---

## First Implementation Target

Use PR #31 as the first test case.

Create one experience record:

```yaml
id: EXP-PR31-001
type: experience
source_type: github_pr
source_uri: https://github.com/jjuniper-dev/personal-cognitive-architecture/pull/31
event_type: schema_review
expected_outcome: introduce canonical knowledge schema
actual_outcome: useful schema added but lifecycle and provenance drift discovered
assessment: partial_success
success_score: 0.65
failure_mode: canonical vocabulary not reconciled before schema enforcement
lesson: schema changes must be checked against lifecycle, policy gate, agent contracts, event taxonomy, and storage models before merge
recommendation: require schema impact checklist for metadata-contract PRs
confidence: 0.9
lifecycle_state: reviewed
```

---

## Implementation Notes

Do not implement model fine-tuning as the first learning mechanism.

Start with explicit outcome tracking, retrospective analysis, and durable lessons learned.

The PCA should first learn through:

```text
Observed outcome -> Reflection -> Lesson -> Backlog or policy adjustment
```

Only later should model-level adaptation be considered.
