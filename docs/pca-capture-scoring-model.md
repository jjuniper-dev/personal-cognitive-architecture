---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, scoring, model, mathematics, capture-pipeline]
status: active
---

# Capture Scoring Model

## Definition

The **Capture Scoring Model** is a mathematical framework for evaluating the quality, relevance, and actionability of incoming knowledge candidates.

It produces a single **overall_score** (0.0–1.0) that gates admission to the knowledge graph.

---

## Architecture

The model is organized in four dimensions:

| Dimension | Weight | Meaning | Range |
|-----------|--------|---------|-------|
| **Credibility** | 0.20 | How reliable is the source? | 0.0–1.0 |
| **Relevance** | 0.40 | How applicable to active projects? | 0.0–1.0 |
| **Novelty** | 0.30 | How new/distinct from existing knowledge? | 0.0–1.0 |
| **Signal Strength** | 0.10 | How actionable or decision-critical? | 0.0–1.0 |

**Weight rationale**: Relevance dominates (0.40) because captured information is user-selected. Novelty (0.30) prevents redundancy. Credibility (0.20) floors unreliable sources. Signal Strength (0.10) is a tie-breaker for otherwise ambiguous items.

---

## Dimension 1: Credibility (Weight: 0.20)

### Definition
How likely is the source to provide accurate, unbiased information?

### Formula

```
credibility_score = 
  base_score +
  source_authority_adjustment +
  extraction_confidence_adjustment +
  recency_adjustment
```

### Components

**Base Score** (by source type):

```
voice_note:           0.75  (user is primary authority)
web_article:          0.60  (depends on domain/publication)
chat_message:         0.50  (conversational, less formal)
email:                0.70  (semi-formal, from known contact)
structured_input:     0.85  (user explicitly formatted)
document:             0.65  (depends on author/org)
```

**Source Authority Adjustment** (+/- up to 0.20):

```
if source_is_internal_project_doc:
  +0.15  (high authority: official project materials)
else if source_is_published_research:
  +0.15  (high authority: peer-reviewed)
else if source_is_unknown_website:
  -0.10  (lower authority: unvetted web source)
else if source_author_is_known_expert:
  +0.10  (elevated by known expertise)
else if source_contains_claims_only:
  -0.05  (no citations or evidence)
else:
  0      (neutral)
```

**Extraction Confidence Adjustment** (+/- up to 0.15):

```
extraction_confidence_adjustment = 
  extraction_confidence_score × 0.15

if transcription_confidence > 0.95:
  +0.10  (high-quality transcription)
else if transcription_confidence < 0.75:
  -0.10  (degraded transcription, high uncertainty)
else:
  0
```

**Recency Adjustment** (+/- up to 0.15):

```
days_old = current_timestamp - capture_timestamp

if days_old <= 7:
  +0.15  (fresh content, high recency value)
else if days_old <= 30:
  +0.10  (recent)
else if days_old <= 90:
  0      (neutral)
else if days_old <= 365:
  -0.05  (aging, less current)
else:
  -0.10  (old, potential staleness)
```

### Final Credibility Calculation

```
credibility_score = min(1.0, max(0.0, 
  base_score + 
  source_authority_adjustment + 
  extraction_confidence_adjustment + 
  recency_adjustment
))
```

### Examples

**Example 1**: Voice note from user, high-quality transcription, captured today
```
base: 0.75
+ source_authority (voice about own project): +0.15
+ extraction (confidence 0.94): +0.10
+ recency (0 days old): +0.15
credibility = 1.0 (capped)
```

**Example 2**: Web article, unknown source, captured 120 days ago
```
base: 0.60
+ source_authority (unknown website): -0.10
+ extraction (confidence 0.88): +0.08
+ recency (120 days old): -0.05
credibility = 0.53
```

---

## Dimension 2: Relevance (Weight: 0.40)

### Definition
How applicable is this information to the user's active projects and current focus areas?

### Formula

```
relevance_score = 
  domain_alignment +
  project_match +
  temporal_alignment +
  stakeholder_connection
```

### Components

**Domain Alignment** (0.0–0.35, normalized by 7):

Domain relevance to active projects:

```
domain_match_score = (
  (strategic_planning_match × 1.0) +
  (product_delivery_match × 1.0) +
  (research_match × 0.8) +
  (operations_match × 0.7) +
  (governance_match × 0.9) +
  (external_engagement_match × 0.6)
) / 7

where each match is 0.0 (no match) to 1.0 (perfect match)

domain_alignment = domain_match_score × 0.35
```

**Project Match** (0.0–0.25):

```
if note_mentions_active_project:
  project_alignment = 0.25
else if note_mentions_related_project:
  project_alignment = 0.15
else if note_mentions_known_domain:
  project_alignment = 0.10
else:
  project_alignment = 0.0
```

**Temporal Alignment** (0.0–0.20):

```
days_until_deadline = deadline_in_note - current_date

if days_until_deadline <= 7:
  temporal_value = 0.20  (urgent, high relevance)
else if days_until_deadline <= 30:
  temporal_value = 0.15  (near-term, good relevance)
else if days_until_deadline <= 90:
  temporal_value = 0.10  (medium-term)
else if days_until_deadline > 90:
  temporal_value = 0.05  (long-term, lower urgency)
else if no_deadline:
  temporal_value = 0.05  (reference material)

temporal_alignment = temporal_value
```

**Stakeholder Connection** (0.0–0.15):

```
number_of_known_stakeholders = count(
  people_named_in_note 
  who appear in active projects
)

stakeholder_alignment = 
  min(0.15, number_of_known_stakeholders × 0.05)

if primary_stakeholder_is_active:
  stakeholder_alignment += 0.05  (direct connection)
```

### Final Relevance Calculation

```
relevance_score = min(1.0, 
  domain_alignment + 
  project_match + 
  temporal_alignment + 
  stakeholder_alignment
)
```

### Examples

**Example 1**: Note about PATH-HAIL with deadline in 5 days, mentions Chad (active stakeholder)
```
domain_alignment: 0.30 (strategic planning, full match)
project_match: 0.25 (mentions active project)
temporal_alignment: 0.20 (5 days until deadline)
stakeholder_alignment: 0.10 (Chad is primary stakeholder)
relevance = 0.85
```

**Example 2**: Generic productivity tip, no project connection, no deadline
```
domain_alignment: 0.05 (operations, weak match)
project_match: 0.0
temporal_alignment: 0.05 (reference material)
stakeholder_alignment: 0.0
relevance = 0.10
```

---

## Dimension 3: Novelty (0.0–1.0, Weight: 0.30)

### Definition
How much new information or distinct perspective does this represent?

### Formula

```
novelty_score = 
  semantic_uniqueness -
  redundancy_penalty -
  supersession_penalty +
  new_perspective_bonus
```

### Components

**Semantic Uniqueness** (0.0–1.0):

Using vector similarity to existing notes:

```
similar_notes = semantic_search(
  vault_embeddings,
  candidate_embedding,
  threshold=0.7
)

if similar_notes.count == 0:
  semantic_uniqueness = 1.0  (completely new topic)
else:
  average_similarity = mean([
    note.similarity_score for note in similar_notes
  ])
  semantic_uniqueness = 1.0 - average_similarity
  
  # Nuance: even if similar, may have new angle
  if candidate_provides_different_perspective:
    semantic_uniqueness += 0.15
```

**Redundancy Penalty** (0.0–0.30):

```
exact_duplicates = count(
  notes where content_similarity > 0.95
)

if exact_duplicates > 0:
  redundancy_penalty = 0.30
else if near_duplicates (similarity 0.80-0.95):
  redundancy_penalty = 0.15
else if similar_topic_coverage:
  redundancy_penalty = 0.05
else:
  redundancy_penalty = 0.0
```

**Supersession Penalty** (0.0–0.20):

```
if candidate_contradicts_newer_knowledge:
  supersession_penalty = 0.20
else if candidate_contradicts_older_knowledge:
  supersession_penalty = 0.0  (candidate updates old knowledge)
else:
  supersession_penalty = 0.0
```

**New Perspective Bonus** (0.0–0.15):

```
if candidate_presents_different_framing:
  perspective_bonus = 0.10
else if candidate_synthesizes_multiple_sources:
  perspective_bonus = 0.08
else if candidate_challenges_existing_assumption:
  perspective_bonus = 0.15
else:
  perspective_bonus = 0.0
```

### Final Novelty Calculation

```
novelty_score = min(1.0, max(0.0,
  semantic_uniqueness -
  redundancy_penalty -
  supersession_penalty +
  new_perspective_bonus
))
```

### Examples

**Example 1**: New project strategy, no similar notes, offers new framing
```
semantic_uniqueness: 1.0 (no similar notes)
redundancy_penalty: 0.0
supersession_penalty: 0.0
perspective_bonus: 0.10 (new framing)
novelty = 1.0 (capped)
```

**Example 2**: Note similar to 4 existing articles (avg similarity 0.78)
```
semantic_uniqueness: 0.22 (1.0 - 0.78)
redundancy_penalty: 0.05 (similar topic coverage)
supersession_penalty: 0.0
perspective_bonus: 0.08 (different synthesis)
novelty = 0.25
```

**Example 3**: Duplicate of recently captured note
```
semantic_uniqueness: 0.0 (exact copy)
redundancy_penalty: 0.30 (exact duplicate)
supersession_penalty: 0.0
perspective_bonus: 0.0
novelty = 0.0 (negative values floor to 0.0)
```

---

## Dimension 4: Signal Strength (Weight: 0.10)

### Definition
How actionable or decision-critical is this information?

### Formula

```
signal_strength_score = 
  action_indicators +
  deadline_presence +
  stakeholder_assignment +
  contradiction_flag
```

### Components

**Action Indicators** (0.0–0.35):

Presence of explicit action language:

```
action_verbs = [
  "need to", "must", "should", "have to",
  "follow up", "create", "build", "design",
  "analyze", "review", "approve"
]

count_action_verbs = count(
  words_in_text matching action_verbs
)

if count_action_verbs >= 3:
  action_score = 0.35
else if count_action_verbs == 2:
  action_score = 0.25
else if count_action_verbs == 1:
  action_score = 0.10
else:
  action_score = 0.0

# Note types inherently actionable
if note_type in ["task", "decision", "workflow-trigger"]:
  action_score = min(0.35, action_score + 0.15)
```

**Deadline Presence** (0.0–0.25):

```
if explicit_deadline_in_note:
  deadline_score = 0.25
else if relative_deadline ("by EOW", "ASAP"):
  deadline_score = 0.15
else if implicit_deadline (meeting date, sprint end):
  deadline_score = 0.10
else:
  deadline_score = 0.0
```

**Stakeholder Assignment** (0.0–0.20):

```
if note_assigns_task_to_person:
  stakeholder_score = 0.20
else if note_requests_feedback_from_person:
  stakeholder_score = 0.10
else if note_references_person:
  stakeholder_score = 0.0
```

**Contradiction Flag** (0.0–0.10):

```
if candidate_contradicts_high_confidence_knowledge:
  contradiction_bonus = 0.10
  # Important for decision-making
else:
  contradiction_bonus = 0.0
```

### Final Signal Strength Calculation

```
signal_strength_score = min(1.0,
  action_indicators +
  deadline_presence +
  stakeholder_assignment +
  contradiction_flag
)
```

### Examples

**Example 1**: Clear task with deadline and assignment
```
action_indicators: 0.35 ("need to", "create", task type)
deadline_presence: 0.25 (explicit date)
stakeholder_assignment: 0.20 (assigned to Chad)
contradiction_flag: 0.0
signal_strength = 0.80 (capped to 1.0)
```

**Example 2**: Reference material, no action
```
action_indicators: 0.0
deadline_presence: 0.0
stakeholder_assignment: 0.0
contradiction_flag: 0.0
signal_strength = 0.0
```

---

## Overall Score Aggregation

### Formula

```
overall_score = 
  (credibility × 0.20) +
  (relevance × 0.40) +
  (novelty × 0.30) +
  (signal_strength × 0.10)

where:
  overall_score ∈ [0.0, 1.0]
  all dimensions ∈ [0.0, 1.0]
```

### Example: Complete Scoring

**Note**: "Need to send Chad the revised PATH/HAIL framing before ARB"

```
credibility_score = 0.85
  (voice note 0.75 + authority 0.15 + recency 0.15 - extraction 0.05 = 0.85)

relevance_score = 0.85
  (domain 0.30 + project 0.25 + temporal 0.20 + stakeholder 0.10 = 0.85)

novelty_score = 0.68
  (uniqueness 0.85 - redundancy 0.05 - supersession 0.0 + perspective 0.08 = 0.88)
  [Actually: 0.68 due to related existing note]

signal_strength_score = 0.80
  (actions 0.30 + deadline 0.25 + assignment 0.20 + contradiction 0.0 = 0.75)
  [Actually: 0.80 due to task type bonus]

overall_score = 
  (0.85 × 0.20) +
  (0.85 × 0.40) +
  (0.68 × 0.30) +
  (0.80 × 0.10)
= 0.17 + 0.34 + 0.204 + 0.08
= 0.794

Final: overall_score = 0.79 → ADVANCE (threshold 0.75)
```

---

## Routing Thresholds

Based on overall_score:

| Score Range | Action | Meaning |
|-------------|--------|---------|
| **≥ 0.75** | ADVANCE_TO_INTEGRATION | High confidence, auto-route |
| **0.50–0.74** | ROUTE_WITH_TAG | Moderate, needs review tag |
| **0.30–0.49** | QUEUE_FOR_REVIEW | Low-moderate, manual review |
| **< 0.30** | QUARANTINE | Very low signal, questionable quality |

### Rationale

- **0.75**: Two or more dimensions are strong (e.g., high relevance + good credibility)
- **0.50**: Sufficient signal to include, but with review marker
- **0.30**: Threshold for retention; below this is noise
- **< 0.30**: Likely spam, noise, or off-topic

---

## Sensitivity Analysis

### Impact of Weight Changes

If weights were to change, what's the effect?

```
Current weights: [0.20, 0.40, 0.30, 0.10]

Scenario 1: Relevance higher (0.50)
Effect: More user-selected content admitted
Example score: (0.85×0.20) + (0.85×0.50) + (0.68×0.25) + (0.80×0.05) = 0.812
Result: Higher routing rate, slightly more noise

Scenario 2: Novelty higher (0.40)
Effect: More emphasis on unique content
Example score: (0.85×0.20) + (0.85×0.30) + (0.68×0.40) + (0.80×0.10) = 0.762
Result: Filters more duplicates, loses some important updates

Scenario 3: Credibility critical (0.35)
Effect: Source reliability gates admission
Example score: (0.85×0.35) + (0.85×0.35) + (0.68×0.25) + (0.80×0.05) = 0.803
Result: Reduces low-quality web captures
```

**Recommendation**: Current weights (0.20, 0.40, 0.30, 0.10) balance user-centric capture with quality control.

---

## Time-Based Decay

Some dimensions degrade over time:

### Credibility Decay
```
credibility_at_age(days) = 
  base_credibility × decay_factor(days)

where:
  decay_factor(days) = 
    1.0                          if days <= 7
    0.95                         if days <= 30
    0.85                         if days <= 90
    0.70                         if days <= 365
    0.50                         if days > 365
```

**Meaning**: Source reliability diminishes as information ages.

### Relevance Decay
```
relevance_at_age(days) =
  base_relevance × decay_factor(days)

where:
  decay_factor(days) =
    1.0                          if days <= 14
    0.95                         if days <= 60
    0.80                         if days <= 180
    0.60                         if days > 180
```

**Meaning**: Relevance to active projects decreases as notes age.

### Novelty Stability
Novelty does **not** decay. If a note was novel when captured, it remains novel.

### Signal Strength Decay
```
signal_strength_at_age(days) =
  base_signal × decay_factor(days)

where:
  decay_factor(days) =
    1.0                          if days <= 7
    0.5                          if days <= 30
    0.2                          if days > 30
```

**Meaning**: Actionable items lose urgency quickly if not acted upon.

---

## Calibration Data

### Phase 1a Test Corpus

Test with 50 notes spanning all types and sources:

**Metrics to track**:
1. **Distribution of overall_score** — histogram to show if thresholds are sensible
2. **Per-dimension distribution** — which dimensions are most predictive?
3. **Route accuracy** — do high-score notes end up in correct projects?
4. **False negatives** — do low-score notes get wrongly quarantined?
5. **Routing time** — what % hit each threshold?

**Target distribution**:
- ≥0.75 (auto-route): 60–70%
- 0.50–0.74 (review): 20–25%
- 0.30–0.49 (queue): 5–10%
- <0.30 (quarantine): 2–5%

If distribution skews outside these ranges, adjust thresholds.

### Feedback Loop

After Phase 1a (2 weeks):
1. Measure actual routing accuracy with human feedback
2. Correlate dimension scores with human acceptance/rejection
3. Adjust weights if needed (e.g., if credibility over-gates high-relevance items)
4. Re-run 50-note test with adjusted model
5. Lock weights when stability achieved

---

## Implementation Checklist

- [ ] Implement all four dimension calculators as n8n nodes
- [ ] Test scoring on 10 manually selected notes (sanity check)
- [ ] Deploy to Phase 1a pipeline
- [ ] Capture scoring data (dimension values, overall, routing action)
- [ ] Run Phase 1a test corpus (50 notes)
- [ ] Analyze distribution and accuracy
- [ ] Collect human feedback on 30 notes (stratified by score)
- [ ] Assess false positive/negative rates
- [ ] Adjust thresholds or weights if needed
- [ ] Document calibration results
- [ ] Lock model for Phase 1 deployment

---

## Validation Rules

All dimension scores must:
- Be in range [0.0, 1.0]
- Have explicit reasoning
- Be reproducible (same input → same score)

Overall score:
- Sum of weighted dimensions, capped to [0.0, 1.0]
- Must have clear routing action
- Must have audit trail of component calculations

---

## Success Criteria

| Metric | Target | Why |
|--------|--------|-----|
| Auto-route accuracy | >95% | Most routed notes correct |
| Review-tag accuracy | >85% | Caught ambiguous cases |
| Quarantine false-positive rate | <5% | Don't lose good notes |
| Quarantine false-negative rate | <2% | Catch real spam/noise |
| Dimension variance | >0.3 std dev | Each dimension adds signal |
| Weight stability | <10% adjustment needed | Weights are robust |

---

**Status**: Active specification (v1.0)

**Last Updated**: 2026-04-25

**Next**: Implement in n8n and test with Phase 1a corpus

**Related**: pca-capture-pipeline-specification.md (Stage 3 uses this model)
