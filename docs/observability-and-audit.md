---
type: architecture
version: Phase-2
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [observability, audit, compliance, tracing, lineage, logging]
---

# PCA Observability & Audit

## Executive Summary

The Observability & Audit layer provides:

- **Execution Tracing** — Request → Inference → Decision → Audit trail
- **Lineage Tracking** — How decisions depend on specific data/sources
- **Compliance Logging** — Who did what when (human-readable + machine-queryable)
- **Monitoring & Alerting** — Real-time system health, performance, cost
- **Retention & Privacy** — 7-year compliance windows, encryption at rest

Every decision in PCA is **fully traceable and auditable** — required for governance, compliance, and continuous improvement.

---

## Core Principles

### 1. Immutability

Once logged, audit records cannot be modified or deleted (only archived).

```
Audit Log Entry
├─ Timestamp (UTC)
├─ Request ID
├─ Decision
├─ Outcome
└─ Status: IMMUTABLE
```

### 2. Completeness

Every decision point creates an audit record:

- ✅ Control plane decisions (policy evaluation, gate results)
- ✅ Agent executions (prompt, response, cost)
- ✅ Tool invocations (which tool, parameters, result)
- ✅ Human decisions (approval, rejection, rationale)
- ✅ System failures (errors, timeouts, retries)

### 3. Queryability

Audit logs are indexed and queryable for compliance, debugging, and analysis.

### 4. Performance

Audit logging must not be the critical path (asynchronous where possible).

---

## Execution Tracing

### Request Lifecycle

Every request generates a trace:

```
Time: 2026-05-12T14:30:00Z
Request ID: req-2026-05-12-0042
Entry Point: n8n webhook
Input: {"video_url": "https://youtube.com/watch?v=abc123"}
         │
         ├─[T+0ms] Classification: ROUTINE
         ├─[T+5ms] Policy evaluation: POL-0001 ALLOW
         ├─[T+10ms] Trust gate: confidence=95% PASS
         ├─[T+15ms] Model router: Haiku (fast scoring)
         ├─[T+20ms] Agent spawn: agent-screening-v1
         │   ├─ Prompt tokens: 1250
         │   ├─ Response tokens: 145
         │   └─ Latency: 1850ms
         ├─[T+1870ms] Scoring result: PROMOTE (89/100)
         ├─[T+1875ms] Neo4j UPSERT: 1 record inserted
         ├─[T+1880ms] Obsidian write: validation-note.md created
         ├─[T+1885ms] Output validation: PASS
         └─[T+1890ms] Completion: SUCCESS
         
Output: {"routing": "PROMOTE", "confidence": 0.95}
Status: SUCCESS
Total Latency: 1890ms
Cost: CAD $0.018
```

### Trace Structure (JSON)

```json
{
  "trace_id": "trace-2026-05-12-0042",
  "request_id": "req-2026-05-12-0042",
  "timestamp": "2026-05-12T14:30:00Z",
  "user_id": "user-001",
  
  "request": {
    "source": "n8n-webhook",
    "path": "/webhook/youtube-validation",
    "method": "POST",
    "input_size_bytes": 256,
    "input_hash": "sha256:abc123def456..."
  },
  
  "spans": [
    {
      "span_id": "span-001",
      "name": "sensitivity_classification",
      "start_time": "2026-05-12T14:30:00.000Z",
      "end_time": "2026-05-12T14:30:00.005Z",
      "duration_ms": 5,
      "status": "SUCCESS",
      "output": {
        "sensitivity": "ROUTINE",
        "decision_type": "validation"
      }
    },
    {
      "span_id": "span-002",
      "name": "policy_gate_evaluation",
      "start_time": "2026-05-12T14:30:00.005Z",
      "end_time": "2026-05-12T14:30:00.010Z",
      "duration_ms": 5,
      "status": "SUCCESS",
      "output": {
        "policies_evaluated": ["POL-0001"],
        "policy_result": "ALLOW",
        "constraints_met": true
      }
    },
    {
      "span_id": "span-003",
      "name": "agent_execution",
      "start_time": "2026-05-12T14:30:00.020Z",
      "end_time": "2026-05-12T14:30:01.870Z",
      "duration_ms": 1850,
      "status": "SUCCESS",
      "agent_id": "agent-screening-v1",
      "model": "claude-3-5-haiku",
      "output": {
        "scores": {
          "credibility": 85,
          "quality": 92,
          "relevance": 88,
          "alignment": 90
        },
        "routing": "PROMOTE"
      },
      "cost": 0.018,
      "tokens": {
        "input": 1250,
        "output": 145
      }
    }
  ],
  
  "outcome": {
    "status": "SUCCESS",
    "result": {"routing": "PROMOTE", "confidence": 0.95},
    "total_latency_ms": 1890,
    "cost": 0.018
  },
  
  "audit": {
    "audit_record_id": "audit-2026-05-12-0042",
    "logged_at": "2026-05-12T14:30:01.900Z",
    "retention_until": "2033-05-12"  # 7 years
  }
}
```

---

## Lineage Tracking

### Data Lineage Graph

**Question:** "Why was this video classified as ARCHIVE?"

**Answer:** Lineage graph explains the full chain:

```
Video Input (abc123)
    ├─ Extracted transcript: "Claude models are frozen..."
    │   └─ Source: YouTube transcript API
    │
    ├─ Scoring by agent-screening-v1
    │   ├─ Credibility: 45 (controversial claim)
    │   │   ├─ Contrasts with: Obsidian note "Claude-Freezing-Study.md" (95% confidence)
    │   │   └─ Source credibility check against Neo4j
    │   ├─ Quality: 72 (decent production)
    │   └─ Relevance: 58 (marginally aligned)
    │
    ├─ Routing decision
    │   ├─ Composite score: 68
    │   ├─ Relevance floor: 58 < 60? NO
    │   └─ → Classification: INBOX (not ARCHIVE)
    │
    └─ Final decision
        └─ User decision: ARCHIVE (overrides recommendation)
            └─ Reason: "Source is known misinformation"
            └─ Escalation: esc-2026-05-12-0099
```

### Lineage Data Structure

```json
{
  "lineage_id": "lineage-2026-05-12-0042",
  "entity_id": "video-abc123",
  "entity_type": "VideoCapture",
  "decision": "ARCHIVE",
  
  "lineage_path": [
    {
      "step": 1,
      "stage": "input_capture",
      "input": "youtube.com/watch?v=abc123",
      "output": "VideoCapture object",
      "timestamp": "2026-05-12T14:00:00Z"
    },
    {
      "step": 2,
      "stage": "transcript_extraction",
      "input": "VideoCapture.video_id",
      "output": "transcript_text (5200 chars)",
      "source": "YouTube API v3",
      "timestamp": "2026-05-12T14:01:00Z"
    },
    {
      "step": 3,
      "stage": "agent_screening",
      "agent": "agent-screening-v1",
      "input": "transcript",
      "output": "scores: credibility=45, quality=72, relevance=58",
      "inference_id": "inf-2026-05-12-0042",
      "timestamp": "2026-05-12T14:30:00Z"
    },
    {
      "step": 4,
      "stage": "routing_decision",
      "input": "scores",
      "decision_logic": "composite_score=68; relevance=58 >= 60 PASS; → INBOX",
      "output": "INBOX recommendation",
      "timestamp": "2026-05-12T14:30:01Z"
    },
    {
      "step": 5,
      "stage": "human_decision",
      "human_id": "user@domain.com",
      "human_decision": "ARCHIVE (override INBOX recommendation)",
      "reasoning": "Source is known misinformation outlet",
      "escalation_id": "esc-2026-05-12-0099",
      "timestamp": "2026-05-12T14:35:00Z"
    }
  ],
  
  "dependencies": [
    {
      "depends_on": "YouTube API transcript for abc123",
      "relationship": "input_to_scoring",
      "strength": "critical"
    },
    {
      "depends_on": "Obsidian note: Claude-Freezing-Study.md (95% confidence)",
      "relationship": "contradiction_check",
      "strength": "important"
    },
    {
      "depends_on": "agent-screening-v1 (version 1.0.0)",
      "relationship": "scoring_agent",
      "strength": "critical"
    }
  ]
}
```

### Lineage Queries

**Query 1: "Show me all data that depends on this Obsidian note"**

```cypher
MATCH (note:ObsidianNote {id: 'Claude-Freezing-Study'})
MATCH path = (note)-[:USED_BY|:CONTRADICTS|:SUPPORTS]*(decision:Decision)
RETURN path
ORDER BY decision.timestamp DESC
LIMIT 20
```

**Query 2: "What caused this decision?"**

```cypher
MATCH (decision:Decision {id: 'video-abc123-ARCHIVE'})
MATCH (decision)<-[:CAUSED_BY]-(score:Score)
MATCH (score)<-[:COMPUTED_BY]-(agent:Agent)
RETURN decision, score, agent
```

**Query 3: "Did this source change trigger any decisions?"**

```sql
SELECT 
  d.decision_id,
  d.entity_id,
  d.decision,
  d.changed_at
FROM decisions d
INNER JOIN lineage l ON d.decision_id = l.final_decision
WHERE l.lineage_path LIKE '%source_id=45%'
  AND d.changed_at BETWEEN '2026-01-01' AND '2026-05-12'
ORDER BY d.changed_at DESC;
```

---

## Compliance & Audit Logging

### Audit Log Entry Format

Every decision creates an immutable audit log entry:

```json
{
  "audit_id": "audit-2026-05-12-0042",
  "timestamp": "2026-05-12T14:30:01.900Z",
  "request_id": "req-2026-05-12-0042",
  
  "decision_log": {
    "decision_type": "knowledge_classification",
    "decision": "ARCHIVE",
    "sensitivity_level": "ROUTINE",
    "policy_evaluated": "POL-0001-agent-neo4j-read",
    "policy_result": "ALLOW"
  },
  
  "actor_log": {
    "initiator": "system",  # or "user@domain.com"
    "agent_id": "agent-screening-v1",
    "model": "claude-3-5-haiku"
  },
  
  "resource_log": {
    "resource_type": "VideoCapture",
    "resource_id": "video-abc123",
    "operation": "CLASSIFY",
    "before_state": null,  # First classification
    "after_state": {"routing": "ARCHIVE"}
  },
  
  "control_plane_log": {
    "sensitivity_classifier_result": "ROUTINE",
    "policy_gate_result": "ALLOW",
    "trust_threshold_result": "PASS (confidence=95%)",
    "model_router_result": "Haiku",
    "output_validation_result": "PASS"
  },
  
  "execution_log": {
    "execution_id": "exec-2026-05-12-0042",
    "status": "SUCCESS",
    "latency_ms": 1890,
    "cost": {
      "amount": 0.018,
      "currency": "CAD"
    }
  },
  
  "metadata": {
    "ip_address": "192.168.1.50",
    "user_agent": "n8n/1.0",
    "session_id": "sess-abc123",
    "correlation_id": "req-2026-05-12-0042"
  },
  
  "signature": {
    "algorithm": "SHA-256",
    "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "signed_at": "2026-05-12T14:30:01.900Z"
  }
}
```

### Compliance Fields by Regulation

**GDPR Compliance:**

```json
{
  "gdpr": {
    "data_subject_id": "user-001",
    "personal_data_processed": ["user_id", "session_id"],
    "legal_basis": "consent",
    "consent_given": true,
    "consent_timestamp": "2026-01-01T00:00:00Z",
    "purpose": "knowledge_management",
    "retention_period": "7 years"
  }
}
```

**PIPEDA Compliance (Canadian):**

```json
{
  "pipeda": {
    "personal_information": ["user_id", "timestamp"],
    "use_limitation": "knowledge_management_only",
    "accuracy_maintained": true,
    "access_request_method": "contact_privacy_officer@company.com"
  }
}
```

**HIPAA Compliance (if health data):**

```json
{
  "hipaa": {
    "phi_involved": false,  # No personal health information
    "if_phi_involved": {
      "encryption": "AES-256",
      "access_control": "role_based",
      "audit_control": "automatic"
    }
  }
}
```

---

## Monitoring & Alerting

### Key Metrics (Prometheus)

```
# Request volume
pca_requests_total{
  sensitivity="routine|sensitive|critical",
  status="success|failure|escalation"
}

# Latency (milliseconds)
pca_request_latency_seconds{
  stage="classification|policy|inference|output",
  agent="agent_id"
}

# Cost tracking (CAD)
pca_inference_cost_total{
  model="haiku|sonnet|qwen7b|qwen32b",
  agent="agent_id"
}

# Agent performance
pca_agent_agreement_rate{
  agent_pair="screening+critical"
}

pca_agent_escalation_rate{
  agent="agent_id"
}

# System health
pca_gpu_utilization_percent
pca_memory_usage_bytes
pca_neo4j_query_latency_seconds
pca_postgresql_connections_active
```

### Alert Rules (Grafana)

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| **High error rate** | >5% errors in 5 min | Critical | Page on-call |
| **GPU out of memory** | Ollama OOM errors | High | Scale down model |
| **Policy gate stalled** | 100+ pending escalations | High | Review escalation queue |
| **Cost anomaly** | >$10 today (baseline $5) | Medium | Review requests |
| **Database slow** | Neo4j query >5s | Medium | Check indices |
| **API timeout** | Anthropic API latency >10s | Medium | Fallback to local model |
| **Disk space** | <20% free on /pca | Low | Archive old logs |

### Grafana Dashboards

**Dashboard 1: System Health**

```
Top row:
├─ Requests (24h): 1,247
├─ Success rate: 98.2%
├─ Avg latency: 1.8s
└─ Cost (24h): CAD $2.14

Middle row:
├─ GPU Utilization: 62%
├─ Memory: 18GB / 32GB
├─ Neo4j: 42k nodes
└─ Error rate: 1.8%

Bottom row:
├─ Request volume (24h line chart)
├─ Latency by stage (stacked bar)
├─ Cost trend (line chart, 30 days)
└─ Alert history
```

**Dashboard 2: Agent Performance**

```
Top row:
├─ Agent-Screening: 847 reqs, 98% success
├─ Agent-Critical: 843 reqs, 99% success
├─ Agreement rate: 94%
└─ Avg disagreement: 8 points

Middle row:
├─ Screening latency: 1.2s
├─ Critical latency: 1.4s
├─ Cost/video: CAD $0.018
└─ Confidence distribution (histogram)

Bottom row:
├─ Escalation rate by trigger
├─ Routing distribution (PROMOTE/INBOX/ARCHIVE pie chart)
└─ Confidence vs. actual quality (scatter plot)
```

---

## Log Retention & Compliance

### Retention Policy

```
Log Type                  | Retention Period | Storage | Access
──────────────────────────┼──────────────────┼─────────┼────────────────
Audit logs                | 7 years          | Archive | Read-only
Execution traces          | 90 days          | Hot     | Full access
Error logs                | 30 days          | Hot     | Engineering
User access logs          | 2 years          | Archive | Security audit
Inference models/prompts  | Permanent        | Archive | Legal hold
```

### Encryption & Security

**At Rest:**

```
Archive logs (PostgreSQL):
├─ Table-level encryption: AES-256
├─ Key storage: /etc/pca/db-key.enc
└─ Rotation: Annual

Obsidian vault:
├─ File encryption: Optional (user choice)
├─ If encrypted: AES-256-GCM
└─ Key: Managed by user
```

**In Transit:**

```
All API calls: TLS 1.3
├─ Anthropic API: HTTPS
├─ PostgreSQL: SSL/TLS required
├─ Redis: TLS optional (local only, less critical)
└─ Neo4j: Bolt+TLS
```

### Compliance Export

**Query: "Export all audit logs for user-001 (GDPR Right to Access)"**

```sql
SELECT 
  audit_id,
  timestamp,
  resource_type,
  operation,
  result,
  metadata
FROM audit_logs
WHERE data_subject_id = 'user-001'
  AND timestamp BETWEEN '2026-01-01' AND '2026-05-12'
ORDER BY timestamp DESC;

-- Output: JSON export, signed, delivered to user
```

---

## Audit Query Patterns

### Pattern 1: "Who approved this decision?"

```sql
SELECT 
  a.audit_id,
  a.timestamp,
  a.resource_id,
  a.decision,
  a.actor_log.initiator as approver,
  a.resource_log.after_state
FROM audit_logs a
WHERE a.resource_id = 'video-abc123'
  AND a.decision_log.decision_type = 'classification'
ORDER BY a.timestamp DESC
LIMIT 1;
```

### Pattern 2: "Which decisions have high cost?"

```sql
SELECT 
  a.audit_id,
  a.request_id,
  a.resource_id,
  a.execution_log.cost.amount as cost,
  a.execution_log.latency_ms,
  a.actor_log.agent_id
FROM audit_logs a
WHERE a.execution_log.cost.amount > 0.05  # > $0.05
  AND a.timestamp > DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY cost DESC
LIMIT 20;
```

### Pattern 3: "How often do agents disagree?"

```sql
SELECT 
  DATE_FORMAT(a.timestamp, '%Y-%m-%d') as date,
  a.control_plane_log.agent_disagreement_count,
  COUNT(*) as total_decisions,
  ROUND(100 * 
    SUM(CASE WHEN a.control_plane_log.agent_disagreement_count > 0 THEN 1 ELSE 0 END) 
    / COUNT(*), 2) as disagreement_rate_percent
FROM audit_logs a
WHERE a.timestamp > DATE_SUB(NOW(), INTERVAL 90 DAY)
  AND a.decision_log.decision_type = 'validation'
GROUP BY DATE_FORMAT(a.timestamp, '%Y-%m-%d')
ORDER BY date DESC;
```

### Pattern 4: "What caused an escalation?"

```sql
SELECT 
  e.escalation_id,
  e.created_at,
  e.trigger_type,
  e.severity,
  e.content_summary,
  e.resolution,
  e.resolved_at,
  TIMESTAMPDIFF(MINUTE, e.created_at, e.resolved_at) as response_time_minutes
FROM escalations e
WHERE e.escalation_id = 'esc-2026-05-12-0099'
LIMIT 1;
```

---

## Integration with Control Plane

The Observability & Audit layer **records the decisions** made by the Cognitive Control Plane:

```
Control Plane Decision
     │
     ├─ Sensitivity Classifier
     │  └─ [AUDIT] Classified as ROUTINE/SENSITIVE/CRITICAL
     │
     ├─ Policy Gate
     │  └─ [AUDIT] Evaluated policies, result: ALLOW/DENY/ESCALATE
     │
     ├─ Trust Threshold Gate
     │  └─ [AUDIT] Confidence=95%, result: PASS/FAIL
     │
     ├─ Model Router
     │  └─ [AUDIT] Selected model: Haiku
     │
     ├─ Execution Authorization
     │  └─ [AUDIT] Authorized execution, constraints applied
     │
     ├─ Inference Execution
     │  └─ [AUDIT] Agent executed, tokens/cost tracked
     │
     └─ Output Validation
        └─ [AUDIT] Output validated, result logged

Result: Complete audit trail from request → decision → outcome
```

---

## Revision History

- **2026-05-12:** Initial version. Specified execution tracing, lineage tracking, compliance logging, monitoring, and retention policies.

