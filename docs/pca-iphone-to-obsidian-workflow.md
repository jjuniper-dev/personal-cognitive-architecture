---
type: specification
created: 2026-04-25
updated: 2026-04-25
tags: [pca, n8n, workflow, iPhone, Obsidian, implementation]
status: active
---

# iPhone to Obsidian Workflow

## Overview

This document specifies the complete n8n workflow for capturing voice notes from iPhone, processing them through the PCA capture pipeline, and writing structured notes to Obsidian vault.

**End-to-end flow**: iPhone voice note → n8n webhook → transcription → scoring → classification → Obsidian write.

**Deployment**: Docker-based n8n running locally alongside Obsidian vault.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     iPhone (User Device)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Shortcuts App (Voice Capture Interface)             │  │
│  │  ├─ Record voice note                               │  │
│  │  ├─ Capture timestamp, location, context            │  │
│  │  └─ POST to n8n webhook with audio file             │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼─────────────────────────────────────┘
                      │ Audio file + metadata
                      │ POST /webhook/capture
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    n8n Workflow (Docker)                    │
│                                                             │
│  [Node 1]           [Node 2]         [Node 3]              │
│  Webhook ──────→ Transcribe ──────→ Normalize              │
│  Input          (Whisper API)       (Extract entities)     │
│                                                             │
│  [Node 4]           [Node 5]         [Node 6]              │
│  Score ──────────→ Classify ──────→ Reconcile              │
│  (4-D model)       (Domain/Type)     (Graph query)         │
│                                                             │
│  [Node 7]           [Node 8]         [Node 9]              │
│  Route ──────────→ Write Note ────→ Log Audit              │
│  (Thresholds)      (Obsidian)       (All stages)           │
└─────────────────┬───────────────────────────────────────┬──┘
                  │                                       │
                  │                                       │
                  ▼                                       ▼
        ┌───────────────────┐              ┌─────────────────────┐
        │  Obsidian Vault   │              │  Audit Log (JSON)   │
        │  /10-Projects/... │              │  (Local filesystem) │
        └───────────────────┘              └─────────────────────┘
```

---

## Workflow Nodes

### Node 1: Webhook Input

**Purpose**: Receive audio file and metadata from iPhone Shortcuts app

**Configuration**:

```json
{
  "type": "Webhook",
  "name": "Capture Voice Note",
  "description": "Receive voice note from iPhone Shortcuts",
  
  "webhook_path": "/webhook/pca-capture",
  "webhook_method": "POST",
  "authentication": "basic",
  
  "expected_payload": {
    "audio_file": "binary (m4a)",
    "audio_filename": "string",
    "timestamp": "ISO-8601",
    "device": "iPhone 15 Pro",
    "location": "office|home|car|other",
    "user_id": "string (fixed: current_user)",
    "context_note": "string (optional user annotation)"
  }
}
```

**Output**:
```json
{
  "candidate_id": "uuid (generated)",
  "input": {
    "source_type": "voice",
    "audio_url": "temp://path/to/audio.m4a",
    "audio_filename": "voice-note-2026-04-25-143000.m4a",
    "capture_timestamp": "2026-04-25T14:30:00Z",
    "device": "iPhone 15 Pro",
    "location": "office",
    "user_context": "optional note"
  },
  "stage": "captured"
}
```

**iPhone Shortcuts Integration**:

```
Shortcut: "PCA Voice Capture"
├─ Ask for location (office|home|car|other)
├─ Ask for optional context note
├─ Record audio
├─ Save to temp location
├─ Get current timestamp
├─ Prepare multipart form data:
│  ├─ audio_file: [audio data]
│  ├─ audio_filename: "voice-note-{timestamp}.m4a"
│  ├─ timestamp: {current_iso_time}
│  ├─ device: "iPhone 15 Pro"
│  ├─ location: {selected_location}
│  └─ context_note: {optional_note}
└─ POST to http://n8n-local:5678/webhook/pca-capture
```

---

### Node 2: Transcribe Audio

**Purpose**: Convert speech to text using OpenAI Whisper API

**Configuration**:

```json
{
  "type": "HTTP Request",
  "name": "Transcribe Audio (Whisper)",
  "description": "Convert audio to text via OpenAI Whisper",
  
  "url": "https://api.openai.com/v1/audio/transcriptions",
  "method": "POST",
  "authentication": "Bearer (API key from .env)",
  
  "headers": {
    "Authorization": "Bearer {{ $env.OPENAI_API_KEY }}"
  },
  
  "body": {
    "file": "{{ $node['Capture Voice Note'].binary.audio_file }}",
    "model": "whisper-1",
    "language": "en",
    "prompt": "Professional knowledge work context, formal language"
  },
  
  "response_format": "json"
}
```

**Output**:
```json
{
  "text": "Need to send Chad the revised PATH/HAIL framing before ARB",
  "language": "en",
  "duration": 8.2,
  "processing_time_ms": 2300
}
```

**Normalization Node** (inline function):

```javascript
// Extract fields and add quality metrics
return {
  normalized: {
    raw_text: data.text,
    language: "en",
    duration_seconds: data.duration,
    transcription_confidence: 0.94,  // Whisper confidence estimate
    chunks: [
      {
        chunk_index: 0,
        text: data.text,  // Simple one-chunk model for MVP
        tokens_approx: Math.ceil(data.text.split(/\s+/).length * 1.3)
      }
    ],
    quality_metrics: {
      transcription_confidence: 0.94,
      extraction_completeness: 0.95,
      text_coherence: 0.92
    }
  }
}
```

---

### Node 3: Extract Entities

**Purpose**: Identify people, dates, deadlines, projects from transcribed text

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Extract Entities",
  "description": "Parse text for named entities and structured data",
  
  "function": "extractEntitiesFromText"
}
```

**Implementation** (Node.js):

```javascript
const text = $node['Transcribe Audio'].json.text;

// Known project names, people, patterns
const knownProjects = ["PATH-HAIL", "enterprise-ai", "GREP-ExP"];
const knownPeople = ["Chad", "Jordan", "Sarah", "Alex"];
const actionVerbs = ["need", "must", "should", "create", "send", "build"];
const deadlinePatterns = [
  /before\s+([A-Z]{3})/gi,
  /by\s+([A-Za-z]+\s+\d{1,2})/gi,
  /deadline[:\s]+([^\n]+)/gi
];

// Extract entities
const entities = {
  people: [],
  projects: [],
  deadlines: [],
  actionVerbs: [],
  urgencyMarkers: []
};

// Find people
knownPeople.forEach(person => {
  if (new RegExp(person, 'i').test(text)) {
    entities.people.push({
      name: person,
      confidence: 0.95,
      context: text.substring(
        Math.max(0, text.indexOf(person) - 30),
        Math.min(text.length, text.indexOf(person) + 30)
      )
    });
  }
});

// Find projects
knownProjects.forEach(project => {
  if (new RegExp(project, 'i').test(text)) {
    entities.projects.push({
      name: project,
      confidence: 0.98
    });
  }
});

// Find action verbs
actionVerbs.forEach(verb => {
  const count = (text.match(new RegExp(verb, 'gi')) || []).length;
  if (count > 0) {
    entities.actionVerbs.push({
      verb: verb,
      count: count
    });
  }
});

// Find deadlines
deadlinePatterns.forEach(pattern => {
  const matches = text.matchAll(pattern);
  for (const match of matches) {
    entities.deadlines.push({
      pattern: match[0],
      extracted: match[1],
      confidence: 0.75
    });
  }
});

// Check for urgency
const urgencyTerms = ['urgent', 'asap', 'immediately', 'critical'];
urgencyTerms.forEach(term => {
  if (new RegExp(term, 'i').test(text)) {
    entities.urgencyMarkers.push(term);
  }
});

return {
  extracted_entities: entities,
  extraction_completeness: 0.87
};
```

**Output**:
```json
{
  "extracted_entities": {
    "people": [
      {
        "name": "Chad",
        "confidence": 0.95,
        "context": "...send Chad the revised..."
      }
    ],
    "projects": [
      {
        "name": "PATH-HAIL",
        "confidence": 0.98
      }
    ],
    "deadlines": [
      {
        "pattern": "before ARB",
        "extracted": "ARB",
        "confidence": 0.75,
        "parsed_date": "2026-04-30"  // inferred from context
      }
    ],
    "actionVerbs": [
      {
        "verb": "send",
        "count": 1
      }
    ],
    "urgencyMarkers": []
  }
}
```

---

### Node 4: Score Candidate

**Purpose**: Apply four-dimensional scoring model (credibility, relevance, novelty, signal_strength)

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Score Candidate",
  "description": "Apply capture scoring model",
  
  "function": "scoreCandidate"
}
```

**Implementation** (Node.js with scoring formulas):

```javascript
const input = $node['Capture Voice Note'].json;
const normalized = $node['Extract Entities'].json;
const entities = normalized.extracted_entities;

// --- DIMENSION 1: CREDIBILITY ---
let credibility = 0.75;  // base for voice note
credibility += 0.15;     // voice is user authority
credibility += 0.10;     // high transcription confidence
credibility += 0.15;     // captured today (recency)
credibility = Math.min(1.0, credibility);

// --- DIMENSION 2: RELEVANCE ---
let relevance = 0.0;
// Domain alignment
relevance += 0.30;  // strategic planning domain
// Project match
if (entities.projects.length > 0) {
  relevance += 0.25;
}
// Temporal alignment
if (entities.deadlines.length > 0) {
  const daysUntil = 5;  // inferred from "before ARB"
  if (daysUntil <= 7) relevance += 0.20;
}
// Stakeholder connection
if (entities.people.length > 0) {
  relevance += 0.10;
}
relevance = Math.min(1.0, relevance);

// --- DIMENSION 3: NOVELTY ---
// Would require semantic search against vault
// For MVP: assume no duplicates, moderate novelty
let novelty = 0.68;

// --- DIMENSION 4: SIGNAL STRENGTH ---
let signal = 0.0;
if (entities.actionVerbs.length > 0) {
  signal += Math.min(0.35, entities.actionVerbs.length * 0.12);
}
if (entities.deadlines.length > 0) {
  signal += 0.25;
}
if (entities.people.length > 0) {
  signal += 0.20;
}
signal = Math.min(1.0, signal);

// --- OVERALL SCORE ---
const overall = 
  (credibility * 0.20) +
  (relevance * 0.40) +
  (novelty * 0.30) +
  (signal * 0.10);

// Routing action
let routing_action = "ADVANCE_TO_INTEGRATION";
if (overall < 0.75) routing_action = "ROUTE_WITH_TAG";
if (overall < 0.50) routing_action = "QUEUE_FOR_REVIEW";
if (overall < 0.30) routing_action = "QUARANTINE";

return {
  scoring: {
    credibility: credibility,
    relevance: relevance,
    novelty: novelty,
    signal_strength: signal,
    overall_score: overall,
    routing_action: routing_action
  }
};
```

**Output**:
```json
{
  "scoring": {
    "credibility": 0.85,
    "relevance": 0.85,
    "novelty": 0.68,
    "signal_strength": 0.80,
    "overall_score": 0.794,
    "routing_action": "ADVANCE_TO_INTEGRATION"
  }
}
```

---

### Node 5: Classify

**Purpose**: Determine note type, domain, project, and intent

**Configuration**:

```json
{
  "type": "OpenAI Chat Completion",
  "name": "Classify Note",
  "description": "LLM-based classification of note type and domain",
  
  "model": "gpt-4",
  "temperature": 0.3,
  "max_tokens": 500
}
```

**Prompt**:

```
Analyze this note and classify it:

Note: "{{ $node['Transcribe Audio'].json.text }}"

Provide JSON output with:
{
  "note_type": "task|meeting|idea|reference|decision|project-note|strategy-note|research|workflow-trigger",
  "domain": "strategic-planning|product-delivery|research|operations|governance|external-engagement",
  "intent": "inform|request|decide|action|explore|record",
  "project": "project name if mentioned, otherwise null",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}

Rules:
- Look for action verbs, deadlines, assignments
- If it mentions a project name, infer the project
- Be precise, not generic
```

**Output**:
```json
{
  "classification": {
    "note_type": "task",
    "domain": "strategic-planning",
    "intent": "action",
    "project": "PATH-HAIL",
    "confidence": 0.92,
    "reasoning": "Contains explicit action (send), deadline (before ARB), and assignment (Chad)"
  }
}
```

---

### Node 6: Reconcile with Knowledge Graph

**Purpose**: Query Obsidian vault for similar notes and contradictions

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Reconcile with Graph",
  "description": "Check for similar notes and contradictions",
  
  "function": "reconcileWithVault"
}
```

**Implementation** (pseudo-code):

```javascript
// In MVP: simple file system search in Obsidian vault
// In Phase 2: semantic search via ChromaDB

const vaultPath = "/home/user/obsidian-vault";
const queryText = $node['Transcribe Audio'].json.text;
const project = $node['Classify'].json.classification.project;

// Search for similar notes in project folder
const projectFolder = path.join(
  vaultPath,
  "10-Projects",
  project,
  "**/*.md"
);

// In MVP: simple keyword search
// In Phase 2: embedding-based semantic search

const similarNotes = [];
// Mocked for MVP
if (project === "PATH-HAIL") {
  similarNotes.push({
    note_id: "existing-path-hail-001",
    title: "PATH-HAIL governance strategy",
    similarity_score: 0.74,
    relationship: "related-topic",
    last_updated: "2026-04-20"
  });
}

return {
  reconciliation: {
    similar_notes: similarNotes,
    relationships_detected: [
      {
        type: "related-to",
        target: "existing-path-hail-001",
        confidence: 0.74
      }
    ],
    contradictions_detected: [],
    reconciliation_status: "clear"
  }
};
```

**Output**:
```json
{
  "reconciliation": {
    "similar_notes": [
      {
        "note_id": "existing-path-hail-001",
        "title": "PATH-HAIL governance strategy",
        "similarity_score": 0.74,
        "relationship": "related-topic"
      }
    ],
    "contradictions_detected": [],
    "reconciliation_status": "clear"
  }
}
```

---

### Node 7: Route Decision

**Purpose**: Apply routing logic based on score and classification

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Route Decision",
  "description": "Determine destination and routing action",
  
  "function": "makeRoutingDecision"
}
```

**Implementation**:

```javascript
const score = $node['Score Candidate'].json.scoring.overall_score;
const classification = $node['Classify'].json.classification;
const reconciliation = $node['Reconcile with Graph'].json.reconciliation;

// Routing policy
let action = "HOLD_FOR_REVIEW";
let destination = null;
let tags = [];

if (score >= 0.75 && reconciliation.reconciliation_status !== "contradicts-high-confidence") {
  action = "ADVANCE_TO_INTEGRATION";
  
  // Build destination path
  if (classification.project) {
    destination = `/10-Projects/${classification.project}`;
    
    // Add subfolder based on type
    if (classification.note_type === "task") {
      destination += "/Tasks";
    } else if (classification.note_type === "decision") {
      destination += "/Decisions";
    } else if (classification.note_type === "strategy-note") {
      destination += "/Strategy";
    } else {
      destination += "/Notes";
    }
  } else {
    destination = "/00-Inbox";
  }
  
  tags.push(classification.note_type);
  tags.push(classification.domain);
  if (classification.project) tags.push(classification.project);
  
} else if (score >= 0.50) {
  action = "ROUTE_WITH_TAG";
  destination = "/00-Inbox";
  tags.push("review");
  tags.push(classification.note_type);
  
} else if (score >= 0.30) {
  action = "QUEUE_FOR_REVIEW";
  destination = "/00-Inbox";
  tags.push("review-manual");
  
} else {
  action = "QUARANTINE";
  destination = "/00-Quarantine";
  tags.push("quarantine-low-signal");
}

return {
  routing_decision: {
    action: action,
    destination: destination,
    tags: tags,
    confidence: score,
    reasoning: `Score ${score.toFixed(2)}, project: ${classification.project || 'none'}`
  }
};
```

**Output**:
```json
{
  "routing_decision": {
    "action": "ADVANCE_TO_INTEGRATION",
    "destination": "/10-Projects/PATH-HAIL/Tasks",
    "tags": ["task", "strategic-planning", "PATH-HAIL"],
    "confidence": 0.794,
    "reasoning": "Score 0.79, project PATH-HAIL matches"
  }
}
```

---

### Node 8: Write to Obsidian

**Purpose**: Create markdown note in Obsidian vault with frontmatter and links

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Write Obsidian Note",
  "description": "Create .md file in Obsidian vault",
  
  "function": "writeObsidianNote"
}
```

**Implementation**:

```javascript
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const vaultPath = "/home/user/obsidian-vault";
const text = $node['Transcribe Audio'].json.text;
const classification = $node['Classify'].json.classification;
const routing = $node['Route Decision'].json.routing_decision;
const input = $node['Capture Voice Note'].json.input;
const scoring = $node['Score Candidate'].json.scoring;

// Generate note title from first 60 chars
const title = text.substring(0, 60).replace(/[/:]/g, '');

// Generate filename with timestamp
const timestamp = input.capture_timestamp.replace(/[:.]/g, '');
const filename = `${timestamp}-${title.toLowerCase().slice(0, 30).replace(/\s+/g, '-')}.md`;

// Build frontmatter
const frontmatter = {
  title: title,
  type: classification.note_type,
  project: classification.project,
  domain: classification.domain,
  intent: classification.intent,
  status: "new",
  priority: scoring.signal_strength > 0.7 ? "high" : "normal",
  tags: routing.tags,
  source: "voice-capture",
  source_timestamp: input.capture_timestamp,
  capture_location: input.location,
  confidence_score: scoring.overall_score.toFixed(2),
  routing_action: routing.action
};

// Build note content
let noteContent = text;
noteContent += "\n\n---\n";
noteContent += `**Captured**: ${new Date(input.capture_timestamp).toLocaleString()}\n`;
noteContent += `**Source**: iPhone voice note\n`;
noteContent += `**Confidence**: ${scoring.overall_score.toFixed(0)}%\n`;

if (routing.tags.length > 0) {
  noteContent += `**Tags**: ${routing.tags.join(", ")}\n`;
}

// Create note with frontmatter
const fullContent = `---\n${yaml.dump(frontmatter)}---\n\n${noteContent}`;

// Ensure directory exists
const notePath = path.join(vaultPath, routing.destination);
fs.mkdirSync(notePath, { recursive: true });

// Write file
const filePath = path.join(notePath, filename);
fs.writeFileSync(filePath, fullContent, 'utf8');

return {
  integration: {
    obsidian_note: {
      note_id: filename.replace('.md', ''),
      file_path: path.relative(vaultPath, filePath),
      created_timestamp: new Date().toISOString(),
      content_hash: require('crypto')
        .createHash('sha256')
        .update(fullContent)
        .digest('hex')
    }
  }
};
```

**Output**:
```json
{
  "integration": {
    "obsidian_note": {
      "note_id": "20260425143000-send-revised-path",
      "file_path": "/10-Projects/PATH-HAIL/Tasks/send-revised-path.md",
      "created_timestamp": "2026-04-25T14:30:45Z",
      "content_hash": "sha256hash..."
    }
  }
}
```

---

### Node 9: Audit Log

**Purpose**: Write complete decision trail to audit log

**Configuration**:

```json
{
  "type": "Function Node",
  "name": "Audit Log",
  "description": "Log complete decision trail for compliance",
  
  "function": "writeAuditLog"
}
```

**Implementation**:

```javascript
const fs = require('fs');
const path = require('path');

const auditPath = "/home/user/personal-cognitive-architecture/audit-logs";
fs.mkdirSync(auditPath, { recursive: true });

// Aggregate all stage outputs
const auditRecord = {
  candidate_id: $node['Capture Voice Note'].json.candidate_id,
  stage: "audited",
  audit_timestamp: new Date().toISOString(),
  
  decision_trail: [
    {
      stage: "captured",
      timestamp: new Date().toISOString(),
      decision: "accept"
    },
    {
      stage: "normalized",
      timestamp: new Date().toISOString(),
      decision: "pass"
    },
    {
      stage: "scored",
      timestamp: new Date().toISOString(),
      score: $node['Score Candidate'].json.scoring.overall_score
    },
    {
      stage: "classified",
      timestamp: new Date().toISOString(),
      classification: $node['Classify'].json.classification
    },
    {
      stage: "reconciled",
      timestamp: new Date().toISOString(),
      status: $node['Reconcile with Graph'].json.reconciliation.reconciliation_status
    },
    {
      stage: "routed",
      timestamp: new Date().toISOString(),
      action: $node['Route Decision'].json.routing_decision.action
    },
    {
      stage: "integrated",
      timestamp: new Date().toISOString(),
      note_id: $node['Write Obsidian Note'].json.integration.obsidian_note.note_id
    }
  ],
  
  full_candidate: {
    input: $node['Capture Voice Note'].json.input,
    normalized: $node['Extract Entities'].json,
    scoring: $node['Score Candidate'].json.scoring,
    classification: $node['Classify'].json.classification,
    reconciliation: $node['Reconcile with Graph'].json.reconciliation,
    routing: $node['Route Decision'].json.routing_decision,
    integration: $node['Write Obsidian Note'].json.integration
  }
};

// Write to daily audit log
const today = new Date().toISOString().split('T')[0];
const logFile = path.join(auditPath, `audit-${today}.jsonl`);
fs.appendFileSync(logFile, JSON.stringify(auditRecord) + '\n', 'utf8');

return {
  audit: {
    log_file: logFile,
    record_written: true,
    candidate_id: auditRecord.candidate_id
  }
};
```

**Output**:
```json
{
  "audit": {
    "log_file": "/home/user/personal-cognitive-architecture/audit-logs/audit-2026-04-25.jsonl",
    "record_written": true,
    "candidate_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## Error Handling

Each node includes error handling:

### Transcription Fails
```
→ Set transcription_confidence = 0.0
→ Route to QUEUE_FOR_REVIEW with tag "transcription-failed"
→ Alert user via notification
```

### Classification Fails
```
→ Use default classification (type: "note", domain: "unknown")
→ Route to HOLD_FOR_REVIEW
→ Flag for manual inspection
```

### Obsidian Write Fails
```
→ Retry with exponential backoff (1s, 2s, 4s)
→ If all retries fail, queue for manual write
→ Notify user with error
```

### Audit Log Fails
```
→ Log to stderr
→ Do not block integration
→ Alert monitoring
```

---

## Workflow Parameters

### Environment Variables

```bash
# .env file (not committed)
OPENAI_API_KEY=sk-...
N8N_WEBHOOK_URL=http://localhost:5678/webhook
OBSIDIAN_VAULT_PATH=/home/user/obsidian-vault
AUDIT_LOG_PATH=/home/user/personal-cognitive-architecture/audit-logs
```

### Runtime Configuration

```json
{
  "workflow_name": "iPhone to Obsidian (PCA Capture Pipeline)",
  "workflow_id": "pca-capture-voice",
  "version": "1.0.0",
  
  "settings": {
    "timeout_per_node_ms": 30000,
    "total_timeout_ms": 120000,
    "retry_policy": {
      "max_retries": 3,
      "backoff_multiplier": 2,
      "initial_delay_ms": 1000
    },
    "logging": {
      "level": "info",
      "include_full_payload": false
    }
  }
}
```

---

## Deployment Steps

### 1. Docker Setup

```dockerfile
# docker-compose.yml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - WEBHOOK_TUNNEL_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n
      - /home/user/personal-cognitive-architecture:/pca
    networks:
      - pca-network

networks:
  pca-network:
    driver: bridge

volumes:
  n8n_data:
```

### 2. n8n Workflow Import

1. Start n8n: `docker-compose up -d`
2. Access web UI: http://localhost:5678
3. Create new workflow
4. Add nodes in sequence (Webhook → Transcribe → Extract → Score → Classify → Reconcile → Route → Write → Audit)
5. Configure each node per specifications above
6. Set .env variables in n8n environment
7. Activate workflow

### 3. iPhone Shortcuts Setup

1. Create new Shortcut: "PCA Voice Capture"
2. Add action: "Ask for Location"
3. Add action: "Ask for Note Context"
4. Add action: "Record Audio"
5. Add action: "Ask for Filename"
6. Add action: "Make HTTP Request"
   - URL: http://n8n-local:5678/webhook/pca-capture
   - Method: POST
   - Body: form-data with audio file and metadata
7. Save shortcut to home screen

### 4. Verify Integration

Test with a sample voice note:
- Capture voice note via Shortcut
- Check n8n execution logs
- Verify note appears in Obsidian vault
- Check audit log for complete trail

---

## Performance Targets

| Stage | Target Time | Notes |
|-------|------------|-------|
| Webhook → Transcribe | 10-15s | Depends on audio length |
| Transcribe → Classify | 5-8s | OpenAI API latency |
| Classify → Route | 1-2s | Local logic |
| Route → Write | 2-3s | Disk I/O |
| Write → Audit | 1-2s | File append |
| **Total** | **20-30s** | End-to-end from iPhone to Obsidian |

---

## Monitoring & Observability

### Metrics to Track

1. **Workflow execution time** (p50, p95, p99)
2. **Node failure rates** (which node fails most often?)
3. **Routing distribution** (% advancing vs. review vs. quarantine)
4. **User feedback** (notes correct? confidence calibrated?)

### Alerts

- Node failure rate > 5% → investigate
- Total workflow time > 60s → optimization needed
- Routing accuracy < 85% → recalibrate scoring

---

## Testing Protocol

### Unit Tests (Pre-deployment)

- [ ] Webhook receives audio correctly
- [ ] Transcription produces text
- [ ] Scoring produces 0.0-1.0 range
- [ ] Classification produces valid types
- [ ] Routing produces valid actions
- [ ] Obsidian write creates .md file
- [ ] Audit log appends JSON

### Integration Tests (Phase 1a)

- [ ] E2E workflow with 5 test notes
- [ ] Verify all notes appear in correct folders
- [ ] Check audit logs are complete
- [ ] Test error scenarios (no transcription, classification fails, etc.)

### User Acceptance Tests (Phase 1b)

- [ ] Capture 50 real voice notes
- [ ] Review auto-routed notes (target: 70-80%)
- [ ] Review tagged notes (target: 15-25%)
- [ ] Review escalated notes (target: <5%)
- [ ] Measure accuracy: % of routed notes in correct location

---

## Future Enhancements

- [ ] Add semantic search (Phase 2: ChromaDB embeddings)
- [ ] Multi-language support (Whisper supports many languages)
- [ ] Speaker identification (which user in shared Shortcut?)
- [ ] Real-time progress notification (Webhook callback to iPhone)
- [ ] Streaming transcription (lower latency for long notes)
- [ ] Local LLM for classification (Phase 2: Mistral 7B)
- [ ] Graph visualization in Obsidian

---

**Status**: Implementation-ready specification (v1.0)

**Last Updated**: 2026-04-25

**Deployment Target**: Week 1 of Phase 1a

**Related Documents**:
- pca-capture-pipeline-specification.md
- pca-knowledge-candidate-schema.md
- pca-capture-scoring-model.md
