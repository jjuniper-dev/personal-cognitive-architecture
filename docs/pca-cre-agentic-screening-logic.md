---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, reconciliation, agentic-screening, logic-formalization]
status: active
---

# PCA Cognitive Reconciliation Engine — Disagreement-Driven Agentic Screening

## Overview

The Cognitive Reconciliation Engine implements the **Disagreement-Driven Agentic Screening Pattern** for robust decision assurance. Rather than relying on unreliable model confidence scores, the CRE infers genuine uncertainty from **independent agent disagreement**, enabling robust contradiction detection and belief evolution.

This formalization provides concrete decision logic, escalation rules, and human-in-the-loop controls for the reconciliation workflow.

## Pattern Definition

**Formal Name**: Disagreement-Driven Agentic Screening Pattern

**Plain Language**: Independent AI Review with Escalation Pattern

**Core Principle**: Use inter-agent disagreement (not model confidence) as the uncertainty signal for governance and escalation.

### Why This Architecture Matters

**Problem It Solves**: Most AI screening pipelines rely on a single model's confidence score—which is often poorly calibrated and can be confidently wrong.

**Solution**: Independent parallel agents review the same input. Disagreement signals real ambiguity requiring escalation. Agreement indicates convergence.

**Why It's Enterprise-Grade**:
- **Disagreement as signal**: Agent disagreement is a more defensible proxy for ambiguity than declared model confidence
- **Peer review analog**: Approximates dual review + adjudication (scientific review practice)
- **Strategic human placement**: Humans reserved for ambiguous cases, not every decision
- **Auditable triage**: Each decision traced to its pathway (auto-label, ensemble, human)
- **Governance alignment**: Separates decision-making from uncertainty estimation

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
  "overall_confidence": 0.0-1.0,
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

**Note on overall_confidence**: Aggregate confidence across all analyzed relationships and contradictions. Used by the Agreement Gate and Auto-Label logic to determine if convergent decisions are high-enough confidence to integrate without further review.

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

**Triggered When**: Screening Agent and Critical Agent agree **AND** combined confidence ≥ 0.80

**Outcome**: High-confidence integration without further review

**Actions**:
1. Label relationships with agreed classification
2. Update confidence scores based on convergence strength
3. Integrate to knowledge graph immediately
4. Log decision with audit trail
5. Monitor for future disconfirming evidence

**Confidence Formula** (Auto-Label):
```
combined_confidence = 
  (critical_agent.overall_confidence × 0.6) +
  (screening_agent.overall_confidence × 0.4) +
  convergence_bonus(+0.1 if both agents agree)

auto_label_eligible = 
  (agents_agree) AND (combined_confidence ≥ 0.80)

IF auto_label_eligible THEN
  → Integrate to graph
  → Use combined_confidence as integration confidence
ELSE
  → Route to Ensemble Arbitration (disagreement or low confidence)
```

**Critical Safeguard**: If both agents agree but combined confidence is below 0.80, escalate to Ensemble Arbitration rather than auto-labeling. This prevents low-confidence but convergent decisions from being integrated directly.

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

# Escalation policy: 50-66% consensus (0.5-0.66) must escalate
# Therefore: uncertainty >= 0.34 requires escalation
escalation_required = 
  uncertainty >= 0.34 OR critical_request_clarification
```

**Interpretation**:
- **Uncertainty = 0.0**: Perfect agent agreement (100% consensus) → Auto-label (if confidence ≥ 0.80)
- **Uncertainty ≤ 0.34**: >66% consensus → Ensemble resolution succeeds, integrate
- **Uncertainty 0.34-1.0**: 50-66% consensus → Escalate to human review
- **Uncertainty = 1.0**: Complete disagreement (50/50 tie) → Definite human review

**Policy Alignment**: This threshold ensures that any ensemble outcome with less than 66% consensus (50-66% range) is routed to human review per the documented escalation table.

## Risk Assessment & Mitigation

This is a strong architecture, but not magic. Known risks and mitigations:

### Risk 1: Correlated Failure (Both Agents Wrong)

**Risk**: If both agents share the same base model, prompt family, or blind spots, agreement may still be wrong.

**Severity**: Medium-High (silent failure risk)

**Mitigation**:
- Diversify base models where feasible (GPT-4 + Claude, for example)
- Use different prompt families or temperature settings
- Document agent architecture (what model, what prompts, what settings)
- Monitor for persistent agreement-on-wrong cases (post-human-review analysis)
- Consider ensemble with a third independent agent for high-stakes cases

### Risk 2: Ensemble Instability

**Risk**: Randomized majority voting can drift if the case is poorly framed or task instructions are ambiguous.

**Severity**: Low-Medium (detectable through disagreement rate tracking)

**Mitigation**:
- Track persistent disagreement classes (which topics consistently cause disagreement)
- Refine task instructions and exclusion criteria for high-disagreement domains
- Increase ensemble runs (N=5-7) for borderline cases
- Add task exemplars to prompts to clarify edge cases
- Monitor ensemble stability over time

### Risk 3: Prompt Augmentation Drift

**Risk**: RLHF-Lite via prompt augmentation is useful, but can become messy over time (undocumented changes, inconsistent guidance).

**Severity**: Low (manageable with versioning)

**Mitigation**:
- Version all prompts (e.g., `screening-v1.2.3`)
- Log all prompt changes with rationale
- Test augmented prompts before promoting to production
- Maintain a canonical "baseline" prompt for comparison
- Review prompt drift quarterly

### Risk 4: Escalation Bottleneck

**Risk**: If too many cases escalate to human review, the efficiency gain collapses and the system becomes a human-annotation tool.

**Severity**: Medium (operational viability concern)

**Mitigation**:
- Track disagreement rate as a platform KPI (target: <20% escalation)
- Monitor whether disagreement rate increases over time
- Analyze escalated cases to identify systematic failure modes
- Invest in agent improvement (better prompts, better retrieval) for high-escalation domains
- Set escalation budget (if >25% escalate, pause and diagnose)

## Implementation Checklist

- [ ] Implement Screening Agent with fast retrieval (3-5 hop neighborhood)
- [ ] Implement Critical Agent with deep analysis (full graph traversal)
- [ ] **Add overall_confidence to both agent outputs**
- [ ] Create Agreement Gate with confidence floor check (≥ 0.80)
- [ ] Implement Ensemble Arbitration (multi-run voting)
- [ ] **Set escalation threshold to >= 0.34 (50-66% consensus)**
- [ ] Build Human Review interface and logging
- [ ] Implement RLHF-Lite feedback loop with prompt versioning
- [ ] Create audit trail logging for all decisions (including decision pathway)
- [ ] Build monitoring dashboard (agent agreement rates, escalation frequency, disagreement classes)
- [ ] Define prompt augmentation pipeline with change logging
- [ ] Test disagreement patterns and resolution quality
- [ ] **Set up risk monitoring (correlated failures, ensemble stability, prompt drift, escalation bottleneck)**

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
