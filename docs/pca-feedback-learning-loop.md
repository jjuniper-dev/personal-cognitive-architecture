---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, feedback, learning, calibration, improvement]
status: active
---

# PCA Feedback & Learning Loop

## Definition

The **Feedback & Learning Loop** is the mechanism by which PCA improves over time. It captures user corrections, validates system decisions, and uses that data to refine scoring weights, routing policies, and model selections.

This is the critical missing piece in most AI systems: **the path from observation to improvement**.

---

## Why Feedback Loops Matter

Without feedback:
- Scoring weights drift from reality
- Routing decisions become inconsistent
- Models degrade as context shifts
- Silent failures accumulate

With feedback:
- System learns what matters to *you*
- Confidence scores calibrate to reality
- Routing improves month-to-month
- Errors become visible and correctable

---

## Architecture

```
User Interactions
├─ Marks item as relevant/irrelevant
├─ Overrides routing decision
├─ Updates classification
├─ Searches and doesn't find item (false negative)
└─ Gets alerted about irrelevant item (false positive)
        ↓
┌─────────────────────────────────────────┐
│  FEEDBACK CAPTURE LAYER                 │
│  ├─ Implicit (user behavior)            │
│  ├─ Explicit (user marks as useful)     │
│  └─ Derived (items user acts on)        │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  FEEDBACK AGGREGATION                   │
│  ├─ Collect by pattern (ideas, knowledge, signals) │
│  ├─ Aggregate by decision type (routing, classification) │
│  └─ Calculate accuracy metrics          │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  ANALYSIS LAYER                         │
│  ├─ Compare predicted vs. actual        │
│  ├─ Identify systematic errors          │
│  ├─ Calculate weight sensitivity        │
│  └─ Flag models for retraining          │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  IMPROVEMENT LAYER                      │
│  ├─ Adjust scoring weights              │
│  ├─ Update routing thresholds           │
│  ├─ Retrain classification models       │
│  └─ Approve/reject changes (user gate)  │
└─────────────────┬───────────────────────┘
                  ↓
Updated Scoring Weights & Policies
        ↓
Next Cycle (Test, Validate, Deploy)
```

---

## Layer 1: Feedback Capture

### Implicit Feedback

Actions that indicate signal strength without explicit marking:

```json
{
  "implicit_feedback": [
    {
      "feedback_type": "user-action",
      "action": "searches-for-note",
      "note_id": "uuid",
      "timestamp": "2026-04-25T14:30:00Z",
      "interpretation": "Note was valuable enough to search for → relevance signal"
    },
    {
      "feedback_type": "user-action",
      "action": "opens-note-multiple-times",
      "note_id": "uuid",
      "access_count": 5,
      "days_since_creation": 7,
      "interpretation": "High engagement → high value to user"
    },
    {
      "feedback_type": "user-action",
      "action": "links-to-note",
      "from_note_id": "uuid-1",
      "to_note_id": "uuid-2",
      "timestamp": "2026-04-25T14:30:00Z",
      "interpretation": "User connected two pieces of knowledge → relationship is real"
    },
    {
      "feedback_type": "user-action",
      "action": "ignores-alert",
      "alert_id": "uuid",
      "dismisses_count": 3,
      "timestamps": ["2026-04-20", "2026-04-21", "2026-04-22"],
      "interpretation": "Alert is false positive → routing rule is too aggressive"
    },
    {
      "feedback_type": "user-action",
      "action": "archives-note",
      "note_id": "uuid",
      "reason": "not-relevant",
      "timestamp": "2026-04-25T14:30:00Z",
      "interpretation": "Note was routed incorrectly → reduce confidence for similar notes"
    }
  ]
}
```

### Explicit Feedback

User explicitly marks items as useful/not useful:

```json
{
  "explicit_feedback": [
    {
      "feedback_id": "uuid",
      "item_id": "note-uuid",
      "pattern_type": "structured-knowledge",
      "timestamp": "2026-04-25T14:30:00Z",
      
      "user_rating": {
        "relevant": true,
        "confidence": "high",
        "reasoning": "Directly applicable to PATH-HAIL strategy"
      },
      
      "classification_correction": {
        "original_type": "idea",
        "corrected_type": "strategy-note",
        "explanation": "This was strategic insight, not just an idea"
      },
      
      "confidence_assessment": {
        "original_confidence_score": 0.72,
        "user_confidence_assessment": "high",
        "mismatch": true,
        "reason": "System underestimated relevance to active project"
      },
      
      "routing_feedback": {
        "original_routing": "provisional",
        "should_have_been": "trusted",
        "impact": "high (false negative)"
      }
    },
    
    {
      "feedback_id": "uuid",
      "item_id": "signal-uuid",
      "pattern_type": "dynamic-signals",
      "timestamp": "2026-04-25T14:30:00Z",
      
      "user_rating": {
        "relevant": false,
        "confidence": "high",
        "reasoning": "Alert was about unrelated topic"
      },
      
      "routing_feedback": {
        "original_routing": "critical-alert",
        "should_have_been": "archive",
        "impact": "medium (false positive, alert fatigue)"
      }
    }
  ]
}
```

### Derived Feedback

Infer signal strength from user actions:

```json
{
  "derived_feedback": {
    "high_value_items": {
      "criteria": "accessed >2 times in 30 days OR linked from other notes",
      "feedback_signal": "relevance_increase +0.1",
      "frequency": "weekly scan"
    },
    
    "ignored_items": {
      "criteria": "routed >0 times, never accessed, not linked",
      "feedback_signal": "relevance_decrease -0.1",
      "frequency": "weekly scan"
    },
    
    "acted_on_items": {
      "criteria": "task completed, decision made, research published",
      "feedback_signal": "signal_strength_increase +0.15",
      "frequency": "monthly scan"
    },
    
    "contradicted_items": {
      "criteria": "user corrects classification >1 time",
      "feedback_signal": "flag for manual review + retraining",
      "frequency": "continuous"
    }
  }
}
```

---

## Layer 2: Feedback Aggregation

### By Pattern Type

```
Pattern 1: Structured Knowledge
├─ Total ingested: 150
├─ User-marked relevant: 132 (88%)
├─ User-marked irrelevant: 18 (12%)
├─ False positives (marked irrelevant): 8
├─ False negatives (never marked, high engagement): 12
└─ Accuracy: 0.94 (relevant marked correctly)

Pattern 2: Unstructured Ideas
├─ Total ingested: 485
├─ Promoted to knowledge: 97 (20%)
├─ Archived as not useful: 388 (80%)
├─ Classification corrections: 23 (4.7%)
├─ Accuracy: 0.75 (promotions were correct)

Pattern 3: Dynamic Signals
├─ Total ingested: 2847
├─ Routed as CRITICAL: 18
├─ User marked relevant: 16 (89%)
├─ User marked irrelevant: 2 (11%, false positives)
├─ False negatives (important signals archived): 3
└─ CRITICAL precision: 0.89, recall: 0.84
```

### By Decision Type

```
Routing Decisions
├─ Auto-route (Pattern 1, conf >= 0.80)
│  ├─ Total: 120
│  ├─ User accepted: 118 (98%)
│  ├─ User overrode: 2 (2%)
│  └─ Accuracy: 0.98
├─ Provisional (Pattern 1, 0.65-0.79)
│  ├─ Total: 30
│  ├─ User confirmed: 27 (90%)
│  ├─ User rejected: 3 (10%)
│  └─ Accuracy: 0.90
└─ Critical Alert (Pattern 3, score > 0.75)
   ├─ Total: 18
   ├─ User marked relevant: 16 (89%)
   ├─ User marked irrelevant: 2 (11%)
   └─ Accuracy: 0.89

Classification Decisions
├─ Note type accuracy (idea vs. task): 0.91
├─ Project assignment accuracy: 0.87
├─ Domain classification accuracy: 0.85
└─ Intent classification accuracy: 0.89
```

---

## Layer 3: Analysis

### Metric Calculation

```json
{
  "analysis": {
    "overall_accuracy": {
      "routing_accuracy": 0.91,
      "classification_accuracy": 0.88,
      "weighted_accuracy": 0.90,
      "target_accuracy": 0.95,
      "gap": 0.05
    },
    
    "per_pattern_accuracy": {
      "structured-knowledge": {
        "routing_accuracy": 0.94,
        "classification_accuracy": 0.92,
        "overall": 0.93
      },
      "unstructured-ideas": {
        "routing_accuracy": 0.75,
        "classification_accuracy": 0.82,
        "overall": 0.78
      },
      "dynamic-signals": {
        "routing_accuracy": 0.89,
        "classification_accuracy": 0.85,
        "overall": 0.87
      }
    },
    
    "error_analysis": {
      "false_positives": {
        "pattern_1_provisional": {
          "count": 3,
          "rate": 0.10,
          "root_cause": "relevance score too aggressive for moderate-confidence sources",
          "recommendation": "lower relevance weight from 0.40 to 0.35"
        },
        "pattern_3_critical_alerts": {
          "count": 2,
          "rate": 0.11,
          "root_cause": "signal_score threshold too low, catching marginal signals",
          "recommendation": "raise critical threshold from 0.75 to 0.80"
        }
      },
      
      "false_negatives": {
        "pattern_1_auto_route": {
          "count": 2,
          "rate": 0.02,
          "root_cause": "low-confidence articles from reputable sources being held for review",
          "recommendation": "increase source credibility adjustment from +0.15 to +0.20"
        }
      }
    },
    
    "weight_sensitivity": {
      "credibility_weight": {
        "current": 0.20,
        "sensitivity": "low (changing ±0.05 changes accuracy <1%)",
        "recommendation": "stable, no change"
      },
      "relevance_weight": {
        "current": 0.40,
        "sensitivity": "high (changing ±0.05 changes accuracy ~3%)",
        "recommendation": "consider reducing to 0.35 to avoid false positives"
      },
      "novelty_weight": {
        "current": 0.30,
        "sensitivity": "medium (changing ±0.05 changes accuracy ~2%)",
        "recommendation": "stable, no change"
      }
    }
  }
}
```

### Model Performance

```
Classification Model (GPT-4)
├─ Accuracy: 0.88
├─ Precision (high-confidence predictions): 0.92
├─ Recall (catches all true cases): 0.84
├─ F1 score: 0.88
├─ Latency: 2.1s (acceptable)
└─ Recommendation: Retrain on feedback data to improve recall

Scoring Model (Custom)
├─ Calibration: Well-calibrated (predicted 0.80 ≈ actual 0.80)
├─ Ranking accuracy: 0.91 (correct ordering of items)
├─ Threshold tuning: Provisional threshold (0.72) may be too low
└─ Recommendation: Retrain on feedback to adjust thresholds
```

---

## Layer 4: Improvement

### Weight Adjustment

```
Current weights (pca-capture-scoring-model.md):
  credibility: 0.20
  relevance: 0.40
  novelty: 0.30
  signal_strength: 0.10

Proposed weights (based on feedback analysis):
  credibility: 0.20 (no change)
  relevance: 0.35 (-0.05, reduce false positives in provisional tier)
  novelty: 0.30 (no change)
  signal_strength: 0.15 (+0.05, improve critical signal detection)

Rationale:
  1. Relevance was too aggressive, causing false positives
  2. Signal strength was underweighted, missing important signals
  3. Credibility and novelty are well-calibrated
```

### Threshold Tuning

```
Current thresholds (pca-capture-pipeline-specification.md):
  >= 0.75: ADVANCE_TO_INTEGRATION
  0.50-0.74: ROUTE_WITH_TAG
  0.30-0.49: QUEUE_FOR_REVIEW
  < 0.30: QUARANTINE

Proposed thresholds (based on accuracy analysis):
  >= 0.76: ADVANCE_TO_INTEGRATION (raise from 0.75)
  0.52-0.75: ROUTE_WITH_TAG (tighten range)
  0.31-0.51: QUEUE_FOR_REVIEW
  < 0.31: QUARANTINE

Rationale:
  1. Current threshold caught 2 false positives at 0.72-0.74
  2. Raising to 0.76 keeps those out of auto-route
  3. Provisional tier now 0.52-0.75 (was 0.50-0.74)
```

### Policy Changes

```
Dynamic Signals Pattern (Pattern 3):
  Current: Critical alert threshold 0.75
  Proposed: Critical alert threshold 0.80
  Rationale: 2 false positives (11% of alerts)
  Impact: Fewer alerts, but may miss 1-2 important signals per month
  Approval: User must confirm change

Unstructured Ideas Pattern (Pattern 2):
  Current: DDV classification for ideas with confidence 0.40-0.70
  Proposed: Lower threshold to 0.35-0.65 to catch more edge cases
  Rationale: Classification accuracy only 0.78, need more review
  Impact: More items flagged for review, more learning data
  Approval: User must confirm change
```

### Model Retraining

```
Monthly retraining schedule:

1. Collect feedback from last 30 days
2. Generate training dataset:
   - Input: candidate features (text, source, metadata)
   - Output: user feedback (correct classification, relevance)
3. Retrain classification model (if sample size > 50)
   - Use local Mistral 7B (Phase 2)
   - Fine-tune on domain-specific feedback
   - Validate against test set
4. Validate improvement:
   - Run on held-out test set
   - Compare accuracy to current model
   - If improvement >= 2%, deploy new model
   - If degradation, rollback
5. Update control plane policies if needed
```

---

## Layer 5: User Gate & Deployment

### Change Approval Workflow

```
System detects issue:
  Accuracy dropped below 85%
  False positive rate > 10%
  Model retraining shows improvement
        ↓
System proposes changes:
  "Recommend raising critical alert threshold from 0.75 to 0.80"
  "Impact: 2 fewer false positives per month"
  "Risk: May miss 1 important signal per quarter"
        ↓
User reviews and approves/rejects:
  ✓ Approve → deploy immediately
  ✗ Reject → system continues with current settings
  ? Ask questions → system explains rationale
        ↓
Deploy changes:
  Update config files
  Update scoring weights in scoring engine
  Log change to audit trail
  Test on next 50 captures before full deployment
```

### A/B Testing for Weight Changes

For significant changes, run A/B test:

```
Scenario: Considering relevance weight reduction 0.40 → 0.35

Phase 1: Baseline (Week 1)
  ├─ Current weights: relevance 0.40
  ├─ Measure: routing accuracy, false positive rate
  └─ Baseline: accuracy 91%, false positives 10%

Phase 2: A/B Test (Week 2-3)
  ├─ Control (50%): relevance 0.40
  ├─ Treatment (50%): relevance 0.35
  ├─ Measure: accuracy and false positive rate for each
  └─ Analyze: which performs better?

Phase 3: Comparison
  ├─ Control accuracy: 91%, false positives: 10%
  ├─ Treatment accuracy: 92%, false positives: 5%
  ├─ Winner: Treatment (better accuracy, fewer false positives)
  └─ Deploy: Roll out relevance 0.35 to 100%
```

---

## Feedback Cycle Cadence

### Real-Time (Immediate)
- User marks item as relevant/irrelevant
- System records feedback instantly
- No immediate action, but informs future similar items

### Daily (Overnight)
- Aggregate feedback from last 24 hours
- Recalculate accuracy metrics
- Alert if accuracy drops >2%

### Weekly
- Derive feedback from implicit signals
- Identify systematically wrong predictions
- Flag for manual review if pattern detected

### Monthly
- Full analysis: accuracy per pattern, per decision type
- Calculate weight sensitivity
- Retrain models if sample size sufficient
- Generate improvement recommendations
- User reviews and approves changes

### Quarterly
- Major calibration review
- Assess whether thresholds still make sense
- Compare to business outcomes (tasks completed, insights acted on)
- Plan architectural changes if needed

---

## Success Metrics

### System Health

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Overall accuracy | >0.95 | 0.90 | -0.05 |
| False positive rate | <0.05 | 0.10 | -0.05 |
| False negative rate | <0.05 | 0.07 | -0.02 |
| User feedback loop engagement | >50% | 35% | -15% |
| Model retraining frequency | Monthly | Quarterly | Improve |

### User Satisfaction

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Auto-routed items user keeps | >95% | % of items not archived within 7 days |
| Items user searches for | >20% | Items accessed >1 time |
| Alerts user acts on | >80% | % of critical alerts leading to action |
| User overrides system | <5% | % of decisions user reverses |
| User engagement with feedback | >60% | % of feedback form completions |

---

## Implementation Checklist

### Phase 1a (Week 1-2)
- [ ] Capture explicit user feedback (marks as relevant/irrelevant)
- [ ] Log all routing decisions to feedback table
- [ ] Calculate basic accuracy metrics (% correct routing)
- [ ] Display feedback summary to user (monthly digest)

### Phase 1b (Week 3)
- [ ] Capture implicit feedback (searches, links, access patterns)
- [ ] Derive signal strength from user behavior
- [ ] Identify false positives/negatives systematically
- [ ] Create recommendation engine (propose weight changes)

### Phase 1c (Week 4)
- [ ] Implement user approval workflow for changes
- [ ] Deploy approved weight/threshold changes
- [ ] Test retraining pipeline (manual, not automatic)
- [ ] Generate monthly calibration reports

### Phase 2
- [ ] Automate model retraining (local Mistral 7B)
- [ ] Implement A/B testing for major changes
- [ ] Add feature importance analysis (which features most predictive?)
- [ ] Enable temporal feedback (seasonality, concept drift)

---

## Non-Negotiable Principles

1. **User is the source of truth** — system improves by learning from user feedback
2. **No silent changes** — weight/threshold changes require user approval
3. **Improvement is measurable** — every change includes before/after metrics
4. **Learning is continuous** — monthly calibration as baseline
5. **Failure is visible** — false positives and negatives are tracked explicitly
6. **Feedback is actionable** — system proposes specific improvements with rationale

---

## Analogy: AI Lifecycle Management

This feedback loop is the PCA implementation of responsible AI practices:

| Responsibility | PCA Implementation | Purpose |
|---|---|---|
| **Monitoring** | Weekly accuracy metrics | Know when system degrades |
| **Validation** | User feedback collection | Verify predictions are correct |
| **Correction** | Weight adjustment workflow | Fix systematic errors |
| **Learning** | Monthly retraining | Adapt to user's evolving context |
| **Transparency** | Change approval process | User understands and controls improvements |
| **Governance** | Audit trail of all changes | Enable compliance and forensics |

This is the feedback mechanism that makes AI systems trustworthy and improves them over time — exactly what HC/PHAC needs for their enterprise systems.

---

**Status**: Active specification (v1.0)

**Last Updated**: 2026-04-25

**Next**: Implement feedback capture mechanisms in n8n workflows

**Related**:
- pca-ingestion-patterns.md (patterns being improved)
- pca-control-plane-specification.md (policies being refined)
- pca-compliance-and-governance.md (audit and traceability)
