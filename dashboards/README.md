---
type: documentation
created: 2026-04-25
updated: 2026-04-25
tags: [pca, dashboard, monitoring, chainlit]
status: active
---

# PCA Operational Dashboard

Real-time visualization of PCA ingestion pipeline using Chainlit.

## Overview

The PCA Dashboard monitors:

- **Agent Activity** — Orchestrator, Capture Worker, Validation Worker, Integration Worker
- **Pipeline Stages** — Each capture flowing through Capture → Normalize → Score → Classify → Reconcile → Route → Write
- **Performance Metrics** — Throughput, latency, cost, accuracy
- **Queue Status** — Pending items, in-progress, escalations
- **Cost Tracking** — Daily spend vs. budget

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Chainlit Web Interface                         │
│  ├─ Real-time traces                           │
│  ├─ Metrics dashboard                          │
│  ├─ Cost breakdown                             │
│  └─ Agent activity summary                     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│  Audit Log Reader                              │
│  ├─ Parse JSONL files                          │
│  ├─ Filter by time/stage/source                │
│  └─ Aggregate metrics                          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│  Audit Logs (audit-YYYY-MM-DD.jsonl)          │
│  ├─ One entry per pipeline stage               │
│  ├─ Timestamped decisions                      │
│  └─ Cost and latency data                      │
└─────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

```bash
pip install chainlit>=0.7.0
```

### Setup

```bash
# 1. Navigate to dashboard directory
cd /path/to/personal-cognitive-architecture/dashboards

# 2. Run Chainlit app
chainlit run chainlit-pca-monitor.py

# 3. Open in browser
# Chainlit UI will appear at http://localhost:8000
```

## Usage

### Available Commands

#### `/status`
Show current queue status and key metrics.

```
Queue Status
├─ Pending: 3 items
├─ In Progress: 1 item
└─ Escalations: 0 items

Today's Summary
├─ Total Captures: 47
├─ Success Rate: 91%
├─ Avg Latency: 12.3ms
└─ Cost: $0.47
```

#### `/traces`
Show last 10 pipeline operations with full details.

```
📥 Captured
├─ ID: 550e8400
├─ Type: voice
├─ Action: ✅ ADVANCE_TO_INTEGRATION
├─ Latency: 23ms
├─ Cost: $0.00
└─ Time: 2026-04-25T14:30:00Z
```

#### `/metrics`
Detailed performance metrics and routing distribution.

```
Queue Status: Pending 3 | In Progress 1 | Escalations 0

Routing Distribution
├─ Auto-Route: 68.1% (32 items) ✅
├─ Review Tag: 23.4% (11 items) 🏷️
├─ Escalate: 4.3% (2 items) ⚠️
└─ Quarantine: 4.3% (2 items) 🚫

Performance
├─ Total Captures: 47
├─ Success Rate: 91.5%
├─ Avg Latency: 12.3ms
├─ Daily Cost: $0.47
└─ Accuracy (Month): 89.2%
```

#### `/cost`
Cost breakdown by operation type.

```
Daily Total: $0.47

By Operation:
├─ Classification: $0.28
├─ Transcription: $0.15
├─ Validation: $0.04
└─ Other: $0.00

Budget: $50.00/month
Estimated Monthly: $14.10
```

#### `/accuracy`
Routing accuracy and calibration metrics.

```
Routing Accuracy: 89.2%

By Pattern:
├─ Structured Knowledge: 92% ✅
├─ Unstructured Ideas: 78% 🟡
└─ Dynamic Signals: 87% ✅

False Positives: 3 (escalated but not needed)
False Negatives: 2 (should have been escalated)
```

#### `/agents`
Agent activity summary showing throughput per agent.

```
Orchestrator (Control Plane)
├─ Routing Decisions: 47
└─ Escalations: 2

Capture Worker (Ingestion)
├─ Captured: 47
└─ Normalized: 47

Validation Worker (Scoring & Classification)
├─ Scored: 47
├─ Classified: 47
└─ Reconciled: 47

Integration Worker (Storage)
├─ Integrated: 45
└─ Triggered: 43
```

#### `/graph`
Interactive knowledge graph visualization of all captured notes and their relationships.

```
🔗 Knowledge Graph (Interactive)

- Nodes: 142
- Relationships: 287

Node Types:
- Note: 89
- Concept: 38
- Person: 15

Tips:
- Drag nodes to move them around
- Click and drag the background to pan
- Scroll to zoom
- Use "Fit to View" to see the entire graph
- Use "Stabilize" to arrange nodes more organically
```

#### `/watch`
Live updates with 5-second auto-refresh for 1 minute.

```
⏱️ Update 1 — 14:30:45
Queue: ⏳ 3 | 🔄 1 | ⚠️ 0
Cost: $0.47 | Success: 91.5%

⏱️ Update 2 — 14:30:50
Queue: ⏳ 2 | 🔄 2 | ⚠️ 0
Cost: $0.48 | Success: 92.0%
```

## Data Sources

### Neo4j Knowledge Graph

The `/graph` command displays an interactive visualization of the PCA knowledge graph stored in Neo4j.

**Setup**:
```bash
# 1. Install Neo4j (Community Edition or higher)
# Visit: https://neo4j.com/download/

# 2. Start Neo4j
neo4j start

# 3. Verify connection
# Dashboard will auto-connect when /graph command is used

# 4. Seed with Obsidian data (optional)
# Use pca-orchestrator agent to sync vault to Neo4j
```

**Graph Structure**:
- **Nodes**: Notes, Concepts, People (extracted from captured content)
- **Relationships**: related-to, depends-on, contradicts, extends
- **Properties**: confidence scores, domains, project tags

**Query Options** (Future):
- Filter by project
- Filter by domain
- Show contradictions only
- Impact analysis (what changes if I update X?)
- Knowledge gaps (what's missing?)

### Audit Logs

The dashboard reads from JSONL audit logs:

**Location**: `../audit-logs/audit-YYYY-MM-DD.jsonl`

**Format** (one entry per line):
```json
{
  "audit_timestamp": "2026-04-25T14:30:00Z",
  "candidate_id": "550e8400-e29b-41d4-a716-446655440000",
  "source_type": "voice",
  "stage": "routed",
  "routing_action": "ADVANCE_TO_INTEGRATION",
  "processing_time_ms": 23,
  "cost_usd": 0.0,
  "confidence": 0.91,
  "destination": "/10-Projects/PATH-HAIL/Tasks",
  "status": "success"
}
```

## Metrics Calculated

### Real-Time Metrics

- **Queue Status**: Pending, in-progress, escalated items
- **Throughput**: Captures per minute (24-hour rolling)
- **Success Rate**: % of successful integrations
- **Average Latency**: Mean processing time
- **Daily Cost**: Total API spend
- **Routing Distribution**: % by action (auto-route, review, escalate, quarantine)

### Accuracy Metrics

- **Overall Accuracy**: % of correct routing decisions
- **Accuracy by Pattern**: Separate metrics for voice, articles, signals
- **False Positive Rate**: % incorrectly escalated
- **False Negative Rate**: % that should have been escalated

## Integration with PCA

### Data Flow

```
n8n Workflow
  └─ Produces audit entry
      └─ Writes to audit-YYYY-MM-DD.jsonl
          └─ Dashboard reads every 5s
              └─ Displays in Chainlit UI
```

### Example Workflow Integration

In your n8n workflow, after routing decision:

```javascript
// Final audit log entry
const auditEntry = {
  audit_timestamp: new Date().toISOString(),
  candidate_id: candidate.id,
  source_type: candidate.source_type,
  stage: "routed",
  routing_action: routing.action,
  processing_time_ms: Date.now() - startTime,
  cost_usd: models.cost,
  confidence: routing.confidence,
  destination: routing.destination,
  status: "success"
};

// Append to audit log
fs.appendFileSync(
  `audit-${new Date().toISOString().split('T')[0]}.jsonl`,
  JSON.stringify(auditEntry) + '\n'
);
```

## Performance Targets

The dashboard tracks against these targets:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Success Rate | >95% | <90% |
| Avg Latency | <20ms | >60ms |
| Daily Cost | <$2 | >$5 |
| Accuracy | >90% | <85% |
| Escalation Rate | <10% | >20% |

## Troubleshooting

### Dashboard shows "No recent audit logs found"

**Cause**: Audit logs not being generated

**Fix**:
1. Check that n8n workflow is running and writing to audit logs
2. Verify audit log path: `~/personal-cognitive-architecture/audit-logs/`
3. Check file permissions (should be readable by Chainlit process)

### Metrics seem stale

**Cause**: Audit logs not being updated

**Fix**:
1. Check that ingestion is happening (submit a test capture)
2. Verify audit log file is being written to
3. Restart Chainlit: `chainlit run chainlit-pca-monitor.py`

### Cost appears very high

**Cause**: Models are being called when they shouldn't be

**Fix**:
1. Check `data/routing-rules.json` for cost-optimization settings
2. Verify model selection logic in n8n workflow
3. Review recent traces (`/traces`) to see which operations are costly

## Neo4j Integration

### Neo4j Client API

The `dashboards/utils/neo4j_client.py` module provides a Python interface to Neo4j:

```python
from utils.neo4j_client import Neo4jClient

client = Neo4jClient(uri="neo4j://localhost:7687", username="neo4j")
client.connect()

# Get full knowledge graph
nodes, relationships = client.get_knowledge_graph(limit=100)

# Get project-specific subgraph
project_nodes, project_rels = client.get_project_graph("PATH-HAIL")

# Find contradictions
contradictions = client.get_contradictions()

# Analyze impact of changes
related_nodes, related_rels = client.get_related_notes(note_id="550e8400", depth=3)

# Get domain-specific graph
domain_nodes, domain_rels = client.get_domain_graph("AI-Safety")

# Get statistics
stats = client.get_stats()
# Returns: {total_nodes, total_relationships, total_projects}
```

### Neovis.js Visualization

The `/graph` command uses Neovis.js (vis-network library) to render an interactive visualization with:
- **Physics-based layout**: Nodes repel each other, connected nodes attract
- **Interactive controls**: Zoom, pan, drag nodes, fit to view
- **Type-based coloring**: Different colors for Note/Concept/Person nodes
- **Directional edges**: Arrows show relationship direction

## Future Enhancements

### Phase 2 Dashboard

- [ ] Graph filtering options (by project, domain, relationship type)
- [ ] Contradiction highlighting (show conflicting knowledge edges in red)
- [ ] Impact analysis visualization (highlight cascade of changes)
- [ ] Feedback loop integration (show user corrections on graph)
- [ ] Weight sensitivity analysis (which scoring weights matter most?)
- [ ] A/B testing dashboard (compare old vs. new weights)
- [ ] Custom alerts (set thresholds for metrics)

### Phase 3 Dashboard

- [ ] Multi-user support (per-project dashboards)
- [ ] Historical trends (30-day, 90-day, yearly views)
- [ ] Anomaly detection (alert on unusual patterns)
- [ ] Export to Grafana or Datadog
- [ ] Neo4j query builder (drag-and-drop graph queries)
- [ ] Knowledge gap detection (suggest missing connections)

## Architecture Notes

The dashboard is **read-only**. It:
- ✅ **Can**: Monitor, visualize, alert
- ❌ **Cannot**: Modify configurations, delete logs, change policies

Configuration changes flow through the Orchestrator + user approval workflow, not through the dashboard.

---

**Status**: Active (v1.0)
**Last Updated**: 2026-04-25
**Related**: ../docs/pca-compliance-and-governance.md (audit requirements)
