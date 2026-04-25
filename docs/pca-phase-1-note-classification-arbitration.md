---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, phase-1, ingestion, classification, arbitration]
status: active
---

# Phase 1: Note Classification & Arbitration

## Overview

Phase 1 MVP is: **n8n → Obsidian → structured note in vault**

The critical decision point is not retrieval or reasoning—it is **note classification and routing**.

When a new note arrives in Inbox, the system must decide:
- What kind of note is this?
- What project does it belong to?
- Where should it live?
- Should it be auto-routed or held for review?

This document applies the **Disagreement-Driven Agentic Screening Pattern** to note classification, using **decision corroboration** (multiple evaluators) instead of single-agent trust.

## Trust Models: Which One to Use

### Model 1: Single-Agent Trust

One classifier decides everything:
- note_type
- project
- tags
- destination

**Problem**: Silent failure. Model is wrong, moves note to wrong place, note disappears.

**Use**: Not recommended for operational ingestion.

### Model 2: Rule-Plus-Agent Trust

LLM proposes; deterministic rules validate or constrain.

**Approach**:
- LLM: "What is this note about?"
- Rules: "Does it match known patterns?"
- Intersection: Route if both agree, review if diverge

**Strength**: Catches many errors, adds transparency

**Weakness**: Rules are static; can miss novel patterns that LLM recognizes

### Model 3: Multi-Agent Adjudication (Recommended for Phase 1)

Multiple evaluators review the same note. Disagreement becomes a signal.

**Approach**:
- Agent A (semantic): "What does this note mean?"
- Agent B (action): "What should happen operationally?"
- Agent C (taxonomy): "Does this fit known structures?"
- Comparison: Agreement → automate; disagreement → review

**Strength**: Catches both silent failures and novel cases. Transparent, auditable, scalable.

---

## Phase 1 Implementation: Option B (Recommended)

### Architecture

```
Inbox Note
    ↓
┌─────────────────────────────────────────┐
│  Stage 1: Semantic Classification       │
│  ├─ Primary LLM: Semantic meaning       │
│  │  (note_type, project, confidence)    │
│  └─ Secondary LLM: Action intent        │
│     (operational intent, confidence)    │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Stage 2: Deterministic Validation      │
│  ├─ Rule engine: Pattern matching       │
│  │  (contains action verbs, person      │
│  │   names, explicit deadlines, etc.)   │
│  ├─ Taxonomy checker: Known projects    │
│  │  (folders, naming conventions)       │
│  └─ Context retrieval: Prior history    │
│     (similar notes, past projects)      │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Stage 3: Agreement Scoring             │
│  ├─ Compare semantic + action + rules   │
│  ├─ Calculate agreement score           │
│  └─ Apply routing policy                │
└─────────────┬───────────────────────────┘
              ↓
        ┌─────┴─────┬──────────┐
        ↓           ↓          ↓
   ┌─────────┐ ┌──────────┐ ┌──────────────┐
   │Auto-    │ │Review    │ │Escalate/     │
   │Route    │ │Tag +     │ │Block Auto-   │
   │(High    │ │Route     │ │Route (Strong │
   │Agree)   │ │(Mild     │ │Disagreement) │
   │         │ │Disagree) │ │              │
   └─────────┘ └──────────┘ └──────────────┘
        ↓           ↓          ↓
   Destination  Inbox +    Manual Review
   Folder       Review     Queue
               Tag
```

### Stage 1: Semantic Classification

**Primary Agent**: Semantic Classifier

Role: Understand the meaning of the note

Input:
```
{
  "note_id": "uuid",
  "content": "string",
  "source": "string (capture source)",
  "timestamp": "ISO-8601"
}
```

Output:
```json
{
  "agent": "semantic_classifier",
  "note_id": "uuid",
  "classification": {
    "note_type": "task|meeting|idea|reference|decision|project-note|strategy-note|research",
    "project": "string (inferred project name)",
    "tags": ["string"],
    "confidence": 0.0-1.0
  },
  "reasoning": "string",
  "suggested_destination": "/string/path/in/vault"
}
```

**Secondary Agent**: Action Intent Classifier

Role: Understand what should happen operationally

Output:
```json
{
  "agent": "action_classifier",
  "note_id": "uuid",
  "classification": {
    "action_type": "task|decision|follow-up|research|reference|no-action",
    "primary_actor": "string (who should act, if known)",
    "deadline": "ISO-8601 or null",
    "priority": "low|medium|high",
    "confidence": 0.0-1.0
  },
  "reasoning": "string"
}
```

### Stage 2: Deterministic Validation

**Rule Engine**: Pattern Matching

Inspect note content for explicit signals:

```
Patterns (weighted):
├─ Action signals (HIGH)
│  ├─ "need to", "must", "have to", "should"
│  ├─ "follow up", "follow-up", "FYI"
│  ├─ task emoji or #task tag
│  └─ weight: +0.2 confidence for task classification
├─ Person signals (MEDIUM)
│  ├─ Named people (Chad, Jordan, etc.)
│  ├─ role references (stakeholder, reviewer, etc.)
│  └─ weight: +0.1 confidence for task/decision
├─ Deadline signals (HIGH)
│  ├─ date references (before X, by EOW, etc.)
│  ├─ urgency markers (URGENT, asap)
│  └─ weight: +0.15 confidence for task
└─ Project signals (MEDIUM)
   ├─ known project names (PATH-HAIL, etc.)
   ├─ folder patterns
   └─ weight: +0.1 confidence in project inference

Output:
{
  "rule_check": "pass|flag|fail",
  "detected_patterns": ["action-verb", "person-name", "deadline"],
  "confidence_adjustment": +0.15,
  "suggested_type": "task|idea|reference"
}
```

**Taxonomy Checker**: Known Structures

Check if inferred project/folder exists in Obsidian:

```
{
  "project_exists": boolean,
  "folder_exists": boolean,
  "naming_match": 0.0-1.0,
  "confidence_adjustment": -0.1 if unknown, +0.1 if known
}
```

**Context Retrieval**: Prior History (Optional for Phase 1)

If available, check similar past notes:

```
{
  "similar_notes_found": number,
  "common_classification": "string",
  "consistency_score": 0.0-1.0
}
```

### Stage 3: Agreement Scoring

**Agreement Formula**:

```
agreement_score = 
  weighted_average([
    semantic_note_type == action_type ? 0.3 : 0.0,
    abs(semantic_confidence - action_confidence) < 0.15 ? 0.2 : 0.0,
    rule_check == "pass" ? 0.2 : 0.0,
    project_exists ? 0.15 : 0.0,
    semantic_project == action_project ? 0.15 : 0.0
  ])

# Result: 0.0-1.0 agreement score
```

**Routing Policy**:

```
IF agreement_score >= 0.85 AND semantic_confidence >= 0.80 THEN
  → Auto-route to destination
  → No review needed
  → action: AUTO_ROUTE

ELSE IF agreement_score >= 0.65 AND semantic_confidence >= 0.70 THEN
  → Route to project
  → Add "review" tag
  → action: ROUTE_WITH_TAG

ELSE IF note_type == sensitive_domain THEN
  → Block auto-route
  → Escalate to review queue
  → action: ESCALATE_SENSITIVE

ELSE IF agreement_score < 0.65 OR semantic_confidence < 0.65 THEN
  → Keep in Inbox
  → Add "review" tag
  → action: HOLD_FOR_REVIEW

ELSE (strong disagreement or ambiguity)
  → Escalate to manual review
  → action: ESCALATE_MANUAL
```

---

## Decision Arbitration Schema

Every note classification decision must be logged with this schema:

```json
{
  "decision_id": "uuid",
  "note_id": "uuid",
  "timestamp": "ISO-8601",
  "content_hash": "sha256",
  
  "semantic_classification": {
    "note_type": "string",
    "project": "string",
    "confidence": 0.0-1.0
  },
  
  "action_classification": {
    "action_type": "string",
    "deadline": "ISO-8601 or null",
    "confidence": 0.0-1.0
  },
  
  "rule_check": {
    "patterns_detected": ["string"],
    "confidence_adjustment": -0.3 to +0.3,
    "pass": boolean
  },
  
  "agreement_score": 0.0-1.0,
  "final_action": "AUTO_ROUTE|ROUTE_WITH_TAG|HOLD_FOR_REVIEW|ESCALATE_SENSITIVE|ESCALATE_MANUAL",
  
  "destination": "/vault/path or null",
  "review_required": boolean,
  
  "human_review": {
    "reviewer": "string or null",
    "review_timestamp": "ISO-8601 or null",
    "decision": "accept|reject|modify",
    "reasoning": "string or null"
  },
  
  "tags": ["string"]
}
```

---

## Examples

### Example 1: Clear Task (High Agreement)

**Note Content**:
```
Need to send Chad the revised PATH/HAIL convergence framing before ARB
```

**Semantic Classifier**:
- note_type: task
- project: PATH-HAIL
- confidence: 0.88

**Action Classifier**:
- action_type: task
- primary_actor: Chad
- deadline: (inferred from "before ARB")
- confidence: 0.84

**Rule Check**:
- Patterns: "need to", person name "Chad", deadline context
- Pass: true
- Adjustment: +0.15

**Taxonomy Check**:
- project_exists: true (PATH-HAIL folder known)
- folder_exists: true (/10-Projects/PATH-HAIL/Tasks)
- Adjustment: +0.1

**Agreement Score**:
- (0.88 + 0.84) / 2 = 0.86 base
- Plus rule pass: +0.2
- Plus taxonomy match: +0.1
- **Final: 0.92**

**Routing Decision**: ✅ **AUTO_ROUTE** to `/10-Projects/PATH-HAIL/Tasks`

---

### Example 2: Ambiguous Strategic Note (Low Agreement)

**Note Content**:
```
PATH may need a different governance narrative if HAIL remains the operational entry point
```

**Semantic Classifier**:
- note_type: idea
- project: PATH-HAIL
- confidence: 0.74

**Action Classifier**:
- action_type: strategy-note
- project: enterprise-ai (or PATH-HAIL?)
- confidence: 0.69

**Rule Check**:
- Patterns: none detected (no explicit action verbs, no people, no deadlines)
- Pass: false
- Adjustment: -0.1

**Taxonomy Check**:
- project_exists: yes (PATH-HAIL)
- But project from action_classifier: enterprise-ai (also exists)
- Mismatch
- Adjustment: -0.05

**Agreement Score**:
- Semantic: idea vs. Action: strategy-note (disagreement) → -0.1
- Confidence gap: 0.74 vs 0.69 (small) → +0.05
- Rule fail: -0.1
- Project mismatch: -0.05
- **Final: 0.52**

**Routing Decision**: ⚠️ **HOLD_FOR_REVIEW**
- Add tag: "review"
- Stays in Inbox
- Note: "Semantic classifier says PATH-HAIL idea; action classifier says enterprise-ai strategy. No clear action signals. Needs human judgment on project placement."

---

## Phase 1 Success Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Auto-route rate | 70-80% | Most notes routed automatically |
| Review-tag rate | 15-25% | Mild disagreement caught |
| Escalation rate | <5% | Serious issues caught |
| Auto-route accuracy | >95% | Routed notes are correct |
| False negatives | <2% | Misclassified notes are rare |

---

## Implementation Roadmap

### Phase 1a: Foundation (Week 1-2)
- [ ] Implement semantic classifier (LLM prompt)
- [ ] Implement action classifier (LLM prompt)
- [ ] Define rule engine patterns
- [ ] Create decision arbitration schema
- [ ] Build n8n workflow for classification pipeline

### Phase 1b: Validation (Week 3)
- [ ] Test with 50 manual notes from Inbox
- [ ] Measure agreement scores
- [ ] Calibrate confidence thresholds
- [ ] Tune rule patterns

### Phase 1c: Deployment (Week 4)
- [ ] Deploy to live ingestion
- [ ] Monitor agreement scores
- [ ] Log all decisions to audit trail
- [ ] Prepare for human review queue

### Phase 1d: Feedback Loop (Ongoing)
- [ ] Collect human review decisions
- [ ] Analyze where disagreements occur
- [ ] Refine prompts based on patterns
- [ ] Update rules for new domains

---

## Why This Design Works for Phase 1

1. **Practical**: Uses proven components (LLM + rules + taxonomy)
2. **Safe**: Disagreement triggers review, not auto-routing
3. **Transparent**: Every decision logged and auditable
4. **Scalable**: Humans review only ambiguous cases
5. **Improvable**: Feedback loop built in
6. **Enterprise-Grade**: Mirrors real control patterns
7. **Aligned**: Uses same Disagreement-Driven pattern as CRE

This bridges strategic architecture to operational reality.
