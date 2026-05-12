---
type: architecture
version: Phase-4
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [agents, runtime, autonomy, mcp, execution, authorization]
---

# PCA Agent Runtime Model

## Executive Summary

The Agent Runtime Model defines how agents execute autonomously within PCA boundaries. It specifies:

- **Agent Anatomy** — What constitutes an agent (identity, capabilities, constraints)
- **Execution Semantics** — Request → Agent → Response flow
- **Autonomy Boundaries** — What agents can and cannot do
- **Agent Communication** — Inter-agent dialogue and coordination
- **Tool Invocation** — How agents access external systems (with control plane gates)
- **Failure Handling** — Recovery, timeouts, and escalation

Agents are **not autonomous in the sense of independent goal-setting**. They are **constrained executors** of human-directed tasks, with authority limited by policy gates and trust thresholds.

This is the foundation for **Phase 4: Reasoning & Agents** — when PCA transitions from validation/reconciliation to active reasoning and multi-agent collaboration.

---

## Agent Anatomy

### Agent Identity

Each agent has:

```
Agent {
  id: string              # Unique identifier (e.g., "agent-screening-v1")
  name: string            # Human-readable name ("Screening Agent")
  model: string           # Base LLM (e.g., "claude-3-5-sonnet")
  version: string         # Semantic version ("1.0.0")
  created: timestamp      # Birth date
  
  # Purpose & scope
  purpose: string         # What this agent is designed to do
  domain: string          # Knowledge domain (e.g., "validation", "reconciliation")
  capabilities: [string]  # List of tools it can invoke
  
  # Constraints
  max_concurrent_requests: int       # Max requests in flight
  request_timeout_seconds: int       # Execution deadline
  max_tokens_per_response: int       # Output limit
  cost_limit_per_request: float      # Max $ per request
  
  # Governance
  created_by: string              # Human who created it
  approved_by: string             # Human who approved it
  audit_enabled: bool             # Audit every execution
  
  # Lifecycle
  status: "active" | "archived" | "suspended"
  deactivation_reason: string?    # If not active, why
}
```

### Agent Instantiation

Agents are created through an explicit **governance process**:

```
1. Proposal
   ├─ Author: "We need an agent to reconcile contradictions"
   ├─ Purpose: "Detect and rank knowledge contradictions"
   ├─ Domain: "reconciliation"
   └─ Requested tools: ["Neo4j.READ", "Claude.INFERENCE"]

2. Review (Engineering + User)
   ├─ Questions: "Will this agent replace human decisions? (No, escalates)"
   ├─ Capability assessment: "Can this LLM do this job?"
   ├─ Risk assessment: "What could go wrong?"
   └─ Decision: Approve / Reject / Revise

3. Implementation
   ├─ Prompt engineering
   ├─ Tool testing
   ├─ Safety validation
   └─ Documentation

4. Approval (HITL Gate)
   ├─ Final review of system prompt
   ├─ Tool permissions verified
   ├─ Audit logging enabled
   └─ Sign-off: "This agent is authorized to operate"

5. Deployment
   ├─ Register in Neo4j: CREATE Agent node
   ├─ Enable in orchestration: n8n workflow updated
   ├─ Monitor: Prometheus + Grafana dashboards created
   └─ Live: Agent accepts requests

6. Deactivation (if needed)
   ├─ Reason: "Replaced by agent-contradiction-v2"
   ├─ Handoff: Migrate active requests to new agent
   ├─ Archive: Keep execution history, disable new requests
   └─ Audit: Document why and when deactivated
```

---

## Execution Semantics

### Request Flow

```
User/System initiates request
         │
         ▼
[Control Plane: Sensitivity Classifier]
  Is this ROUTINE / SENSITIVE / CRITICAL?
         │
         ├─ROUTINE────────────────────┐
         │                            │
         ├─SENSITIVE──────────────────┤
         │                            │
         └─CRITICAL──────────────────┬┤
                                     ││
                                     ▼▼
                          [Policy Gate Evaluation]
                          - Applicable policies?
                          - Permission check?
                          - Resource limits OK?
                                     │
                                  DENY or ALLOW
                                     │
                      ┌──────────────┴─────────────┐
                      │                            │
                    DENY                        ALLOW
                      │                            │
                   [Escalate]            [Trust Threshold Gate]
                      │                    - Confidence ≥?
                      │                    - Agents agree?
                      │                    - Hard floors met?
                      │                            │
                      │                    [Model Router]
                      │                    - Which agent?
                      │                    - Which model?
                      │                    - Local or cloud?
                      │                            │
                      │                    [Agent Execution]
                      │                    - Agent receives request
                      │                    - Executes with LLM
                      │                    - Invokes authorized tools
                      │                    - Returns response
                      │                            │
                      │                    [Output Validation]
                      │                    - Constraints applied?
                      │                    - Confidence sufficient?
                      │                    - Audit logged?
                      │                            │
                      │      ┌─────────────────────┘
                      │      │
                      └──────┴─────────────────────┐
                                                   │
                                            Return Response
                                         or Escalation
```

### Agent Execution Context

When an agent runs, it receives:

```json
{
  "request_id": "req-2026-05-12-0042",
  "agent_id": "agent-contradiction-detector-v1",
  "sensitivity": "SENSITIVE",
  
  "input": {
    "new_belief": "Claude Opus can fine-tune models",
    "existing_beliefs": [
      {
        "statement": "Claude models are frozen inference engines",
        "confidence": 0.95,
        "sources": ["doc-001", "doc-045"]
      }
    ],
    "context": {
      "domain": "knowledge_management",
      "user_id": "user-001",
      "session_id": "session-abc123"
    }
  },
  
  "authorization": {
    "tools_available": [
      "Neo4j.READ",
      "Neo4j.QUERY",
      "Claude.INFERENCE"
    ],
    "constraints": {
      "max_tokens": 2000,
      "timeout_seconds": 10,
      "cost_limit": 0.05
    }
  },
  
  "system_prompt": "You are a contradiction detection agent...",
  "execution_deadline": "2026-05-12T14:35:10Z"
}
```

### Agent Response Format

```json
{
  "request_id": "req-2026-05-12-0042",
  "agent_id": "agent-contradiction-detector-v1",
  "timestamp": "2026-05-12T14:35:08Z",
  "execution_time_ms": 2150,
  
  "result": {
    "decision": "CONTRADICTION_DETECTED",
    "confidence": 0.87,
    "reasoning": "The new assertion contradicts the existing belief...",
    
    "analysis": {
      "contradiction_score": 0.92,
      "severity": "high",
      "recommended_action": "ESCALATE_TO_USER",
      "suggested_resolution": [
        "Accept new belief and reduce old confidence to 0.70",
        "Reject new belief and maintain old confidence at 0.95",
        "Mark as open question pending additional evidence"
      ]
    },
    
    "tool_invocations": [
      {
        "tool": "Neo4j.QUERY",
        "query": "MATCH (b:Belief) WHERE b.statement CONTAINS 'frozen' RETURN b LIMIT 10",
        "result_count": 3,
        "execution_time_ms": 45
      },
      {
        "tool": "Claude.INFERENCE",
        "model": "claude-3-5-sonnet",
        "input_tokens": 350,
        "output_tokens": 127,
        "cost": 0.0042
      }
    ]
  },
  
  "status": "SUCCESS",
  "cost": {
    "total": 0.0042,
    "limit": 0.05,
    "remaining_budget": 0.0458
  },
  
  "audit": {
    "control_decision_id": "ctd-2026-05-12-0047",
    "policy_evaluated": ["POL-0003-contradiction-escalation"],
    "authorization": "ALLOW",
    "escalation_triggered": true,
    "escalation_id": "esc-2026-05-12-0047"
  }
}
```

---

## Autonomy Boundaries

### What Agents CAN Do

✅ **Permitted Actions:**

1. **Read Data**
   - Query Neo4j knowledge graph
   - Search ChromaDB vector index
   - Retrieve Obsidian vault content
   - Analyze metadata in PostgreSQL

2. **Generate Analysis**
   - Score/rank items
   - Detect patterns
   - Synthesize insights
   - Generate explanations

3. **Invoke Approved Tools**
   - Neo4j.READ (query-only)
   - ChromaDB.SEARCH (vector similarity)
   - Claude.INFERENCE (via control plane)
   - Ollama.INFERENCE (local models)

4. **Create Temporary State**
   - Store in Redis session cache
   - Create execution logs
   - Track metrics in Prometheus

5. **Request Human Decisions**
   - Escalate ambiguous cases
   - Ask clarifying questions
   - Propose alternatives with reasoning

### What Agents CANNOT Do

❌ **Forbidden Actions:**

1. **Modify Data Without Approval**
   - No Neo4j.WRITE without HITL gate
   - No Obsidian vault edits
   - No user deletion or modification

2. **Create New Agents or Policies**
   - Cannot self-replicate
   - Cannot write policies
   - Cannot change its own constraints

3. **Make High-Consequence Decisions Autonomously**
   - Cannot approve resource spending
   - Cannot delete knowledge (humans decide)
   - Cannot create new automation rules

4. **Bypass Authorization Gates**
   - Cannot escalate without policy gate approval
   - Cannot use tools outside capability list
   - Cannot override trust thresholds

5. **Communicate Directly with External Services**
   - Cannot call external APIs (must go through orchestrator)
   - Cannot send emails/messages (requires human approval)
   - Cannot schedule future actions

6. **Retain Memory Across Requests**
   - No persistent learning without RLHF gate
   - No parameter updates (frozen models)
   - State only in Redis (ephemeral, < 24h)

### Boundary Enforcement

**Control Plane blocks any unauthorized action:**

```python
def execute_agent_tool_invocation(
    agent_id: str,
    tool_name: str,
    operation: str,
    parameters: dict
) -> Result | Escalation:
    
    # 1. Check agent capability
    agent = get_agent(agent_id)
    if tool_name not in agent.capabilities:
        return Escalation("Agent lacks capability")
    
    # 2. Check operation permission
    policy = get_applicable_policy(agent, tool_name, operation)
    
    if policy.effect == "DENY":
        return Escalation("Operation denied by policy")
    
    if policy.effect == "ESCALATE_TO_HUMAN":
        return escalate_to_human(agent, tool_name, operation)
    
    # 3. Check resource constraints
    if would_exceed_limits(agent, tool_name, parameters):
        return Escalation("Would exceed resource limits")
    
    # 4. Execute with monitoring
    with audit_context(agent_id, tool_name):
        try:
            result = invoke_tool(tool_name, parameters)
            log_success(agent_id, tool_name, result)
            return result
        except TimeoutError:
            log_timeout(agent_id, tool_name)
            return Escalation("Agent execution timeout")
        except Exception as e:
            log_error(agent_id, tool_name, e)
            return Escalation("Agent execution failed")
```

---

## Agent Communication & Coordination

### Inter-Agent Dialogue

Agents can collaborate on complex tasks:

```
User: "Assess this new video and reconcile with existing knowledge"
         │
         ▼
[Orchestrator routes request]
         │
    ┌────┴─────┐
    │           │
[Agent A]   [Agent B]
Scoring    Reconciliation
    │           │
    └─────┬─────┘
          │
    [Both return results]
    [Orchestrator synthesizes]
         │
         ▼
    [Final response]
```

**Example: Dual-Agent Validation (Phase 1)**

```
Request: Score video on credibility (4 dimensions)
         │
    ┌────┴────┐
    │         │
 Screening   Critical
  Agent      Agent
    │         │
   Score    Score
  (T=0.3)   (T=0.8)
    │         │
    └────┬────┘
         │
    [Compare scores]
    - Per-dimension agreement?
    - If agree → confidence 95%
    - If disagree → confidence 40%
         │
         ▼
    [Route decision]
    PROMOTE (>80) | INBOX (60-80) | ARCHIVE (<60)
```

**Example: Contradiction Detection (Phase 2)**

```
Request: New knowledge contradicts existing belief
         │
    ┌────┴──────────────────────┐
    │                            │
[Screening Agent]         [Critical Agent]
    │                            │
Analyze source       Analyze new assertion
credibility           logic & evidence
    │                            │
    └────────────┬───────────────┘
                 │
        [Compare assessments]
        - Is source credible?
        - Is logic sound?
        - Confidence?
                 │
                 ▼
        [Joint recommendation]
        "Accept", "Reject", or "Lower confidence"
```

### Agent Failure Handling

**If an agent fails:**

```
Agent execution
     │
     ├─ Success → Return result
     │
     ├─ Timeout (>deadline)
     │  └─ Escalate to user with partial results
     │
     ├─ Tool Authorization Denied
     │  └─ Escalate to engineering (policy issue)
     │
     ├─ Tool Execution Failed
     │  └─ Retry once, then escalate
     │
     ├─ LLM API Error (Anthropic down)
     │  └─ Fallback to local model (Qwen2.5), then escalate
     │
     └─ Unknown Error
        └─ Log incident, escalate to engineering
```

---

## Tool Invocation Authorization

### Tool Capability Matrix

```
Tool               | Agent Type | Operation | Phase | Policy
───────────────────┼────────────┼───────────┼───────┼────────────────────
Neo4j.READ         | Screening  | QUERY     | 1+    | POL-0001: ALLOW
Neo4j.WRITE        | Any        | UPSERT    | 1+    | POL-0002: ESCALATE
Neo4j.WRITE        | Any        | DELETE    | 4+    | POL-0002: DENY
ChromaDB.SEARCH    | Reasoning  | QUERY     | 4+    | POL-0010: ALLOW
Claude.INFERENCE   | Any        | CALL      | 1+    | POL-0011: GATED
Ollama.INFERENCE   | Any        | CALL      | 2+    | POL-0012: ALLOW
Obsidian.WRITE     | Any        | EDIT      | 5+    | POL-0020: ESCALATE
Obsidian.READ      | Any        | QUERY     | 1+    | POL-0021: ALLOW
```

### Tool Request Example

**Before Authorization (What Agent Requests):**

```json
{
  "tool": "Neo4j",
  "operation": "WRITE",
  "query": "MATCH (v:VideoCapture {id: 'abc123'}) SET v.score = 85",
  "agent_id": "agent-scoring-v1"
}
```

**Control Plane Evaluation:**

```
1. Agent has Neo4j in capabilities? ✓ (Yes)
2. Apply policy POL-0002 "No WRITE without HITL" 
3. Effect = ESCALATE_TO_HUMAN
4. Create escalation record
5. Return: Escalation (not execution)
```

**After Authorization (If User Approves):**

```json
{
  "status": "APPROVED",
  "escalation_id": "esc-2026-05-12-0047",
  "approved_by": "user@domain.com",
  "approved_at": "2026-05-12T14:35:30Z",
  "execution_authorization": {
    "tool": "Neo4j",
    "operation": "WRITE",
    "agent_id": "agent-scoring-v1",
    "constraints": {
      "max_records_affected": 1,
      "timeout_seconds": 5
    }
  }
}
```

---

## Agent Lifecycle Management

### Creating an Agent (Phase 4+)

```yaml
proposal_id: "prop-2026-05-12-agent-xyz"
created_by: "engineering-lead@company.com"
created_at: "2026-05-12"

agent_specification:
  name: "Contradiction Detector"
  model: "claude-3-5-sonnet"
  purpose: "Detect knowledge contradictions and propose resolutions"
  
  system_prompt: |
    You are a contradiction detection agent. Your job is to:
    1. Analyze the new assertion
    2. Search for contradicting beliefs
    3. Assess contradiction severity (0-100)
    4. Recommend resolution (accept, reject, lower confidence)
    
    Always explain your reasoning. Always escalate to user when uncertain.
  
  capabilities:
    - "Neo4j.READ"
    - "Claude.INFERENCE"
  
  constraints:
    max_concurrent_requests: 4
    request_timeout_seconds: 10
    max_tokens_per_response: 2000
    cost_limit_per_request: 0.05
  
  governance:
    requires_human_approval: true
    audit_level: "DETAILED"
    escalation_default: "TO_USER"

review_checklist:
  - [ ] Purpose is clear and justified?
  - [ ] Model selection appropriate?
  - [ ] System prompt prevents hallucinations?
  - [ ] Tool permissions minimal and justified?
  - [ ] Error handling defined?
  - [ ] Escalation criteria clear?

approval:
  reviewed_by: "user@domain.com"
  engineering_reviewed_by: "eng@domain.com"
  approved_at: "2026-05-12T15:00:00Z"
  approval_reasoning: "Agent constrains authority appropriately. Escalates on uncertainty. Approved for Phase 2+ deployment."
```

### Deploying an Agent

```bash
# 1. Register in Neo4j
neo4j@:~> CREATE (a:Agent {
  id: "agent-contradiction-v1",
  name: "Contradiction Detector",
  model: "claude-3-5-sonnet",
  status: "active",
  created_at: timestamp()
})

# 2. Create n8n workflow
# - Add HTTP node to receive requests
# - Add Claude API node with approved prompt
# - Add Neo4j query node for context
# - Add response formatting node

# 3. Add to Model Router
# Update docs/runtime-policy-gate.md:
# - Add agent to routing table
# - Add capability matrix entry
# - Add constraint rules

# 4. Enable monitoring
# - Create Grafana dashboard for agent execution
# - Add Prometheus metrics:
#   * pca_agent_requests_total
#   * pca_agent_errors_total
#   * pca_agent_latency_seconds

# 5. Live
# Agent now handles requests matching its purpose
```

### Deactivating an Agent

**Why agents are deactivated:**

- Replaced by improved version
- Task no longer needed
- Quality degraded
- Security concern identified
- Responsible human left

**Deactivation process:**

```
1. Set status = "suspended" (stop new requests)
2. Migrate active requests to fallback agent
3. Archive execution logs (keep audit trail)
4. Document reason & date
5. Keep Neo4j node (historical record)
6. Set created_by to "archived"
7. Update documentation

Neo4j:
SET a.status = "archived"
SET a.archived_at = timestamp()
SET a.archived_reason = "Replaced by agent-contradiction-v2"
SET a.archived_by = "engineering-lead"
```

---

## Integration with Control Plane

Agent execution is completely mediated by the Cognitive Control Plane:

```
Agent Request
     │
     ├─ Sensitivity Classifier
     │  └─ Is agent request ROUTINE/SENSITIVE/CRITICAL?
     │
     ├─ Policy Gate
     │  └─ Evaluate: "Can this agent use this tool?"
     │
     ├─ Trust Threshold Gate
     │  └─ Check: "Is confidence sufficient?"
     │
     ├─ Model Router
     │  └─ Select: "Which model/agent should execute?"
     │
     ├─ Execution Authorization
     │  └─ Verify: "All constraints satisfied?"
     │
     └─ Output Validation
        └─ Ensure: "Result meets constraints?"

Every step can result in:
- ALLOW (continue)
- DENY (escalate)
- ESCALATE_TO_HUMAN (wait for approval)
```

**No agent has implicit permission to do anything.** Every action requires explicit authorization from the control plane.

---

## Revision History

- **2026-05-12:** Initial version. Specified agent anatomy, execution semantics, autonomy boundaries, communication patterns, and lifecycle management.

