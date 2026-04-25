---
type: integration-guide
created: 2026-04-25
updated: 2026-04-25
tags: [pca, weak-signals, rss, signal-detection]
status: active
---

# WeakSignalFinder Integration Guide

## Overview

WeakSignalFinder is an RSS-based signal detection system that monitors news feeds for emerging themes and weak signals. It processes articles through NLP to identify trending words, semantic neighborhoods, and novel topics—feeding high-confidence signals into the PCA Capture pipeline.

## Architecture

### How It Fits in PCA

```
RSS Feeds (configured)
    ↓
[WeakSignalFinder]
    ├─ Aggregates articles by language/region
    ├─ NLP processing (lemmatization, text cleaning)
    ├─ Frequency analysis (trending words/themes)
    └─ Semantic neighborhood building
    ↓
[Signal Output] → JSON with word frequencies, clusters
    ↓
[PCA Capture Worker]
    ├─ Source type: "rss-signal"
    ├─ Normalize signal data
    └─ Extract emerging topics
    ↓
[PCA Validation Worker]
    ├─ Score signal novelty
    ├─ Assess urgency
    └─ Route to knowledge graph
```

### Key Responsibilities

**WeakSignalFinder**:
- Polls configured RSS feeds on schedule
- Cleans, lemmatizes, and processes article text
- Calculates word/topic frequencies
- Identifies semantic clusters (words appearing together)
- Outputs timestamped JSON with:
  - Top trending words (with frequency scores)
  - Semantic neighborhoods (contextual relationships)
  - Language/region breakdowns
  - Article source metadata

**PCA Capture Worker Integration**:
- Consumes WeakSignalFinder JSON output
- Normalizes signals into capture schema
- Extracts metadata (trends, clusters, novelty indicators)
- Flags high-confidence emerging themes
- Passes to Validation Worker for scoring

## Setup

### 1. Environment & Dependencies

**Python Requirements**: 3.9+ (3.11+ recommended)  
**RAM**: 2-4 GB available  
**Storage**: ~500MB for spaCy models + outputs

### 2. Directory Structure

```
personal-cognitive-architecture/
├── external/
│   └── weak-signal-finder/
│       ├── main.py
│       ├── requirements.txt
│       ├── libCore/
│       │   ├── input/
│       │   │   └── rssFeed.json (configured feeds)
│       │   └── ...
│       ├── log/
│       ├── saveState/
│       ├── dataset/
│       └── local_api/
├── workflows/
│   └── n8n/
│       └── weak-signal-polling.json (n8n workflow)
└── agents/
    └── weak-signal-worker.md (this agent spec)
```

### 3. Installation

```bash
# Clone WeakSignalFinder
git clone https://github.com/LittleViewer/WeakSignalFinder.git \
  /home/user/personal-cognitive-architecture/external/weak-signal-finder

cd external/weak-signal-finder

# Install dependencies
pip install -r requirements.txt

# Download spaCy language models (adjust languages as needed)
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
# Add more as needed for your configured feed languages

# Create required directories
mkdir -p log saveState dataset local_api
```

### 4. RSS Feed Configuration

**File**: `external/weak-signal-finder/libCore/input/rssFeed.json`

```json
{
  "feeds": [
    {
      "name": "TechNews",
      "url": "https://feeds.example.com/tech.xml",
      "language": "en",
      "region": "global",
      "category": "technology",
      "priority": 0.9,
      "enabled": true
    },
    {
      "name": "SecurityAlerts",
      "url": "https://feeds.example.com/security.xml",
      "language": "en",
      "region": "global",
      "category": "security",
      "priority": 1.0,
      "enabled": true
    }
  ],
  "processingConfig": {
    "cleanText": true,
    "lemmatize": true,
    "minWordFreq": 2,
    "topWordsCount": 50,
    "semanticNeighborhoodDepth": 3
  }
}
```

## Operation

### Running WeakSignalFinder

**Manual execution**:
```bash
cd external/weak-signal-finder
python main.py
```

**Via Scheduler** (n8n workflow, see weak-signal-polling.json):
- Scheduled daily/weekly based on feed velocity
- Outputs JSON file: `dataset/signals_YYYY-MM-DD.json`
- Stores state in `saveState/` for deduplication

### Output Format

```json
{
  "timestamp": "2026-04-25T10:30:00Z",
  "period": "daily",
  "languages": ["en", "fr"],
  "topWords": [
    {
      "word": "quantum",
      "frequency": 42,
      "score": 0.95,
      "language": "en",
      "category": "technology",
      "novelty": 0.82
    }
  ],
  "semanticNeighborhoods": [
    {
      "hub": "quantum",
      "neighbors": ["computing", "cryptography", "security"],
      "cooccurrence_frequency": 18,
      "strength": 0.78
    }
  ],
  "sources": {
    "count": 247,
    "languages": ["en", "fr"],
    "top_feeds": ["TechNews", "SecurityAlerts"]
  }
}
```

## Integration with PCA

### Capture Worker Adapter

The Capture Worker will:

1. **Poll** `dataset/` directory for new signal files
2. **Parse** JSON structure
3. **Transform** into capture schema:

```json
{
  "source_type": "rss-signal",
  "source": "weak-signal-finder",
  "content_type": "signal-trends",
  "timestamp": "2026-04-25T10:30:00Z",
  "normalized_text": "[Formatted summary of top trends]",
  "metadata": {
    "trending_topics": ["quantum computing", "security"],
    "signal_count": 42,
    "novelty_indicators": [0.82, 0.75],
    "semantic_clusters": 8,
    "languages": ["en", "fr"],
    "feed_sources": 247
  },
  "quality_metrics": {
    "data_completeness": 0.98,
    "language_detection": 0.99,
    "trend_confidence": 0.89
  }
}
```

4. **Validate** quality metrics (completeness > 0.90)
5. **Pass** to Validation Worker

### Validation Worker Scoring

Validation Worker will assess:

- **Novelty Score**: Is this trend genuinely new? (0.0-1.0)
- **Urgency Score**: Does this require immediate attention? (0.0-1.0)
- **Confidence Score**: How reliable are the trend signals? (0.0-1.0)
- **Relevance**: Does this align with configured interests?

**Escalation Triggers**:
- Novelty > 0.80 AND Confidence > 0.75 → Flag as emerging signal
- Urgency > 0.85 → Priority review
- Multiple semantic clusters → Pattern recognition opportunity

## Monitoring & Maintenance

### Health Checks

```bash
# Verify spaCy models loaded
python -c "import spacy; spacy.load('en_core_web_sm')"

# Check feed connectivity
curl -I https://feeds.example.com/tech.xml

# Verify output directory
ls -lh dataset/ | tail -5
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Memory errors | Increase available RAM or reduce feed count |
| Slow processing | Run during off-peak hours or use fewer languages |
| Missing output files | Check `log/` for errors; verify feed URLs |
| Stale signals | Check `saveState/` for deduplication; refresh manually |

## Cost & Performance

### Resources

- **CPU**: Minimal (I/O bound)
- **Memory**: 2-3 GB during processing
- **Disk**: ~100MB per week of signal history
- **Network**: Depends on RSS feed count and latency

### Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Feed poll cycle | 1-2 hours | Configurable |
| Processing latency | 5-15 mins | Depends on feed volume |
| Output JSON size | 1-5 MB | Daily signal file |
| Feed success rate | >95% | Some feeds may timeout |

## Next Steps

1. ✓ Clone and install WeakSignalFinder
2. ✓ Configure `rssFeed.json` with your RSS sources
3. ✓ Download spaCy models for your languages
4. → Create n8n workflow for scheduled polling
5. → Implement Capture Worker adapter (see agents/weak-signal-worker.md)
6. → Test end-to-end signal flow
7. → Monitor and tune scoring thresholds

---

**Status**: Integration specification (v1.0)  
**Last Updated**: 2026-04-25  
**Related**: agents/weak-signal-worker.md, capture-worker.md, pca-orchestrator.md
