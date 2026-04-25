---
type: architecture-principle
created: 2026-04-25
updated: 2026-04-25
tags: [pca, ddv, validation, governance, control-plane]
status: active
---

# Disagreement-Driven Validation (DDV)

## Definition

A control pattern where multiple independent evaluators assess an item, and divergence between their outputs is treated as a **signal requiring escalation**, not as a problem to be resolved automatically.

## Purpose

Prevent silent misclassification and implicit automation failures by making uncertainty visible and actionable.

## Core Principle

> Disagreement is not a bug. It is valuable information about ambiguity.

Rather than asking "Which evaluator is right?", DDV asks: "Is there enough agreement to act safely?"

## Where It Lives in the Architecture

```
Capture → Classification → Validation → Routing → Storage
                        ↑
                 DDV lives here
                 (control plane, not intelligence layer)
```

Specifically: **Between classification and routing**

This is the decision point where the system decides whether to automate or escalate.

## Mechanism (Minimal Implementation)

### 1. Two Evaluators

- **Primary**: LLM classifier (semantic meaning, intent, project)
- **Secondary**: Validator (deterministic rules OR secondary LLM role)

No more than two for Phase 1. Enough to detect disagreement, simple to operate.

### 2. Agreement Model (Simple)

```
IF note_type matches AND project matches
  → HIGH agreement

ELSE IF one of {note_type, project} matches
  → MEDIUM disagreement

ELSE IF neither matches OR confidence gap > 0.2
  → HIGH disagreement
```

Keep it legible. No complex math.

### 3. Action Policy

| Agreement | Action | Rationale |
|-----------|--------|-----------|
| **HIGH** | Auto-route | Safe to automate |
| **MEDIUM** | Route + tag "review" | Escalate for human oversight |
| **HIGH** | Block move, tag "needs-triage" | Ambiguous case, requires human judgment |

## Implementation in n8n

**Create an explicit workflow node called "DDV Check"**

Not "if/else comparison." Not "validate outputs."

Call it what it is: **Disagreement-Driven Validation**

That naming anchors it in the system design.

### Node Logic

```
Input: [primary_classification, secondary_validation]

Agreement Check:
  IF primary.note_type == secondary.note_type
    AND primary.project == secondary.project
    AND abs(primary.confidence - secondary.confidence) < 0.2
  THEN
    agreement_level = "high"
    action = "auto_route"
  
  ELSE IF one matches
  THEN
    agreement_level = "medium"
    action = "route_with_review_tag"
  
  ELSE
  THEN
    agreement_level = "high_disagreement"
    action = "escalate_to_triage"

Output: {
  agreement_level,
  action,
  primary_output,
  secondary_output,
  disagreement_reason (if applicable)
}
```

## Metadata & Traceability

Every processed note carries DDV metadata:

```yaml
validation:
  primary_type: "idea"
  primary_project: "PATH-HAIL"
  primary_confidence: 0.74
  
  secondary_type: "strategy-note"
  secondary_project: "enterprise-ai"
  secondary_confidence: 0.69
  
  agreement_level: "high_disagreement"
  action: "escalate_to_triage"
  
  decision_timestamp: "2026-04-25T10:30:00Z"
  decision_path: "ddv_check → escalation_queue"
```

This enables:
- Auditability (full trace of decision)
- Learning signal (feedback on where disagreement occurs)
- Enterprise-grade traceability

## Why This Pattern Is Architecturally Strong

| Aspect | Weak Pattern | Strong Pattern (DDV) |
|--------|--------------|---------------------|
| **Uncertainty handling** | Try to eliminate | Detect, measure, act on |
| **Automation trigger** | Confidence threshold | Evaluator agreement |
| **Failure detection** | Hidden (silent failure) | Visible (escalation signal) |
| **Human placement** | All decisions OR emergencies | Ambiguous cases only |
| **Auditability** | Black-box confidence score | Explicit disagreement reason |
| **Feedback loop** | Limited | Rich (disagreement types, patterns, outcomes) |

## Alignment with Enterprise Patterns

This mirrors:
- **Dual review** in safety systems
- **Policy validation** in financial systems
- **Peer review** in scientific systems
- **Exception handling** in enterprise governance

DDV brings these proven patterns to knowledge architecture.

## Risk Surfaces (What Could Go Wrong)

### Risk 1: Both Evaluators Wrong (Same Blind Spot)

**If**: Primary and secondary share same base model or prompt family

**Then**: High agreement might be confidently wrong

**Mitigation**: Diversify evaluators (different models, different prompt families, different heuristics)

### Risk 2: Threshold Tuning Drifts

**If**: Agreement thresholds are hand-tuned without monitoring

**Then**: Escalation behavior becomes inconsistent

**Mitigation**: Track disagreement distribution; monitor escalation rates; version agreement rules

### Risk 3: Bottleneck If Too Much Escalates

**If**: Agreement rates drop below 70%

**Then**: Human review queue becomes overloaded

**Mitigation**: Set KPI for disagreement rate (<30%); if exceeded, diagnose and refine evaluators

## Evolution Path

### Phase 1: Foundation

- Two evaluators (primary LLM + rules)
- Simple agreement model
- Three-tier action policy
- Basic metadata logging

### Phase 2: Learning Loop

- Track disagreement patterns
- Analyze what causes escalation
- Refine prompts and rules based on patterns
- Monitor agreement rate as KPI

### Phase 3: Multi-Domain Tuning

- Domain-specific agreement thresholds
- Specialized evaluators for complex domains
- Formal feedback loop (human decisions → prompt augmentation)

## Operational Checklist

- [ ] Name this pattern explicitly in system design (DDV)
- [ ] Create n8n node called "DDV Check"
- [ ] Define agreement model (simple rules, not math-heavy)
- [ ] Implement action policy (three tiers)
- [ ] Add metadata to every processed note
- [ ] Monitor agreement rate as KPI
- [ ] Document disagreement patterns
- [ ] Version agreement rules for traceability
- [ ] Create escalation queue for high-disagreement cases

## Non-Negotiable Principles

1. **Disagreement is not a failure state.** It is a feature.
2. **Evaluators must be independent.** No shared context between primary and secondary.
3. **Agreement is not sufficient alone.** High agreement must also meet confidence threshold.
4. **Escalation is always an option.** Never force resolution of ambiguous cases.
5. **Every decision is logged.** Metadata enables learning and auditability.

## Relationship to Other Patterns

- **DDV ⊂ Disagreement-Driven Agentic Screening** — DDV is the operational implementation at the validation layer
- **DDV ⊂ Human-in-the-Loop Governance** — Escalation gates route uncertain cases to humans
- **DDV ⊂ Continuous Improvement** — Disagreement patterns become feedback signals

## Success Criteria

| Metric | Target | Why |
|--------|--------|-----|
| Agreement rate (high + medium) | >85% | Most notes classified confidently |
| Escalation rate | <15% | Serious disagreements caught |
| Auto-route accuracy | >95% | Routed notes are correct |
| False negatives | <2% | Misclassified notes are rare |
| Disagreement pattern tracking | 100% | All patterns logged for analysis |

---

**Status**: Active design principle (v1.0)

**Last Updated**: 2026-04-25

**Next Review**: After Phase 1a implementation (2 weeks)
