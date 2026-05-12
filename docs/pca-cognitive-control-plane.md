---
type: architecture
version: Phase-2
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [control-plane, governance, policy, authorization, zero-trust]
---

# PCA Cognitive Control Plane

## Executive Summary

The Cognitive Control Plane is the explicit authorization, policy, and routing layer that governs:

- **Model selection** (which LLM for which decision)
- **Tool invocation** (what agents can execute)
- **Cloud burst** (when local vs cloud inference)
- **Sensitivity classification** (data handling rules)
- **Escalation** (when humans must approve)
- **Trust thresholds** (confidence gates)

It implements **Zero Trust Cognition** — every inference, agent, and decision requires explicit authorization before execution.

**This is not optional.** It is the architectural layer that separates:

- **Governed AI** (what PCA is)
- **Autonomous AI** (what PCA is not)

---

## Design Principles

### 1. Default Deny

Every action begins in a **denied** state until:

- Policy explicitly permits it
- Authorization gates are passed
- Trust thresholds are satisfied
- HITL approval (if required) is obtained

No inference runs without authorization.
No agent executes without approval.
No tool invocation happens automatically.

### 2. Least Privilege

Each agent, model, and tool receives:

- Minimum scope needed for its task
- Time-bounded authority
- Resource limits
- Output restrictions

Not:
- "Full API access"
- "Open execution"
- "Permanent permissions"

### 3. Explicit Policy Over Implicit Heuristics

Control decisions are:

- **Written policies** (version-controlled, auditable)
- **Queryable rules** (not hidden in code)
- **Human-readable** (non-experts can understand)
- **Change-controlled** (governance review before deployment)

Not:
- Emergent from model behavior
- Implicit in prompt engineering
- Black-box LLM decisions
- Discovered post-hoc

### 4. Human Authority Preserved

Humans remain the final authority on:

- High-consequence decisions
- Contradictions detected by reconciliation engine
- Novel situations not covered by policy
- Model disagreements
- Cloud resource decisions

Automation supports humans. Humans don't support automation.

---

## Control Plane Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   INCOMING REQUEST / INFERENCE                  │
│  (Agent decision, tool invocation, model query, execution)      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
            ┌─────────────▼─────────────┐
            │   SENSITIVITY CLASSIFIER  │
            │  (What kind of decision?) │
            └─────────────┬─────────────┘
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
    ┌──▼──┐          ┌─────▼─────┐     ┌──────▼──┐
    │ROUTINE       │SENSITIVE   │     │ CRITICAL │
    │(auto)       │(gated)      │     │(HITL)    │
    └──┬──┘       └──┬──┘       │     └──────┬──┘
       │             │          │            │
    ┌──▼────────────▼──────────▼────────────▼──┐
    │         POLICY GATE EVALUATION             │
    │  - Applicable rules?                       │
    │  - Trust threshold met?                    │
    │  - Resource limits OK?                     │
    │  - Time window valid?                      │
    └──┬──────────────────────────────────────┬──┘
       │                                      │
    DENY                                    PASS
       │                                      │
    ┌──▼──────┐                    ┌─────────▼──────┐
    │ESCALATE │                    │MODEL ROUTER    │
    │TO HUMAN │                    │Select inference│
    └─────────┘                    │model & params  │
                                   └─────────┬──────┘
                                             │
                            ┌────────────────▼──────────────┐
                            │   EXECUTION AUTHORIZATION     │
                            │ - Does model have permission? │
                            │ - Output constraints?         │
                            │ - Monitoring enabled?         │
                            └────────────┬──────────────────┘
                                         │
                        ┌────────────────▼──────────────┐
                        │  INFERENCE EXECUTION          │
                        │  (Model processes request)    │
                        └────────────────┬──────────────┘
                                         │
                        ┌────────────────▼──────────────┐
                        │  OUTPUT VALIDATION            │
                        │  - Correct sensitivity level? │
                        │  - Confidence sufficient?     │
                        │  - Audit record created?      │
                        └────────────────┬──────────────┘
                                         │
                        ┌────────────────▼──────────────┐
                        │  RETURN AUTHORIZED RESULT     │
                        └───────────────────────────────┘
```

---

## Control Plane Components

### 1. Sensitivity Classifier

**Purpose:** Categorize incoming decision by consequence and risk.

**Classification Levels:**

| Level | Examples | Decision | Approval |
|-------|----------|----------|----------|
| **Routine** | Document scoring, tag assignment, routine retrieval | Fast path, policy-gated | Policy only |
| **Sensitive** | Knowledge integration decisions, agent routing, minor escalations | Policy + confidence gate | Policy + metrics |
| **Critical** | Model contradictions, cloud burst approval, user deletion, new agent creation | Explicit human review | Manual approval |

**Classifier Logic:**

```
IF decision_type IN (knowledge_integration, agent_routing):
  sensitivity = SENSITIVE
ELIF decision_type IN (contradiction, cloud_burst, deletion, automation_change):
  sensitivity = CRITICAL
ELSE:
  sensitivity = ROUTINE
```

**Not a model.**
Not a heuristic.
A deterministic lookup table.

---

### 2. Policy Gate

**Purpose:** Evaluate whether a decision is permitted given current context.

**Policy Format:**

```yaml
Policy Name: "Agent Tool Invocation"
Applies To: ROUTINE, SENSITIVE, CRITICAL

Rules:
  - Rule: "Screening Agent can invoke Neo4j READ queries"
    Condition:
      agent: "Screening Agent"
      tool: "Neo4j"
      operation: "READ"
    Effect: ALLOW
    
  - Rule: "No agent can DELETE without HITL approval"
    Condition:
      operation: "DELETE"
    Effect: ESCALATE_TO_HUMAN
    
  - Rule: "Claude Sonnet can access Obsidian vault"
    Condition:
      model: "Claude Sonnet"
      resource: "Obsidian"
    Effect: ALLOW
    Constraints:
      - max_files: 100
      - max_size_mb: 50
      - read_only: true
    
  - Rule: "Rate limit: max 100 inferences/hour"
    Condition:
      time_window: "1h"
    Effect: ALLOW if count < 100 else DENY
```

**Evaluation:**

```
For each applicable rule in priority order:
  1. Check if conditions match
  2. If match and Effect = ALLOW → proceed
  3. If match and Effect = DENY → reject
  4. If match and Effect = ESCALATE → send to human
  5. Apply Constraints if present
  
If no rule matches → DEFAULT_DENY
```

---

### 3. Trust Threshold Gate

**Purpose:** Confidence-based authorization.

**Components:**

| Metric | Source | Threshold | Action |
|--------|--------|-----------|--------|
| **Agent agreement** | Dual-agent validation | < 15pt diff | ALLOW |
| **Overall score** | Validation layer | > 80 | ALLOW, < 60 | DENY |
| **Relevance score** | Validation layer | ≥ 60 | ALLOW |
| **Model confidence** | LLM intrinsic | > threshold | ALLOW |
| **Source credibility** | Validation layer | > 75 | ALLOW |

**Example Gate:**

```
IF validation_score >= 80 AND agent_agreement = true:
  authorization = AUTO_APPROVE
ELIF validation_score >= 60 AND validation_score < 80:
  authorization = POLICY_GATED
ELSE:
  authorization = ESCALATE_TO_HUMAN
```

---

### 4. Model Router

**Purpose:** Select the appropriate inference model for the decision.

**Routing Table:**

| Decision Type | Input Size | Latency Req | Model | Rationale |
|---------------|------------|-------------|-------|-----------|
| Document scoring | < 5KB | < 100ms | Haiku (local) | Fast, cost-efficient |
| Complex synthesis | > 10KB | < 5s | Sonnet (cloud) | Quality, reasoning |
| Real-time chat | — | < 500ms | Qwen2.5-7B (local) | Latency critical |
| Deep analysis | — | flexible | Qwen2.5-32B (local) | Quality, local |
| User-facing summary | — | < 2s | Sonnet | Quality, user experience |

**Routing Logic:**

```python
def route_inference(decision_type, input_size, latency_requirement):
    if latency_requirement < 100ms:
        return "Qwen2.5-7B"  # Local, fastest
    elif input_size < 5KB and decision_type == "scoring":
        return "Haiku"  # Cloud, cost-efficient
    elif latency_requirement < 5s:
        return "Sonnet"  # Cloud, best quality
    else:
        return "Qwen2.5-32B"  # Local, deep analysis
```

**Not learned from data.**
Not emergent from prompts.
A deterministic decision tree.

---

### 5. Escalation Framework

**Purpose:** Route decisions to humans when policy or confidence gates fail.

**Escalation Triggers:**

| Trigger | Severity | Recipient | Action |
|---------|----------|-----------|--------|
| Policy DENY | High | Engineering | Reconsider policy |
| Trust threshold unmet | Medium | User | Manual review requested |
| Agent disagreement (20% conf) | Medium | User | Review & decide |
| Contradiction detected | High | User + Engineering | Model conflict |
| Cloud burst decision | High | User | Compute cost approval |
| Novel situation | Medium | User | No matching policy |

**Escalation Message:**

```json
{
  "escalation_id": "esc-2026-05-12-001",
  "trigger": "agent_disagreement",
  "severity": "medium",
  "content_summary": "Screening Agent scored 45, Critical Agent scored 72 on credibility",
  "difference": 27,
  "confidence": "20%",
  "decision_needed": "Accept one score or request revalidation",
  "recipient": "user",
  "timeout": "24h",
  "action_required": true
}
```

---

### 6. Output Constraint Engine

**Purpose:** Restrict inference outputs based on sensitivity and policy.

**Constraint Types:**

| Constraint | Example | Effect |
|-----------|---------|--------|
| **Sensitivity Filter** | No credentials in output | Strip matching patterns |
| **Confidence Gate** | Min 60% confidence required | Suppress low-confidence outputs |
| **Scope Limit** | Max 10 results returned | Truncate results |
| **Format Requirement** | Markdown only | Transform output format |
| **Audit Trail** | Log all deletions | Create audit record |

**Example Policy:**

```
Model: Claude Sonnet
Output Constraints:
  - Must include confidence score (if reasoning)
  - No credentials, API keys, or passwords
  - Max 5000 tokens
  - Cite sources (Obsidian references)
  - Audit log required for DELETE operations
```

---

## Control Plane Decisions

### Decision 1: Model Selection

**Question:** Which model executes this inference?

**Answer:** Model Router (deterministic routing table)

**Inputs:**
- Decision type
- Input size
- Latency requirement
- Available resources

**Output:** Model name + parameters

**Example:**
```
Input: Score 2KB document on "credibility"
Decision Type: scoring
Input Size: 2KB
Latency: < 100ms
→ Route to: Qwen2.5-7B (local, fast)
Temperature: 0.3
Max tokens: 150
```

---

### Decision 2: Tool Invocation

**Question:** Can this agent use this tool?

**Answer:** Policy Gate (deterministic rule evaluation)

**Inputs:**
- Agent identity
- Tool requested
- Operation (READ/WRITE/DELETE)
- Resource constraints

**Output:** ALLOW | DENY | ESCALATE

**Example:**
```
Input: Screening Agent requests Neo4j WRITE
Agent: Screening Agent
Tool: Neo4j
Operation: WRITE
→ Policy Rule: "No agent can WRITE without HITL approval"
→ Result: ESCALATE_TO_HUMAN
```

---

### Decision 3: Cloud Burst

**Question:** Should this computation run in the cloud?

**Answer:** Explicit policy + user approval

**Criteria:**
- Local GPU available?
- Task complexity exceeds local capacity?
- User budget allows cloud costs?
- User approves cloud execution?

**Decision Tree:**
```
IF local_inference_available AND sufficient_resources:
  execute_locally()
ELIF task_needs_cloud:
  escalate_to_user("Cloud burst needed. Cost: $X. Approve?")
  IF user_approves:
    execute_on_cloud()
  ELSE:
    escalate_to_user("Cloud inference denied. Task queued for local batch.")
ELSE:
  deny("Insufficient resources and cloud not available")
```

---

### Decision 4: Sensitivity-Based Routing

**Question:** How should this decision be processed?

**Answer:** Sensitivity Classifier → appropriate path

**Mapping:**

| Input | Classifier | Path | Gate | Approval |
|-------|-----------|------|------|----------|
| Score video | ROUTINE | Fast | Policy | Auto |
| Integrate contradictory knowledge | SENSITIVE | Medium | Policy + confidence | Policy |
| Delete user data | CRITICAL | Slow | Manual review | User |

---

## Integration with PCA Layers

### Layer 3: Validation Layer

Produces:
- Confidence scores (65-95)
- Agent agreement (true/false)
- Credibility, quality, relevance, alignment scores

**Feeds to Control Plane:**
- Trust Threshold Gate
- Escalation Framework

---

### Layer 4: Cognitive Reconciliation Engine

Produces:
- Reinforce/Contradict/Expand/Ignore relationships
- Updated confidence (Bayesian)
- Contradiction flags

**Feeds to Control Plane:**
- Sensitivity Classifier (contradiction = CRITICAL)
- Escalation Framework (model disagreement)
- Trust Threshold Gate (new confidence)

---

### Layer 6: Reasoning & Agents

**Before Execution:**
- Control Plane authorizes model selection
- Policy Gate permits tool invocation
- Output Constraints prepared

**After Execution:**
- Result validated against Output Constraints
- Audit record created
- Escalation triggered if confidence insufficient

---

## Runtime Guarantees

### Authorization Completeness

Every inference must pass:

1. ✅ Sensitivity Classification
2. ✅ Policy Gate Evaluation
3. ✅ Trust Threshold Gate
4. ✅ Model Router Selection
5. ✅ Execution Authorization
6. ✅ Output Validation

If any gate **fails**, decision **escalates or denies**.

### No Implicit Permissions

- No model has blanket access to tools
- No tool is "always available"
- No agent is "fully autonomous"
- No inference is "approved by default"

### Auditability

Every decision creates:

```json
{
  "control_decision_id": "ctd-2026-05-12-001",
  "timestamp": "2026-05-12T15:30:00Z",
  "request_type": "inference",
  "sensitivity_level": "SENSITIVE",
  "policy_rules_evaluated": ["Agent Tool Invocation", "Rate Limit"],
  "policy_result": "ALLOW",
  "trust_gate_result": "PASS (confidence 78%)",
  "model_routed_to": "Claude Sonnet",
  "output_constraints_applied": ["No credentials", "Cite sources"],
  "execution_time_ms": 1250,
  "result_confidence": 0.78,
  "audit_log": "audit-id-001"
}
```

---

## Migration Path

### Phase 1 (Current)

Control Plane is mostly implicit:
- Validation layer scores, but routing is manual
- Policy exists in code comments
- HITL approval is ad-hoc

### Phase 2

Explicit Control Plane implemented:
- Sensitivity Classifier running
- Policy Gate evaluating rules
- Trust Threshold gating decisions
- Model Router selecting inference models

### Phase 3+

Full Autonomous Governance:
- Self-documenting policy
- Runtime policy updates
- Observability feeding back to policy
- Learning from user overrides

---

## Policy Template

Teams implementing this should standardize on:

```yaml
---
policy_id: "POL-001-agent-authorization"
version: "1.0"
created: "2026-05-12"
last_updated: "2026-05-12"
applies_to:
  - "Screening Agent"
  - "Critical Agent"

rules:
  - id: "rule-001"
    name: "Neo4j READ Access"
    applies_to:
      agent: "*"  # All agents
      operation: "READ"
      resource: "Neo4j"
    effect: "ALLOW"
    
  - id: "rule-002"
    name: "No WRITE Without HITL"
    applies_to:
      operation: "WRITE"
    effect: "ESCALATE_TO_HUMAN"
    
  - id: "rule-003"
    name: "Confidence Gate 60%"
    applies_to:
      decision_type: "knowledge_integration"
    effect: "ALLOW if confidence > 60 else ESCALATE"

constraints:
  - rate_limit: "100 inferences/hour"
  - max_concurrent: "4"
  - cost_limit: "$10/day"
  - timeout: "30s per inference"

oversight:
  - policy_owner: "Engineering Lead"
  - review_frequency: "quarterly"
  - audit_required: true
  - escalation_recipients:
    - "user@domain.com"
    - "engineering@domain.com"
```

---

## Revision History

- **2026-05-12:** Initial version. Formalized Cognitive Control Plane as explicit authorization layer.
