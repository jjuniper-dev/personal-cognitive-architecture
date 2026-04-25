---
type: schema
created: 2026-04-25
updated: 2026-04-25
tags: [pca, schema, knowledge-candidate, data-model]
status: active
---

# Knowledge Candidate Schema

## Definition

A **Knowledge Candidate** is any piece of information entering the PCA system. It flows through nine pipeline stages, accumulating metadata, decisions, and lineage at each step.

This document defines the JSON schema for a Knowledge Candidate as it transforms from raw capture through final integration into the knowledge graph.

## Principle

> A knowledge candidate is not committed to memory until it has been: captured, normalized, scored, classified, reconciled, routed, integrated, and audited.

Each stage adds fields without destroying prior information. Full lineage is retained.

---

## Stage 0: Raw Input (Pre-Capture)

Multi-modal input before standardization.

```json
{
  "input_id": "uuid",
  "capture_timestamp": "2026-04-25T14:30:00Z",
  "source_type": "voice|web|chat|file|email|structured",
  
  "voice": {
    "audio_url": "s3://capture-bucket/audio-uuid.m4a",
    "duration_seconds": 45,
    "device": "iPhone 15 Pro",
    "location": "office"
  },
  
  "web": {
    "url": "https://example.com/article",
    "title": "Article Title",
    "html": "raw html content"
  },
  
  "chat": {
    "thread_id": "slack-thread-123",
    "message_id": "msg-456",
    "participant_ids": ["user_id_1", "user_id_2"],
    "text": "full conversation text"
  },
  
  "file": {
    "filename": "document.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 1024000,
    "base64_content": "base64..."
  },
  
  "structured": {
    "schema": "task|meeting|decision|research-log",
    "fields": {}
  },
  
  "metadata": {
    "user_id": "current_user",
    "context_note": "optional user context at capture time"
  }
}
```

---

## Stage 1: Captured Candidate

After input has been received and queued for processing.

```json
{
  "candidate_id": "uuid (stable across all stages)",
  "stage": "captured",
  "capture_timestamp": "2026-04-25T14:30:00Z",
  
  "input": {
    "source_type": "voice|web|chat|file|email|structured",
    "source_metadata": { ... raw input ... }
  },
  
  "processing": {
    "queued_at": "2026-04-25T14:30:05Z",
    "status": "queued|in-progress|waiting-for-review|failed",
    "stage_processing_time_ms": 0
  },
  
  "lineage": {
    "events": [
      {
        "timestamp": "2026-04-25T14:30:05Z",
        "event": "captured",
        "detail": "Input received and queued"
      }
    ]
  }
}
```

---

## Stage 2: Normalized Candidate

After transcription, extraction, chunking, and language normalization.

```json
{
  "candidate_id": "uuid",
  "stage": "normalized",
  
  "capture": { ... previous stage ... },
  
  "normalized": {
    "raw_text": "Full transcribed or extracted text",
    "language": "en|fr",
    "detected_language_confidence": 0.98,
    
    "chunks": [
      {
        "chunk_index": 0,
        "text": "Chunk of text",
        "byte_start": 0,
        "byte_end": 150,
        "tokens_approx": 25,
        "metadata": {
          "source_paragraph": 0,
          "timestamp_seconds": 5.2
        }
      }
    ],
    
    "extraction": {
      "extracted_entities": [
        {
          "type": "person|date|location|org|product",
          "value": "Chad",
          "context": "surrounding text",
          "confidence": 0.92
        }
      ],
      
      "structured_fields": {
        "deadline": "2026-04-30",
        "priority": "high",
        "project_references": ["PATH-HAIL"]
      }
    },
    
    "quality_metrics": {
      "transcription_confidence": 0.94,
      "extraction_completeness": 0.87,
      "text_coherence": 0.91
    }
  },
  
  "processing": {
    "normalized_at": "2026-04-25T14:30:15Z",
    "stage_processing_time_ms": 10000,
    "status": "success|warning|error",
    "errors": []
  },
  
  "lineage": { ... previous lineage ... }
}
```

---

## Stage 3: Scored Candidate

After four-dimensional scoring and validation.

```json
{
  "candidate_id": "uuid",
  "stage": "scored",
  
  "capture": { ... previous stages ... },
  
  "scoring": {
    "credibility": {
      "score": 0.85,
      "factors": [
        {
          "factor": "known_source",
          "contribution": +0.15,
          "reasoning": "Source is established project"
        },
        {
          "factor": "extraction_confidence",
          "contribution": +0.10,
          "reasoning": "High extraction confidence"
        }
      ]
    },
    
    "relevance": {
      "score": 0.92,
      "factors": [
        {
          "factor": "user_captured_explicitly",
          "contribution": +0.30,
          "reasoning": "User selected this content"
        },
        {
          "factor": "domain_match",
          "contribution": +0.40,
          "reasoning": "Matches active project domain"
        },
        {
          "factor": "temporal_proximity",
          "contribution": +0.22,
          "reasoning": "Recent capture, timely content"
        }
      ]
    },
    
    "novelty": {
      "score": 0.68,
      "factors": [
        {
          "factor": "similar_notes_exist",
          "contribution": -0.20,
          "reasoning": "Similar content in vault"
        },
        {
          "factor": "new_perspective",
          "contribution": +0.18,
          "reasoning": "Different framing than existing notes"
        }
      ]
    },
    
    "signal_strength": {
      "score": 0.76,
      "factors": [
        {
          "factor": "action_indicators",
          "contribution": +0.30,
          "reasoning": "Contains explicit action verbs"
        },
        {
          "factor": "deadline_present",
          "contribution": +0.25,
          "reasoning": "Specific deadline mentioned"
        },
        {
          "factor": "person_assignment",
          "contribution": +0.21,
          "reasoning": "Clear actor identified"
        }
      ]
    },
    
    "overall_score": {
      "formula": "(credibility × 0.20) + (relevance × 0.40) + (novelty × 0.30) + (signal_strength × 0.10)",
      "score": 0.81,
      "routing_action": "ADVANCE_TO_INTEGRATION",
      "reasoning": "Score >= 0.75 and no contradictions detected"
    }
  },
  
  "validation": {
    "passes_credibility_floor": true,
    "passes_relevance_threshold": true,
    "flag_level": "none|low|medium|high",
    "flags": []
  },
  
  "processing": {
    "scored_at": "2026-04-25T14:30:25Z",
    "stage_processing_time_ms": 5000,
    "status": "success"
  },
  
  "lineage": { ... previous lineage ... }
}
```

---

## Stage 4: Classified Candidate

After domain, type, and intent classification.

```json
{
  "candidate_id": "uuid",
  "stage": "classified",
  
  "capture": { ... previous stages ... },
  "scoring": { ... previous scoring ... },
  
  "classification": {
    "domain": {
      "inferred": "strategic-planning|product-delivery|research|operations|governance|external-engagement",
      "confidence": 0.88,
      "rationale": "Content discusses organizational strategy"
    },
    
    "note_type": {
      "inferred": "task|meeting|idea|reference|decision|project-note|strategy-note|research|workflow-trigger",
      "confidence": 0.92,
      "rationale": "Contains explicit action assignment with deadline"
    },
    
    "intent": {
      "primary": "inform|request|decide|action|explore|record",
      "secondary": ["action"],
      "confidence": 0.85,
      "rationale": "Primary intent is task assignment"
    },
    
    "project": {
      "inferred": "PATH-HAIL",
      "confidence": 0.89,
      "alternate_projects": [
        {
          "project": "enterprise-ai",
          "confidence": 0.31
        }
      ],
      "rationale": "Explicit project mention and context alignment"
    },
    
    "tags": [
      {
        "tag": "deliverable",
        "source": "content-analysis",
        "confidence": 0.87
      },
      {
        "tag": "urgent",
        "source": "extracted-priority-field",
        "confidence": 0.95
      }
    ],
    
    "suggested_destination": {
      "path": "/10-Projects/PATH-HAIL/Tasks",
      "rationale": "Task type for PATH-HAIL project",
      "confidence": 0.89
    }
  },
  
  "processing": {
    "classified_at": "2026-04-25T14:30:30Z",
    "stage_processing_time_ms": 3000,
    "status": "success"
  },
  
  "lineage": { ... previous lineage ... }
}
```

---

## Stage 5: Reconciled Candidate

After comparison with existing knowledge graph.

```json
{
  "candidate_id": "uuid",
  "stage": "reconciled",
  
  "capture": { ... previous stages ... },
  "scoring": { ... previous scoring ... },
  "classification": { ... previous classification ... },
  
  "reconciliation": {
    "knowledge_graph_query": {
      "query_type": "semantic-similarity|exact-match|relationship-check",
      "similar_notes": [
        {
          "note_id": "existing-note-uuid",
          "title": "Previous related note",
          "similarity_score": 0.74,
          "relationship": "same-topic|related-topic|contradicts|supersedes|extends",
          "last_updated": "2026-04-20"
        }
      ]
    },
    
    "relationships_detected": [
      {
        "type": "related-to|depends-on|contradicts|updates|extends",
        "target_node_id": "uuid",
        "target_title": "Related topic",
        "confidence": 0.85,
        "reasoning": "Shares key concepts and project context"
      }
    ],
    
    "contradictions_detected": [
      {
        "contradiction_id": "uuid",
        "existing_node_id": "uuid",
        "existing_statement": "Fact from existing knowledge",
        "candidate_statement": "Contradicting fact from new candidate",
        "confidence_of_contradiction": 0.78,
        "severity": "low|medium|high",
        "reasoning": "Different claims about same topic"
      }
    ],
    
    "updates_existing": [
      {
        "target_node_id": "uuid",
        "update_type": "add-nuance|refine|correct|supersede",
        "existing_confidence": 0.65,
        "new_information_confidence": 0.88,
        "rationale": "New information is more recent and higher confidence"
      }
    ],
    
    "reconciliation_status": "clear|requires-review|contradicts-high-confidence|defer-to-review",
    "reconciliation_notes": "Candidate is compatible with existing knowledge or specific review needed"
  },
  
  "processing": {
    "reconciled_at": "2026-04-25T14:30:35Z",
    "stage_processing_time_ms": 4000,
    "status": "success"
  },
  
  "lineage": { ... previous lineage ... }
}
```

---

## Stage 6: Routed Candidate

After routing decision has been made.

```json
{
  "candidate_id": "uuid",
  "stage": "routed",
  
  "capture": { ... previous stages ... },
  "scoring": { ... previous scoring ... },
  "classification": { ... previous classification ... },
  "reconciliation": { ... previous reconciliation ... },
  
  "routing_decision": {
    "action": "ADVANCE_TO_INTEGRATION|ROUTE_WITH_TAG|ESCALATE_FOR_REVIEW|TRIGGER_WORKFLOW|QUEUE_FOR_REVIEW|QUARANTINE",
    "confidence": 0.91,
    "routing_timestamp": "2026-04-25T14:30:40Z",
    
    "decision_logic": {
      "agreement_score": 0.91,
      "semantic_confidence": 0.92,
      "rule_check": "pass",
      "taxonomy_match": true,
      "reconciliation_status": "clear"
    },
    
    "destination": {
      "path": "/10-Projects/PATH-HAIL/Tasks",
      "vault_location": "obsidian-vault",
      "accessibility": "personal"
    },
    
    "tags_to_apply": [
      "task",
      "urgent",
      "PATH-HAIL",
      "action-required"
    ],
    
    "review_required": false,
    "review_reason": null,
    
    "downstream_triggers": [
      {
        "trigger_type": "create-task",
        "target_system": "task-management",
        "parameters": {
          "title": "From note: Send revised PATH/HAIL framing",
          "priority": "high",
          "assignee": "Chad"
        }
      }
    ],
    
    "quarantine_reason": null,
    "escalation_reason": null
  },
  
  "processing": {
    "routed_at": "2026-04-25T14:30:40Z",
    "stage_processing_time_ms": 1000,
    "status": "success"
  },
  
  "lineage": { ... previous lineage ... }
}
```

---

## Stage 7: Integrated Candidate

After writing to Obsidian vault.

```json
{
  "candidate_id": "uuid",
  "stage": "integrated",
  
  "capture": { ... all previous stages ... },
  "routing_decision": { ... routing ... },
  
  "integration": {
    "obsidian_note": {
      "note_id": "obsidian-uuid",
      "file_path": "/10-Projects/PATH-HAIL/Tasks/Send-revised-PATH-HAIL-framing.md",
      "created_timestamp": "2026-04-25T14:30:45Z",
      "content_hash": "sha256-hash",
      
      "frontmatter": {
        "title": "Send revised PATH/HAIL framing",
        "type": "task",
        "project": "PATH-HAIL",
        "status": "new",
        "priority": "high",
        "assignee": "Chad",
        "deadline": "2026-04-30",
        "source_candidate_id": "uuid",
        "source_timestamp": "2026-04-25T14:30:00Z",
        "tags": ["task", "urgent", "deliverable"]
      },
      
      "body": "Full note content",
      "version": 1
    },
    
    "graph_integration": {
      "relationships_created": [
        {
          "from_node": "new-note-uuid",
          "to_node": "existing-note-uuid",
          "relationship_type": "related-to"
        }
      ],
      "contradictions_logged": [
        {
          "contradiction_id": "uuid",
          "status": "flagged-for-review"
        }
      ]
    },
    
    "atomization": {
      "chunks_created": [
        {
          "chunk_id": "uuid",
          "index": 0,
          "original_byte_range": [0, 200],
          "chunk_text": "First paragraph of note"
        }
      ]
    },
    
    "versioning": {
      "version_id": "v1-2026-04-25T14:30:45Z",
      "prior_version": null,
      "changelog": "Initial capture from voice note"
    }
  },
  
  "processing": {
    "integrated_at": "2026-04-25T14:30:45Z",
    "stage_processing_time_ms": 2000,
    "status": "success"
  },
  
  "lineage": { ... previous lineage with integration event ... }
}
```

---

## Stage 8: Triggered Candidate

After downstream workflows have been initiated.

```json
{
  "candidate_id": "uuid",
  "stage": "triggered",
  
  "capture": { ... all previous stages ... },
  "integration": { ... previous integration ... },
  
  "triggers": {
    "workflow_triggers": [
      {
        "trigger_id": "uuid",
        "trigger_type": "create-task|send-notification|schedule-review|route-to-inbox",
        "target_system": "task-management|notification|calendar|inbox",
        "trigger_timestamp": "2026-04-25T14:30:50Z",
        "status": "success|pending|failed",
        "external_id": "task-id-in-external-system",
        "external_url": "https://..."
      },
      {
        "trigger_id": "uuid2",
        "trigger_type": "route-to-inbox",
        "target_system": "obsidian-inbox",
        "trigger_timestamp": "2026-04-25T14:30:50Z",
        "status": "success",
        "detail": "Added review tag and linked from related notes"
      }
    ],
    
    "event_emissions": [
      {
        "event_id": "uuid",
        "event_type": "candidate_integrated",
        "event_timestamp": "2026-04-25T14:30:50Z",
        "subscribers": ["review-queue", "task-system"],
        "payload": {
          "candidate_id": "uuid",
          "note_id": "obsidian-uuid",
          "project": "PATH-HAIL"
        }
      }
    ]
  },
  
  "processing": {
    "triggers_emitted_at": "2026-04-25T14:30:50Z",
    "stage_processing_time_ms": 1500,
    "status": "success"
  },
  
  "lineage": { ... with trigger events ... }
}
```

---

## Stage 9: Audited Candidate

Final stage with complete governance metadata.

```json
{
  "candidate_id": "uuid",
  "stage": "audited",
  
  "capture": { ... all previous stages ... },
  "triggers": { ... previous triggers ... },
  
  "audit": {
    "governance": {
      "data_classification": "public|internal|confidential|secret",
      "classification_timestamp": "2026-04-25T14:30:00Z",
      "classification_reasoning": "User-captured work context"
    },
    
    "decision_trail": [
      {
        "timestamp": "2026-04-25T14:30:00Z",
        "stage": "captured",
        "decision_point": "input-accepted",
        "decision": "accept",
        "rationale": "Valid input from trusted source"
      },
      {
        "timestamp": "2026-04-25T14:30:15Z",
        "stage": "normalized",
        "decision_point": "quality-check",
        "decision": "pass",
        "quality_metrics": { ... },
        "rationale": "High-quality transcription"
      },
      {
        "timestamp": "2026-04-25T14:30:25Z",
        "stage": "scored",
        "decision_point": "scoring-gate",
        "decision": "pass",
        "overall_score": 0.81,
        "rationale": "Score >= 0.75"
      },
      {
        "timestamp": "2026-04-25T14:30:40Z",
        "stage": "routed",
        "decision_point": "routing-decision",
        "decision": "ADVANCE_TO_INTEGRATION",
        "confidence": 0.91,
        "rationale": "High agreement between classifiers, clear project match"
      }
    ],
    
    "compliance": {
      "tbs_automated_decision_logging": true,
      "bias_check_performed": true,
      "bias_flags": [],
      "accessibility_check": "na",
      "retention_policy": "standard-24-months"
    },
    
    "quality_metrics": {
      "end_to_end_processing_time_ms": 20500,
      "stages_completed": 9,
      "stages_with_errors": 0,
      "final_confidence": 0.91
    }
  },
  
  "processing": {
    "audited_at": "2026-04-25T14:30:51Z",
    "stage_processing_time_ms": 500,
    "status": "complete"
  },
  
  "lineage": {
    "events": [
      {
        "timestamp": "2026-04-25T14:30:00Z",
        "event": "captured",
        "detail": "Input received and queued"
      },
      {
        "timestamp": "2026-04-25T14:30:15Z",
        "event": "normalized",
        "detail": "Text transcribed, entities extracted"
      },
      {
        "timestamp": "2026-04-25T14:30:25Z",
        "event": "scored",
        "detail": "Four-dimensional scoring complete"
      },
      {
        "timestamp": "2026-04-25T14:30:30Z",
        "event": "classified",
        "detail": "Domain: strategic-planning, Type: task, Project: PATH-HAIL"
      },
      {
        "timestamp": "2026-04-25T14:30:35Z",
        "event": "reconciled",
        "detail": "Compatible with existing knowledge, no contradictions"
      },
      {
        "timestamp": "2026-04-25T14:30:40Z",
        "event": "routed",
        "detail": "Routed to PATH-HAIL/Tasks with high confidence"
      },
      {
        "timestamp": "2026-04-25T14:30:45Z",
        "event": "integrated",
        "detail": "Written to Obsidian vault, relationships created"
      },
      {
        "timestamp": "2026-04-25T14:30:50Z",
        "event": "triggered",
        "detail": "Task created in external system, review queue notified"
      },
      {
        "timestamp": "2026-04-25T14:30:51Z",
        "event": "audited",
        "detail": "Complete audit trail finalized"
      }
    ]
  }
}
```

---

## Design Principles

### 1. Immutable History
Fields from prior stages are never overwritten, only extended. This preserves the full decision trail.

### 2. Confidence All the Way Down
Every decision (score, classification, routing) includes explicit confidence levels and reasoning.

### 3. Atomic Integrity
A candidate is either at a stage completely or not at all. Partial progress is not stored.

### 4. Explicit Reasoning
Every field includes `reasoning`, `rationale`, or `detail` explaining why that decision was made.

### 5. Auditability First
The schema is designed to answer: "Why did the system do that?" at any point in the pipeline.

### 6. Failure Transparency
Failed candidates include `status: error` and detailed error information, never silently dropped.

---

## Validation Rules

### Required Fields by Stage

**Stage 1 (Captured)**:
- `candidate_id`, `stage`, `capture_timestamp`, `input`, `processing`

**Stage 2 (Normalized)**:
- All Stage 1 + `normalized.raw_text`, `normalized.chunks`, `processing.status: success`

**Stage 3 (Scored)**:
- All prior + `scoring.overall_score.score`, `scoring.overall_score.routing_action`

**Stage 4 (Classified)**:
- All prior + `classification.note_type.inferred`, `classification.project.inferred`

**Stage 5 (Reconciled)**:
- All prior + `reconciliation.reconciliation_status`

**Stage 6 (Routed)**:
- All prior + `routing_decision.action`, `routing_decision.destination` (or quarantine/escalation reason)

**Stage 7 (Integrated)**:
- All prior + `integration.obsidian_note.note_id`, `integration.obsidian_note.file_path`

**Stage 8 (Triggered)**:
- All prior + `triggers.workflow_triggers[]` (may be empty)

**Stage 9 (Audited)**:
- All prior + `audit.decision_trail[]`, `processing.status: complete`

---

## Example Flow: Voice Note

A user captures a voice note: "Need to send Chad the revised PATH/HAIL framing before ARB."

```
Stage 0 (Raw Input)
  ↓ [audio file received]
Stage 1 (Captured)
  candidate_id: 550e8400-e29b-41d4-a716-446655440000
  status: queued
  ↓ [transcription: "Need to send Chad..."]
Stage 2 (Normalized)
  raw_text: "Need to send Chad the revised PATH/HAIL framing before ARB."
  extracted_entities: [Chad, PATH-HAIL]
  extracted_deadline: 2026-04-30
  ↓ [scoring: 0.81]
Stage 3 (Scored)
  overall_score: 0.81
  routing_action: ADVANCE_TO_INTEGRATION
  ↓ [classification: task, PATH-HAIL]
Stage 4 (Classified)
  note_type: task
  project: PATH-HAIL
  ↓ [reconciliation: clear]
Stage 5 (Reconciled)
  reconciliation_status: clear
  relationships_detected: [related-to existing note on PATH-HAIL strategy]
  ↓ [routing: auto-route]
Stage 6 (Routed)
  action: ADVANCE_TO_INTEGRATION
  destination: /10-Projects/PATH-HAIL/Tasks
  ↓ [Obsidian write]
Stage 7 (Integrated)
  obsidian_note.file_path: /10-Projects/PATH-HAIL/Tasks/Send-revised-PATH-HAIL-framing.md
  ↓ [create task trigger]
Stage 8 (Triggered)
  workflow_triggers: [create-task → task-management]
  ↓ [finalize audit]
Stage 9 (Audited)
  processing.status: complete
  end_to_end_processing_time_ms: 20500
```

---

## Integration with n8n

Each n8n node corresponds to a stage and outputs a Knowledge Candidate in the appropriate schema:

1. **Webhook Input** → Stage 1 schema
2. **Transcription** → Stage 2 schema
3. **Scoring Engine** → Stage 3 schema
4. **Classifier LLM** → Stage 4 schema
5. **Reconciliation Query** → Stage 5 schema
6. **Routing Logic** → Stage 6 schema
7. **Obsidian Write** → Stage 7 schema
8. **Trigger Emission** → Stage 8 schema
9. **Audit Logger** → Stage 9 schema

---

## Success Criteria

- [ ] Schema passes JSON validation for all 9 stages
- [ ] Real captures can be serialized through all stages without information loss
- [ ] Decision trail is complete and auditable (can answer "why" at any point)
- [ ] No candidate is in "incomplete" state in persistence
- [ ] All relationships between candidates are traceable
- [ ] Confidence scores can be aggregated and analyzed across pipeline

---

**Status**: Active schema specification (v1.0)

**Last Updated**: 2026-04-25

**Next**: Create pca-capture-scoring-model.md (mathematical formalization of Stage 3 scoring)
