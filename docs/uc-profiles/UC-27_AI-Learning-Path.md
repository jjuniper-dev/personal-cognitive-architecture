# UC-27 · AI Learning Path
**Cluster:** Enterprise Architecture  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control

---

## Purpose
Curate and maintain a structured AI learning path for the EA practice — tracking emerging AI/ML concepts, GC-relevant AI governance developments, and technical upskilling resources. Keeps the EA practice current without drowning in noise.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Weekly — ingest new resources, update learning queue |
| Manual | Add resource or topic via Ayla |
| Event-driven | UC-05 AI Talks extracts a topic → add to learning queue |

---

## Agent Flow

```
[Weekly Schedule / Manual / UC-05 event]
    │
    ▼
[Resource Collector — n8n]
  • ArXiv RSS (AI governance, ML safety, applied AI)
  • Microsoft Learn (Azure AI, Purview, Fabric — MS Learn MCP)
  • GC digital policy feeds (TBS, OCDO publications)
  • Curated newsletters (Import AI, The Batch, etc. — RSS)
  • UC-05 AI Talks queue
    │
    ▼
[Relevance Filter — Haiku T=0.4]
  • Score against EA practice focus areas:
    AI governance, GC frameworks, PATH/HAIL stack,
    data architecture, responsible AI, EU AI Act
  • Discard score < threshold
    │
    ▼
[Learning Item Structurer — Sonnet T=0.3]
  • Classify: concept / tool / framework / policy / technique
  • Estimate: time-to-learn (quick read / deep dive / course)
  • Tag: relevant to ARB / TPO / CDO / personal development
  • Generate: 2-sentence summary + why it matters for EA practice
    │
    ▼
[Output]
  ├──▶ Neo4j: LearningItem node + relationships to capabilities
  ├──▶ Obsidian: /ea/learning/YYYY-WXX.md (weekly digest)
  └──▶ UC-06 Ayla: surface top 3 items on request
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Microsoft Learn MCP | Azure AI, GC-relevant Microsoft docs |
| `n8n-mcp` · `create_workflow` | Author learning pipeline |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, schedule nodes |
| ArXiv API (HTTP node) | Research paper feed |
| Neo4j (HTTP node) | Learning item graph |
| Obsidian URI / webhook | Weekly digest write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Weekly run |
| RSS Feed Read node | Newsletter and policy feeds |
| HTTP Request node | ArXiv, Microsoft Learn, Neo4j, Obsidian |
| AI Agent node (Haiku) | Relevance filter |
| AI Agent node (Sonnet) | Learning item structuring |
| Code node (JS) | Deduplication, time-to-learn estimation |
| Aggregate node | Combine all sources |

---

## Claude Skills (n8n-skills)

- **Patterns** — scheduled batch digest (same pattern as UC-07)
- **Expression Syntax** — multi-source aggregation, relevance scoring
- **Tools Expert** — Microsoft Learn MCP (connected)

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Microsoft Learn MCP | ✅ Connected |
| UC-05 AI Talks (content source) | 🔴 Not Started |
| Neo4j (learning graph) | 🟡 Shared stack |
| Obsidian vault write pipeline | 🟡 URI live |
| Curated feed list | 🔴 Not yet defined |

---

## Related UCs
- UC-05 AI Talks (content source)
- UC-23 Virtual EA Agent (knowledge consumer)
- UC-25 AI Capability Framework (capability-linked learning items)
- UC-07 News Briefing (structural parallel — same pattern)
