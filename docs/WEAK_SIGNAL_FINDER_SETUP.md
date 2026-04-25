---
type: setup-summary
created: 2026-04-25
tags: [pca, weak-signals, integration]
status: active
---

# WeakSignalFinder Setup Summary

## What We've Set Up

Your Personal Cognitive Architecture now has a complete integration for **WeakSignalFinder**, a system that detects emerging themes and weak signals from RSS feeds.

### Overview

WeakSignalFinder monitors news feeds, applies NLP processing, and identifies trending topics and semantic clusters. These signals feed into your PCA's Capture → Validation → Knowledge Graph pipeline for early pattern detection.

## Files Created

### Documentation

1. **`docs/weak-signal-finder-integration.md`** (Primary reference)
   - Architecture overview
   - Setup instructions  
   - Operation procedures
   - Monitoring and maintenance

2. **`docs/weak-signal-finder-quickstart.md`** (Get started in 15 min)
   - Step-by-step setup
   - Configuration examples
   - Troubleshooting guide
   - Tuning reference

3. **`docs/WEAK_SIGNAL_FINDER_SETUP.md`** (This file)
   - Summary of what's been created
   - How pieces fit together

### Code & Configuration

1. **`agents/weak-signal-worker.md`** (Agent specification)
   - Responsibilities and scope
   - Input/output contracts
   - Processing pipeline
   - Error handling patterns

2. **`agents/weak-signal-worker.py`** (Implementation)
   - Signal polling and extraction
   - Novelty detection
   - Quality validation
   - Deduplication logic
   - Ready to integrate with Capture Worker

3. **`agents/weak-signal-worker-requirements.txt`** (Python dependencies)

4. **`workflows/n8n/weak-signal-polling.json`** (Automation workflow)
   - Hourly polling schedule
   - WeakSignalFinder execution
   - Signal extraction
   - Webhook ingestion to Capture Worker

## Architecture

```
RSS Feeds (configured)
    ↓
[WeakSignalFinder] (external tool)
    • Aggregates articles
    • NLP processing (spaCy)
    • Trend detection
    ↓
[Signal Output] (JSON)
    • Top trending words
    • Semantic clusters
    • Coverage metadata
    ↓
[Weak Signal Worker] (agents/weak-signal-worker.py)
    • Polls for new signals
    • Extracts trending topics
    • Detects novelty
    • Validates quality
    • Deduplicates
    ↓
[PCA Capture Worker]
    • Normalizes into capture schema
    • Adds metadata
    ↓
[PCA Validation Worker]
    • Scores novelty & urgency
    • Routes to knowledge graph
    ↓
[Knowledge Graph (Obsidian)]
    • Stores emerging signals
    • Links to source articles
    • Available for cross-domain pattern matching
```

## Integration Points

### 1. Signal Source
- **Input**: RSS feed URLs configured in `libCore/input/rssFeed.json`
- **Output**: `dataset/signals_YYYY-MM-DD.json` (WeakSignalFinder)

### 2. Weak Signal Worker
- **Input**: WeakSignalFinder JSON output (signals_*.json files)
- **Function**: Normalize, validate, detect novelty, deduplicate
- **Output**: PCA Capture schema (ready for Capture Worker)

### 3. n8n Automation
- **Trigger**: Hourly schedule (configurable)
- **Function**: Execute WeakSignalFinder, extract output, POST to webhook
- **Target**: Capture Worker ingestion webhook

### 4. PCA Pipeline
- **Capture Worker**: Receives signal data via webhook
- **Validation Worker**: Scores novelty, urgency, relevance
- **Knowledge Graph**: Stores resolved signals with source metadata

## Getting Started

### Quickest Path (15 minutes)

1. Follow **`docs/weak-signal-finder-quickstart.md`**
   - Clone WeakSignalFinder
   - Install dependencies
   - Configure 3-5 RSS feeds
   - Test manual run
   - Set up n8n workflow

2. Verify operation:
   - Signal files appear in `dataset/`
   - Weak Signal Worker successfully normalizes them
   - n8n workflow runs on schedule

### Full Integration (1-2 hours)

1. Read **`docs/weak-signal-finder-integration.md`** for architecture details
2. Configure your RSS feeds for your specific interests
3. Tune Weak Signal Worker parameters:
   - `novelty_threshold` (when to escalate)
   - `dedup_window_days` (signal history window)
   - `top_words_to_extract` (how many trends to monitor)
4. Integrate with Capture Worker webhook
5. Connect Validation Worker for scoring
6. Set up alerts for high-novelty signals

## Key Features

### ✓ Automatic Signal Detection
- Polls RSS feeds on schedule (default: 1 hour)
- Identifies trending topics and semantic clusters
- Provides novelty scores for each trend

### ✓ Quality Validation
- Checks data completeness (must be >90%)
- Language detection confidence
- Trend confidence based on coverage

### ✓ Deduplication
- Maintains 30-day history of signals
- Calculates similarity to avoid repeats
- Prevents alert fatigue

### ✓ Scalable
- Process 100s of RSS feeds
- Support multiple languages
- Low resource requirements (2-4 GB RAM)

### ✓ Debuggable
- Clear logging at each stage
- JSON output easy to inspect
- Integration with PCA audit trails

## Configuration Reference

### Essential Files

```
personal-cognitive-architecture/
├── external/
│   └── weak-signal-finder/
│       └── libCore/input/rssFeed.json          ← CONFIGURE THIS
├── agents/
│   ├── weak-signal-worker.py                   ← RUNS THIS
│   └── weak-signal-worker.md                   ← EXPLAINS THIS
└── workflows/n8n/
    └── weak-signal-polling.json                ← AUTOMATES THIS
```

### Environment Variables

```bash
export WSF_ROOT="~/personal-cognitive-architecture/external/weak-signal-finder"
export WSF_OUTPUT_DIR="$WSF_ROOT/dataset"
export WSF_POLL_INTERVAL_MINUTES=60
export PCA_ROOT="~/personal-cognitive-architecture"
```

## Monitoring & Operations

### Daily Checks

```bash
# Verify signal files are being generated
ls -lh external/weak-signal-finder/dataset/ | tail -5

# Check for processing errors
tail -20 external/weak-signal-finder/log/*.log

# Monitor ingestion
grep "rss-signal" logs/capture-worker.log
```

### Troubleshooting

| Symptom | First Step |
|---------|-----------|
| No signal files | Run `python main.py` in WeakSignalFinder dir |
| Memory errors | Reduce feed count or add RAM |
| Stale signals | Check spaCy models installed |
| Slow processing | Use fewer languages/feeds |

See: `docs/weak-signal-finder-quickstart.md#troubleshooting` for detailed solutions.

## What's NOT Included

This setup focuses on:
- ✓ Signal detection from RSS feeds
- ✓ Signal normalization and validation
- ✓ Integration with PCA pipeline

This setup does NOT yet include:
- ❌ Capture Worker webhook implementation (you'll need to implement or point to existing)
- ❌ Validation Worker scoring logic (uses existing specification)
- ❌ Obsidian vault integration (handled by existing PCA pipeline)
- ❌ Alert routing (use existing PCA Orchestrator rules)

## Next Steps

### Phase 1: Verification (1-2 hours)
- [ ] Clone WeakSignalFinder
- [ ] Install and test manually
- [ ] Configure RSS feeds
- [ ] Verify signal output

### Phase 2: Integration (2-4 hours)
- [ ] Set up n8n workflow
- [ ] Connect to Capture Worker
- [ ] Test end-to-end signal flow
- [ ] Tune novelty thresholds

### Phase 3: Operations (ongoing)
- [ ] Monitor signal quality
- [ ] Tune feed list (add/remove sources)
- [ ] Track novelty score accuracy
- [ ] Iterate on validation rules

## Documentation Structure

```
docs/
├── weak-signal-finder-integration.md      ← Full reference
├── weak-signal-finder-quickstart.md       ← Fast setup
├── WEAK_SIGNAL_FINDER_SETUP.md           ← This file
└── ...

agents/
├── weak-signal-worker.md                  ← Agent spec
├── weak-signal-worker.py                  ← Implementation
├── weak-signal-worker-requirements.txt    ← Dependencies
└── ...

workflows/n8n/
└── weak-signal-polling.json               ← Automation
```

## Support

- **WeakSignalFinder source**: https://github.com/LittleViewer/WeakSignalFinder
- **PCA architecture**: See `docs/pca-north-star.md` and `docs/pca-operating-model.md`
- **Integration questions**: See `docs/weak-signal-finder-integration.md`

---

**Setup Date**: 2026-04-25  
**Status**: Ready for deployment  
**Estimated Setup Time**: 15-30 minutes  
**Maintenance**: 5 minutes/day for monitoring
