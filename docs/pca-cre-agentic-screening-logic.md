---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, reconciliation, agentic-screening, logic-formalization]
status: active
---

# PCA Cognitive Reconciliation Engine — Agentic Screening Logic

## Overview

The Cognitive Reconciliation Engine implements the **Agentic Screening Pattern** for disagreement-driven decision assurance. Rather than relying on model confidence scores, the CRE infers uncertainty from **independent agent disagreement**, enabling robust contradiction detection and belief evolution.

This formalization provides concrete decision logic, escalation rules, and human-in-the-loop controls for the reconciliation workflow.

## Core Pattern: Disagreement-Driven Assurance

```
Input (New Knowledge) 
    ↓
┌─────────────────────────────────────────┐
│  Stage 1: Parallel Independent Review   │
│  ├─ Screening Agent (fast review)       │
│  └─ Critical Agent (deep analysis)      │
│  (No shared context between agents)     │
└─────────────────┬───────────────────────┘
                  ↓
         ┌────────────────────┐
         │ Agreement Gate     │
         │ Do agents agree?   │
         └────────┬───────┬──┘
              Yes │       │ No
                  ↓       ↓
            ┌─────────┐ ┌──────────────────────┐
            │Auto-    │ │Ensemble Arbitration  │
            │Label    │ │(Multi-run voting)    │
            │(High    │ └─────────┬────────────┘
            │Conf)    │           ↓
            └────┬────┘    ┌──────────────┐
                 ↓         │ Resolved?    │
            ┌─────────┐    └────┬─────┬───┘
            │Integrate │       Yes│    │No
            │to Graph  │         ↓    ↓
            └──────────┘    ┌────────────────────┐
                            │ Human Review       │
                            │ (Final Authority)  │
                            └────────┬───────────┘
                                     ↓
                            ┌────────────────────┐
                            │ Update Graph       │
                            │ + Feedback Loop    │
                            │ (RLHF-Lite)       │
                            └────────────────────┘
```

## Stage 1: Parallel Independent Review

### Screening Agent

**Role**: Fast, lightweight evaluation of new input against knowledge graph

**Responsibilities**:
- Retrieve semantically related nodes (3-5 hops, constrained scope)
- Classify relationship type (reinforcement/challenge/expansion/novel/null)
- Assign preliminary relationship strength (-1.0 to +1.0)
- Flag obvious contradictions (high confidence mismatch)
- Return decision: **Accept** or **Escalate**

**Latency SLA**: < 1 second

**Output Schema**:
```json
{
  "agent_type": "screening",
  "input_id": "uuid",
  "related_nodes": [
    {
      "node_id": "uuid",
      "relationship_type": "reinforcement|challenge|expansion|novel|null",
      "relationship_strength": -1.0 to +1.0,
      "confidence": 0.0-1.0
    }
  ],
  "contradictions_detected": [
    {
      "conflicting_nodes": ["uuid", "uuid"],
      "severity": "low|medium|high",
      "explanation": "string"
    }
  ],
  "preliminary_decision": "accept|escalate",
  "reasoning": "string"
}
```

### Critical Agent

**Role**: Deep, comprehensive analysis using full knowledge graph context

**Responsibilities**:
- Full knowledge graph traversal (all domains, unrestricted scope)
- Multi-hop relationship analysis (5+ hops, chains of reasoning)
- Retrieve supporting and contradicting evidence for each relationship
- Calculate impact propagation (how downstream nodes are affected)
- Assess contradiction severity and scope
- Return decision: **Accept**, **Escalate**, or **Request_Clarification**

**Latency SLA**: < 3 seconds

**Output Schema**:
```json
{
  "agent_type": "critical",
  "input_id": "uuid",
  "comprehensive_analysis": {
    "direct_relationships": [
      {
        "node_id": "uuid",
        "relationship_type": "reinforcement|challenge|expansion|novel|null",
        "supporting_evidence": ["source1", "source2"],
        "contradicting_evidence": ["source3"],
        "confidence": 0.0-1.0
      }
    ],
    "cascading_effects": [
      {
        "affected_domain": "string",
        "impact_type": "reinforces|challenges|requires_restructure",
        "confidence": 0.0-1.0
      }
    ],
    "contradiction_analysis": {
      "total_contradictions": number,
      "high_severity_count": number,
      "system_wide_scope": boolean,
      "recommendation": "accept|escalate|restructure"
    }
  },
  "final_decision": "accept|escalate|request_clarification",
  "confidence": 0.0-1.0,
  "reasoning": "string"
}
```

## Stage 2: Agreement Gate

**Decision Logic**:

```
IF screening_decision == critical_decision THEN
  → Proceed to Auto-Label (agreement = high confidence)
  → Uncertainty Signal: LOW
  
ELSE IF screening_decision != critical_decision THEN
  → Proceed to Ensemble Arbitration (disagreement = uncertainty)
  → Uncertainty Signal: HIGH
  
IF critical_agent.final_decision == "request_clarification" THEN
  → Regardless of screening agent decision
  → Escalate to Human Review with clarification request
```

**Key Principle**: Disagreement is a signal of genuine uncertainty, not unreliable models. The system treats disagreement as valuable information requiring deeper investigation.

## Stage 3A: Auto-Label (Agreement Path)

**Triggered When**: Screening Agent and Critical Agent agree

**Outcome**: High-confidence integration without further review

**Actions**:
1. Label relationships with agreed classification
2. Update confidence scores based on convergence strength
3. Integrate to knowledge graph immediately
4. Log decision with audit trail
5. Monitor for future disconfirming evidence

**Confidence Formula** (Auto-Label):
```
confidence = 
  (critical_agent.confidence × 0.6) +
  (screening_agent.confidence × 0.4) +
  convergence_bonus(+0.1 if both agents agree)
```

**Example**:
```json
{
  "decision_type": "auto_label",
  "input_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "accept",
  "reasoning": "Both agents independently identified this as 'expansion' with high confidence (screening: 0.88, critical: 0.91). Convergence indicates genuine relationship.",
  "confidence": 0.92,
  "integration_target": "node-health-policy-023",
  "timestamp": "2026-04-25T10:30:00Z"
}
```

## Stage 3B: Ensemble Arbitration (Disagreement Path)

**Triggered When**: Screening Agent and Critical Agent disagree on relationship type or severity

**Outcome**: Multi-run voting to resolve disagreement before escalation

**Process**:

1. **Generate Ensemble** — Run both agents again (N=3-5 runs each) with different retrieval contexts
2. **Aggregate Decisions** — Collect all responses
3. **Probabilistic Majority Vote**:
   ```
   winning_decision = argmax(
     count(agent_decision) / total_runs
   )
   confidence = winning_count / total_runs
   ```
4. **Apply Tie-Breaking Rules**:
   - If tie (50/50), escalate to Human Review
   - If > 66% consensus, proceed to integrated outcome
   - If 50-66% consensus, escalate to Human Review

**Ensemble Output Schema**:
```json
{
  "decision_type": "ensemble_arbitration",
  "input_id": "uuid",
  "disagreement_summary": {
    "screening_agent_decisions": ["accept", "accept", "escalate"],
    "critical_agent_decisions": ["escalate", "escalate", "accept"]
  },
  "ensemble_runs": 5,
  "vote_distribution": {
    "accept": 2,
    "escalate": 3
  },
  "consensus_level": 0.6,
  "winning_decision": "escalate",
  "confidence": 0.6,
  "tie_breaking_applied": false,
  "next_action": "escalate_to_human_review"
}
```

## Stage 4: Resolution Gate

**Decision Logic**:

```
IF (auto_label OR ensemble_consensus_high) THEN
  → Integrate to knowledge graph
  → Confidence: auto_label_confidence OR ensemble_confidence
  → Logging: Complete audit trail with agent decisions

ELSE IF (ensemble_tie OR ensemble_consensus_medium) THEN
  → Route to Human Review
  → Provide: Full agent reasoning, disagreement summary, evidence
  → Escalation Priority: High

ELSE IF (critical_agent.request_clarification) THEN
  → Route to Human Review
  → Request: Specific clarification from human operator
  → Clarification Points: From critical agent analysis
```

## Stage 5: Human Review (High-Impact Path)

**Triggered When**:
- Agent disagreement unresolved by ensemble
- Critical agent requests clarification
- Contradiction severity is high
- System-wide cascading effects detected
- Novel input challenges foundational beliefs

**Human Review Inputs**:
1. Complete agent reasoning from both agents
2. Ensemble voting results
3. Evidence supporting each decision
4. Contradiction analysis
5. Cascading effect assessment
6. Clarification request (if any)

**Human Review Decision Options**:
- **Accept** — Integrate input, update graph
- **Request_Clarification** — Ask operator for additional context
- **Restructure** — Existing knowledge needs reorganization
- **Reject** — Input is unreliable or outdated
- **Flag_for_Research** — Mark for future investigation

**Feedback Loop (RLHF-Lite)**:
```
Human Decision → Analyzed Against Agent Reasoning
                ↓
        Disagreement Patterns
                ↓
        Prompt Augmentation
                ↓
        Update Agent Instructions
                ↓
        Improve Future Screening/Critical Decisions
```

**Human Review Output**:
```json
{
  "decision_type": "human_review",
  "input_id": "uuid",
  "human_reviewer": "operator_id",
  "review_timestamp": "ISO-8601",
  "human_decision": "accept|reject|request_clarification|restructure|flag_for_research",
  "human_reasoning": "string",
  "confidence_override": 0.0-1.0,
  "feedback_for_agents": "string",
  "follow_up_actions": ["action1", "action2"]
}
```

## Stage 6: Integration & Feedback Loop

### Knowledge Graph Integration

**Accepted Inputs** (from Auto-Label, Ensemble, or Human Review):
1. Create or update relationship nodes
2. Store confidence score (from winning decision pathway)
3. Tag with relationship type and evidence links
4. Log complete decision trail (agent reasoning, votes, human approval)
5. Set up monitoring for contradicting evidence

**Rejected Inputs**:
1. Store in dispute log
2. Mark as "contested" or "outdated"
3. Flag related nodes for re-evaluation
4. Create research task if needed

### Feedback Loop

**Purpose**: Improve agent decision-making over time through human oversight

**Mechanism**:
1. Compare agent disagreements against human final decision
2. Identify patterns in agent errors
3. Augment system prompts with clarifying examples
4. Update agent instructions for similar future cases
5. Monitor improvement in agent agreement rates

**Example Loop**:
```
Agents: disagreed on "health-policy" domain relationship
Human:  determined it was "expansion", not "contradiction"

→ Analyze: Agents under-weighted domain-specific evidence
→ Update: Add health-policy-specific reasoning examples to prompts
→ Monitor: Track agent agreement improvement on similar inputs
```

## Escalation Thresholds

| Condition | Decision | Escalation |
|-----------|----------|-----------|
| Agents agree (>80% confidence) | Auto-Label | None |
| Agents disagree, >66% ensemble consensus | Ensemble | None |
| Agents disagree, 50-66% consensus | Ensemble | Human Review |
| Agents disagree, 50/50 tie | Ensemble | Human Review (Required) |
| Critical agent: request_clarification | N/A | Human Review (Required) |
| Contradiction severity: High | N/A | Human Review (Required) |
| System-wide cascading effects | N/A | Human Review (Required) |
| Novel input challenging foundational beliefs | N/A | Human Review (Required) |

## Uncertainty Measurement

**Key Insight**: Uncertainty is inferred from **agent disagreement**, not confidence scores alone

**Uncertainty Calculation**:
```
disagreement_rate = 
  (screening_decision != critical_decision) ? 1.0 : 0.0

ensemble_consensus = 
  max_vote_count / total_runs

uncertainty = 
  disagreement_rate × (1.0 - ensemble_consensus)

escalation_required = 
  uncertainty > 0.4 OR critical_request_clarification
```

**Interpretation**:
- **Uncertainty = 0.0**: Perfect agent agreement → Auto-label (high confidence)
- **Uncertainty = 0.2-0.4**: Mild disagreement → Ensemble resolution usually succeeds
- **Uncertainty = 0.4-0.8**: Significant disagreement → Likely human review needed
- **Uncertainty > 0.8**: Severe disagreement → Definite human review + research task

## Implementation Checklist

- [ ] Implement Screening Agent with fast retrieval (3-5 hop neighborhood)
- [ ] Implement Critical Agent with deep analysis (full graph traversal)
- [ ] Create Agreement Gate logic
- [ ] Implement Ensemble Arbitration (multi-run voting)
- [ ] Build Human Review interface and logging
- [ ] Implement RLHF-Lite feedback loop
- [ ] Create audit trail logging for all decisions
- [ ] Build monitoring dashboard (agent agreement rates, escalation frequency)
- [ ] Define prompt augmentation pipeline
- [ ] Test disagreement patterns and resolution quality

## Success Criteria

1. **Agent Agreement Rate**: >80% for low-impact inputs (auto-label pathway)
2. **Ensemble Resolution**: >85% of disagreements resolved without human review
3. **Escalation Quality**: Human review required only for genuinely ambiguous cases
4. **Feedback Loop Effectiveness**: Agent agreement rate improves over time
5. **Contradiction Detection**: >95% precision in detecting material contradictions
6. **Latency**: Screening + Critical agents complete within 4 seconds (SLA: <1s + <3s)
7. **Auditability**: 100% of decisions traceable to agent reasoning and evidence

## Comparison to Confidence-Based Approach

| Aspect | Traditional Confidence | Disagreement-Driven |
|--------|------------------------|-------------------|
| **Uncertainty Signal** | Model probability score | Agent disagreement |
| **Robustness** | Single model; calibration unclear | Multiple independent agents |
| **Failure Detection** | Missed when model is confidently wrong | Caught by agent disagreement |
| **Human Escalation** | Threshold-based (confidence < X) | Disagreement-based (agents disagree) |
| **Feedback Loop** | Limited to retraining | Explicit RLHF-Lite + prompt augmentation |
| **Auditability** | Black-box confidence score | Transparent agent reasoning |

---

This formalization enables the PCA to implement **genuine cognitive reconciliation** through independent reasoning agents, disagreement-driven escalation, and human-in-the-loop governance.
