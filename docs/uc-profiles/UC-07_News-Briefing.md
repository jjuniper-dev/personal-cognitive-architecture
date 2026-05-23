# UC-07 · News Briefing
**Cluster:** Automation  
**Status:** 🟡 Was live on Zapier — migrating to n8n  
**Layer:** L3 Workflow & Integration

---

## Purpose
Deliver a curated, personalised daily news briefing — filtered by topic interests, formatted for audio (Kokoro TTS) and/or text delivery. Replaces manual news scanning with a structured, opinionated digest.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily at configured time (e.g. 07:00 ET) |
| Manual | On-demand via Ayla ("give me my briefing") |

---

## Agent Flow

```
[Schedule / Manual Trigger]
    │
    ▼
[Feed Collector — n8n]
  • RSS feeds (curated list): AI, tech, Ottawa/Canada news, deep house/music
  • NewsAPI / Perplexity for gap-fill
  • Deduplicate against yesterday's briefing index
    │
    ▼
[Relevance Filter — Haiku T=0.4]
  • Score each item against interest profile (UC-04 preferences)
  • Discard score < threshold
  • Tag by domain: AI / Tech / Local / Music / World
    │
    ▼
[Synthesis Agent — Sonnet T=0.3]
  • Write briefing sections per domain
  • Max 3 items per section, 2–3 sentences each
  • Add brief editorial framing where relevant
    │
    ▼
[Format Router — Switch]
    │
    ├──▶ [Text output]
    │      • Obsidian write: /briefings/YYYYMMDD.md
    │      • Optional: push to notification / Slack
    │
    └──▶ [Audio output — Kokoro TTS]
           • Convert briefing text to speech
           • Deliver via file / notification
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author migrated briefing workflow |
| `n8n-mcp` · `search_nodes` | RSS, NewsAPI, schedule nodes |
| `n8n-mcp` · `deploy_template` | Find closest existing news/briefing template as base |
| RSS Feed node (n8n native) | Feed collection |
| NewsAPI (HTTP node) | Gap-fill news source |
| Perplexity API (HTTP node) | Contextual news lookup |
| Kokoro TTS (HTTP node / local) | Audio output |
| Obsidian URI / webhook | Vault write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily run |
| Webhook trigger | On-demand via Ayla |
| RSS Feed Read node | Feed ingestion |
| HTTP Request node | NewsAPI, Perplexity, Kokoro TTS |
| AI Agent node (Haiku) | Relevance filtering |
| AI Agent node (Sonnet) | Briefing synthesis |
| Code node (JS) | Deduplication logic, feed merging |
| Switch node | Text vs audio routing |
| Aggregate node | Collect all feed items before filtering |

---

## Claude Skills (n8n-skills)

- **Patterns** — scheduled batch pipeline with filter gate
- **Expression Syntax** — array iteration over feed items, date formatting
- **Validation Expert** — RSS node config, deduplication index structure

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Zapier migration (source workflow) | 🟡 Existing Zapier workflow to port |
| Curated RSS feed list | 🟡 Exists from Zapier version — needs review |
| UC-04 Likes/Dislikes (interest profile) | 🔴 Not Started — use hardcoded topics interim |
| NewsAPI key | ✅ Assumed available (was in Zapier) |
| Perplexity API key | 🟡 Needs confirmation |
| Kokoro TTS (local) | 🟡 Referenced in system — confirm endpoint |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Known Issues / Watch Items
- Zapier → n8n port: RSS + filter + LLM synthesis pattern is well-supported in zie619 n8n library — check for existing template before building from scratch
- Audio delivery mechanism (Kokoro TTS) needs a defined endpoint and output path before the format router can be built
- Deduplication index: simplest approach is a Code node maintaining a date-keyed Set in static data; consider Neo4j if briefing history needs to be queryable
- Interest profile: hardcode topics (AI, tech, Ottawa, deep house) until UC-04 is live

---

## Related UCs
- UC-04 Likes/Dislikes (interest profile — future personalisation)
- UC-06 Ayla Assistant (on-demand trigger)
- UC-32 Automated Briefing Generation (professional briefing counterpart)
