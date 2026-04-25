---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, control-plane, governance, routing, policy]
status: active
---

# PCA Control Plane Specification

## Definition

The **Control Plane** is the governance and routing layer that sits above the ingestion pipelines. It defines:

- **Ingestion policies** — what sources are allowed, what governance applies
- **Routing rules** — where data flows based on signal type, confidence, and sensitivity
- **Compute/cost controls** — which processing paths are used, when to use local vs. API
- **Model selection logic** — which classifiers, scorers, embedders are used for each pattern
- **Access controls** — what knowledge is available to which agents/users
- **Audit trails** — compliance and observability

This is the PCA equivalent of the enterprise control plane layer (PATH) that HC/PHAC uses to govern HAIL (runtime) and Purview (governance).

---

## Architecture Overview

```
┌────────────────────────────────────────────────┐
│         CONTROL PLANE (Policy Layer)           │
│                                                │
│  ┌──────────────┬──────────────┬──────────┐  │
│  │  Ingestion   │   Routing    │ Compute  │  │
│  │   Policies   │    Rules     │ Controls │  │
│  └──────────────┴──────────────┴──────────┘  │
│                                                │
└────────────────┬─────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐ ┌──────────┐ ┌─────────┐
│ Pattern │ │ Pattern  │ │ Pattern │
│   1     │ │    2     │ │   3     │
│Structured│ │Unstructed│ │Dynamics │
└─────────┘ └──────────┘ └─────────┘
    │            │            │
    └────────────┼────────────┘
                 ▼
    ┌────────────────────────┐
    │   RUNTIME (HAIL)       │
    │  Obsidian | Vector DB  │
    └────────────────────────┘
```

---

## Layer 1: Ingestion Policies

### What is Allowed?

Define source whitelist/blacklist and governance tier:

```json
{
  "ingestion_policies": [
    {
      "policy_id": "policy-001",
      "source_type": "web-article",
      "description": "General web articles and news",
      "status": "active",
      
      "sources_allowed": [
        {
          "domain": "*.bbc.com",
          "credibility_tier": "reputable",
          "requires_review": false
        },
        {
          "domain": "*.linkedin.com/pulse/*",
          "credibility_tier": "moderate",
          "requires_review": "high-priority-only"
        },
        {
          "domain": "*.medium.com",
          "credibility_tier": "moderate",
          "requires_review": false
        }
      ],
      
      "sources_blocked": [
        {
          "domain": "*.misinformation-tracker.org",
          "reason": "known disinformation source"
        }
      ],
      
      "governance": {
        "classification": "unclassified",
        "data_handling": "standard-ingestion",
        "retention_days": 730,
        "audit_required": true
      },
      
      "processing_path": "pattern-1-structured-knowledge"
    },
    
    {
      "policy_id": "policy-002",
      "source_type": "voice-note",
      "description": "iPhone voice captures of personal thoughts",
      "status": "active",
      
      "sources_allowed": [
        {
          "device": "iPhone 15 Pro",
          "credibility_tier": "user",
          "requires_review": false
        }
      ],
      
      "governance": {
        "classification": "personal",
        "data_handling": "local-only",
        "retention_days": 0,
        "audit_required": false
      },
      
      "processing_path": "pattern-2-unstructured-ideas"
    },
    
    {
      "policy_id": "policy-003",
      "source_type": "rss-feed",
      "description": "News and signal feeds",
      "status": "active",
      
      "sources_allowed": [
        {
          "feed": "https://...",
          "name": "HC news feed",
          "credibility_tier": "internal",
          "requires_review": false,
          "poll_interval_minutes": 60
        }
      ],
      
      "governance": {
        "classification": "internal",
        "data_handling": "standard-ingestion",
        "retention_days": 90,
        "audit_required": true
      },
      
      "processing_path": "pattern-3-dynamic-signals"
    }
  ]
}
```

### Policy Application Logic

```
For each inbound source:
  1. Extract source URL/type
  2. Match against ingestion policies
  3. If no match:
     → Check default policy (allow or block?)
     → Apply governance tier
  4. If match found:
     → Apply source-specific governance
     → Validate against credibility tier
     → Determine if review required
     → Route to correct processing path
```

---

## Layer 2: Routing Rules

### Signal Type → Processing Path

Route based on signal type, confidence, and governance requirements:

```json
{
  "routing_rules": [
    {
      "rule_id": "route-001",
      "name": "Structured Knowledge Auto-Route",
      "trigger": {
        "pattern_type": "structured-knowledge",
        "confidence_min": 0.80,
        "source_credibility": "reputable",
        "governance_classification": "unclassified"
      },
      "action": {
        "destination": "vector-db + knowledge-graph",
        "requires_review": false,
        "tags": ["trusted-knowledge"],
        "state": "trusted"
      }
    },
    
    {
      "rule_id": "route-002",
      "name": "Structured Knowledge Provisional",
      "trigger": {
        "pattern_type": "structured-knowledge",
        "confidence_min": 0.65,
        "confidence_max": 0.79,
        "source_credibility": ["moderate", "reputable"]
      },
      "action": {
        "destination": "obsidian-vault + vector-db",
        "requires_review": true,
        "tags": ["provisional", "pending-review"],
        "state": "provisional",
        "review_priority": "high"
      }
    },
    
    {
      "rule_id": "route-003",
      "name": "Unstructured Ideas to Inbox",
      "trigger": {
        "pattern_type": "unstructured-ideas",
        "confidence_max": 0.75
      },
      "action": {
        "destination": "obsidian-inbox",
        "requires_review": false,
        "tags": ["inbox", "requires-triage"],
        "state": "inbox",
        "deferred_processing": true
      }
    },
    
    {
      "rule_id": "route-004",
      "name": "Dynamic Signals High Priority",
      "trigger": {
        "pattern_type": "dynamic-signals",
        "signal_score_min": 0.75,
        "urgency": "high"
      },
      "action": {
        "destinations": ["alert-queue", "obsidian-inbox"],
        "requires_review": true,
        "tags": ["critical-alert"],
        "escalation_required": true,
        "notifications": ["push", "email"]
      }
    },
    
    {
      "rule_id": "route-005",
      "name": "Sensitive Content Quarantine",
      "trigger": {
        "governance_classification": ["protected-b", "confidential"],
        "pattern_type": "any"
      },
      "action": {
        "destination": "local-vault-only",
        "requires_review": true,
        "requires_approval": true,
        "tags": ["sensitive", "requires-approval"],
        "audit_required": true,
        "access_control": "restricted"
      }
    }
  ]
}
```

### Routing Decision Logic

```
For each processed candidate:
  1. Evaluate against all applicable routing rules (in priority order)
  2. First rule that triggers wins
  3. Apply action (destination, review requirement, tags, notifications)
  4. Log decision to audit trail
  5. Update candidate state based on action
```

---

## Layer 3: Compute/Cost Controls

### Model Selection Logic

Choose which models/APIs to use based on signal type, confidence, and cost:

```json
{
  "compute_controls": {
    "transcription": {
      "models": [
        {
          "model_id": "whisper-local",
          "type": "local",
          "latency_ms": 3000,
          "quality": 0.94,
          "cost_per_run": 0.0,
          "triggers": [
            {
              "pattern": "unstructured-ideas",
              "confidence_min": 0.0,
              "use_when": "always"
            },
            {
              "pattern": "structured-knowledge",
              "confidence_min": 0.0,
              "use_when": "volume > 100/day"
            }
          ]
        },
        {
          "model_id": "whisper-api",
          "type": "external-api",
          "latency_ms": 2000,
          "quality": 0.96,
          "cost_per_run": 0.01,
          "triggers": [
            {
              "pattern": "structured-knowledge",
              "confidence_min": 0.0,
              "use_when": "high-quality-required"
            }
          ]
        }
      ],
      "default_model": "whisper-local",
      "fallback_model": "whisper-api"
    },
    
    "classification": {
      "models": [
        {
          "model_id": "gpt-4",
          "type": "external-api",
          "latency_ms": 2000,
          "quality": 0.94,
          "cost_per_run": 0.03,
          "triggers": [
            {
              "pattern": "all",
              "confidence_min": 0.0,
              "use_when": "default"
            }
          ]
        },
        {
          "model_id": "mistral-7b-local",
          "type": "local",
          "latency_ms": 5000,
          "quality": 0.87,
          "cost_per_run": 0.0,
          "triggers": [
            {
              "pattern": "unstructured-ideas",
              "confidence_min": 0.0,
              "use_when": "always"
            },
            {
              "pattern": "all",
              "use_when": "cost-optimization-mode"
            }
          ]
        }
      ],
      "default_model": "gpt-4",
      "cost_optimization_threshold": 100,
      "local_fallback": "mistral-7b-local"
    },
    
    "embeddings": {
      "models": [
        {
          "model_id": "all-miniLM-l6-v2",
          "type": "local",
          "latency_ms": 100,
          "quality": 0.89,
          "cost_per_run": 0.0,
          "triggers": [
            {
              "pattern": "all",
              "use_when": "always"
            }
          ]
        }
      ],
      "default_model": "all-miniLM-l6-v2"
    }
  },
  
  "cost_budgets": {
    "monthly_budget_usd": 50,
    "per_pattern_budgets": {
      "structured-knowledge": 30,
      "unstructured-ideas": 5,
      "dynamic-signals": 15
    },
    "alerts": {
      "warn_at_percent": 80,
      "block_at_percent": 100
    }
  }
}
```

### Cost Optimization Strategy

```
IF cost_this_month >= budget THEN
  → Switch non-critical workflows to local models
  → Reduce API polling frequency
  → Increase batch processing window
  → Alert user to cost situation

IF monthly_cost < 50% budget THEN
  → Can afford higher-quality models
  → Increase validation depth
  → Enable real-time processing
```

---

## Layer 4: Access Controls

### Knowledge Graph Access

Define what knowledge is accessible to different agents/users:

```json
{
  "access_control_policies": [
    {
      "access_id": "acl-001",
      "resource": "knowledge-graph",
      "classification": "unclassified",
      "access_rules": [
        {
          "principal": "user",
          "action": ["read", "write", "delete"],
          "scope": "all-unclassified",
          "conditions": "none"
        },
        {
          "principal": "rag-agent",
          "action": ["read"],
          "scope": "trusted+provisional",
          "conditions": "confidence >= 0.65"
        },
        {
          "principal": "external-api",
          "action": [],
          "scope": "none",
          "conditions": "access-denied"
        }
      ]
    },
    
    {
      "access_id": "acl-002",
      "resource": "knowledge-graph",
      "classification": "protected-b",
      "access_rules": [
        {
          "principal": "user",
          "action": ["read", "write"],
          "scope": "all-sensitive",
          "conditions": "local-only"
        },
        {
          "principal": "rag-agent",
          "action": [],
          "scope": "none",
          "conditions": "no-access-to-sensitive"
        }
      ]
    },
    
    {
      "access_id": "acl-003",
      "resource": "vector-db",
      "classification": "all",
      "access_rules": [
        {
          "principal": "retrieval-agent",
          "action": ["semantic-search"],
          "scope": "all-accessible",
          "conditions": "respect-classification"
        },
        {
          "principal": "user",
          "action": ["search", "delete"],
          "scope": "all",
          "conditions": "none"
        }
      ]
    }
  ]
}
```

---

## Layer 5: Audit & Compliance

### Audit Trail Requirements

Every routing decision must be logged:

```json
{
  "audit_entry": {
    "entry_id": "uuid",
    "timestamp": "2026-04-25T14:30:00Z",
    "subject": "candidate_id",
    
    "control_plane_decision": {
      "ingestion_policy_applied": "policy-001",
      "routing_rule_triggered": "route-002",
      "destination": "obsidian-vault",
      "governance_classification": "unclassified",
      "requires_review": true,
      "reason": "confidence 0.72 is provisional threshold"
    },
    
    "models_used": [
      {
        "model": "whisper-local",
        "latency_ms": 2800,
        "cost_usd": 0.0
      },
      {
        "model": "gpt-4",
        "latency_ms": 2100,
        "cost_usd": 0.03
      }
    ],
    
    "access_control": {
      "classification": "unclassified",
      "access_granted_to": ["user", "rag-agent"]
    },
    
    "tags": ["structured-knowledge", "provisional", "PATH-HAIL"]
  }
}
```

### Compliance Reporting

```
Monthly reports:
├─ Total documents ingested (by pattern)
├─ Routing decisions (distribution across actions)
├─ Model costs (actual vs. budget)
├─ Access violations (attempts denied)
├─ Review queue status (pending reviews)
├─ Governance classification distribution
├─ Sensitive data handling (if applicable)
└─ Audit log health (missing entries?)

Alerts:
├─ Cost budget exceeded
├─ High review queue backlog
├─ Access violations
├─ Model errors (confidence scores unusual)
└─ Policy violations (unauthorized source detected)
```

---

## Integration: Ingestion Policies → Routes → Compute

### Complete Example Flow

```
Scenario: User saves article from BBC News

Step 1: INGESTION POLICY
  Source: bbc.com
  Policy match: policy-001 (web-articles)
  Credibility tier: reputable
  Governance: unclassified
  Processing path: pattern-1-structured-knowledge
  ✓ Allowed

Step 2: PROCESSING
  Route to transcription + extraction
  Default models:
    ├─ whisper-local (cost: $0.00)
    ├─ gpt-4 (cost: $0.03)
    └─ all-miniLM-l6-v2 (cost: $0.00)
  Output: Candidate with confidence 0.78

Step 3: ROUTING RULES
  Candidate confidence: 0.78 (falls in 0.65-0.79 range)
  Rule match: route-002 (provisional)
  Action:
    ├─ Destination: obsidian-vault + vector-db
    ├─ Requires review: true
    ├─ State: provisional
    └─ Tags: [provisional, pending-review]

Step 4: ACCESS CONTROL
  Classification: unclassified
  User access: read/write/delete ✓
  RAG agent access: read (provisional) ✓

Step 5: AUDIT LOG
  ├─ Policy applied: policy-001
  ├─ Route applied: route-002
  ├─ Cost: $0.03
  ├─ Classification: unclassified
  └─ Timestamp: 2026-04-25T14:30:00Z
```

---

## Implementation Checklist

### Phase 1a
- [ ] Define ingestion policies for all three patterns
- [ ] Create routing rules for high/medium/low confidence buckets
- [ ] Set up local model fallbacks for cost control
- [ ] Implement audit logging for all decisions
- [ ] Deploy access control framework (basic)

### Phase 1b
- [ ] Add dynamic cost tracking and budget alerts
- [ ] Implement multi-tier review queue (priority-based)
- [ ] Add compliance reporting dashboard
- [ ] Enable policy updates without redeployment

### Phase 2
- [ ] Integrate with local LLM (Mistral 7B)
- [ ] Add temporal policies (different rules for time-sensitive data)
- [ ] Implement policy learning (adjust based on user feedback)
- [ ] Enable fine-grained access control (per-user, per-project)

---

## Non-Negotiable Principles

1. **Policy is code** — all decisions are explicit, versioned, auditable
2. **Governance scales with sensitivity** — unclassified has light controls, protected-b has strong controls
3. **Compute is optimizable** — local-first, API fallback
4. **Access is explicit** — deny by default, whitelist what's allowed
5. **Every decision is logged** — audit trail enables compliance and learning

---

## Analogy: HC/PHAC Equivalence

| PCA Component | HC/PHAC Equivalent | Purpose |
|---|---|---|
| Ingestion Policies | Data intake policies | Define what sources are trusted |
| Routing Rules | PATH routing logic | Send data to correct processing tier |
| Compute Controls | Compute resource policies | Optimize for cost/quality/latency |
| Access Control | IAM (Identity/Access Mgmt) | Restrict data to authorized users |
| Audit Trail | Purview audit logs | Compliance and forensics |
| Knowledge Graph | Data Lake structure | Canonical, queryable store |

**Key insight**: Your PCA control plane is doing at personal scale what PATH does at enterprise scale — governing data flow, enforcing policy, managing compute, ensuring compliance.

---

**Status**: Active specification (v1.0)

**Last Updated**: 2026-04-25

**Next**: Create feedback loop specification (user validation, model calibration, learning)

**Related**:
- pca-ingestion-patterns.md (pattern workflows)
- pca-feedback-learning-loop.md (learning from control plane decisions)
- pca-compliance-and-governance.md (enterprise governance framework)
