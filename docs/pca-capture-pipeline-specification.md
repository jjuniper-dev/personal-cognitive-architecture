---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, capture, pipeline, ingestion, governance]
status: active
---

# PCA Capture Pipeline Specification

## Overview

The capture pipeline is a **controlled transformation of raw stimuli into decision-ready knowledge**. It is not passive storage; it is an active intake system with governance, scoring, and downstream consequences.

Each stage has explicit control points where information is validated, scored, or escalated. The pipeline prevents cognitive pollution by refusing low-signal input and contradictions until they are reconciled.

**Core Design Principle**: Control what is allowed to influence your thinking.

---

## Stage 1: Capture (Ingestion Layer)

### Objective
Minimize friction, maximize signal intake

### Input Sources (Multi-Modal)

| Source | Method | Metadata |
|--------|--------|----------|
| **Voice** | iPhone shortcut → speech-to-text | timestamp, device, location |
| **Web** | Browser extension / manual paste | URL, domain, context |
| **Video** | YouTube → transcript / summary | video URL, duration, channel |
| **Chat** | Manual paste or API webhook | platform, participants, timestamp |
| **Files** | PDF/Doc upload or email forward | filename, author, date created |
| **Structured** | Forms, API, or direct input | schema validation, source ID |

### Characteristics

- **Event-driven**: Triggered by user action or passive monitoring
- **No structure required**: Raw input accepted as-is
- **Metadata attached immediately**: Every capture gets source + timestamp + context
- **Intentionally lossy but fast**: Don't overthink structure at this stage

### Capture Event Schema

```json
{
  "capture_id": "uuid",
  "timestamp": "ISO-8601",
  "source": {
    "type": "voice|web|video|chat|file|structured",
    "platform": "string (iPhone Shortcuts, browser, etc.)",
    "url": "string or null",
    "metadata": {}
  },
  "raw_content": "string (original input, unprocessed)",
  "content_hash": "sha256",
  "capture_context": {
    "user_note": "Why I captured this",
    "project": "string or null",
    "tags": ["string"]
  },
  "processing_status": "captured",
  "next_stage": "normalization"
}
```

### Control Point 1: Accept or Reject Capture

```
IF raw_content is empty OR content_hash matches recent capture
  → Log as duplicate, do not advance
  
ELSE IF content_length > 50,000 words
  → Flag for chunking (see Normalization)
  → Advance with chunking flag set
  
ELSE
  → Advance to Normalization
```

---

## Stage 2: Normalization (Pre-Processing Layer)

### Objective
Convert raw input into machine-processable units

### Transformations

#### 2.1 Transcription (if applicable)

Input: Audio or video

Output: Clean text transcript

```
Process:
  speech-to-text → text normalization → punctuation recovery
  
Quality check:
  confidence_score < 0.85 → flag for manual review
  
Schema output:
{
  "transcript": "string",
  "confidence": 0.0-1.0,
  "language": "en",
  "manual_review_required": boolean
}
```

#### 2.2 Extraction (HTML → text/markdown)

Input: Web content

Output: Clean text or markdown

```
Process:
  HTML parse → remove boilerplate → extract main content →
  convert to markdown → resolve links
  
Preserve:
  - Headings and structure
  - Links (convert to markdown format)
  - Code blocks (with language tags)
  - Tables (markdown or structured)
  
Remove:
  - Navigation elements
  - Ads, tracking pixels
  - Boilerplate (footer, sidebar)
  - Duplicate content
  
Schema output:
{
  "normalized_content": "markdown string",
  "extraction_confidence": 0.0-1.0,
  "preserved_links": ["url"],
  "structure": {
    "headings": ["h1", "h2", "h3"],
    "has_code_blocks": boolean,
    "has_tables": boolean
  }
}
```

#### 2.3 Chunking (Semantic Segmentation)

Input: Content >5000 words or complex structure

Output: Logical chunks

```
Process:
  Identify semantic boundaries (sections, topics, paragraphs)
  Create chunks of 500-1500 words each
  Preserve context (parent section, page number)
  
Each chunk becomes:
{
  "chunk_id": "uuid",
  "parent_capture_id": "uuid",
  "sequence": 1,
  "content": "string (chunk text)",
  "context": {
    "section_heading": "string",
    "page_number": number,
    "parent_chunk_id": "uuid or null"
  },
  "is_final_chunk": boolean
}

Note: Each chunk is processed independently through subsequent stages
```

#### 2.4 Metadata Enrichment

Attach structured metadata to every normalized item:

```json
{
  "metadata": {
    "source": "string (exact source type)",
    "author": "string or null",
    "domain": "string (inferred: AI, EA, personal, etc.)",
    "date_published": "ISO-8601 or null",
    "date_accessed": "ISO-8601",
    "language": "en|other",
    "content_type": "article|research|conversation|task|idea|reference",
    "length_words": number,
    "has_images": boolean,
    "has_code": boolean,
    "confidence_extraction": 0.0-1.0
  }
}
```

### Output: Knowledge Candidate

A "knowledge candidate" is the standardized format after normalization:

```json
{
  "candidate_id": "uuid",
  "capture_id": "uuid",
  "timestamp": "ISO-8601",
  "source_type": "string",
  "normalized_content": "string (markdown or text)",
  "metadata": { ... },
  "processing_stage": "normalized",
  "next_stage": "scoring_and_validation"
}
```

### Control Point 2: Validate Normalization Quality

```
IF extraction_confidence < 0.70
  → Flag for manual review before scoring
  
ELSE IF normalized_content is empty
  → Discard and log (failed extraction)
  
ELSE
  → Advance to Scoring & Validation
```

---

## Stage 3: Scoring & Validation (Gatekeeping Layer)

### Objective
Prevent cognitive pollution by filtering low-signal input

### Scoring Model

Each candidate is scored across four dimensions:

#### 3.1 Credibility Score (0.0-1.0)

Measures: Trustworthiness of source

**Factors**:
- Source track record (published, academic, known authority)
- Author expertise (verified, relevant field)
- Content claims (supported by evidence, citations)
- Recency (if time-sensitive)

**Calibration**:
- Published research (0.9-1.0)
- Known authority (0.8-0.9)
- Peer/personal knowledge (0.7-0.8)
- Unverified claim (0.4-0.6)
- Suspicious source (0.0-0.3)

```
credibility_score = 
  (source_authority × 0.4) +
  (author_expertise × 0.3) +
  (evidence_quality × 0.2) +
  (recency_factor × 0.1)
```

#### 3.2 Relevance Score (0.0-1.0)

Measures: Alignment with goals, projects, domains

**Factors**:
- Domain match (captures from relevant fields)
- Project alignment (specific to current work)
- Goal alignment (supports known objectives)
- Time sensitivity (timely for current context)

**Calibration**:
- Direct match to active project (0.95-1.0)
- Relevant to domain (0.7-0.9)
- Peripherally relevant (0.4-0.7)
- Weakly related (0.2-0.4)
- Off-topic (0.0-0.2)

```
relevance_score = 
  (domain_match × 0.35) +
  (project_alignment × 0.35) +
  (goal_alignment × 0.2) +
  (time_sensitivity × 0.1)
```

#### 3.3 Novelty Score (0.0-1.0)

Measures: New information vs redundant

**Factors**:
- Semantic novelty (vs existing knowledge)
- Unique perspective (new angle on known topic)
- Depth addition (extends existing knowledge)
- Redundancy penalty (duplicate or similar)

**Calibration**:
- Entirely new domain/concept (0.95-1.0)
- New angle on known topic (0.7-0.9)
- Extends existing knowledge (0.6-0.8)
- Reinforces known (0.3-0.6)
- Likely duplicate (0.0-0.3)

```
novelty_score = 
  (semantic_novelty × 0.4) +
  (unique_perspective × 0.3) +
  (depth_addition × 0.2) +
  (1 - redundancy_penalty × 0.1)
```

#### 3.4 Signal Strength (0.0-1.0)

Measures: Depth and utility of content

**Factors**:
- Content depth (comprehensive vs surface-level)
- Specificity (concrete vs vague)
- Actionability (can be applied)
- Clarity (well-written, understandable)

**Calibration**:
- Deep, specific, actionable (0.9-1.0)
- Solid, useful content (0.7-0.9)
- Adequate but general (0.5-0.7)
- Superficial or unclear (0.3-0.5)
- Noise or junk (0.0-0.3)

```
signal_strength = 
  (content_depth × 0.3) +
  (specificity × 0.3) +
  (actionability × 0.2) +
  (clarity × 0.2)
```

### Overall Scoring Formula

```
overall_score = 
  (credibility × 0.20) +        # Filter junk early
  (relevance × 0.40) +          # Dominate: is this relevant?
  (novelty × 0.30) +            # Dominate: is this new?
  (signal_strength × 0.10)      # Refine: is it useful?

Result: 0.0-1.0
```

**Rationale for weights**: You're capturing primarily relevant information (self-selected), so credibility is a veto (not noisy junk) but relevance and novelty drive deep processing.

### Routing Decision

```json
{
  "score_components": {
    "credibility": 0.0-1.0,
    "relevance": 0.0-1.0,
    "novelty": 0.0-1.0,
    "signal_strength": 0.0-1.0
  },
  "overall_score": 0.0-1.0,
  "routing": "advance|inbox|quarantine",
  "reasoning": "string (why this routing)"
}
```

### Control Point 3: Routing Decision

```
IF overall_score >= 0.75
  AND credibility >= 0.60  # Credibility veto
  AND relevance >= 0.60    # Relevance bar
  → Route to CLASSIFICATION (advance to next stage)

ELSE IF overall_score >= 0.50
  AND relevance >= 0.40
  → Route to INBOX (queue for manual review)
  → Tag with: "review-low-confidence"

ELSE IF credibility < 0.40
  → Route to QUARANTINE
  → Log as "suspicious source"
  → Do not advance further

ELSE
  → Route to INBOX
  → Tag with: "review-low-score"
```

---

## Stage 4: Classification & Tagging

### Objective
Establish semantic identity before integration

Each candidate is tagged across three dimensions:

### 4.1 Domain Classification

```
Domains (examples, not exhaustive):
  - AI/ML
  - Research & Evidence
  - Governance & Ethics
  - EA/Strategy
  - Personal
  - Technical
  - Health & Well-being
  - Other

Output:
{
  "domain": "string",
  "domain_confidence": 0.0-1.0,
  "secondary_domains": ["string"]
}
```

### 4.2 Content Type

```
Types:
  - insight (pattern, realization, understanding)
  - fact (verifiable claim, data point)
  - opinion (perspective, argument, interpretation)
  - task (actionable item, follow-up)
  - reference (resource, citation, source)
  - question (unclear, needs clarification)
  - contradiction (conflicts with known beliefs)

Output:
{
  "content_type": "string",
  "type_confidence": 0.0-1.0
}
```

### 4.3 Intent

```
Intents:
  - learn (build understanding)
  - act (drive decision or action)
  - explore (investigate further)
  - question (clarify or challenge)
  - integrate (add to knowledge graph)
  - monitor (track for future relevance)

Output:
{
  "intent": "string",
  "intent_confidence": 0.0-1.0
}
```

### Classification Schema

```json
{
  "candidate_id": "uuid",
  "classification": {
    "domain": "string",
    "domain_confidence": 0.0-1.0,
    "content_type": "string",
    "type_confidence": 0.0-1.0,
    "intent": "string",
    "intent_confidence": 0.0-1.0,
    "tags": ["string"],
    "estimated_value": "low|medium|high"
  },
  "processing_stage": "classified",
  "next_stage": "cognitive_reconciliation"
}
```

### Control Point 4: Classification Quality

```
IF (domain_confidence + type_confidence + intent_confidence) / 3 < 0.60
  → Flag for manual classification
  
ELSE
  → Advance to Cognitive Reconciliation
```

---

## Stage 5: Cognitive Reconciliation (Core Intelligence Layer)

### Objective
Compare against existing knowledge; detect relationships and contradictions

This is where the candidate becomes cognitive input.

### Reconciliation Evaluation

Each classified candidate is evaluated against the knowledge graph:

**Relationship Types**:
- **Reinforces**: Confirms existing knowledge (increases confidence)
- **Challenges**: Contradicts existing knowledge (requires attention)
- **Expands**: Adds depth or related context
- **Novel**: Introduces new domain or concept (no existing knowledge)
- **Null**: No meaningful relationship

### Reconciliation Schema

```json
{
  "candidate_id": "uuid",
  "reconciliation": {
    "relationships": [
      {
        "related_node_id": "uuid",
        "relationship_type": "reinforces|challenges|expands|novel|null",
        "confidence": 0.0-1.0,
        "evidence": "string"
      }
    ],
    "contradictions": [
      {
        "conflicting_nodes": ["uuid", "uuid"],
        "severity": "low|medium|high",
        "implication": "string",
        "requires_review": boolean
      }
    ],
    "confidence_adjustment": -0.3 to +0.3,
    "recommended_action": "integrate|review|escalate|hold"
  }
}
```

### Control Point 5: Reconciliation Outcome

```
IF contradictions with high severity
  → Route to ROUTING (escalate for human review)

ELSE IF contradictions with medium severity
  AND recommended_action == "review"
  → Route to ROUTING (tag for review, but can advance)

ELSE
  → Advance to ROUTING with reconciliation complete
```

---

## Stage 6: Routing Decision (Control Layer)

### Objective
Decide what happens next based on all prior scoring and analysis

### Routing Policy

```
Input: [overall_score, classification, reconciliation, domain]

IF high_severity_contradiction
  → Action: ESCALATE_FOR_REVIEW
  → Destination: Human Review Queue
  → Tags: ["contradiction", "requires-decision"]

ELSE IF overall_score >= 0.75
  AND no_contradictions
  AND relationship_type IN ["reinforces", "expands"]
  → Action: ADVANCE_TO_INTEGRATION
  → Destination: Knowledge Graph (mapped to existing node)
  → Tags: ["auto-routed", "linked"]

ELSE IF content_type == "task"
  AND intent == "act"
  → Action: TRIGGER_WORKFLOW
  → Destination: Task queue / n8n trigger
  → Tags: ["task", "action-required"]

ELSE IF recommended_action == "review"
  → Action: ROUTE_WITH_TAG
  → Destination: Inbox + review tag
  → Tags: ["needs-review", domain]

ELSE IF overall_score >= 0.50
  → Action: QUEUE_FOR_REVIEW
  → Destination: Inbox (manual review)
  → Tags: ["low-confidence", domain]

ELSE
  → Action: QUARANTINE
  → Destination: Quarantine folder
  → Tags: ["low-score", "manual-review-optional"]
```

### Routing Schema

```json
{
  "candidate_id": "uuid",
  "routing_decision": {
    "action": "ADVANCE_TO_INTEGRATION|ROUTE_WITH_TAG|ESCALATE_FOR_REVIEW|TRIGGER_WORKFLOW|QUEUE_FOR_REVIEW|QUARANTINE",
    "destination": "knowledge-graph|inbox|review-queue|workflow-trigger|quarantine",
    "tags": ["string"],
    "priority": "low|medium|high",
    "assigned_to": "human|system|workflow",
    "review_required": boolean,
    "reasoning": "string"
  }
}
```

---

## Stage 7: Structured Insertion (Knowledge Integration)

### Objective
Persist decision-ready knowledge into long-term memory

### Target: Obsidian Knowledge Graph

Each candidate that reaches integration is:

1. **Atomized** — One core idea per node (avoid mega-notes)
2. **Linked** — Bi-directional relationships to related nodes
3. **Versioned** — Source and timestamp retained
4. **Searchable** — Tags, domain, metadata indexed

### Integration Schema

```json
{
  "obsidian_note": {
    "file_path": "/DOMAIN/YYYY-MM/note-title.md",
    "frontmatter": {
      "title": "string",
      "created": "ISO-8601",
      "updated": "ISO-8601",
      "domain": "string",
      "type": "concept|insight|reference|decision",
      "source": "string (original capture source)",
      "source_url": "string or null",
      "tags": ["string"],
      "confidence": 0.0-1.0,
      "relationships": ["[[related-note]]"]
    },
    "body": "markdown content (normalized, integrated)",
    "audit_trail": {
      "capture_id": "uuid",
      "candidate_id": "uuid",
      "routing_decision_timestamp": "ISO-8601",
      "integration_timestamp": "ISO-8601"
    }
  }
}
```

### Control Point 7: Integration Validation

```
Before writing to Obsidian:

IF file_path already exists
  → Merge with existing note (don't duplicate)
  → Update relationships
  
ELSE IF relationships cannot be resolved
  → Hold in queue for manual resolution
  
ELSE
  → Write to vault
  → Create backlinks
  → Log in audit trail
```

---

## Stage 8: Trigger Emission (Event Layer)

### Objective
Activate downstream processes when knowledge is integrated

### Trigger Types

```json
{
  "triggers": [
    {
      "type": "create_task",
      "condition": "content_type == 'task'",
      "payload": {
        "task_title": "string",
        "due_date": "ISO-8601 or null",
        "project": "string",
        "priority": "low|medium|high"
      }
    },
    {
      "type": "start_research_thread",
      "condition": "intent == 'explore'",
      "payload": {
        "topic": "string",
        "related_notes": ["[[note]]"]
      }
    },
    {
      "type": "trigger_agent_workflow",
      "condition": "domain == 'AI' AND signal_strength >= 0.8",
      "payload": {
        "workflow": "n8n_workflow_id",
        "input": "candidate_data"
      }
    },
    {
      "type": "schedule_review",
      "condition": "contradiction detected",
      "payload": {
        "review_date": "ISO-8601",
        "context": "contradiction details"
      }
    }
  ]
}
```

### Control Point 8: Trigger Execution

```
After knowledge graph integration:

FOR EACH trigger
  IF condition is met
    → Execute trigger
    → Log execution
    
  ELSE
    → Skip and log
```

---

## Stage 9: Audit & Governance Overlay (Cross-Cutting)

### Objective
Maintain trust, traceability, and reversibility across all stages

### What is Logged

At **every stage**, log:

```json
{
  "audit_entry": {
    "timestamp": "ISO-8601",
    "stage": "capture|normalize|score|classify|reconcile|route|integrate|trigger",
    "candidate_id": "uuid",
    "actor": "system|human|workflow",
    "action": "string",
    "input": "summary of input",
    "output": "summary of output",
    "decision": "accept|reject|escalate|modify",
    "reasoning": "why this decision",
    "tags": ["string"]
  }
}
```

### Audit Trail Supports

- **Explainability**: Trace why a note was routed to Inbox vs integrated
- **Bias detection**: Identify patterns in scoring, rejection, escalation
- **Reversibility**: Can undo/modify decisions with full context
- **Compliance**: Evidence of governance and human oversight
- **Learning**: Analyze disagreement patterns, improve prompts

### Control Point 9: Audit Completeness

```
IF any stage lacks audit entry
  → Flag as incomplete
  → Do not allow further processing
  
ELSE
  → Stage can complete
  → Continue pipeline
```

---

## Complete Pipeline Flow (Compressed)

```
[1. Capture]
   raw input from multi-modal sources
   ↓
[2. Normalize]
   transcribe, extract, chunk, enrich metadata
   ↓
[3. Score & Validate]
   credibility/relevance/novelty/signal
   overall_score >= 0.75 → advance
   ↓
[4. Classify]
   domain, type, intent, tags
   ↓
[5. Reconcile]
   compare against knowledge graph
   detect relationships, contradictions
   ↓
[6. Route]
   integrate | review | escalate | trigger
   ↓
[7. Insert]
   write to Obsidian (atomized, linked, versioned)
   ↓
[8. Trigger]
   emit downstream events (tasks, workflows, reviews)
   ↓
[9. Audit (Cross-Cutting)]
   log every decision, reasoning, outcome
```

---

## Implementation Checklist

### Data Structures
- [ ] Define Capture Event schema
- [ ] Define Knowledge Candidate schema
- [ ] Define Routing Decision schema
- [ ] Define Obsidian Note schema with frontmatter
- [ ] Define Audit Entry schema

### Scoring & Validation
- [ ] Implement credibility scoring (source database)
- [ ] Implement relevance scoring (project/domain mapping)
- [ ] Implement novelty scoring (semantic duplicate detection)
- [ ] Implement signal strength scoring (content analysis)
- [ ] Calibrate thresholds (test with 50 real captures)

### Processing Pipeline
- [ ] Build transcription handler (audio → text)
- [ ] Build extraction handler (HTML → markdown)
- [ ] Build chunking handler (semantic segmentation)
- [ ] Build metadata enrichment (automatic tagging)
- [ ] Build classifier (LLM + rules for domain/type/intent)

### Reconciliation
- [ ] Wire reconciliation to knowledge graph (see CRE spec)
- [ ] Implement relationship detection
- [ ] Implement contradiction flagging
- [ ] Implement confidence adjustment

### Integration
- [ ] Build Obsidian writer (create notes with proper structure)
- [ ] Build relationship mapper (create backlinks)
- [ ] Build version control (track source + timestamp)
- [ ] Test atomic note creation (one idea per note)

### Triggers & Workflows
- [ ] Define trigger types (task, research, workflow, review)
- [ ] Build trigger executor (emit to n8n or task queue)
- [ ] Wire to downstream systems

### Governance & Audit
- [ ] Build audit logger (all stages)
- [ ] Build audit dashboard (visibility into routing decisions)
- [ ] Build review queue (for escalated items)
- [ ] Build feedback loop (human decisions → model improvement)

---

## Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Capture flow-through** | >90% complete capture → Obsidian | End-to-end coverage |
| **Auto-integration rate** | 60-70% | Most captures routed without review |
| **Review queue** | 20-30% | Meaningful escalation |
| **Quarantine rate** | <5% | Junk filtered early |
| **Integration accuracy** | >95% | Routed notes are in correct location |
| **Reconciliation quality** | >90% | Relationships correctly detected |
| **Audit trail completeness** | 100% | Every decision traceable |

---

## Non-Negotiable Principles

1. **Scoring is explicit and tunable.** Every weight can be adjusted based on feedback.
2. **Multiple control points prevent silent failure.** Each stage has a decision gate.
3. **Audit trail is complete.** Every decision is logged with reasoning.
4. **Reversibility is preserved.** Original source and timestamp retained.
5. **Human review is reserved for ambiguity.** Not every decision requires human eyes.
6. **Integration is atomic.** One idea per note, not mega-documents.
7. **Triggers are intentional.** No automatic actions without explicit payload.

---

**Status**: Implementation-ready specification (v1.0)

**Next Steps**:
1. Define scoring model mathematically (with calibration data)
2. Create n8n workflow design (iPhone → Obsidian pipeline)
3. Test with 50 real captures (calibrate thresholds)
4. Deploy and monitor (adjust weights based on routing decisions)
