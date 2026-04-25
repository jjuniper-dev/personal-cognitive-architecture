---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, ingestion, patterns, architecture, use-cases]
status: active
---

# PCA Ingestion Patterns

## Definition

An **Ingestion Pattern** is a repeatable workflow for capturing information from a specific source type, processing it according to its signal characteristics, and routing it to appropriate storage and action layers.

PCA uses three primary patterns, each optimized for a different signal type and confidence profile.

---

## Pattern 1: Structured Knowledge Capture

### Purpose
Build trusted, queryable knowledge base (RAG-ready); forms long-term memory backbone.

### Signal Characteristics
- **Type**: Articles, PDFs, research, documentation, reports
- **Signal Quality**: High
- **Noise Level**: Low
- **Confidence Profile**: Medium → High (after validation)
- **Processing Depth**: Deep
- **Governance Tier**: Strong

### Workflow

```
Source (Web / PDF / Report)
        ↓
Capture Layer
├─ Browser clipper (web articles)
├─ iPhone Shortcut (PDFs from email)
└─ Email integration (incoming documents)
        ↓
Pre-Processing
├─ Text extraction (OCR if needed)
├─ Metadata tagging (source, author, date, topic)
├─ Quality check (readability, language detection)
└─ Deduplication (already in vault?)
        ↓
Semantic Processing
├─ Chunking (propositions, not pages)
├─ Entity extraction (concepts, people, definitions)
└─ Embeddings generation (for vector DB)
        ↓
Validation Layer (CRITICAL)
├─ Confidence scoring (0.0-1.0)
├─ Source credibility check (publication, author, peer-review status)
├─ Content coherence assessment
├─ Contradiction detection (vs. existing knowledge)
└─ Governance classification (Unclassified / Protected B analogue)
        ↓
Storage
├─ Vector DB (embeddings for RAG)
├─ Knowledge Graph (concepts, relationships)
├─ Obsidian vault (human-readable version)
└─ State: Inbox → Provisional → Trusted
        ↓
Retrieval Ready
├─ RAG pipelines (semantic search)
├─ Graph traversal (relationship navigation)
├─ Citation generation (traceable to source)
└─ Summarization (executive summary generation)
```

### Implementation Layers

**Capture Layer**:
```json
{
  "source_type": "web|pdf|email|document",
  "source_url": "https://...",
  "source_metadata": {
    "title": "Article Title",
    "author": "Author Name",
    "publication_date": "2026-04-25",
    "domain": "example.com",
    "word_count": 3500
  },
  "captured_timestamp": "2026-04-25T14:30:00Z",
  "capture_method": "browser-clipper|shortcut|email|manual-upload"
}
```

**Pre-Processing Output**:
```json
{
  "extracted_text": "Full article text...",
  "metadata": {
    "title": "Article Title",
    "author": "Author Name",
    "publication_date": "2026-04-25",
    "topic_tags": ["strategic-planning", "ai-governance"],
    "language": "en",
    "estimated_read_time_minutes": 12
  },
  "quality_metrics": {
    "text_extraction_confidence": 0.98,
    "language_detection_confidence": 0.99,
    "is_duplicate": false
  }
}
```

**Semantic Processing Output**:
```json
{
  "chunks": [
    {
      "chunk_id": "uuid",
      "text": "Chunk text (one proposition or key idea)",
      "chunk_index": 0,
      "embedding": [0.123, 0.456, ...],
      "key_concepts": ["governance", "ai-risk"],
      "entities": [
        {
          "type": "organization",
          "value": "Health Canada"
        }
      ]
    }
  ],
  "summary": "1-2 sentence summary of document",
  "key_points": ["point 1", "point 2", "point 3"]
}
```

**Validation Output**:
```json
{
  "confidence_score": 0.88,
  "source_credibility": {
    "publication_tier": "peer-reviewed|reputable|unverified",
    "author_expertise": 0.85,
    "domain_authority": 0.92,
    "credibility_score": 0.89
  },
  "content_validation": {
    "coherence": 0.94,
    "factual_clarity": 0.91,
    "contradictions_detected": 0,
    "requires_expert_review": false
  },
  "governance": {
    "classification": "unclassified",
    "handling_instructions": "Standard ingestion, full RAG access",
    "retention_policy": "24-months"
  },
  "routing_decision": "ADVANCE_TO_TRUSTED_KNOWLEDGE"
}
```

### Success Criteria

| Metric | Target | Why |
|--------|--------|-----|
| Chunk quality (coherence) | >0.90 | Enables accurate retrieval |
| Source credibility validation | 100% | Enterprise governance |
| RAG retrieval accuracy | >0.85 | Useful for synthesis tasks |
| Duplicate detection | >0.98 | Prevents redundancy |
| Processing time per document | <5 min | Practical for daily workflow |

---

## Pattern 2: Unstructured Idea / Thought Capture

### Purpose
Capture cognition in real-time (thinking exhaust); forms dynamic memory layer.

### Signal Characteristics
- **Type**: Voice notes, quick thoughts, insights, questions, observations
- **Signal Quality**: Low → Medium (raw, unrefined)
- **Noise Level**: Medium (not all thoughts are actionable)
- **Confidence Profile**: Low (initial) → Medium/High (after classification)
- **Processing Depth**: Deferred (light at capture, deep later)
- **Governance Tier**: Light (no sensitive data by design)

### Workflow

```
Source (Voice / Text / Thought)
        ↓
Capture Layer
├─ iPhone Shortcut (voice recording)
├─ Quick text input (30 seconds max)
└─ Context annotation (optional location, mood, project)
        ↓
Light Structuring (MINIMAL FRICTION)
├─ Auto-transcription (voice → text)
├─ Auto-tagging (topic, intent, urgency)
│  └─ Use simple heuristics, not ML (fast)
└─ Minimal formatting (don't slow capture)
        ↓
Classification Layer (DDV-Ready)
├─ Is this:
│  ├─ Idea (novel thought, insight, question)
│  ├─ Task (action item, deadline-driven)
│  ├─ Decision (choice point, consequence)
│  ├─ Reference (quote, fact, bookmark)
│  └─ Question (open question, research need)
├─ Confidence: Low (0.4-0.7 typical)
└─ Flag for DDV validation if ambiguous
        ↓
Storage
├─ Obsidian vault (primary)
├─ State: Inbox (default, low confidence)
└─ Metadata: timestamp, intent classification, DDV flag
        ↓
Deferred Processing (Optional, User-Driven)
├─ Promote to knowledge pipeline (if valuable)
├─ Link to existing graph nodes (if relationships exist)
├─ Archive if not relevant (periodic cleanup)
└─ Reconcile with high-confidence knowledge
```

### Implementation Layers

**Capture Layer**:
```json
{
  "source_type": "voice|text|thought",
  "capture_timestamp": "2026-04-25T14:30:00Z",
  "device": "iPhone 15 Pro",
  "location": "office|home|car|other",
  "raw_input": "voice note transcript or text",
  "duration_seconds": 45,
  "user_context": "optional: what triggered this thought"
}
```

**Light Structuring Output**:
```json
{
  "transcribed_text": "Cleaned transcription",
  "auto_tags": {
    "topic": "PATH-HAIL",
    "intent": "action|question|insight|reference",
    "urgency": "low|medium|high",
    "confidence": 0.65
  },
  "metadata": {
    "estimated_importance": 0.58,
    "contains_deadlines": true,
    "contains_people": ["Chad"],
    "contains_projects": ["PATH-HAIL"]
  }
}
```

**Classification Output**:
```json
{
  "classification": {
    "primary_type": "task|idea|decision|reference|question",
    "confidence": 0.62,
    "rationale": "Contains action verb + person name + timeline",
    "ddv_ready": true,
    "requires_expert_input": false
  },
  "suggested_actions": [
    "Route to PATH-HAIL/Tasks",
    "Link to related note on governance"
  ]
}
```

**Storage State**:
```json
{
  "note_id": "uuid",
  "vault_location": "/00-Inbox",
  "state": "inbox",
  "confidence": 0.62,
  "classification": "task",
  "tags": ["task", "PATH-HAIL", "action-required"],
  "created": "2026-04-25T14:30:00Z",
  "status": "awaiting-user-decision"
}
```

### Key Design Decisions

1. **Speed > Structure at Ingest**
   - Voice capture is friction-minimized
   - No complex classification at capture time
   - Auto-tagging is simple heuristics, not ML

2. **Validation is Deferred**
   - Light confidence scores (0.4-0.7 typical)
   - DDV validation happens later (user-driven or batch)
   - Allows "thinking without judgment"

3. **Explicit Separation**
   - Capture (immediate)
   - Validation (deferred)
   - Structuring (optional, user-driven)
   - This is where most PKM systems fail

### Success Criteria

| Metric | Target | Why |
|--------|--------|-----|
| Capture friction | <30s per note | Speed is the point |
| Transcription accuracy | >0.90 | Enables later processing |
| User promotion rate | 20-40% | Healthy signal:noise |
| False positives (noise) | <15% | Some friction acceptable |
| Processing latency | Immediate | Real-time capture |

---

## Pattern 3: Dynamic Signal Ingestion

### Purpose
Maintain situational awareness; feed decision-making layer with filtered external intelligence.

### Signal Characteristics
- **Type**: RSS feeds, APIs, web scraping, news, monitoring
- **Signal Quality**: Variable (low → medium)
- **Noise Level**: High (volume dominates)
- **Confidence Profile**: Low (pre-filtered, automated)
- **Processing Depth**: Shallow (filtering + scoring)
- **Governance Tier**: Automated (rules-driven)

### Workflow

```
Source (RSS / APIs / Web Scraping)
        ↓
Ingestion Agent (Scheduled)
├─ Scheduled pull (hourly / daily / weekly)
├─ API polling (news APIs, RSS feeds)
└─ Web scraping (if no structured feed available)
        ↓
Normalization
├─ Deduplication (exact + semantic)
├─ Format standardization (title, URL, date, source)
├─ Timestamp normalization (capture time vs. publication time)
└─ Language detection + filtering
        ↓
Signal Scoring (Automated)
├─ Relevance (0.0-1.0)
│  └─ keyword matching, domain alignment, project relevance
├─ Urgency (0.0-1.0)
│  └─ freshness, temporal markers (breaking, urgent, deadline)
└─ Impact (0.0-1.0)
   └─ reach, authority, potential consequence
        ↓
Classification
├─ Route bins:
│  ├─ INFO (score < 0.40): Archive/discard
│  ├─ IMPORTANT (0.40-0.70): Knowledge base
│  └─ CRITICAL (>0.70): Alert + escalation
└─ Topic tagging (projects, domains, keywords)
        ↓
Routing
├─ Low → Archive (or discard)
├─ Medium → Knowledge base (Obsidian, Vector DB)
├─ High → Alert (Push notification, Slack, email)
└─ Optional: Human review queue (for CRITICAL edge cases)
        ↓
Optional Enrichment (if routed to KB)
├─ Summarization (1-sentence summary)
├─ Entity extraction (people, organizations, events)
├─ Graph linking (relationships to existing knowledge)
└─ Source credibility annotation
```

### Implementation Layers

**Ingestion Agent Configuration**:
```json
{
  "feed_sources": [
    {
      "type": "rss|api|webhook",
      "url": "https://...",
      "name": "Source Name",
      "poll_interval_minutes": 60,
      "parser": "rss|json|html",
      "enabled": true
    }
  ],
  "deduplication": {
    "exact_match": true,
    "semantic_dedup": true,
    "dedup_window_days": 7
  }
}
```

**Normalization Output**:
```json
{
  "item_id": "uuid",
  "source": "RSS feed name",
  "title": "Article Title",
  "url": "https://...",
  "summary": "Brief description",
  "publication_timestamp": "2026-04-25T10:00:00Z",
  "ingestion_timestamp": "2026-04-25T14:30:00Z",
  "is_duplicate": false,
  "language": "en"
}
```

**Signal Scoring Output**:
```json
{
  "relevance_score": 0.75,
  "relevance_factors": [
    {
      "factor": "mentions_PATH-HAIL",
      "contribution": +0.30
    },
    {
      "factor": "mentions_governance",
      "contribution": +0.25
    }
  ],
  "urgency_score": 0.45,
  "urgency_factors": [
    {
      "factor": "published_today",
      "contribution": +0.30
    },
    {
      "factor": "no_explicit_deadline",
      "contribution": -0.15
    }
  ],
  "impact_score": 0.62,
  "combined_signal_score": 0.61
}
```

**Routing Decision**:
```json
{
  "signal_score": 0.61,
  "classification": "IMPORTANT",
  "routing_action": "ROUTE_TO_KNOWLEDGE_BASE",
  "escalation_required": false,
  "destination": "/10-Projects/PATH-HAIL/External-Intelligence",
  "tags": ["intelligence", "PATH-HAIL", "governance"],
  "alert_sent": false
}
```

### Thresholds and Policies

```
Signal Score → Action

< 0.30: DISCARD
  └─ Clear spam or off-topic

0.30-0.50: ARCHIVE
  └─ Low relevance, possible future value
  └─ Keep in vector DB for semantic search

0.50-0.70: ROUTE_TO_KNOWLEDGE_BASE
  └─ Moderate relevance
  └─ Add to Obsidian with tags
  └─ Include in vector DB

0.70-0.85: ROUTE_WITH_PRIORITY
  └─ High relevance
  └─ Add to Obsidian + flag for review
  └─ Include summary in daily brief

> 0.85: CRITICAL_ALERT
  └─ Very high relevance + urgency
  └─ Push notification
  └─ Escalate to human review
  └─ Include in decision-critical summary
```

### Feedback Loop (Critical)

```
User marks item as:
├─ Relevant (reinforce signal model)
├─ Not relevant (adjust weights)
├─ Acted on (track as business outcome)
└─ Duplicated (improve dedup logic)

Monthly calibration:
├─ Measure false positives (classified as CRITICAL, marked irrelevant)
├─ Measure false negatives (classified as ARCHIVE, turned out important)
├─ Adjust scoring weights if needed
└─ Report on signal quality metrics
```

### Success Criteria

| Metric | Target | Why |
|--------|--------|-----|
| Processing latency | <30s per 100 items | Near real-time |
| Deduplication accuracy | >0.98 | No noise from duplicates |
| CRITICAL precision | >0.90 | Alerts are actionable |
| CRITICAL recall | >0.85 | Don't miss important signals |
| User feedback loop | 100% of CRITICAL | Enable learning |
| False positive rate | <0.10 | Too much false alert = alert fatigue |

---

## Unified Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    INGESTION SOURCES                         │
│  Articles | Thoughts | Feeds | Documents | Voice | APIs     │
└──────────────┬──────────────┬──────────────┬─────────────────┘
               │              │              │
    ┌──────────▼──┐  ┌───────▼────┐  ┌─────▼──────┐
    │ Structured  │  │ Unstructured│  │  Dynamic   │
    │  Knowledge  │  │    Ideas    │  │  Signals   │
    │             │  │             │  │            │
    │ (Deep)      │  │ (Deferred)  │  │ (Filtered) │
    └──────────────┘  └─────────────┘  └────────────┘
               │              │              │
               └──────────────┴──────────────┘
                              ↓
                ┌─────────────────────────────┐
                │   PROCESSING LAYER          │
                │ Chunk | Classify | Score    │
                └──────────┬────────────────┘
                           ↓
                ┌─────────────────────────────┐
                │ VALIDATION / GOVERNANCE     │
                │ Confidence | DDV | Rules    │
                └──────────────┬──────────────┘
                               ↓
                ┌─────────────────────────────┐
                │    STORAGE LAYER            │
                │ Graph | Vector | Obsidian   │
                └──────────────┬──────────────┘
                               ↓
        ┌──────────────┬──────────┴────────┬──────────────┐
        ↓              ↓                    ↓              ↓
    Trusted        Provisional        Inbox         Archive
    Knowledge      Knowledge          (Low conf)    (Signals)
    (RAG-ready)    (Pending review)
        │              │                    │              │
        ↓              ↓                    ↓              ↓
    ┌─────────────────────────────────────────────────────┐
    │ RETRIEVAL / ACTION LAYER                            │
    │ RAG | Graph Traversal | Alerts | Decisions | Reports │
    └─────────────────────────────────────────────────────┘
```

---

## Pattern Selection Matrix

| Characteristic | Structured Knowledge | Unstructured Ideas | Dynamic Signals |
|---|---|---|---|
| **Source Diversity** | Low (articles, PDFs) | Low (voice, text) | High (feeds, APIs) |
| **Signal Quality** | High | Low | Variable |
| **Processing Depth** | Deep | Deferred | Shallow |
| **Confidence at Ingest** | Medium | Low | Low |
| **Time to Trustworthy** | Minutes | Hours/Days | Seconds |
| **Governance** | Strong | Light | Automated |
| **User Friction** | Medium (structured capture) | Low (speed) | None (automated) |
| **Primary Use** | Long-term memory | Thinking capture | Situational awareness |
| **Feedback Loop** | Expert review | User curation | Implicit (signal model) |

---

## Implementation Checklist

### Phase 1a (Week 1-2)
- [ ] Implement Pattern 2 (Ideas) - simplest, highest impact
- [ ] Set up voice capture pipeline (iPhone → n8n → Obsidian)
- [ ] Deploy DDV validation for idea classification
- [ ] Test with 50 real captures

### Phase 1b (Week 3)
- [ ] Implement Pattern 1 (Structured Knowledge)
- [ ] Set up browser clipper integration
- [ ] Deploy validation layer (credibility scoring)
- [ ] Test with 20 articles

### Phase 1c (Week 4)
- [ ] Implement Pattern 3 (Dynamic Signals)
- [ ] Set up RSS feed ingestion
- [ ] Deploy signal scoring and routing
- [ ] Configure alert thresholds

### Phase 2
- [ ] Add semantic deduplication (embeddings)
- [ ] Implement feedback loops for all patterns
- [ ] Build calibration dashboards
- [ ] Enable cross-pattern enrichment (link signals to ideas to knowledge)

---

## Non-Negotiable Principles

1. **Capture must be friction-minimized** — speed > structure at ingest
2. **Validation is explicit** — confidence scores are mandatory, not implicit
3. **Storage preserves signal type** — don't force ideas into knowledge formats
4. **Governance scales with confidence** — low-confidence content has light governance
5. **Feedback loops are built-in** — patterns improve based on user validation

---

**Status**: Active specification (v1.0)

**Last Updated**: 2026-04-25

**Next**: Create control plane specification (governance overlay, routing rules, compute controls)

**Related**: 
- pca-capture-pipeline-specification.md (operational flow)
- pca-control-plane-specification.md (governance and routing)
- pca-feedback-learning-loop.md (validation and learning)
