# UC-20 · State of Democracy Tracker
**Cluster:** Open Source  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration / L1 Knowledge & Control

---

## Purpose
Open-source tool for tracking democratic health indicators across jurisdictions — legislative activity, electoral integrity, press freedom, civic institution signals. Public counterpart to UC-08 Democracy Monitor. Designed for researchers, journalists, and civic technologists.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily batch — ingest new legislative and electoral data |
| Event-driven | RSS / API alert on tracked jurisdictions |
| API call | External query for jurisdiction health snapshot |
| Manual | Researcher-initiated audit or data refresh |

---

## Agent Flow

```
[Schedule / Event / API Trigger]
    │
    ▼
[Multi-Jurisdiction Data Collector — n8n]
  • Parliament of Canada (bills, votes, Hansard)
  • Elections Canada (electoral data)
  • International: Europarl, US Congress API, V-Dem dataset updates
  • Press freedom: RSF Index RSS, CPJ alerts
  • Civic institution signals: Wikipedia edits on tracked articles, court decisions RSS
    │
    ▼
[Normalisation Agent — Haiku T=0.3]
  • Map jurisdiction-specific data to shared schema
  • Classify event type: vote / bill / election / press-freedom / institution
  • Assign confidence score to each data point
    │
    ▼
[Change Detection — Code node]
  • Diff against stored baseline per jurisdiction
  • Compute delta scores on tracked indicators
    │
    ▼
[Analysis Agent — Sonnet T=0.3]
  • Contextualise changes: trend / anomaly / escalation
  • Generate jurisdiction health summary
  • Flag critical events for alert tier
    │
    ▼
[Output Router]
  ├──▶ Neo4j (graph store) — all normalised events
  ├──▶ API endpoint — serve jurisdiction snapshots to consumers
  ├──▶ Obsidian / Markdown — researcher-facing report
  └──▶ UC-08 Democracy Monitor feed — personal alert path
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author tracker workflow |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, schedule nodes |
| Parliament of Canada API (HTTP node) | Canadian legislative data |
| US Congress API (HTTP node) | US legislative data |
| Europarl RSS (HTTP node) | EU parliamentary data |
| V-Dem dataset (HTTP / file node) | Academic democracy indicators |
| RSF Index RSS (HTTP node) | Press freedom signals |
| Neo4j (HTTP node) | Jurisdiction graph storage |
| Respond to Webhook node | Public API response |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily batch |
| Webhook trigger | API query entry point |
| HTTP Request node | All data sources |
| RSS Feed Read node | Press freedom, news feeds |
| AI Agent node (Haiku) | Data normalisation |
| AI Agent node (Sonnet) | Analysis and summary |
| Code node (JS) | Schema mapping, baseline diff, delta scoring |
| Merge / Aggregate nodes | Multi-jurisdiction data combination |
| Respond to Webhook node | Serve API responses |
| Switch node | Route by jurisdiction or event type |

---

## Claude Skills (n8n-skills)

- **Patterns** — fan-out collection → normalise → analyse → multi-output
- **Expression Syntax** — schema mapping across heterogeneous API responses
- **Validation Expert** — multi-API error handling, schema validation
- **Tools Expert** — Respond to Webhook for public API serving

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker for dev) | ✅ Live |
| Neo4j (graph store) | ✅ Live |
| Parliament of Canada API | 🟡 Public — endpoint mapping needed |
| US Congress API key | 🟡 Free — easy to obtain |
| V-Dem dataset access | 🟡 Public academic dataset — download or API |
| RSF API / RSS | 🟡 Public |
| Shared schema with UC-08 | 🔴 Not yet defined — coordinate first |
| GitHub repo (public release) | 🔴 Not yet created |
| UC-08 Democracy Monitor (personal variant) | 🔴 Not Started |

---

## Open Source Considerations
- Shared data schema with UC-08 is a hard requirement — define schema before building either workflow
- Public API serving requires authentication strategy for rate limiting — consider API key gating even for open-source version
- V-Dem data usage: check licence terms for redistribution of derived data
- Design for GitHub Actions deployment as alternative to self-hosted n8n
- Consider a status-site companion (similar to `jjuniper-dev/status-site` pattern) for public dashboard

---

## Known Issues / Watch Items
- Scope risk: multi-jurisdiction tracking is a deep rabbit hole — define MVP jurisdictions (Canada, USA, EU) and add incrementally
- Build UC-08 first as the personal proof-of-concept, extract reusable components for UC-20
- API consistency across jurisdictions is poor — expect significant normalisation work in the Code node

---

## Related UCs
- UC-08 Democracy Monitor (personal variant — build first, share schema)
- UC-06 Ayla Assistant (query interface)
- UC-01 Knowledge Graph (democratic events as graph entities)
- UC-32 Automated Briefing Generation (democracy tracker as briefing source)
