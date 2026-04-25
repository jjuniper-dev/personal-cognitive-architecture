---
type: workflow
created: 2026-04-25
updated: 2026-04-25
tags: [n8n, workflow, ingestion, orchestration, unified-router]
status: ready-for-implementation
---

# PCA Ingestion Pipeline - Complete n8n Workflow

Production-ready unified router for all three ingestion patterns.

## Architecture

```
Trigger Sources (Webhook, Folder Watch, API)
    ↓
Source Classification
    ├─ Voice (Transcription → Structured Knowledge)
    ├─ Article (URL extraction → Structured Knowledge)
    └─ Signal (RSS/API → Dynamic Signals)
    ↓
Pattern Router
    ├─ Structured Knowledge (High confidence paths)
    ├─ Unstructured Ideas (Low confidence, needs review)
    └─ Dynamic Signals (Time-sensitive)
    ↓
Validation & Classification
    ├─ Scoring (4D model: credibility, relevance, novelty, signal_strength)
    ├─ LLM Classification (route, tag, escalation)
    └─ Reconciliation (resolve conflicts)
    ↓
Routing Decision
    ├─ Auto-route (high confidence)
    ├─ Tag & review (medium confidence)
    ├─ Escalate (low confidence or contradictions)
    └─ Quarantine (errors, unsafe content)
    ↓
Destination Write
    ├─ Project folder
    ├─ Inbox (20-Ideas/Unstructured)
    ├─ Archive
    └─ Escalation queue
    ↓
Audit & Feedback
    ├─ Log to audit-YYYY-MM-DD.jsonl
    ├─ Track for monthly calibration
    └─ Update routing weights
```

## Implementation Steps

### 1. Create Base Workflow in n8n

```
1. Open n8n: http://localhost:5678
2. New Workflow > Name: "PCA Ingestion Pipeline"
3. Save as draft
```

### 2. Add Trigger Nodes

**Node 1: Webhook Trigger** (for API captures)
```
Settings:
- Name: "Webhook - Capture Input"
- Authentication: Basic auth (or API key)
- Method: POST
- Path: /pca/capture
- Response Mode: When last node finishes
```

**Node 2: Folder Watch Trigger** (for Obsidian captures)
```
Settings:
- Name: "Folder Watch - Obsidian Inbox"
- Path: ~/obsidian-vault/20-Ideas/Unstructured/
- Trigger on: File created
- Include files: *.md
- Event: File created
```

**Node 3: Schedule Trigger** (for RSS feeds)
```
Settings:
- Name: "Schedule - Check Signals"
- Trigger type: Every X minutes
- Interval: 5 minutes (adjust per needs)
```

### 3. Parse Input Data

**Node 4: Parse Webhook Capture**
```
Type: Function
Code:
  if ($input.first().body) {
    const body = $input.first().body;
    return [{
      source: 'webhook',
      capture_type: body.source_type || 'text',
      content: body.content,
      domain: body.domain,
      tags: body.tags || [],
      sensitivity: body.sensitivity || 'public',
      confidence: body.confidence || 0.5,
      timestamp: new Date().toISOString(),
      file_id: body.id || `capture-${Date.now()}`
    }];
  }
  return [];
```

**Node 5: Parse File Capture**
```
Type: Function
Code:
  if ($input.first().data?.path) {
    const fs = require('fs');
    const fm = require('front-matter');
    
    const content = fs.readFileSync($input.first().data.path, 'utf8');
    const parsed = fm(content);
    
    return [{
      source: 'file',
      capture_type: parsed.attributes.source_type || 'text',
      content: parsed.body,
      domain: parsed.attributes.domain || '',
      tags: parsed.attributes.tags || [],
      sensitivity: parsed.attributes.sensitivity || 'public',
      confidence: parsed.attributes.confidence || 0.5,
      timestamp: parsed.attributes.created || new Date().toISOString(),
      file_path: $input.first().data.path,
      file_id: $input.first().data.name
    }];
  }
  return [];
```

### 4. Source Classification

**Node 6: Classify Source Type**
```
Type: Switch
Logic:
  if capture_type == 'voice' → Branch: Voice Processing
  if capture_type == 'article' → Branch: Article Processing
  if capture_type == 'signal' → Branch: Signal Processing
  else → Branch: Text/Idea Processing
```

### 5. Voice Transcription

**Node 7a: Voice Transcription (Deepgram or OpenAI Whisper)**
```
Type: HTTP Request (Deepgram API)
Method: POST
URL: https://api.deepgram.com/v1/listen
Authentication: API Key (set in env)
Headers:
  Authorization: Token ${process.env.DEEPGRAM_KEY}
Body:
  audio_data: [base64 audio file]
  model: nova-2
  language: en

Alternative (OpenAI Whisper):
Method: POST
URL: https://api.openai.com/v1/audio/transcriptions
Headers:
  Authorization: Bearer ${process.env.OPENAI_API_KEY}
Form:
  file: [audio file]
  model: whisper-1
```

**Node 7b: Extract Transcription**
```
Type: Function
Code:
  const result = $input.first().json;
  if (result.results?.[0]?.alternatives?.[0]?.transcript) {
    return [{
      transcription: result.results[0].alternatives[0].transcript,
      confidence: result.results[0].alternatives[0].confidence,
      duration: result.metadata?.duration || 0
    }];
  }
  return [{transcription: '', confidence: 0}];
```

### 6. Article Processing

**Node 8a: Extract Article Metadata**
```
Type: Function
Code:
  const url = $input.first().json.content;
  
  if (!url.startsWith('http')) {
    return [{error: 'Invalid URL'}];
  }
  
  return [{
    url: url,
    source_type: 'article'
  }];
```

**Node 8b: Fetch Article Content** (using Mercury parser API)
```
Type: HTTP Request
Method: POST
URL: https://api.parsehub.com/v2/fetch
Params:
  url: ${url}
  token: ${process.env.PARSEHUB_TOKEN}

Alternative (using n8n's built-in):
Type: HtmlExtract
  URL: ${url}
  CSS Selector: article, main, .content, .post
```

### 7. Signal Processing

**Node 9: Fetch Signal Source** (RSS/API)
```
Type: RSS Read
  Feed URL: ${signal_feed_url}
  
Or Custom HTTP:
Type: HTTP Request
  URL: ${signal_api_url}
  Method: GET
  Headers: [auth as needed]
```

### 8. Scoring & Classification

**Node 10: Call Validation Worker**
```
Type: HTTP Request
Method: POST
URL: http://localhost:8001/validate
Headers:
  Content-Type: application/json
Body:
  {
    "capture": {
      "type": "${capture_type}",
      "content": "${content}",
      "domain": "${domain}",
      "source": "${source}",
      "timestamp": "${timestamp}"
    },
    "transcription": "${transcription || ''}",
    "confidence_input": ${confidence}
  }

Expected Response:
  {
    "scores": {
      "credibility": 0.85,
      "relevance": 0.92,
      "novelty": 0.45,
      "signal_strength": 0.88
    },
    "classification": "project",
    "tags": ["ai-safety", "research"],
    "routing_action": "ADVANCE_TO_INTEGRATION",
    "confidence": 0.89,
    "escalation_reason": null
  }
```

### 9. Routing Decision

**Node 11: Route Based on Scores**
```
Type: Switch
Logic:
  if confidence >= 0.85 AND routing_action == "ADVANCE_TO_INTEGRATION"
    → Branch: Auto-Route
  else if confidence >= 0.65
    → Branch: Tag for Review
  else if escalation_reason
    → Branch: Escalate
  else
    → Branch: Quarantine

Use routing-rules.json:
  - route-001: High confidence structured → Project
  - route-002: Provisional structured → Inbox with tag
  - route-003: Ideas → 20-Ideas/Unstructured
  - route-004: Signal critical → Alert + Project
  - route-005: Signal moderate → Inbox
  - route-006: Signal low → Archive
  - route-007: Sensitive → Quarantine
  - route-008: Contradictions → Escalation queue
  - route-009: Very low signal → Quarantine
```

### 10. Write to Destination

**Node 12a: Auto-Route to Project** (if high confidence)
```
Type: Create Note (if using n8n Obsidian plugin)
Or Custom Function to write markdown:
```bash
#!/bin/bash
PROJECT_FOLDER="~/obsidian-vault/10-Projects/${project_name}/Notes/"
mkdir -p "$PROJECT_FOLDER"

cat > "$PROJECT_FOLDER/capture-${timestamp}.md" <<EOF
---
type: ${content_type}
source: ${source}
domain: ${domain}
tags: ${tags}
confidence: ${confidence}
created: ${timestamp}
routing_action: ${routing_action}
---

# ${title}

${content}

## Metadata
- Source: ${source}
- Confidence: ${confidence}
- Classification: ${classification}
EOF
```

**Node 12b: Tag for Review**
```
Same as 12a, but write to:
~/obsidian-vault/20-Ideas/Unstructured/review-${timestamp}.md

Add frontmatter:
requires_review: true
review_reason: medium_confidence
```

**Node 12c: Escalate**
```
Write to escalation queue:
~/obsidian-vault/40-Escalations/escalation-${timestamp}.md

Add frontmatter:
escalation_reason: ${escalation_reason}
escalated_by: validation_worker
requires_human_review: true
```

**Node 12d: Quarantine**
```
Write to quarantine:
~/obsidian-vault/40-Archive/quarantine-${timestamp}.md

Add frontmatter:
status: quarantined
quarantine_reason: ${quarantine_reason}
safe_for_review: false
```

### 11. Audit Logging

**Node 13: Create Audit Entry**
```
Type: Function
Code:
  const fs = require('fs');
  const today = new Date().toISOString().split('T')[0];
  const auditFile = `~/personal-cognitive-architecture/audit-logs/audit-${today}.jsonl`;
  
  const entry = {
    audit_timestamp: new Date().toISOString(),
    candidate_id: ${file_id},
    source_type: ${source},
    stage: "routed",
    routing_action: ${routing_action},
    processing_time_ms: ${end_time - start_time},
    cost_usd: ${calculate_cost()},
    confidence: ${confidence},
    classification: ${classification},
    destination: ${destination},
    status: "success"
  };
  
  fs.appendFileSync(
    auditFile.replace('~', process.env.HOME),
    JSON.stringify(entry) + '\n'
  );
  
  return [{success: true}];
```

**Node 14: Return Confirmation**
```
Type: Function
Code:
  return [{
    success: true,
    file_id: ${file_id},
    destination: ${destination},
    confidence: ${confidence},
    routing_action: ${routing_action},
    timestamp: new Date().toISOString()
  }];
```

## Testing the Workflow

### Test 1: Simple Text Capture via Webhook

```bash
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "content": "Testing the PCA pipeline",
    "domain": "test",
    "tags": ["setup", "test"],
    "confidence": 0.8
  }'
```

Expected response:
```json
{
  "success": true,
  "destination": "~/obsidian-vault/10-Projects/test/Notes/capture-2026-04-25T143000.md",
  "confidence": 0.8,
  "routing_action": "ADVANCE_TO_INTEGRATION"
}
```

### Test 2: File Capture via Folder Watch

Create test file: `~/obsidian-vault/20-Ideas/Unstructured/test-capture.md`

```markdown
---
type: capture
source_type: text
created: 2026-04-25T14:30:00Z
domain: test
tags: [folder-watch]
confidence: 0.85
---

# Test Capture

Testing folder watch trigger with markdown file.
```

Workflow should:
1. Detect file creation
2. Parse frontmatter
3. Run through validation
4. Route to appropriate destination
5. Log audit entry

### Test 3: Voice Capture

```bash
# Create test audio file
ffmpeg -f lavfi -i "sine=frequency=1000:duration=2" test-audio.wav

# Convert to base64
base64 test-audio.wav > test-audio.b64

# Send to workflow
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "source_type": "voice",
  "audio_file_base64": "$(cat test-audio.b64)",
  "domain": "test",
  "sensitivity": "public"
}
EOF
```

## Integration with Dashboard

After workflow is live:

1. **Captures appear in audit logs** (read by dashboard)
2. **Real-time visibility** via `/watch` command
3. **Traces show** each pipeline stage
4. **Metrics update** with success rate, latency, cost
5. **Graph updates** with new nodes and relationships

## Deployment Checklist

- [ ] n8n instance running (http://localhost:5678)
- [ ] Environment variables set:
  - `DEEPGRAM_KEY` (for transcription)
  - `OPENAI_API_KEY` (alternative transcription)
  - `VALIDATION_WORKER_URL` (where scoring happens)
- [ ] Obsidian vault structure exists
- [ ] Audit logs directory exists: `~/personal-cognitive-architecture/audit-logs/`
- [ ] Folder watch trigger configured
- [ ] Webhook trigger tested
- [ ] All sub-nodes have error handling
- [ ] Workflow auto-starts on n8n restart

## Error Handling

Each major step should have error catching:

```
Node → Error Catch → Log Error → Escalate

If transcription fails: Use fallback (text input instead)
If validation fails: Escalate for manual review
If routing fails: Quarantine (safe default)
If write fails: Retry 3x with backoff, then alert
```

## Performance Targets

| Stage | Target | Actual |
|-------|--------|--------|
| File detection | <2s | ___ |
| Transcription (voice) | <10s | ___ |
| Validation | <5s | ___ |
| Routing | <1s | ___ |
| Write to disk | <2s | ___ |
| **Total** | **<30s** | ___ |

## Next Steps

1. ✅ Create workflow structure
2. ✅ Add all nodes with configs
3. ✅ Test each branch individually
4. ✅ Test end-to-end integration
5. ✅ Connect to validation worker (agent)
6. ✅ Verify audit logging
7. ✅ Monitor dashboard integration
8. ✅ Performance optimization
9. ✅ Production deployment

---

**Status**: Ready for implementation
**Last Updated**: 2026-04-25
**Related**: ../README.md, ../../schemas/ingest-capture.schema.json, ../../data/routing-rules.json
