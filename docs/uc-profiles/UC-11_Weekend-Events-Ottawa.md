# UC-11 · Weekend Events (Ottawa)
**Cluster:** Lifestyle  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Discover and surface Ottawa-area weekend events — food festivals, cultural events, flea markets, live music, community gatherings — filtered by personal preferences (UC-04) and delivered as a curated weekly digest. Replaces manual event scanning.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Thursday evening — weekly digest generation |
| Manual | On-demand via Ayla ("what's on this weekend in Ottawa?") |

---

## Agent Flow

```
[Schedule / Manual Trigger]
    │
    ▼
[Event Collector — n8n]
  • Eventbrite API — Ottawa events this weekend
  • Ottawa Tourism RSS / calendar
  • Facebook Events (public scrape via Apify or similar)
  • Meetup.com API — Ottawa groups
  • City of Ottawa events calendar (RSS / scrape)
  • Google Events (SerpAPI "events near Ottawa" query)
    │
    ▼
[Deduplication + Normalisation — Code node]
  • Merge events by title similarity + date
  • Normalise: title, date, time, location, category, URL
    │
    ▼
[Preference Filter — Haiku T=0.4]
  • Score against UC-04 Likes/Dislikes profile
  • Boost: music, food, markets, cultural events
  • Suppress: sports (unless flagged as interest)
  • Tag: free / paid, indoor / outdoor, dog-friendly
    │
    ▼
[Digest Agent — Sonnet T=0.3]
  • Curate top 8–12 events
  • Write brief editorial note per event (1–2 sentences)
  • Group by: Friday / Saturday / Sunday, category
    │
    ▼
[Output]
  ├──▶ Obsidian: /lifestyle/events/YYYY-WXX.md
  └──▶ UC-06 Ayla: deliver digest conversationally on request
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author event discovery workflow |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, schedule nodes |
| Eventbrite API (HTTP node) | Ticketed event discovery |
| SerpAPI (HTTP node) | Google Events results |
| Meetup.com API (HTTP node) | Community event discovery |
| Apify (HTTP node) | Facebook public events scrape |
| Obsidian URI / webhook | Digest note write |
| UC-06 Ayla webhook | On-demand delivery |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Thursday weekly run |
| Webhook trigger | On-demand Ayla request |
| HTTP Request node | All event APIs |
| RSS Feed Read node | Ottawa Tourism, City calendar |
| Code node (JS) | Deduplication, normalisation, date filtering |
| AI Agent node (Haiku) | Preference scoring |
| AI Agent node (Sonnet) | Digest writing |
| Aggregate / Merge nodes | Combine all sources |
| Set node | Normalised event object assembly |

---

## Claude Skills (n8n-skills)

- **Patterns** — fan-out collection → filter → synthesise (batch digest)
- **Expression Syntax** — date range construction (this Friday → Sunday), array dedup
- **Validation Expert** — multi-API response normalisation

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Eventbrite API key | 🔴 Needs registration |
| SerpAPI key | 🟡 Needed — free tier limited |
| Meetup.com API access | 🟡 Public API available |
| Apify account (Facebook scrape) | 🔴 Paid — evaluate cost |
| UC-04 Likes/Dislikes (preference filter) | 🔴 Not Started — hardcode interim |
| UC-06 Ayla (delivery surface) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |
| Ottawa Google Calendar (previously built) | ✅ Exists — reuse as seed |

---

## Known Issues / Watch Items
- Facebook Events scraping is fragile and ToS-sensitive — Apify has a managed scraper but it's paid; consider skipping unless high-value events are missed by other sources
- Ottawa events landscape is seasonal — winter events very different from summer; consider seasonal weighting in preference filter
- Dog-friendly tag is worth building in from the start (dachshund owner context)
- Ottawa Google Calendar previously built spans multiple seasons — can serve as a seed list of recurring annual events

---

## Related UCs
- UC-04 Likes/Dislikes Graph (preference filter)
- UC-06 Ayla Assistant (delivery and on-demand query)
- UC-12 Event Voting (collaborative shortlisting from this digest)
- UC-13 Lifestyle Concierge (broader lifestyle context)
