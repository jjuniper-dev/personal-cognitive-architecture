# n8n Workflows for PCA

## Overview

n8n workflows orchestrate the PCA capture pipeline. This directory contains workflow definitions, stubs, and deployment instructions.

## Architecture Principle

**One unified ingestion router** that:
1. Classifies source type
2. Applies ingest template
3. Validates metadata
4. Applies routing policy
5. Writes to Obsidian
6. Triggers optional processing

Not three separate workflows — one classifier, three routing paths.

## Workflows

### Core Workflows

#### `pca-ingest-loop.json`
**Purpose**: Main orchestration loop
**Trigger**: Webhook from capture source (iPhone, web, email, RSS)
**Flow**:
1. Receive inbound capture (voice, article, signal)
2. Classify source type
3. Apply ingest template
4. Normalize content
5. Score and validate
6. Apply routing rules
7. Write to Obsidian
8. Log to audit trail
9. Emit downstream events (optional)

**Status**: Stub (ready for implementation)

### Supporting Workflows

#### `pca-signal-ingestion.json`
**Purpose**: Scheduled polling of RSS/API feeds
**Trigger**: Scheduled (hourly / every 6 hours)
**Flow**:
1. Poll all enabled feeds (data/signal-sources.json)
2. Deduplicate
3. Normalize
4. Score signals
5. Classify (info/review/alert)
6. Route to appropriate destination
7. Send alerts if CRITICAL

**Status**: Stub

#### `pca-validation-worker.json`
**Purpose**: Optional high-confidence validation step
**Trigger**: Manual or scheduled (for high-impact items)
**Flow**:
1. Get items marked for review
2. Run deep validation (secondary LLM)
3. Compare to primary classification
4. Flag discrepancies
5. Update routing if confidence changes

**Status**: Stub

#### `pca-reconciliation-check.json`
**Purpose**: Knowledge graph reconciliation
**Trigger**: Called by main ingest loop (Stage 5)
**Flow**:
1. Query Obsidian vault for similar notes
2. Detect contradictions
3. Identify relationships
4. Return reconciliation status

**Status**: Stub

#### `pca-feedback-aggregation.json`
**Purpose**: Monthly calibration pipeline
**Trigger**: Scheduled (monthly)
**Flow**:
1. Collect routing decisions from last 30 days
2. Collect user feedback (marks, corrections)
3. Calculate accuracy metrics
4. Identify systematic errors
5. Recommend weight adjustments
6. Generate report

**Status**: Stub

## Deployment

### Prerequisites
- n8n running locally (Docker recommended)
- Obsidian vault accessible via local filesystem
- OpenAI API key (for Phase 1, will be local LLM in Phase 2)
- Credentials file (.env)

### Installation Steps

```bash
# 1. Start n8n
docker-compose up -d n8n

# 2. Access web UI
open http://localhost:5678

# 3. Create workflows
# - Import pca-ingest-loop.json
# - Import signal ingestion workflow
# - Import reconciliation worker

# 4. Configure credentials
# - Add OpenAI API key
# - Set Obsidian vault path
# - Set signal source registry path

# 5. Deploy webhooks
# - Generate webhook URLs
# - Provide to iPhone Shortcuts app
# - Test with sample capture

# 6. Enable scheduling
# - Signal ingestion: hourly
# - Reconciliation: monthly
```

### Configuration Files

All workflows read from data/ and schemas/ directories:

- `data/routing-rules.json` — Routing policy
- `data/signal-sources.json` — RSS/API registry
- `schemas/ingest-capture.schema.json` — Input validation
- `schemas/validation-result.schema.json` — Output validation
- `schemas/signal-score.schema.json` — Signal scoring

This allows workflow logic to be in n8n, policy to be in JSON.

## Workflow Stubs

Stubs are minimal implementations showing the expected flow. Each stub includes:

1. **Input/Output Schema** — what it expects, what it returns
2. **Decision Logic** — conditionals and branching
3. **Error Handling** — what happens if steps fail
4. **Audit Trail** — what gets logged

### Using Stubs

```bash
# 1. Open stub file
vi workflows/n8n/pca-ingest-loop.stub.json

# 2. Copy stub into n8n UI
# Create new workflow → copy stub JSON

# 3. Fill in actual node configurations
# Replace {{VARIABLE}} with actual settings

# 4. Test with sample data
# Use examples from schemas/*.schema.json

# 5. Deploy
# Activate workflow, test with real capture
```

## Node Reference

### Input Nodes

**Webhook (Ingest)**
- Receives captures from iPhone Shortcuts, browser, email
- Input: multipart form data with audio file + metadata
- Output: structured JSON matching ingest-capture.schema.json

**Schedule (Signal Polling)**
- Polls RSS/API feeds on schedule
- Input: signal-sources.json registry
- Output: array of normalized feed items

### Processing Nodes

**Normalize**
- Transcription (Whisper API)
- Text extraction (if PDF)
- Metadata enrichment

**Score**
- Four-dimensional scoring (four separate JavaScript nodes)
- Weighted aggregation
- Output: validation-result.schema.json

**Classify**
- LLM-based classification (GPT-4)
- Domain, type, project, intent
- Output: classification fields in validation-result

**Route**
- Load routing-rules.json
- Evaluate conditions
- Determine destination and action
- Output: routing decision

**Write Obsidian**
- Select template (based on source_type)
- Populate template variables
- Create .md file in destination
- Create frontmatter
- Create relationships/links

**Audit Log**
- Write to audit trail
- Append to daily JSONL file
- Log all decisions and models used

### Output Nodes

**Obsidian Write**
- Creates note file in vault
- Returns: file_path, note_id

**Alert Trigger**
- Push notification
- Email alert
- Slack message
- Conditional on classification

**Event Emitter**
- Emit downstream events (tasks, reviews, etc.)
- Used by other systems to react

## Testing

### Unit Test

```bash
# Test individual node with sample input
curl -X POST http://localhost:5678/webhook/test \
  -H "Content-Type: application/json" \
  -d @schemas/examples/ingest-capture-example.json
```

### Integration Test

```bash
# Test full workflow with sample data
# 1. Create test note in /00-Inbox/Test
# 2. Verify note appears in correct location
# 3. Check audit log entry
# 4. Verify relationships created
```

### Load Test

```bash
# Simulate 50 captures over 1 hour
# Measure: latency, error rate, cost
# Expected: <30s per capture, zero errors, <$0.10 total
```

## Monitoring

### Health Checks

- **Webhook availability**: Does ingest endpoint respond?
- **Obsidian connectivity**: Can n8n write files?
- **API quota**: OpenAI usage vs. budget
- **Signal feed health**: Are feeds updating?

### Metrics

- **Ingest throughput**: Captures per hour
- **Processing latency**: p50, p95, p99
- **Error rate**: Failed captures
- **Routing distribution**: % by action
- **Cost**: Actual vs. budget

### Alerts

- Webhook down (5min threshold)
- Error rate > 5%
- Latency p95 > 60s
- Monthly cost exceeding budget
- Signal feed stale (no items in 2x expected interval)

## Version Control

Workflows are stored as:
- `.json` files (machine-readable)
- Committed to git (version history)
- Deployed via n8n UI

Updating a workflow:
```bash
1. Edit .json file
2. Commit to git
3. Re-import into n8n
4. Test on dev webhook
5. Deploy to production webhook
```

## Next Steps

1. **Phase 1a**: Implement pca-ingest-loop.json (all three pattern types)
2. **Phase 1b**: Deploy signal ingestion (RSS/API polling)
3. **Phase 1c**: Add validation worker and feedback aggregation
4. **Phase 2**: Migrate to local LLM (Mistral 7B)
5. **Phase 3**: Add enterprise connectors (Azure, etc.)

## Related Documentation

- `../docs/pca-iphone-to-obsidian-workflow.md` — Detailed node specifications
- `../data/routing-rules.json` — Routing policy reference
- `../schemas/` — Input/output contract definitions
