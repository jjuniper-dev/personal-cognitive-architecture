# UC-08 · Democracy Monitor
**Cluster:** Automation  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Monitor democratic health indicators — parliamentary votes, legislative activity, electoral developments, and civic institution signals — across Canada and selected international jurisdictions. Surface anomalies and significant events as structured alerts.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily batch — scrape and compare against baseline |
| Event-driven | RSS / API alert on tracked keywords or entities |
| Manual | On-demand query via Ayla |

---

## Agent Flow

```
[Schedule / Event Trigger]
    │
    ▼
[Data Collector — n8n]
  • Parliament of Canada OpenData API (votes, bills, Hansard)
  • OpenParliament.ca RSS / API
  • Elections Canada feed
  • International: selected RSS (Europarl, US Congress API)
  • Google News RSS for civic/democracy keywords
    │
    ▼
[Change Detector — Code node]
  • Compare against previous snapshot (stored in Neo4j or static data)
  • Flag new votes, bill status changes, election events
    │
    ▼
[Significance Classifier — Haiku T=0.4]
  • Score significance: routine / notable / critical
  • Tag jurisdiction, topic, actors involved
    │
    ├─[Routine]──▶ [Neo4j write — archive only]
    │
    └─[Notable / Critical]──▶ [Analysis Agent — Sonnet T=0.3]
                                 • Summarise event
                                 • Contextualise against tracked history
                                 • Generate alert note
                                 │
                                 ▼
                               [Output Router]
                                 ├──▶ Obsidian: /monitor/democracy/YYYYMMDD.md
                                 └──▶ UC-06 Ayla: push alert to conversation
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author monitoring workflow |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, schedule nodes |
| Parliament of Canada API (HTTP node) | Bills, votes, Hansard |
| OpenParliament.ca API (HTTP node) | Enriched parliamentary data |
| Google News RSS (HTTP node) | Keyword monitoring |
| Neo4j (HTTP node) | Snapshot storage, change detection |
| Obsidian URI / webhook | Alert note write |
| UC-06 Ayla webhook | Push alert to assistant |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily batch |
| RSS Feed Read node | Feed monitoring |
| HTTP Request node | Parliament APIs, Neo4j, Obsidian |
| Code node (JS) | Snapshot diff / change detection |
| AI Agent node (Haiku) | Significance classification |
| AI Agent node (Sonnet) | Event analysis and summary |
| If / Switch node | Route by significance tier |
| Set node | Structure alert payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — monitor-detect-alert (scheduled batch with change gate)
- **Expression Syntax** — snapshot comparison, date/diff logic
- **Validation Expert** — API response schema handling (Parliament API is inconsistent)

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Parliament of Canada API | 🟡 Public — needs endpoint mapping |
| OpenParliament.ca API | 🟡 Public — needs key or scrape strategy |
| Neo4j (snapshot store) | ✅ Live |
| UC-06 Ayla (alert surface) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |
| Jurisdiction / keyword list | 🔴 Not yet defined |
| Open Source version (UC-19) | 🔴 Democracy Monitor has an open-source counterpart — coordinate schema |

---

## Known Issues / Watch Items
- Parliament of Canada API documentation is sparse — may require scraping OpenParliament.ca as primary source
- International jurisdiction monitoring scope creep risk — define a fixed list before building
- This UC has a direct open-source counterpart (UC-19 State of Democracy Tracker) — the personal monitor and the public tracker should share data schema and potentially the same Neo4j graph, separated by access tier

---

## Related UCs
- UC-06 Ayla Assistant (alert delivery)
- UC-19 State of Democracy Tracker (open-source counterpart — shared schema)
- UC-32 Automated Briefing Generation (democracy events as briefing source)
