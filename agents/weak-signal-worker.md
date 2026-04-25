---
type: agent-specification
role: worker
created: 2026-04-25
status: active
---

# Weak Signal Worker Specification

## Identity

**Name**: Weak Signal Worker  
**Role**: RSS signal detection and ingestion  
**Responsibilities**: Poll WeakSignalFinder, normalize signal data, extract emerging themes, feed to Capture pipeline  
**Authority**: Low (executes signal polling and normalization only)  
**Scope**: Stage 1-2 of pipeline (Signal Acquisition → Capture)  

## Purpose

The Weak Signal Worker bridges **WeakSignalFinder** (RSS trend detection) and the **PCA Capture pipeline**. It:

1. **Polls** WeakSignalFinder output on schedule
2. **Extracts** trending topics and semantic clusters
3. **Normalizes** signal data into capture schema
4. **Enriches** with novelty and urgency indicators
5. **Validates** signal quality before passing to Capture Worker
6. **Deduplicates** against recent signals to avoid repeats

The worker **does not make decisions**. It prepares signal data and routes to the Validation Worker via the Capture pipeline.

## Input Contract

**Source**: WeakSignalFinder JSON output file

```json
{
  "timestamp": "2026-04-25T10:30:00Z",
  "topWords": [
    {
      "word": "quantum",
      "frequency": 42,
      "score": 0.95,
      "novelty": 0.82
    }
  ],
  "semanticNeighborhoods": [
    {
      "hub": "quantum",
      "neighbors": ["computing", "cryptography"],
      "strength": 0.78
    }
  ],
  "sources": {
    "count": 247,
    "languages": ["en", "fr"]
  }
}
```

## Output Contract

**Produces**: Normalized signal capture ready for Capture → Validation pipeline

```json
{
  "capture_id": "uuid",
  "source_type": "rss-signal",
  "source_system": "weak-signal-finder",
  "content_type": "signal-trends",
  "timestamp": "2026-04-25T10:30:00Z",
  "normalized_text": "[Formatted summary of emerging trends]",
  "metadata": {
    "signal_type": "trend-emergence",
    "trending_topics": [
      {
        "topic": "quantum computing",
        "frequency": 42,
        "novelty_score": 0.82,
        "confidence": 0.95
      }
    ],
    "semantic_clusters": [
      {
        "hub": "quantum",
        "cluster_size": 5,
        "cluster_strength": 0.78
      }
    ],
    "coverage": {
      "article_count": 247,
      "languages": ["en", "fr"],
      "regions": ["global"],
      "feed_count": 12
    },
    "signal_indicators": {
      "trend_novelty": 0.82,
      "trend_urgency": 0.65,
      "semantic_density": 0.78
    }
  },
  "quality_metrics": {
    "data_completeness": 0.98,
    "language_detection": 0.99,
    "trend_confidence": 0.89,
    "deduplication_check": "passed"
  }
}
```

## Responsibilities

### 1. Signal Polling
- Monitor `external/weak-signal-finder/dataset/` for new output files
- Detect new files by timestamp (avoid reprocessing)
- Handle missing/late signals gracefully
- Retry failed polls with exponential backoff

### 2. Data Extraction
- Parse WeakSignalFinder JSON
- Extract top N trending words (configurable, default: top 20)
- Extract semantic neighborhoods
- Identify emerging clusters (new word combinations)
- Calculate signal strength metrics

### 3. Novelty Detection
- Compare trending topics against recent signals (last 30 days)
- Identify **truly new** trends vs. ongoing coverage
- Calculate novelty score based on:
  - First appearance in feeds
  - Rate of frequency increase
  - Cross-feed consensus
- Mark for escalation if novelty > 0.80

### 4. Data Normalization
- Format trending topics as structured list
- Build human-readable summary text
- Preserve semantic neighborhoods as graph data
- Map article counts to confidence intervals
- Record processing timestamp and data lineage

### 5. Quality Validation
- Check output completeness > 0.90
- Verify language detection accuracy
- Validate trend frequency counts (non-zero)
- Ensure timestamp is recent (< 2 hours old)
- Confirm semantic data integrity

### 6. Deduplication
- Maintain rolling window of recent signals (30 days)
- Compare current trends against historical trends
- Calculate similarity score between signal sets
- Skip processing if similarity > 0.85 (already processed)
- Log deduplicated signals for audit trail

## Processing Pipeline

```
Input: WeakSignalFinder JSON
  ↓
[File Detection]
  ├─ Is file new? (not seen before)
  └─ Is file recent? (< 2 hours old)
  ↓
[Parse JSON]
  ├─ Extract top words
  ├─ Extract semantic neighborhoods
  └─ Extract metadata (coverage, languages)
  ↓
[Novelty Detection]
  ├─ Compare against recent signals
  ├─ Calculate novelty scores
  └─ Flag emerging patterns
  ↓
[Quality Check]
  ├─ Completeness > 0.90?
  ├─ Timestamp valid?
  ├─ Frequency counts reasonable?
  └─ Semantic data present?
  ↓
[Deduplication]
  ├─ Compare against last 30 days
  ├─ Calculate similarity score
  └─ Skip if similarity > 0.85
  ↓
[Normalize & Enrich]
  ├─ Format as capture schema
  ├─ Add novelty/urgency indicators
  └─ Build human-readable summary
  ↓
Output: Capture-ready signal document
```

## Error Handling

### File Not Found
```
→ Check directory permissions
→ Verify WeakSignalFinder output path
→ Log warning, retry in 5 minutes
```

### Invalid JSON
```
→ Log error with file path
→ Flag for manual review
→ Continue with next file
```

### Quality Check Fails
```
→ Log quality metrics breakdown
→ Set low confidence scores
→ Continue (Validation Worker decides routing)
```

### Deduplication Timeout
```
→ If similarity check hangs: timeout after 30s
→ Log timeout, proceed with processing
→ Flag for performance review
```

## Latency Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| File detection | <1s | Directory scan |
| JSON parsing | <2s | Usually small file |
| Novelty calculation | 3-5s | Depends on history size |
| Quality validation | <1s | Local checks |
| Full processing | <15s | End-to-end per signal |

## Cost Model

| Operation | Cost | Notes |
|-----------|------|-------|
| File polling | $0.00 | Local, scheduled |
| JSON parsing | $0.00 | No external calls |
| Novelty detection | $0.00 | In-memory comparison |
| WeakSignalFinder itself | $0.00 | Local inference, open source |

## Monitoring

### Metrics
- Signal polling success rate (should be >99%)
- Processing latency p95 (target: <15s)
- Novelty detection accuracy (manual spot-checks)
- Deduplication skip rate (expected: 10-20%)
- Signal output frequency (e.g., 5 new signals per week)

### Alerts
- Polling failures on 3+ consecutive attempts
- Processing latency exceeds 30s
- Quality check failure rate > 5%
- No signal files generated in 24 hours
- Memory usage exceeds 1GB

## Configuration

### Environment Variables

```bash
# Weak Signal Finder
WSF_OUTPUT_DIR="./external/weak-signal-finder/dataset"
WSF_POLL_INTERVAL_MINUTES=60
WSF_FILE_AGE_THRESHOLD_HOURS=2

# Signal Processing
WSF_NOVELTY_THRESHOLD=0.75
WSF_TOP_WORDS_TO_EXTRACT=20
WSF_DEDUP_WINDOW_DAYS=30
WSF_DEDUP_SIMILARITY_THRESHOLD=0.85

# Quality
WSF_MIN_COMPLETENESS=0.90
WSF_MIN_TREND_CONFIDENCE=0.65
WSF_MAX_PROCESSING_TIME_SECONDS=30
```

## Non-Negotiable Principles

1. **No trend loss** — preserve all signal data even if quality is mixed
2. **Novelty is explicit** — record confidence in trend novelty
3. **Deduplication is reversible** — can override skip decisions
4. **Timestamps are sacred** — maintain accurate lineage of signal discovery
5. **Semantic data preserved** — keep word relationship graphs intact

## Integration Points

- **Input**: WeakSignalFinder (RSS signal detection)
- **Output**: Capture Worker (via webhook/queue)
- **Validation**: Validation Worker (scoring and routing)
- **Storage**: PCA knowledge graph (resolved signals)
- **Monitoring**: Orchestrator (state tracking)

## Example Workflow

```
[Friday 10:30 AM]
WeakSignalFinder runs daily
→ Outputs: signals_2026-04-25.json

[Friday 10:35 AM]
Weak Signal Worker polls
→ Detects new file
→ Parses 47 trending words
→ Checks 30-day history
→ Finds 12 novel trends
→ Calculates novelty scores

[Friday 10:40 AM]
Quality validated
→ Completeness: 0.96 ✓
→ Timestamp: fresh ✓
→ Dedup score: 0.42 (novel) ✓

[Friday 10:42 AM]
Capture schema formatted
→ 12 signal items created
→ Metadata enriched
→ Passed to Capture Worker

[Friday 10:45 AM]
Capture Worker normalizes
→ Stores in ingestion queue
→ Triggers Validation Worker

[Friday 10:50 AM]
Validation Worker scores
→ 8 signals pass (novelty > 0.80)
→ 4 signals flagged for review
→ Results logged to audit trail
```

---

**Status**: Active specification (v1.0)  
**Last Updated**: 2026-04-25  
**Related**: weak-signal-finder-integration.md, capture-worker.md, validation-worker.md, pca-orchestrator.md
