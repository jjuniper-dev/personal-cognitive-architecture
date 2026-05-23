# UC-13 · Lifestyle Concierge
**Cluster:** Lifestyle  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime / L3 Workflow & Integration

---

## Purpose
A personalised lifestyle assistant that synthesises preferences (UC-04), local context (UC-11), and personal schedule to proactively suggest activities, restaurants, experiences, and planning recommendations. The "what should I do / eat / explore" layer of Ayla.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | Conversational request via UC-06 Ayla ("suggest something for Saturday afternoon") |
| Schedule | Weekly proactive nudge — Sunday evening life planning prompt |
| Event-driven | UC-11 event discovered that strongly matches UC-04 profile → push recommendation |

---

## Agent Flow

```
[Request / Schedule / Event Trigger]
    │
    ▼
[Context Assembler — n8n]
  • Pull UC-04 preference profile (likes/dislikes)
  • Pull UC-11 upcoming events shortlist
  • Pull weather forecast (Environment Canada API / Open-Meteo)
  • Pull calendar free slots (Google Calendar MCP)
  • Pull UC-03 recent memories (avoid suggesting recently done activities)
    │
    ▼
[Recommendation Agent — Sonnet T=0.4]
  • Generate 3–5 personalised suggestions
  • Match: weather-appropriate, preference-aligned, novel (not recently done)
  • Include: restaurant picks, activity ideas, event highlights, errand batching
  • Tone: direct, opinionated ("you'd love X because Y")
    │
    ▼
[Output]
  ├──▶ UC-06 Ayla: conversational delivery
  └──▶ Obsidian: /lifestyle/concierge/YYYYMMDD.md (weekly planning note)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author concierge workflow |
| `n8n-mcp` · `search_nodes` | HTTP, schedule, webhook nodes |
| Google Calendar MCP | Free slot lookup |
| Open-Meteo API (HTTP node) | Ottawa weather forecast (free, no key) |
| UC-04 webhook / Neo4j | Preference profile retrieval |
| UC-11 webhook / Neo4j | Upcoming event shortlist |
| UC-03 Obsidian read | Recent memory context |
| UC-06 Ayla webhook | Deliver recommendations |
| Google Places API (HTTP node) | Restaurant / venue details |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Request from Ayla |
| Schedule trigger | Weekly proactive run |
| HTTP Request node | Weather, Google Places, Neo4j, Obsidian |
| AI Agent node (Sonnet) | Recommendation generation |
| Code node (JS) | Context assembly, date/calendar slot parsing |
| Merge node | Combine all context sources |
| Set node | Structure recommendation payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — context-gather → synthesise → deliver (RAG-style recommendation)
- **Expression Syntax** — multi-source context assembly, date/slot manipulation
- **Tools Expert** — Google Calendar MCP integration

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| UC-04 Likes/Dislikes Graph | 🔴 Not Started |
| UC-11 Weekend Events | 🔴 Not Started |
| UC-03 Life Memory Archive | 🔴 Not Started |
| UC-06 Ayla Assistant | 🟡 Planned |
| Google Calendar MCP | ✅ Connected |
| Open-Meteo API | ✅ Free, no key needed |
| Google Places API key | 🔴 Needs GCP project + billing |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Known Issues / Watch Items
- This UC is a synthesis layer — it only becomes useful once UC-04, UC-11, and UC-03 have real data; build last in this cluster
- Weather integration: Open-Meteo is free, accurate for Ottawa, and requires no API key — use it over any paid alternative
- Restaurant suggestions: Google Places API is the gold standard but requires billing; Yelp Fusion API is a free alternative (500 calls/day)
- "Novel" filter: needs to query UC-03 to avoid recommending recently visited places — requires UC-03 to tag location entities

---

## Related UCs
- UC-04 Likes/Dislikes Graph (preference engine)
- UC-11 Weekend Events Ottawa (event input)
- UC-03 Life Memory Archive (novelty filter)
- UC-06 Ayla Assistant (delivery interface)
- UC-14 Birthday Planning (event-specific concierge variant)
