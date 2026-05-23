# UC-14 · Birthday Planning
**Cluster:** Lifestyle  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Proactive birthday tracking and planning — monitor upcoming birthdays from contacts, generate gift ideas based on known preferences, and suggest celebration activities. Ensures no birthday is missed and planning starts early enough to be useful.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily check — scan for birthdays in next 30 / 14 / 7 / 1 days |
| Manual | "Plan something for [person]'s birthday" via Ayla |

---

## Agent Flow

```
[Daily Schedule Trigger]
    │
    ▼
[Birthday Scanner — n8n]
  • Google Contacts API — birthdays in next 30 days
  • Google Calendar — birthday events
  • Obsidian people notes — manually tracked birthdays
    │
    ▼
[Upcoming Birthday Filter — Code node]
  • Bucket: 30-day warning / 14-day reminder / 7-day alert / day-of
  • Check: has planning already started? (Neo4j flag)
    │
    ├─[Already planned]──▶ [Status check only — no action]
    │
    └─[Not yet planned]──▶ [Planning Agent — Sonnet T=0.4]
                              • Retrieve person context from UC-01 graph
                                (relationship, interests, recent interactions)
                              • Generate:
                                - 3 gift ideas with rationale
                                - 2 activity/experience suggestions
                                - Draft message / card text
                              │
                              ▼
                            [Output]
                              ├──▶ UC-06 Ayla: alert + planning brief
                              ├──▶ Obsidian: /lifestyle/birthdays/PERSON-YEAR.md
                              └──▶ Neo4j: mark planning initiated
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author birthday planning workflow |
| `n8n-mcp` · `search_nodes` | Schedule, HTTP, Google nodes |
| Google Calendar MCP | Birthday event detection |
| Google Contacts API (HTTP node) | Contact birthday fields |
| Neo4j (HTTP node) | Person context, planning status flag |
| UC-01 Knowledge Graph | Person entity enrichment |
| UC-06 Ayla webhook | Alert delivery |
| Obsidian URI / webhook | Planning note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily scan |
| HTTP Request node | Google Contacts, Neo4j, Obsidian |
| Code node (JS) | Date bucketing, planning status check |
| AI Agent node (Sonnet) | Gift ideas, activity suggestions, message drafting |
| If / Switch node | Route by time bucket and planning status |
| Set node | Structure planning brief payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — scheduled monitor with stateful planning gate
- **Expression Syntax** — date arithmetic (days until birthday), bucket logic
- **Validation Expert** — Google Contacts API response schema

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Google Calendar MCP | ✅ Connected |
| Google Contacts API access | 🟡 Needs OAuth scope addition |
| UC-01 Knowledge Graph (person context) | 🟡 In Progress |
| Neo4j (planning status store) | ✅ Live |
| UC-06 Ayla (alert delivery) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |
| People / relationship data in Neo4j | 🔴 Not yet populated |

---

## Known Issues / Watch Items
- Person context quality (gift idea relevance) depends entirely on UC-01 graph having real relationship and interest data — this UC becomes valuable only after UC-01 is meaningfully populated
- Google Contacts API requires additional OAuth scopes beyond Calendar — verify scope coverage in n8n Google credential setup
- Privacy: birthday planning notes contain personal relationship data — keep in private vault path, not synced to any public store
- Gift idea generation: prompt should include budget range as a parameter — hardcode a reasonable default until UC-15 Finance integration makes budget context available

---

## Related UCs
- UC-01 Knowledge Graph (person context source)
- UC-06 Ayla Assistant (alert and delivery)
- UC-13 Lifestyle Concierge (activity suggestions overlap)
- UC-15–18 Finance (budget context — future integration)
