---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [phase-2, pipeline, setup, quick-start]
status: active
---

# Phase 2: Core Pipeline - Quick Start

Get the complete ingestion pipeline running in 60 minutes.

## What You'll Have

✅ **n8n Workflow** (unified router for all capture types)  
✅ **Validation Worker** (scoring, classification, routing)  
✅ **Voice Transcription** (Deepgram or Whisper)  
✅ **MP4 Support** (video file transcription)  
✅ **Real-time Dashboard** (monitor everything)  
✅ **End-to-End Integration** (capture → validate → route → display)

## Architecture

```
iPhone Capture (/capture command in Chainlit)
    ↓
n8n Webhook Trigger
    ↓
Source Classification (text, voice, article)
    ↓
Voice Transcription (if needed)
    ↓
Validation Worker (scoring + classification)
    ↓
Routing Decision (auto, review, escalate, quarantine)
    ↓
Write to Obsidian vault
    ↓
Audit Log (JSONL)
    ↓
Chainlit Dashboard (real-time visibility)
```

## Prerequisites

- ✅ Obsidian vault at `~/obsidian-vault/`
- ✅ Chainlit dashboard running
- ✅ n8n server available at `http://localhost:5678`
- ✅ Python 3.9+
- ✅ (Optional) API key for transcription (Deepgram or OpenAI)

## Phase 2 Setup (60 minutes)

### Step 1: Start Services (10 min)

**Terminal 1: n8n**
```bash
# Install n8n if needed
npm install -g n8n

# Start n8n server
n8n start
# Opens at http://localhost:5678
```

**Terminal 2: Validation Worker**
```bash
cd ~/personal-cognitive-architecture/agents

# Install dependencies
pip install -r validation-worker-requirements.txt

# Start validation worker
python validation-worker-impl.py
# Listens at http://127.0.0.1:8001
```

**Terminal 3: Transcription Service (Optional)**
```bash
# If you want voice support
pip install deepgram-sdk  # or: pip install openai

# Set transcription provider
export TRANSCRIPTION_PROVIDER=deepgram
export DEEPGRAM_API_KEY=your_key_here

# TODO: Create transcription-service.py (see voice-transcription-guide.md)
# python agents/transcription-service.py
# Listens at http://127.0.0.1:8002
```

**Terminal 4: Chainlit Dashboard**
```bash
cd ~/personal-cognitive-architecture/dashboards

# Start dashboard
chainlit run chainlit-pca-monitor.py
# Opens at http://localhost:8000
```

### Step 2: Create n8n Workflow (20 min)

Open n8n at http://localhost:5678

1. **New Workflow**
   ```
   Name: PCA Ingestion Pipeline
   Save
   ```

2. **Add Webhook Trigger**
   ```
   Search: Webhook
   Method: POST
   Path: /pca/capture
   Authentication: None (for testing)
   Save
   ```

3. **Add Function Node** (parse input)
   ```
   Search: Function
   Code:
   
   if ($input.first().body) {
     const body = $input.first().body;
     return [{
       source_type: body.source_type || 'text',
       content: body.content,
       domain: body.domain || '',
       tags: body.tags || [],
       timestamp: new Date().toISOString()
     }];
   }
   return [];
   ```

4. **Add HTTP Request Node** (call validation worker)
   ```
   Search: HTTP Request
   URL: http://127.0.0.1:8001/validate
   Method: POST
   Headers: Content-Type: application/json
   Body:
   {
     "type": "{{ $json.source_type }}",
     "content": "{{ $json.content }}",
     "domain": "{{ $json.domain }}",
     "source": "webhook",
     "timestamp": "{{ $json.timestamp }}",
     "tags": "{{ $json.tags }}"
   }
   ```

5. **Add File Write Node** (save to Obsidian)
   ```
   Search: Write Binary File (or Create Note)
   
   For local file write:
   Path: /home/user/obsidian-vault/20-Ideas/Unstructured/capture-{{ $json.file_id }}.md
   File Content:
   ---
   type: capture
   source_type: {{ $json.source_type }}
   created: {{ $json.timestamp }}
   domain: {{ $json.domain }}
   confidence: {{ $json.routing_decision.confidence }}
   ---
   
   # Capture
   
   {{ $json.content }}
   ```

6. **Add Audit Log Node**
   ```
   Search: Function
   Code:
   
   const fs = require('fs');
   const path = require('path');
   const today = new Date().toISOString().split('T')[0];
   const auditPath = path.join(process.env.HOME, 'personal-cognitive-architecture/audit-logs', `audit-${today}.jsonl`);
   
   const entry = {
     audit_timestamp: new Date().toISOString(),
     candidate_id: $json.file_id,
     source_type: $json.source_type,
     stage: 'routed',
     routing_action: $json.routing_decision.routing_action,
     processing_time_ms: 100,  // TODO: calculate actual
     cost_usd: 0.001,
     confidence: $json.routing_decision.confidence,
     destination: $json.routing_decision.destination,
     status: 'success'
   };
   
   fs.appendFileSync(auditPath, JSON.stringify(entry) + '\n');
   
   return [{success: true}];
   ```

7. **Activate Workflow**
   ```
   Click "Activate" (top right)
   Status should show: Workflow is active
   ```

### Step 3: Test End-to-End (15 min)

**Test 1: Via Dashboard /capture Command**
```
1. Open http://localhost:8000
2. Type: /capture
3. Select: Quick thought
4. Content: "Testing the pipeline"
5. Domain: "test"
6. Tags: "e2e-test"
7. Sensitivity: "public"
8. Should see: "✅ Captured to inbox"
```

**Test 2: Via n8n Webhook**
```bash
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "content": "Testing via webhook",
    "domain": "test",
    "tags": ["webhook", "test"]
  }'

# Should return success
```

**Test 3: Verify File Creation**
```bash
# Check file was created
ls -ltr ~/obsidian-vault/20-Ideas/Unstructured/ | tail -2

# View file content
cat ~/obsidian-vault/20-Ideas/Unstructured/capture-*.md | head -20
```

**Test 4: Check Audit Log**
```bash
# Check audit log was written
tail -5 ~/personal-cognitive-architecture/audit-logs/audit-*.jsonl | jq .
```

**Test 5: Monitor Dashboard**
```
1. Open http://localhost:8000
2. Type: /watch
3. Create a new capture (from /capture command or webhook)
4. Should see real-time updates:
   - Queue: ⏳ 1 | 🔄 0 | ⚠️ 0
   - Cost: $0.00X | Success: 100%
5. Type: /traces
6. Should see latest capture as newest entry
```

### Step 4: Add Voice Transcription (15 min - optional)

**If using Deepgram:**
```bash
# Set API key
export DEEPGRAM_API_KEY=your_key_here

# TODO: Add transcription node to n8n workflow
# (see voice-transcription-guide.md for details)
```

**Test Voice Capture:**
```
1. In /capture command:
   → Select "Voice note summary"
   → Record or provide audio
   → Should transcribe automatically
   → Rest of pipeline continues
```

## Verification Checklist

After setup:

- [ ] n8n workflow created and activated
- [ ] Validation worker running (http://127.0.0.1:8001/health returns 200)
- [ ] Dashboard loads (http://localhost:8000)
- [ ] `/capture` command works (creates file in Obsidian)
- [ ] n8n webhook responds (status 200)
- [ ] Audit log file created (audit-YYYY-MM-DD.jsonl exists)
- [ ] Dashboard `/watch` shows captures in real-time
- [ ] Dashboard `/traces` shows recent captures
- [ ] File created in ~/obsidian-vault/20-Ideas/Unstructured/
- [ ] Frontmatter correctly formatted in created files
- [ ] Validation worker classifies captures
- [ ] Routing decisions made (auto/review/escalate/quarantine)

## Performance Expectations

| Step | Duration | Target |
|------|----------|--------|
| Capture creation | <2s | <2s |
| n8n processing | <5s | <10s |
| Validation | <3s | <5s |
| File write | <1s | <2s |
| **Total** | ~11s | <30s |

If total >30s, check:
1. Validation worker logs for slow processing
2. n8n execution logs for delays
3. Network latency between services

## Troubleshooting

### n8n webhook not triggering

```bash
# Check n8n logs
tail -100 ~/.n8n/logs/*.log

# Test webhook directly
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d '{"source_type":"text","content":"test"}'

# Should return something (even if empty 200 response)
```

### Validation worker not responding

```bash
# Check if running
curl http://127.0.0.1:8001/health

# Check logs
# (should see startup message with port)

# Test validation endpoint
curl -X POST http://127.0.0.1:8001/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type":"text",
    "content":"test",
    "source":"test",
    "timestamp":"2026-04-25T14:30:00Z"
  }'
```

### Files not appearing in Obsidian

```bash
# Check folder exists
test -d ~/obsidian-vault/20-Ideas/Unstructured/ && echo "✅ Exists"

# Check file permissions
ls -la ~/obsidian-vault/20-Ideas/

# Check audit log for errors
tail -20 ~/personal-cognitive-architecture/audit-logs/audit-*.jsonl | grep error
```

### Dashboard shows no captures

```bash
# Check audit logs exist
ls -la ~/personal-cognitive-architecture/audit-logs/

# Check dashboard can read them
tail -5 ~/personal-cognitive-architecture/audit-logs/audit-*.jsonl
```

## Next Steps

After Phase 2 is working:

1. **Phase 2a**: Implement agents (orchestrator, capture-worker, etc.)
2. **Phase 2b**: Add graph feedback (show user corrections on knowledge graph)
3. **Phase 2c**: Implement monthly calibration cycle
4. **Phase 3**: Advanced features (anomaly detection, A/B testing, custom alerts)

## Success Criteria

You've completed Phase 2 when:

✅ Captures flow from iPhone (or browser) → n8n → validation → Obsidian  
✅ Routing decisions work correctly  
✅ Dashboard shows real-time metrics  
✅ Audit logs record all operations  
✅ Validation worker classifies correctly  
✅ End-to-end latency <30 seconds  
✅ Voice transcription works (optional)  

---

**Status**: Ready to implement
**Estimated Time**: 60 minutes
**Related**: workflows/n8n/pca-ingest-complete.md, agents/validation-worker-impl.py
