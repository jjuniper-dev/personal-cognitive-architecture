# Knowledge Lifecycle State Machine

## Purpose

The Knowledge Lifecycle State Machine defines how information moves through the Personal Cognitive Architecture (PCA) from raw capture to trusted long-term knowledge.

It exists to:

- separate raw capture from trusted knowledge
- support explainable knowledge evolution
- preserve provenance and lineage
- support governance and review
- reduce accumulation of low-quality information
- prevent silent knowledge drift

## Core Principle

Knowledge should not become trusted merely because it was captured.

All knowledge objects must move through explicit lifecycle states.

## Lifecycle Overview

```text
Captured
  ↓
Inbox
  ↓
Validated
  ↓
Provisional
  ↓
Reconciled
  ↓
Trusted
  ↓
Contested
  ↓
Archived
```

Additional paths:

```text
Rejected
Deleted
Merged
Superseded
```

## Canonical States

### 1. Captured

Meaning:

Raw intake occurred but normalization may not yet be complete.

Characteristics:

- transient state
- minimal metadata
- may contain incomplete structure

Examples:

- voice memo uploaded
- URL captured
- screenshot received
- transcript imported

## 2. Inbox

Meaning:

Information exists in the system but has not yet been validated.

Characteristics:

- untrusted
- reviewable
- searchable with low weighting
- retained for possible future analysis

Allowed actions:

- validation
- tagging
- enrichment
- deletion
- archival

## 3. Validated

Meaning:

Basic quality and relevance checks completed.

Characteristics:

- source scored
- metadata normalized
- duplicates evaluated
- relevance estimated

Validation does not imply truth.

## 4. Provisional

Meaning:

Information appears useful and plausible but has not yet completed reconciliation.

Characteristics:

- may conflict with existing knowledge
- moderate retrieval weighting
- available for exploratory reasoning
- not canonical

Allowed actions:

- reconciliation
- contradiction analysis
- promotion
- rejection

## 5. Reconciled

Meaning:

Information has been compared against existing knowledge.

Characteristics:

- relationships established
- contradiction analysis complete
- confidence updated
- provenance preserved

Possible outcomes:

- trusted
- contested
- archived
- rejected

## 6. Trusted

Meaning:

High-confidence knowledge suitable for reuse, synthesis, and downstream reasoning.

Characteristics:

- strongly sourced
- reconciled
- confidence score above threshold
- policy compliant
- human-reviewed when required

Trusted does not mean permanently true.

## 7. Contested

Meaning:

Contradictory evidence exists.

Characteristics:

- multiple competing interpretations
- confidence instability
- review required
- retrieval should indicate uncertainty

Contested knowledge must preserve all provenance.

## 8. Archived

Meaning:

Knowledge retained for history, lineage, or future reference but removed from active reasoning priority.

Characteristics:

- retrievable
- low active weighting
- historically important
- potentially obsolete

Examples:

- outdated architecture assumptions
- superseded guidance
- old workflows

## 9. Rejected

Meaning:

Knowledge intentionally excluded.

Characteristics:

- false
- irrelevant
- low quality
- duplicated beyond value
- policy violating

Rejected items should retain minimal audit metadata.

## 10. Deleted

Meaning:

Knowledge removed from operational systems.

Requirements:

- approval required
- deletion reason logged
- traceability preserved

## 11. Merged

Meaning:

Knowledge object consolidated into another canonical object.

Characteristics:

- lineage preserved
- duplicate resolution complete
- references redirected

## 12. Superseded

Meaning:

Newer knowledge replaced older understanding.

Characteristics:

- historical lineage retained
- old node preserved
- canonical pointer updated

## State Transitions

| From | To | Conditions |
|---|---|---|
| Captured | Inbox | normalization complete |
| Inbox | Validated | validation completed |
| Validated | Provisional | threshold passed |
| Provisional | Reconciled | reconciliation completed |
| Reconciled | Trusted | confidence + governance threshold met |
| Reconciled | Contested | contradictions unresolved |
| Trusted | Contested | conflicting evidence detected |
| Trusted | Archived | obsolete or low-use |
| Any | Rejected | determined invalid |
| Any | Deleted | approved removal |
| Any | Merged | duplicate consolidation |
| Trusted | Superseded | newer canonical knowledge exists |

## Confidence Model Integration

Each knowledge object should contain:

```yaml
confidence_score:
confidence_reasoning:
contradiction_count:
corroboration_count:
last_reviewed:
review_required:
state:
```

## Human Review Requirements

Human review should be required for:

- promotion to Trusted when sensitivity is high
- replacement of Trusted knowledge
- deletion
- major contradiction events
- policy-sensitive domains

## Retrieval Weighting

| State | Retrieval Weight |
|---|---|
| Trusted | highest |
| Reconciled | high |
| Provisional | medium |
| Inbox | low |
| Archived | low |
| Contested | variable with warning |
| Rejected | excluded by default |

## Event Integration

The lifecycle should emit events.

Examples:

```text
knowledge.promoted
knowledge.demoted
knowledge.contested
knowledge.archived
knowledge.rejected
knowledge.superseded
```

## Storage Expectations

| System | Role |
|---|---|
| Obsidian | Human-readable canonical notes |
| Neo4j | State relationships and lineage |
| Qdrant | Semantic retrieval weighting |
| Event Log | State transition audit |

## MVP Requirements

The MVP should support:

1. Inbox state
2. Provisional state
3. Trusted state
4. Archived state
5. Contested state
6. Confidence scores
7. Human review flags
8. Provenance retention

## Future Evolution

Potential future capabilities:

- automatic confidence decay
- temporal relevance scoring
- contradiction clustering
- causal lineage tracking
- probabilistic belief graphs
- stale knowledge detection
- memory consolidation cycles

## Anti-Patterns

Avoid:

- immediate trust assignment
- silent overwrites
- deleting lineage
- mixing transient capture with canonical knowledge
- untracked confidence changes
- immutable trust assumptions

## Relationship to Other Artifacts

| Artifact | Relationship |
|---|---|
| Reconciliation Engine | Determines lifecycle transitions |
| Event Taxonomy | Emits lifecycle events |
| Runtime Policy Gate | Controls sensitive transitions |
| Agent Registry | Defines which agents may perform transitions |
| Canonical Metadata Schema | Stores lifecycle metadata |