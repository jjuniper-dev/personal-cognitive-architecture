---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [agents, orchestrator, capture-worker, deployment, architecture]
status: ready
---

# PCA Agents - Deployment & Integration Guide

Complete agent system with Orchestrator, Capture Worker, and Validation Worker.

## Architecture

```
                    ┌─────────────────────────────┐
                    │   n8n Ingestion Pipeline    │
                    │  (Webhook + Folder Watch)   │
                    └──────────────┬──────────────┘
                                   ↓
                    ┌─────────────────────────────┐
                    │   Capture Worker (8002)     │
                    │ - Voice transcription       │
                    │ - Article extraction       │
                    │ - Signal/RSS processing    │
                    │ - Quality validation       │
                    └──────────────┬──────────────┘
                                   ↓
                    ┌─────────────────────────────┐
                    │  Orchestrator (8003)        │
                    │ - Dispatch to worker        │
                    │ - Apply routing rules       │
                    │ - Manage escalations        │
                    │ - Monthly calibration       │
                    └──────────────┬──────────────┘
                                   ↓
                    ┌─────────────────────────────┐
                    │ Validation Worker (8001)    │
                    │ - 4D scoring                │
                    │ - LLM classification       │
                    │ - Routing decision         │
                    └──────────────┬──────────────┘
                                   ↓
                    ┌─────────────────────────────┐
                    │  Obsidian Vault             │
                    │  + Audit Logs (JSONL)       │
                    └─────────────────────────────┘
```

## Services

### 1. Validation Worker (Port 8001)
**Already implemented.** Handles scoring and classification.

```
POST /validate
  Input: {type, content, domain, source, timestamp, ...}
  Output: {scores, classification, routing_decision}
```

### 2. Capture Worker (Port 8002)
**New.** Ingests and transcribes captures.

```
POST /capture/voice
  Input: audio file (WAV, MP3, M4A, MP4)
  Output: {source_type, content (transcribed), metadata}

POST /capture/article
  Input: {url}
  Output: {source_type, content (extracted), metadata}

POST /capture/signal
  Input: {feed_url}
  Output: {source_type, content (feed entry), metadata}

POST /capture/text
  Input: {content, domain, tags}
  Output: {source_type, content, metadata}
```

### 3. Orchestrator (Port 8003)
**New.** Control plane for routing and calibration.

```
POST /dispatch
  Input: CaptureRequest (from Capture Worker)
  Output: {success, action, destination, ...}

POST /escalation/{id}/resolve
  Input: {action, feedback}
  Output: updated escalation with user correction

GET /escalations
  Output: List of pending escalations

POST /calibration/monthly
  Output: {accuracy_by_pattern, weight_sensitivity, recommendations}

POST /calibration/apply
  Input: {recommendations, user_approval}
  Output: {status, count, timestamp}
```

## Deployment

### Prerequisites

```bash
# Python 3.9+
python --version

# Node.js (for n8n)
node --version

# Optional: Transcription API keys
export DEEPGRAM_API_KEY=your_key
export OPENAI_API_KEY=your_key
export TRANSCRIPTION_PROVIDER=deepgram  # or: openai, local
```

### Installation

```bash
# 1. Install dependencies for all agents
pip install fastapi uvicorn pydantic openai aiohttp feedparser requests

# 2. Optional: Transcription libraries
pip install deepgram-sdk  # if using Deepgram
pip install openai-whisper  # if using local Whisper
pip install trafilatura  # for better article extraction
```

### Start Services

**Terminal 1: Validation Worker (8001)**
```bash
cd ~/personal-cognitive-architecture/agents
python validation-worker-impl.py
# Listening on http://127.0.0.1:8001
```

**Terminal 2: Capture Worker (8002)**
```bash
cd ~/personal-cognitive-architecture/agents
python capture-worker-impl.py
# Listening on http://127.0.0.1:8002
```

**Terminal 3: Orchestrator (8003)**
```bash
cd ~/personal-cognitive-architecture/agents
python orchestrator-impl.py
# Listening on http://127.0.0.1:8003
```

**Terminal 4: n8n (5678)**
```bash
npm install -g n8n
n8n start
# Listening on http://localhost:5678
```

**Terminal 5: Chainlit Dashboard (8000)**
```bash
cd ~/personal-cognitive-architecture/dashboards
chainlit run chainlit-pca-monitor.py
# Listening on http://localhost:8000
```

### Verify Services

```bash
# Check all services
curl http://127.0.0.1:8001/health  # Validation Worker
curl http://127.0.0.1:8002/health  # Capture Worker
curl http://127.0.0.1:8003/health  # Orchestrator
curl http://localhost:5678          # n8n UI
curl http://localhost:8000          # Chainlit UI
```

## Integration: n8n Workflow with Agents

In n8n, create workflow that calls agents in sequence:

### Workflow: Unified Ingestion Pipeline

**Node 1: Webhook Trigger**
```
POST /webhook/pca/capture
```

**Node 2: Call Capture Worker** (based on source_type)
```
IF source_type == "voice":
  POST http://127.0.0.1:8002/capture/voice
ELSE IF source_type == "article":
  POST http://127.0.0.1:8002/capture/article
ELSE:
  POST http://127.0.0.1:8002/capture/text
```

**Node 3: Call Orchestrator**
```
POST http://127.0.0.1:8003/dispatch
Input: {
  source_type: $node.Node2.json.source_type,
  content: $node.Node2.json.content,
  domain: $input.body.domain,
  ...
}
```

**Node 4: Write Result**
```
Based on orchestrator response:
  IF action == "ADVANCE_TO_INTEGRATION":
    Write to 10-Projects/[domain]/Notes/
  ELSE IF action == "ROUTE_WITH_TAG":
    Write to 20-Ideas/Unstructured/
  ELSE IF action == "ESCALATE_FOR_REVIEW":
    Write to 40-Escalations/
  ELSE:
    Write to 40-Archive/
```

**Node 5: Log Audit**
```
Append to audit-YYYY-MM-DD.jsonl
```

## Testing

### Test 1: Voice Transcription

```bash
# Create test audio
ffmpeg -f lavfi -i "sine=frequency=440:duration=3" test.wav

# Send to Capture Worker
curl -X POST http://127.0.0.1:8002/capture/voice \
  -F "file=@test.wav"

# Should return: {source_type: "voice", content: "transcribed text", ...}
```

### Test 2: Article Extraction

```bash
curl -X POST "http://127.0.0.1:8002/capture/article?url=https://example.com/article"

# Should return: {source_type: "article", content: "extracted text", ...}
```

### Test 3: End-to-End via Orchestrator

```bash
curl -X POST http://127.0.0.1:8003/dispatch \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "content": "Testing the agent system",
    "domain": "test",
    "timestamp": "2026-04-25T12:00:00Z"
  }'

# Should return routing decision
```

### Test 4: Full Pipeline via n8n

```bash
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "content": "Test from webhook",
    "domain": "test"
  }'

# Should trigger entire workflow
```

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Voice transcription | <10s | Deepgram: ~1s per minute of audio |
| Article extraction | <5s | Depends on page size |
| Capture validation | <2s | Local quality checks |
| Validation/scoring | <3s | LLM call |
| Orchestration | <1s | Routing decision |
| **Total** | **<30s** | Goal for end-to-end |

## Monitoring

### Health Endpoints

```bash
# All services have /health endpoint
watch -n 5 'curl -s http://127.0.0.1:8001/health | jq .'
```

### Logs

```bash
# Follow each agent's logs
tail -f /tmp/validation-worker.log
tail -f /tmp/capture-worker.log
tail -f /tmp/orchestrator.log
```

### Metrics

Dashboard commands track:
- `/metrics` — Performance metrics
- `/watch` — Real-time pipeline flow
- `/traces` — Recent operations

## Escalation Management

### View Pending Escalations

```bash
curl http://127.0.0.1:8003/escalations
```

### Resolve Escalation

```bash
curl -X POST "http://127.0.0.1:8003/escalation/escalation-123456/resolve" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approved",
    "feedback": "User confirmed routing"
  }'
```

## Monthly Calibration

### Start Calibration Cycle

```bash
curl -X POST http://127.0.0.1:8003/calibration/monthly
```

Returns:
```json
{
  "month": "2026-04",
  "accuracy_by_pattern": {
    "article": {"accuracy": 0.92, "count": 45},
    "voice": {"accuracy": 0.88, "count": 32}
  },
  "weight_sensitivity": {
    "credibility": 12,
    "relevance": 8
  },
  "recommendations": [...]
}
```

### Apply Recommendations

```bash
curl -X POST http://127.0.0.1:8003/calibration/apply \
  -H "Content-Type: application/json" \
  -d '{
    "recommendations": [...],
    "user_approval": true
  }'
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8002

# Kill process
kill -9 <PID>
```

### Validation Worker Returns 500

```bash
# Check logs
cat /tmp/validation-worker.log | tail -50

# Restart
pkill -f validation-worker
cd ~/personal-cognitive-architecture/agents
python validation-worker-impl.py
```

### Transcription Failing

```bash
# Check transcription provider
curl http://127.0.0.1:8002/health

# Verify API keys
echo $DEEPGRAM_API_KEY
echo $OPENAI_API_KEY

# Check transcription logs
cat /tmp/capture-worker.log | grep -i transcription
```

### Escalations not Persisting

```bash
# Check escalation queue
curl http://127.0.0.1:8003/escalations | jq .

# Verify feedback log exists
ls -la ~/personal-cognitive-architecture/data/feedback-log.jsonl
```

## Production Checklist

- [ ] All services running (validate with /health endpoints)
- [ ] n8n workflow configured and activated
- [ ] Obsidian vault structure verified
- [ ] Audit logs directory exists and writable
- [ ] Transcription API keys set (if using cloud)
- [ ] Routing rules loaded from routing-rules.json
- [ ] Feedback log initialized (data/feedback-log.jsonl)
- [ ] Dashboard accessible and updating
- [ ] End-to-end test successful (< 30s latency)
- [ ] Escalation resolution workflow tested
- [ ] Monthly calibration cycle scheduled

## Next Steps

1. ✅ Deploy all three agents
2. ✅ Create n8n workflow
3. ✅ Test end-to-end
4. ✅ Monitor for 24 hours
5. ✅ Set up monthly calibration schedule
6. ✅ Configure escalation review process

---

**Status**: Ready for deployment
**Last Updated**: 2026-04-25
**Related**: validation-worker-impl.py, capture-worker-impl.py, orchestrator-impl.py
