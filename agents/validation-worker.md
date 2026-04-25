---
type: agent-specification
role: worker
created: 2026-04-25
status: active
---

# Validation Worker Specification

## Identity

**Name**: Validation Worker  
**Role**: Scoring, classification, routing  
**Responsibilities**: Score candidates, classify content, apply routing rules, produce routing decisions  
**Authority**: Low (recommends routing; orchestrator applies rules)  
**Scope**: Stage 3-6 of pipeline (Score → Route)  

## Purpose

The Validation Worker performs **evaluation and routing logic**. It:

1. **Scores** — applies four-dimensional scoring model
2. **Classifies** — domain, type, project, intent via LLM
3. **Reconciles** — checks against knowledge graph
4. **Routes** — evaluates against routing rules
5. **Recommends** — produces routing decision for orchestrator

The Validation Worker **recommends**, the Orchestrator **decides** (especially for escalations).

## Input Contract

Receives normalized candidate from Capture Worker:

```json
{
  "capture_id": "uuid",
  "source_type": "...",
  "normalized_text": "...",
  "metadata": {...},
  "quality_metrics": {...}
}
```

## Output Contract

Produces validation result:

```json
{
  "validation_id": "uuid",
  "capture_id": "uuid",
  "scoring": {...},
  "classification": {...},
  "reconciliation": {...},
  "routing_action": "ADVANCE|ROUTE_WITH_TAG|ESCALATE|QUEUE|QUARANTINE",
  "routing_confidence": 0.91,
  "destination": "/path/in/vault"
}
```

See: `schemas/validation-result.schema.json`

## Responsibilities

### Scoring (Stage 3)

**Four-Dimensional Model**:
```
overall_score = 
  (credibility × 0.20) +
  (relevance × 0.40) +
  (novelty × 0.30) +
  (signal_strength × 0.10)
```

**Credibility** (0.0-1.0):
- Source reliability
- Publication tier, author expertise, domain authority
- Recency (older content degrades)

**Relevance** (0.0-1.0):
- Project/domain alignment
- Stakeholder connection
- Temporal alignment (deadlines)

**Novelty** (0.0-1.0):
- Uniqueness vs. existing knowledge
- Different perspective?
- Synthesizes multiple sources?

**Signal Strength** (0.0-1.0):
- Actionability
- Deadlines/urgency
- Stakeholder assignment

### Classification (Stage 4)

**LLM Prompt** (GPT-4):
```
Analyze this content and classify:
- Note type: task|idea|reference|decision|etc
- Domain: strategic-planning|product-delivery|etc
- Project: inferred project name
- Intent: inform|request|decide|action|etc
- Confidence: 0.0-1.0

Be precise. Explain your reasoning.
```

**Fallback** (if LLM fails):
- Use rule-based heuristics
- Look for action verbs, people, deadlines
- Assign lower confidence

### Reconciliation (Stage 5)

**Knowledge Graph Query**:
1. Semantic search for similar notes (if embeddings available)
2. Check for exact contradictions
3. Identify relationships (related-to, depends-on, supersedes)
4. Return reconciliation status

**Fallback** (if vault unavailable):
- Mark status as "defer-to-review"
- Continue processing
- Escalate if high-impact item

### Routing (Stage 6)

**Load Routing Rules**:
- Load `data/routing-rules.json`
- Evaluate conditions against scored candidate
- Select applicable rule (highest priority)
- Determine destination and action

**Rules** (in order):
1. Sensitive data → Quarantine + escalate
2. Contradicts high-confidence → Escalate + conflict queue
3. Very low confidence (<0.30) → Quarantine
4. Source type + confidence → Pattern-specific rules
5. Default → Inbox + review tag

## Processing Pipeline

```
Input (from Capture Worker)
  ↓
[Parallel Scoring]
├─ Credibility scorer
├─ Relevance scorer
├─ Novelty scorer
└─ Signal strength scorer
  ↓
Aggregate Scores → Overall Score
  ↓
LLM Classification
  ├─ Note type
  ├─ Domain
  ├─ Project
  └─ Confidence
  ↓
Reconciliation Check
  ├─ Query vault
  ├─ Detect contradictions
  └─ Identify relationships
  ↓
Routing Rule Application
  ├─ Load rules
  ├─ Evaluate conditions
  └─ Recommend action
  ↓
Output (to Orchestrator)
```

## Model Selection

### Scoring
- **All local** — JavaScript functions
- **Cost**: $0.00
- **Latency**: <2s

### Classification
- **GPT-4** (Phase 1, default)
- **Mistral 7B local** (Phase 2, cost optimization)
- **Cost**: $0.03 (GPT-4) or $0.00 (local)
- **Latency**: 2-5s

### Reconciliation
- **File search** (Phase 1, basic)
- **Vector DB** (Phase 2, semantic)
- **Cost**: $0.00
- **Latency**: 1-5s

## Fallback Strategy

If any step fails:

```
Scoring fails → Use default scores (0.5 across all dimensions)
Classification fails → Use low confidence (0.4), escalate
Reconciliation fails → Mark as "defer-to-review"
Routing fails → Default to "QUEUE_FOR_REVIEW"

All failures: Log error, continue, escalate if needed
```

## Quality Assurance

### Self-Check Before Output

```
IF overall_score < 0.30 THEN
  Flag as low-signal

IF classification_confidence < 0.50 THEN
  Flag as ambiguous, recommend escalation

IF contradictions_detected AND contradiction_severity > 0.7 THEN
  Flag as requires-approval

IF routing_decision == ESCALATE THEN
  Double-check reasoning, log clearly
```

## Latency Targets

| Step | Target | Notes |
|------|--------|-------|
| Scoring | <2s | All local |
| Classification | 2-5s | LLM-dependent |
| Reconciliation | 1-5s | Depends on vault size |
| Routing | <1s | Rules evaluation |
| **Total** | **<15s** | End-to-end |

## Cost Model (Per Candidate)

| Operation | Cost | Notes |
|-----------|------|-------|
| Scoring | $0.00 | All local |
| Classification (GPT-4) | $0.03 | Phase 1 default |
| Classification (local) | $0.00 | Phase 2 |
| Reconciliation | $0.00 | Vector search |
| **Total** | **$0.03** | Phase 1 average |

## Monitoring

### Metrics
- Classification accuracy (vs. human review)
- Routing accuracy (% correct destinations)
- False positive rate (items incorrectly escalated)
- False negative rate (items should have been escalated)
- Latency p95 (should be <15s)

### Alerts
- Classification latency > 20s
- Routing confidence < 0.50 (systematic ambiguity)
- Accuracy drops below 80% (recalibration needed)
- Escalation rate > 30% (too many edge cases)

## Feedback Loop Integration

The Validation Worker participates in monthly calibration:

1. **Collect** user feedback on routing accuracy
2. **Analyze** false positives and negatives
3. **Measure** weight sensitivity
4. **Recommend** adjustments (e.g., relevance 0.40 → 0.35)
5. **Retrain** classification model if sample size > 50

This enables continuous improvement without human intervention.

## Non-Negotiable Principles

1. **Confidence is explicit** — every score includes uncertainty
2. **Reasoning is logged** — can explain any decision
3. **Escalation is always possible** — no forced automation
4. **No silent failures** — errors are surfaced and logged
5. **Fallbacks are graceful** — system degrades safely

---

**Status**: Active specification (v1.0)
**Last Updated**: 2026-04-25
**Related**: pca-orchestrator.md, capture-worker.md, pca-capture-scoring-model.md
