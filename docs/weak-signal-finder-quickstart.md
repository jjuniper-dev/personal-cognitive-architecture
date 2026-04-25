---
type: quickstart-guide
created: 2026-04-25
tags: [pca, weak-signals, setup, rss]
status: active
---

# WeakSignalFinder Quick Start Guide

Get WeakSignalFinder integrated with your PCA system in 15 minutes.

## Prerequisites

- Python 3.9+ (recommend 3.11+)
- 2-4 GB RAM available
- Git
- n8n instance (running locally or Docker)
- PCA repository cloned and set up

## Step 1: Clone WeakSignalFinder (2 min)

```bash
cd ~/personal-cognitive-architecture

mkdir -p external
git clone https://github.com/LittleViewer/WeakSignalFinder.git \
  external/weak-signal-finder

cd external/weak-signal-finder
```

## Step 2: Install Dependencies (3 min)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language models
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm

# Add more languages as needed (de, es, pt, etc.)
# List available: python -m spacy download --help
```

## Step 3: Create Required Directories (1 min)

```bash
mkdir -p log saveState dataset local_api
```

## Step 4: Configure RSS Feeds (3 min)

Edit `libCore/input/rssFeed.json`:

**Minimal example** (3 feeds):

```json
{
  "feeds": [
    {
      "name": "TechCrunch",
      "url": "https://techcrunch.com/feed/",
      "language": "en",
      "region": "global",
      "category": "technology",
      "priority": 0.9,
      "enabled": true
    },
    {
      "name": "SecurityNews",
      "url": "https://feeds.bleepingcomputer.com/",
      "language": "en",
      "region": "global",
      "category": "security",
      "priority": 1.0,
      "enabled": true
    },
    {
      "name": "HackerNews",
      "url": "https://news.ycombinator.com/rss",
      "language": "en",
      "region": "global",
      "category": "technology",
      "priority": 0.8,
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

**Pro tip**: Start with 3-5 feeds to verify it works, then expand.

## Step 5: Test Manual Run (2 min)

```bash
cd ~/personal-cognitive-architecture/external/weak-signal-finder

# Run once to verify setup
python main.py

# Check output
ls -lh dataset/
cat dataset/signals_*.json | head -50
```

**Expected output**: 
- A JSON file appears in `dataset/` with timestamp name: `signals_YYYY-MM-DD.json`
- Contains `topWords`, `semanticNeighborhoods`, `sources` fields

## Step 6: Set Up PCA Integration (2 min)

```bash
cd ~/personal-cognitive-architecture

# Install Weak Signal Worker
pip install -r agents/weak-signal-worker-requirements.txt

# Test the worker
python agents/weak-signal-worker.py
```

**Expected output**: 
```
✓ Signal normalized and ready for Capture Worker
{
  "capture_id": "signal-20260425-143022",
  "source_type": "rss-signal",
  "source_system": "weak-signal-finder",
  ...
}
```

## Step 7: Configure n8n Workflow (2 min)

1. **Open n8n** (http://localhost:3000 or your instance)
2. **Import workflow**: 
   - Click `+` → Import from file
   - Select `workflows/n8n/weak-signal-polling.json`
3. **Set environment variable**:
   - Click workflow settings ⚙️
   - Add env var: `PCA_ROOT=/home/user/personal-cognitive-architecture`
4. **Configure webhook endpoint**:
   - Change `http://localhost:3000/webhook/capture-ingest` to your actual Capture Worker webhook
5. **Set interval**:
   - Edit "Trigger: Hourly Signal Poll" node
   - Adjust interval (default: 1 hour, recommend: 6-24 hours)
6. **Enable & save**

## Step 8: Verify End-to-End (1 min)

```bash
# Monitor WeakSignalFinder output
watch -n 60 'ls -lh ~/personal-cognitive-architecture/external/weak-signal-finder/dataset/'

# In another terminal, monitor PCA ingestion
tail -f ~/personal-cognitive-architecture/logs/capture-worker.log

# Check that signals appear as captures
grep "rss-signal" logs/*.log
```

## Configuration Reference

### Environment Variables

Add to your `.bashrc` or `.env`:

```bash
# Weak Signal Finder
export WSF_ROOT="~/personal-cognitive-architecture/external/weak-signal-finder"
export WSF_OUTPUT_DIR="$WSF_ROOT/dataset"
export WSF_POLL_INTERVAL_MINUTES=60

# PCA
export PCA_ROOT="~/personal-cognitive-architecture"
export CAPTURE_WEBHOOK_URL="http://localhost:3000/webhook/capture-ingest"
```

### Tuning Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `topWordsCount` | 50 | How many trends to extract per run |
| `minWordFreq` | 2 | Minimum frequency to include word |
| `pollInterval` | 1 hour | How often WeakSignalFinder runs |
| `dedup_window_days` | 30 | How long to remember past signals |
| `novelty_threshold` | 0.75 | Minimum novelty to escalate |

### RSS Feed Sources (Suggested)

**Technology**:
- https://techcrunch.com/feed/
- https://feeds.arstechnica.com/arstechnica/index
- https://www.theverge.com/rss/index.xml

**Security**:
- https://feeds.bleepingcomputer.com/
- https://krebsonsecurity.com/feed/
- https://www.securityweek.com/feed

**Science & AI**:
- https://feeds.arxiv.org/rss/cs.AI
- https://feeds.arxiv.org/rss/stat.ML
- https://feeds.nature.com/nature/rss/current

**Business**:
- https://feeds.bloomberg.com/markets/news.rss
- https://feeds.reuters.com/reuters/businessNews
- https://feeds.cnbc.com/id/100003114/rss.html

## Troubleshooting

### No output files generated

```bash
cd external/weak-signal-finder
python main.py

# Check for errors
cat log/*.log

# Verify spaCy models
python -c "import spacy; spacy.load('en_core_web_sm')"

# Test RSS feed connectivity
curl -I "https://techcrunch.com/feed/"
```

### Memory errors

**Symptoms**: Process killed, Python crashes

**Solution**:
```bash
# Reduce feed count in rssFeed.json (start with 3)
# OR increase available memory
# OR use smaller spaCy models (en_core_web_sm vs en_core_web_lg)
```

### Slow processing

**Symptoms**: Takes >30 minutes to run

**Solution**:
1. Reduce `topWordsCount` in rssFeed.json (try 30 instead of 50)
2. Remove extra language models (keep only en)
3. Run during off-peak hours
4. Check system load: `top` or `htop`

### Empty semantic neighborhoods

**Symptoms**: `semanticNeighborhoods` is empty array

**Solution**:
- Increase `minWordFreq` in config (try 3-5)
- Check feed volume (need 100+ articles for good semantics)
- Verify spaCy model installed correctly

## Next: Full Integration

After successful setup:

1. ✓ WeakSignalFinder running
2. ✓ Manual test passed
3. → Connect to Capture Worker webhook
4. → Set up Validation Worker scoring
5. → Configure notification on high-novelty signals
6. → Tune thresholds based on 1 week of signals

See: `docs/weak-signal-finder-integration.md` for full architecture.

## Key Files

| File | Purpose |
|------|---------|
| `external/weak-signal-finder/libCore/input/rssFeed.json` | RSS feed configuration |
| `agents/weak-signal-worker.py` | Signal normalization code |
| `agents/weak-signal-worker.md` | Worker specification |
| `workflows/n8n/weak-signal-polling.json` | n8n automation workflow |
| `docs/weak-signal-finder-integration.md` | Full integration guide |

## Support

- **WeakSignalFinder Issues**: https://github.com/LittleViewer/WeakSignalFinder/issues
- **PCA Integration Questions**: See `docs/pca-north-star.md` for architecture
- **RSS Feed Issues**: Verify feed URL with: `curl -I <url>`

---

**Estimated total time**: 15 minutes  
**Difficulty**: Beginner  
**Dependencies**: Python, n8n, git
