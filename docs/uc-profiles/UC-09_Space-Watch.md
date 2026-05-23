# UC-09 · Space-Watch
**Cluster:** Automation  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Monitor space events, launches, astronomical phenomena, and space agency news. Surface notable events as structured alerts and briefing inputs. Personal interest / knowledge enrichment use case.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily batch — check launch schedules, event calendars |
| Event-driven | RSS alert on tracked agencies / missions |
| Manual | On-demand query via Ayla ("anything happening in space this week?") |

---

## Agent Flow

```
[Schedule / Manual Trigger]
    │
    ▼
[Data Collector — n8n]
  • Launch Library 2 API (ll2.thespacedevs.com) — launch schedule
  • NASA APIs: APOD, Near-Earth Objects, Artemis updates
  • SpaceX API (informal) / r/spacex RSS
  • ESA news RSS
  • Astronomy event calendars (ICS feed or scrape)
    │
    ▼
[Event Filter — Haiku T=0.4]
  • Score significance: routine / notable / spectacular
  • Tag: launch / discovery / milestone / viewing opportunity
  • Flag Ottawa-visible astronomical events (based on location)
    │
    ├─[Routine]──▶ [Neo4j archive write]
    │
    └─[Notable / Spectacular]──▶ [Summary Agent — Sonnet T=0.3]
                                    • Plain-language event summary
                                    • Add viewing tips if Ottawa-relevant
                                    │
                                    ▼
                                  [Output]
                                    ├──▶ Obsidian: /monitor/space/YYYYMMDD.md
                                    ├──▶ UC-07 briefing feed (inject notable item)
                                    └──▶ UC-06 Ayla alert (spectacular events only)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author space monitoring workflow |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, schedule nodes |
| Launch Library 2 API (HTTP node) | Launch schedule |
| NASA API (HTTP node) | APOD, NEO data |
| RSS Feed node | Agency news feeds |
| Neo4j (HTTP node) | Event archive |
| Obsidian URI / webhook | Alert note write |
| UC-07 briefing webhook | Inject notable events |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily batch |
| HTTP Request node | Launch Library 2, NASA, Neo4j |
| RSS Feed Read node | Agency news |
| AI Agent node (Haiku) | Event significance filter |
| AI Agent node (Sonnet) | Event summary |
| Code node (JS) | Ottawa viewing window logic, date formatting |
| If / Switch node | Significance routing |
| Merge node | Combine sources before filter |

---

## Claude Skills (n8n-skills)

- **Patterns** — monitor-filter-alert (same structural pattern as UC-08)
- **Expression Syntax** — date/time window calculations, geo-context injection
- **Validation Expert** — multi-API response merging

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Launch Library 2 API | 🟡 Public, free tier — no key required |
| NASA API key | 🟡 Free — easy to obtain |
| Neo4j (archive) | ✅ Live |
| UC-07 News Briefing (event injection) | 🟡 Migration in progress |
| UC-06 Ayla (alert surface) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |
| Ottawa timezone / location context | ✅ Known — hardcode in workflow |

---

## Known Issues / Watch Items
- Lower priority relative to UC-07, UC-08 — build after those are stable
- Ottawa-visible events logic: need to define what "visible" means (clear sky assumption, naked-eye threshold, telescope events) — start simple with IFR calendar lookup
- UC-07 briefing injection: define a standard event payload schema shared with UC-08 so the briefing workflow can accept events from both monitors uniformly

---

## Related UCs
- UC-06 Ayla Assistant (alert delivery)
- UC-07 News Briefing (event injection feed)
- UC-01 Knowledge Graph (space concepts as entities)
