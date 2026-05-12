---
type: architecture
version: Phase-2
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [runtime, policy, authorization, approval, escalation, governance]
---

# PCA Runtime Policy Gate

## Executive Summary

The Runtime Policy Gate operationalizes the Policy Gate and Escalation Framework components of the Cognitive Control Plane. It defines:

- **Policy Definition Language** — How policies are written, versioned, and evaluated
- **Approval Tiers** — Three-tier approval model (Routine/Sensitive/Critical)
- **Escalation Triggers** — When and how decisions bubble to humans
- **HITL Workflows** — Structured human-in-the-loop approval processes
- **Trust Thresholds** — Quantitative gates for automatic vs. gated vs. manual decisions
- **Compliance & Audit** — How approval decisions are logged and audited

This document transforms "policy evaluates rules" (conceptual) into "here's how to write policies, evaluate them, escalate them, and audit them" (operational).

---

## Policy Definition Language

Policies are written in YAML, version-controlled, and queryable. Each policy is atomic and independently deployable.

### Policy Structure

```yaml
---
policy_id: "POL-XXXX-[short-name]"
version: "1.0"
created: "2026-05-12"
last_updated: "2026-05-12"
status: "active"  # active | archived | draft | superseded_by

# Scope: which requests does this policy apply to?
applies_to:
  agent: "*"           # specific agent name or "*" for all
  tool: "Neo4j"        # specific tool or "*" for all
  operation: "WRITE"   # READ | WRITE | DELETE | * for all
  sensitivity: "SENSITIVE"  # ROUTINE | SENSITIVE | CRITICAL | *
  resource: "*"        # specific resource pattern or "*"

# Effect: what is the decision?
effect: "ALLOW"  # ALLOW | DENY | ESCALATE_TO_HUMAN | ESCALATE_TO_ENGINEERING

# Constraints: restrictions on the allowed action
constraints:
  max_concurrent: 4
  rate_limit: "100/hour"
  max_tokens: 10000
  timeout_seconds: 30
  resource_limit: "50 MB"

# Conditions: additional predicates
conditions:
  trust_threshold: 80    # minimum confidence required
  agent_agreement: true  # if true, requires dual-agent alignment
  requires_approval: false

# Escalation: if effect is escalate, who and how?
escalation:
  recipient: "user"  # user | engineering | both
  priority: "medium"  # low | medium | high | critical
  timeout_hours: 24
  repeat_if_no_response: true

# Audit metadata
policy_owner: "Engineering Lead"
review_frequency: "quarterly"
last_reviewed: "2026-05-12"
next_review: "2026-08-12"

# Notes: human-readable rationale
notes: |
  Neo4j WRITE operations require HITL approval to prevent accidental
  data corruption. READ-only operations are auto-approved under policy POL-0001.
```

### Policy Inheritance

Policies are evaluated in **priority order**, with the first matching rule determining the result:

```
1. Most specific policies (agent + tool + operation + sensitivity + resource)
2. Tool-specific policies (agent + tool + operation)
3. Operation policies (operation + sensitivity)
4. Broad policies (sensitivity only)
5. Default policy (applies to all)

If no policy matches → DEFAULT_DENY
```

### Policy Examples

#### Example 1: Screening Agent Neo4j READ Access (ROUTINE)

```yaml
policy_id: "POL-0001-agent-neo4j-read"
version: "1.0"
created: "2026-05-12"
status: "active"

applies_to:
  agent: "Screening Agent"
  tool: "Neo4j"
  operation: "READ"
  sensitivity: "ROUTINE"

effect: "ALLOW"

constraints:
  max_concurrent: 4
  rate_limit: "1000/hour"
  timeout_seconds: 10

conditions:
  trust_threshold: 0  # No threshold for routine read

notes: |
  Screening Agent can READ from Neo4j without approval.
  Standard rate limits apply. No trust threshold required.
```

#### Example 2: No WRITE Without HITL (SENSITIVE/CRITICAL)

```yaml
policy_id: "POL-0002-no-write-without-approval"
version: "1.0"
created: "2026-05-12"
status: "active"

applies_to:
  tool: "Neo4j"
  operation: "WRITE"
  sensitivity: "*"

effect: "ESCALATE_TO_HUMAN"

conditions:
  requires_approval: true

escalation:
  recipient: "user"
  priority: "high"
  timeout_hours: 4

notes: |
  All WRITE operations to Neo4j require explicit human approval.
  This prevents accidental data corruption or unauthorized changes.
```

#### Example 3: Knowledge Contradiction Detection (CRITICAL)

```yaml
policy_id: "POL-0003-contradiction-escalation"
version: "1.0"
created: "2026-05-12"
status: "active"

applies_to:
  sensitivity: "CRITICAL"
  decision_type: "knowledge_integration"

conditions:
  contradiction_detected: true
  agent_agreement: false

effect: "ESCALATE_TO_HUMAN"

escalation:
  recipient: "user"
  priority: "critical"
  timeout_hours: 2
  summary_required: true

notes: |
  Contradictions between new and existing knowledge are escalated
  for human review and decision. This prevents corrupting knowledge graph.
```

#### Example 4: Cloud Burst Authorization (CRITICAL)

```yaml
policy_id: "POL-0004-cloud-burst-approval"
version: "1.0"
created: "2026-05-12"
status: "active"

applies_to:
  decision_type: "cloud_inference"
  sensitivity: "CRITICAL"

conditions:
  cost_exceeds: 5.00  # CAD $5 threshold

effect: "ESCALATE_TO_HUMAN"

escalation:
  recipient: "user"
  priority: "high"
  timeout_hours: 1
  cost_disclosure: true

constraints:
  daily_budget_limit: 20.00  # CAD $20/day max

notes: |
  Cloud inference requests exceeding $5 require user approval.
  Daily budget cap enforced at $20. Prevents cost surprises.
```

#### Example 5: Confidence Gate (SENSITIVE)

```yaml
policy_id: "POL-0005-confidence-gate-sensitive"
version: "1.0"
created: "2026-05-12"
status: "active"

applies_to:
  sensitivity: "SENSITIVE"

effect: "ALLOW if confidence >= threshold else ESCALATE_TO_HUMAN"

conditions:
  trust_threshold: 70  # >=70 confidence = auto-allow
  agent_agreement: true  # Both agents must align

escalation:
  recipient: "user"
  priority: "medium"
  timeout_hours: 12

notes: |
  SENSITIVE decisions auto-approve if confidence >=70% AND agents agree.
  Below 70%, escalate to user for review. Prevents unnecessary HITL
  while catching high-uncertainty decisions.
```

---

## Approval Tiers

The control plane assigns three sensitivity levels; each has a different approval path.

### Tier 1: ROUTINE (Fast Path)

**Definition:** Low-consequence decisions with well-established policy.

**Examples:**
- Document scoring (< 5KB)
- Tag assignment from fixed taxonomy
- Routine retrieval queries
- Standard caching operations

**Approval Path:**

```
Request → Sensitivity Classifier: ROUTINE
         ↓
    Policy Gate Evaluation
    ↓
    Matches policy?
    ├─ Yes, effect=ALLOW → Execute (no human gate)
    ├─ Yes, effect=DENY → Escalate to user
    └─ No rule matches → DEFAULT_DENY

Execution Time: < 100ms
Human Involvement: None (unless policy violation)
```

**Example Policy:** POL-0001 (Screening Agent Neo4j READ)

---

### Tier 2: SENSITIVE (Gated)

**Definition:** Medium-consequence decisions where confidence/agreement matters.

**Examples:**
- Knowledge integration (new information vs. existing)
- Agent routing (which agent processes next)
- Model selection for boundary-case inputs
- Budget decisions < $5

**Approval Path:**

```
Request → Sensitivity Classifier: SENSITIVE
         ↓
    Policy Gate Evaluation
    ↓
    Trust Threshold Gate
    ├─ Confidence ≥70% AND agents agree
    │  → Auto-allow (with audit)
    ├─ Confidence 50-69% OR partial agreement
    │  → Policy-gated (check POL rules)
    └─ Confidence <50% OR major disagreement
       → Escalate to user (requires approval)

Execution Time: < 5 seconds
Human Involvement: Conditional (based on confidence)
```

**Decision Tree:**

```
IF confidence >= 80 AND agent_agreement = true:
  result = AUTO_APPROVE
  audit = record_auto_approval(request, confidence, agents)

ELIF confidence >= 60 AND agent_agreement = true:
  check_policy_gate()
  IF policy_gate = ALLOW:
    result = POLICY_GATED_ALLOW
  ELSE:
    result = ESCALATE_TO_USER

ELIF confidence < 60 OR agent_agreement = false:
  result = ESCALATE_TO_USER
  escalation = create_escalation(request, confidence, agreement_status)
```

**Example Policies:** POL-0005 (Confidence Gate), POL-0003 (Contradiction Detection)

---

### Tier 3: CRITICAL (Manual Review)

**Definition:** High-consequence decisions where humans have final authority.

**Examples:**
- Model contradictions (Sonnet vs. Haiku disagree >20 points)
- Knowledge contradiction (new belief conflicts with 95%+ confidence existing belief)
- User deletion (cascade impact on all knowledge graph)
- Automation changes (new agent, new tool permission, policy change)
- Cloud burst > $5

**Approval Path:**

```
Request → Sensitivity Classifier: CRITICAL
         ↓
    Create Escalation Record
    ↓
    Route to Recipient(s)
    ├─ User (if user decision required)
    └─ Engineering (if architectural decision required)
    ↓
    Human Reviews & Decides
    ├─ Approve → Execute with audit
    ├─ Reject → Record denial and reason
    └─ Request clarification → Query system
    ↓
    Execute or Archive

Execution Time: Variable (minutes to hours depending on urgency)
Human Involvement: Required (no automation bypass)
Timeout: 2 hours (critical) to 24 hours (standard)
```

**Decision Tree:**

```
IF decision_type IN (contradiction, model_disagreement, deletion, automation_change):
  escalation = create_escalation_record(
    decision=decision,
    summary=extract_summary(decision),
    confidence=confidence_score,
    reasoning=explain_why_critical()
  )
  send_to_user(escalation)
  
  WAIT for user_response timeout:
    IF user_approves:
      execute(decision)
      audit_record(APPROVED, user_id, timestamp)
    ELIF user_rejects:
      log_rejection(decision, reason)
      audit_record(REJECTED, user_id, timestamp)
    ELIF timeout_exceeded:
      escalate_to_engineering("User did not respond to critical decision")
```

**Example Policies:** POL-0002 (WRITE No-Approval), POL-0003 (Contradiction), POL-0004 (Cloud Burst)

---

## Escalation Triggers & Routing

When a decision cannot be automatically approved, it escalates to humans. Each trigger has a specific recipient, priority, and timeout.

### Escalation Trigger Matrix

| Trigger | Severity | Recipient | Priority | Timeout | Action |
|---------|----------|-----------|----------|---------|--------|
| **Policy DENY** | High | Engineering | High | 24h | Reconsider/revise policy |
| **Confidence <60%** | Medium | User | Medium | 12h | Manual review + decide |
| **Agent disagreement >15 pts** | Medium | User | Medium | 12h | Review conflicting assessments |
| **Contradiction detected** | High | User + Engineering | Critical | 2h | Resolve conflict in knowledge graph |
| **Cloud burst >$5** | High | User | High | 1h | Approve compute cost |
| **Model update requested** | High | Engineering | High | 24h | Review + approve new model |
| **Novel situation** | Medium | User | Medium | 24h | No matching policy, decide precedent |
| **Agent autonomy exceeded** | Critical | Engineering | Critical | 1h | Agent attempted disallowed action |

### Escalation Message Format

All escalations follow this JSON structure:

```json
{
  "escalation_id": "esc-2026-05-12-0047",
  "timestamp": "2026-05-12T14:30:00Z",
  "severity": "critical",
  "trigger_type": "contradiction_detected",
  "recipient": ["user@domain.com"],
  "cc": ["engineering@domain.com"],
  "priority": "critical",
  "timeout_seconds": 7200,
  
  "context": {
    "request_id": "req-2026-05-12-0042",
    "decision_type": "knowledge_integration",
    "input_summary": "New assertion: 'Claude Opus can train custom models' contradicts existing belief at 95% confidence: 'Claude models are read-only inference engines'",
    "data_size_bytes": 1024,
    "processing_time_ms": 250
  },
  
  "escalation_data": {
    "new_assertion": "Claude Opus can train custom models",
    "existing_belief": "Claude models are read-only inference engines",
    "conflict_score": 0.92,
    "source_credibility": 0.65,
    "existing_confidence": 0.95,
    "recommended_action": "Request user decision: Accept new assertion, reject it, or reduce existing confidence"
  },
  
  "required_response": {
    "action": "accept | reject | reduce_confidence | request_clarification",
    "reason": "free text explanation",
    "confidence_adjustment": "if action=reduce_confidence, new confidence value 0-100"
  },
  
  "audit": {
    "control_decision_id": "ctd-2026-05-12-0047",
    "policy_evaluated": "POL-0003-contradiction-escalation",
    "policy_effect": "ESCALATE_TO_HUMAN",
    "trust_gate_result": "FAIL (contradiction_detected)"
  }
}
```

### Escalation Routing Rules

**Recipient Selection:**

```
IF decision_type IN (knowledge_contradiction, model_disagreement):
  recipient = USER  # User has authority over knowledge
  IF severity = critical:
    cc = ENGINEERING  # Inform engineering of major conflicts

ELIF decision_type IN (cloud_burst, compute_resource):
  recipient = USER  # User controls budget
  
ELIF decision_type IN (agent_authorization, policy_violation, automation_change):
  recipient = ENGINEERING  # Engineering owns system architecture
  
ELIF decision_type = novel_situation:
  recipient = USER  # User sets precedent
```

**Priority Assignment:**

```
IF timeout < 1 hour OR severity = critical:
  priority = CRITICAL
  alert_method = [email, in-app notification, system log]
  
ELIF timeout < 4 hours OR severity = high:
  priority = HIGH
  alert_method = [email, in-app notification]
  
ELIF timeout >= 24 hours:
  priority = MEDIUM
  alert_method = [in-app notification, daily digest]
```

---

## Trust Thresholds

Quantitative gates for automatic vs. gated vs. manual approval.

### Confidence Scoring

**Agent Confidence Calculation:**

```
Per-dimension agreement:
  IF |dimension_score_a - dimension_score_b| <= 15 points:
    agreement = true
  ELSE:
    agreement = false

Overall confidence:
  IF all_4_dimensions_agree:
    confidence = 95%  # High certainty
  ELIF 3_of_4_dimensions_agree:
    confidence = 70%  # Moderate certainty
  ELIF 2_of_4_dimensions_agree:
    confidence = 40%  # Low certainty
  ELIF 1_or_fewer_agree:
    confidence = 20%  # Very low certainty
```

### Gate Thresholds by Sensitivity

| Sensitivity | Confidence ≥85% | Confidence 60-84% | Confidence <60% |
|------------|-----------------|-------------------|-----------------|
| **ROUTINE** | Auto-approve | Policy-gated | Auto-deny |
| **SENSITIVE** | Auto-approve | Policy-gated | Escalate to user |
| **CRITICAL** | Policy-gated | Escalate to user | Escalate to user |

### Hard Floors (Non-negotiable Minimums)

**Relevance ≥60:**

If relevance score < 60 (from either agent), the decision routes to ARCHIVE regardless of other dimensions.

```
IF relevance_score < 60:
  result = FORCE_ARCHIVE
  reason = "Relevance floor violated"
  bypass_allowed = false  # Cannot override
```

**Agent Trustworthiness ≥40:**

If either agent scores trustworthiness/credibility < 40, escalate to verify source.

```
IF credibility_score < 40:
  result = ESCALATE_TO_USER
  reason = "Source credibility below minimum"
  message = "Consider requesting clarification or source verification"
```

**Model Agreement on Contradiction:**

If agents disagree on whether contradiction exists (>20 point difference on contradiction confidence):

```
IF contradiction_confidence_difference > 20:
  result = ESCALATE_TO_USER
  reason = "Agents disagree on contradiction status"
  action = "User decides: is this a contradiction or complementary knowledge?"
```

---

## HITL Workflows

### Workflow 1: Knowledge Contradiction Resolution

**Trigger:** New knowledge contradicts existing belief at >80% conflict confidence

**Process:**

```
1. System detects contradiction
   - New: "Claude Opus 4.7 can be fine-tuned"
   - Existing: "Claude models are frozen inference engines" (95% confidence)
   - Conflict score: 92%

2. Create escalation record (esc-*-contradiction)
   - Include both assertions
   - Show source credibility of new assertion
   - Show confidence of existing belief

3. Send to user with three options:
   
   Option A: Accept new assertion
   └─ Action: Update existing belief to "Claude Opus 4.7 cannot be fine-tuned but other models might"
   
   Option B: Reject new assertion
   └─ Action: Archive new assertion, maintain existing belief at 95% confidence
   
   Option C: Reduce existing confidence
   └─ Action: Adjust existing belief confidence to 75% (more uncertain)

4. User responds with decision + reasoning

5. System applies decision:
   - Update Neo4j knowledge graph
   - Log decision in Obsidian decision log
   - Record audit trail (who, when, what, why)

6. If user doesn't respond within 2 hours:
   - Escalate to engineering
   - Engineering decides on conservative approach (usually: reduce confidence, don't add new assertion)
```

### Workflow 2: Cloud Burst Approval

**Trigger:** Inference request would exceed $5 cloud cost

**Process:**

```
1. System detects cloud burst need
   - Request: "Deep synthesis on 50MB dataset"
   - Estimated cost: $8.50
   - Exceeds threshold by: $3.50

2. Create escalation record (esc-*-cloud-burst)
   - Explain why cloud needed (local resources insufficient)
   - Show cost estimate
   - Show daily budget remaining ($20/day cap)

3. Send to user with three options:
   
   Option A: Approve cloud inference
   └─ Action: Execute on cloud, charge to account
   
   Option B: Reject cloud inference
   └─ Action: Queue for local batch processing (runs when GPU available)
   
   Option C: Request cost optimization
   └─ Action: System explores lower-cost alternatives (Haiku instead of Sonnet, smaller model)

4. User responds within 1 hour

5. System executes decision:
   - If approved: execute on cloud immediately
   - If rejected: add to queue with priority indicator
   - If optimize: suggest alternatives + cost savings

6. If user doesn't respond within 1 hour:
   - Automatically reject (default safe)
   - Queue for local processing
   - Notify user task is queued
```

### Workflow 3: Policy Violation Review

**Trigger:** Request matches DENY effect in applicable policy

**Process:**

```
1. System evaluates policy gate
   - Request: Screening Agent attempts Neo4j WRITE
   - Applicable policy: POL-0002 (No WRITE without approval)
   - Policy effect: ESCALATE_TO_HUMAN

2. Create escalation record (esc-*-policy-violation)
   - Show which policy was triggered
   - Explain why policy exists
   - Ask: Is this policy still correct? Should we change it?

3. Route to ENGINEERING (not user)
   - User isn't the policy owner
   - Engineering decides if policy needs revision

4. Engineering reviews:
   
   Option A: Policy is correct, deny request
   └─ Action: Block request, no changes to policy
   
   Option B: Policy is outdated, approve request
   └─ Action: Approve request, create new policy version
   
   Option C: Policy needs refinement
   └─ Action: Create new policy with more nuanced rules (e.g., "WRITE allowed if validated=true")

5. Engineering responds with decision + updated policy (if any)

6. System applies:
   - Execute or deny current request per decision
   - If policy updated: version control the change
   - Audit all decisions tied to policy for consistency
```

### Workflow 4: Agent Disagreement Resolution

**Trigger:** Screening Agent and Critical Agent differ by >15 points on any dimension

**Process:**

```
1. System calculates disagreement
   - Dimension: Credibility
   - Screening Agent: 75
   - Critical Agent: 52
   - Difference: 23 points (exceeds 15 threshold)
   - Confidence: 40% (agents 2 of 4 dimensions agree)

2. Create escalation record (esc-*-agent-disagreement)
   - Show assessments side-by-side
   - Highlight disagreeing dimensions
   - Show reasoning from each agent

3. Send to USER with two options:
   
   Option A: Accept Screening Agent score
   └─ Reasoning: Conservative approach, trust consistency
   
   Option B: Accept Critical Agent score
   └─ Reasoning: Critical agent caught something conservative agent missed

4. User responds with choice + optional notes

5. System applies:
   - Use chosen agent score for final decision
   - Record which agent was trusted
   - Log disagreement pattern (if recurring, may need to retune agents)

6. If user doesn't respond within 12 hours:
   - Default to Screening Agent (conservative)
   - Notify user of default action
```

---

## Compliance & Audit

Every approval decision is logged and queryable for compliance.

### Decision Log Entry

```json
{
  "control_decision_id": "ctd-2026-05-12-0047",
  "timestamp": "2026-05-12T14:35:00Z",
  "request_id": "req-2026-05-12-0042",
  
  "classification": {
    "sensitivity": "CRITICAL",
    "decision_type": "knowledge_integration",
    "trigger": "contradiction_detected"
  },
  
  "policy_evaluation": {
    "applicable_policies": ["POL-0003-contradiction-escalation"],
    "matched_policy": "POL-0003",
    "policy_effect": "ESCALATE_TO_HUMAN",
    "policy_version": "1.0"
  },
  
  "trust_gate": {
    "agent_agreement": false,
    "confidence": 0.20,
    "contradiction_confidence": 0.92,
    "result": "ESCALATE_TO_HUMAN"
  },
  
  "escalation": {
    "escalation_id": "esc-2026-05-12-0047",
    "recipient": "user@domain.com",
    "priority": "critical",
    "created": "2026-05-12T14:35:00Z",
    "timeout": "2026-05-12T16:35:00Z"
  },
  
  "resolution": {
    "resolved_at": "2026-05-12T14:45:00Z",
    "resolved_by": "user@domain.com",
    "action_taken": "reject",
    "reasoning": "New assertion is from unreliable source; existing belief is stronger",
    "result": "APPROVED",
    "execution_id": "exec-2026-05-12-0047"
  },
  
  "audit_trail": {
    "created_by": "system",
    "created_at": "2026-05-12T14:35:00Z",
    "archived": false,
    "retention_policy": "7 years"
  }
}
```

### Audit Queries

**Query 1: All escalations for user**

```sql
SELECT 
  escalation_id, 
  trigger_type, 
  severity, 
  created_at, 
  resolved_at, 
  response_time_minutes
FROM control_decisions
WHERE recipient = 'user@domain.com'
  AND escalation_id IS NOT NULL
  AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY created_at DESC;
```

**Query 2: Policy violations by policy**

```sql
SELECT 
  policy_id,
  COUNT(*) as violation_count,
  AVG(response_time_minutes) as avg_response_time,
  MAX(response_time_minutes) as max_response_time
FROM control_decisions
WHERE policy_effect = 'DENY'
  AND created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY policy_id
ORDER BY violation_count DESC;
```

**Query 3: Agent agreement rate by dimension**

```sql
SELECT 
  dimension,
  COUNT(*) as total_evaluations,
  SUM(CASE WHEN agreement = true THEN 1 ELSE 0 END) as agreements,
  ROUND(100 * SUM(CASE WHEN agreement = true THEN 1 ELSE 0 END) / COUNT(*), 2) as agreement_rate
FROM validation_assessments
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY dimension
ORDER BY agreement_rate ASC;
```

---

## Integration with Control Plane

The Runtime Policy Gate implements three components of the Cognitive Control Plane:

### 1. Policy Gate (Component 2)

The YAML policies and evaluation rules in this document form the Policy Gate:

```
Incoming Request
  ↓
Sensitivity Classifier (produces: ROUTINE | SENSITIVE | CRITICAL)
  ↓
Policy Gate Evaluation
  - Load applicable policies for (agent, tool, operation, sensitivity)
  - Evaluate conditions in priority order
  - Return: ALLOW | DENY | ESCALATE_TO_HUMAN
  ↓
[This document defines how policies are written and evaluated]
```

### 2. Trust Threshold Gate (Component 3)

The confidence thresholds and hard floors in this document form the Trust Threshold Gate:

```
Policy Gate ALLOW
  ↓
Trust Threshold Gate
  - Calculate confidence (0-100% based on agent agreement)
  - Check hard floors (Relevance ≥60, Credibility ≥40)
  - Check sensitivity thresholds (ROUTINE ≥85%, SENSITIVE ≥60%)
  - Return: AUTO_APPROVE | POLICY_GATED | ESCALATE_TO_USER
  ↓
[This document defines confidence calculations and gates]
```

### 3. Escalation Framework (Component 5)

The escalation triggers, routing, and HITL workflows in this document form the Escalation Framework:

```
Policy DENY or Trust Gate FAIL
  ↓
Escalation Framework
  - Determine escalation trigger (policy denial, low confidence, contradiction, etc.)
  - Route to recipient (user, engineering, both)
  - Create escalation record with required response
  - Wait for human decision
  ↓
[This document defines all escalation workflows and decision paths]
```

---

## Migration Path

### Phase 1: Implicit Policies

Current state: Policies exist in code comments, evaluation is ad-hoc.

```
Request → Manual review + intuition → Sometimes escalate
No audit trail. No replay. No consistency.
```

### Phase 2: Explicit Policies (This Document)

Policies are written in YAML, evaluated deterministically, audited.

```
Request → Sensitivity Classifier → Policy Gate (YAML rules) → Trust Threshold → [Auto/Gated/Escalate] → Audit Log
Full traceability. Consistent decisions. Queryable compliance.
```

### Phase 3+: Autonomous Governance

Policies self-document, update based on feedback, measure their effectiveness.

```
Request → Control Plane → Execution → Outcome → Policy Feedback Loop → Policy Optimization
Continuous improvement without human rewrites.
```

---

## Revision History

- **2026-05-12:** Initial version. Formalized Runtime Policy Gate operationalizing Policy Gate and Escalation Framework from Cognitive Control Plane.

