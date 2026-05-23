# UC-05 · AI Talks
**Cluster:** Personal Knowledge  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control / L3 Workflow & Integration

---

## Purpose
Capture, transcribe, summarise, and index AI-related talks, lectures, podcasts, and conference sessions. Extract key insights, speakers, concepts, and citations into the knowledge graph. Keeps the personal AI knowledge base current without manual note-taking.

---

## Trigger
| Type | Source |
|------|--------|
| URL submission | User submits YouTube / podcast URL to Ayla or n8n webhook |
| RSS / feed monitor | Scheduled poll of curated AI talk feeds (YouTube channels, podcast RSS) |
| Manual | File drop (audio/video) to watched folder |

---

## Agent Flow

```
[Input: URL or file]
    │
    ▼
[Source Handler — n8n Switch]
  • YouTube URL → yt-dlp audio extraction or transcript fetch
  • Podcast URL → RSS item + audio download
  • File → direct to transcription
    │
    ▼
[Transcription]
  • YouTube: attempt caption fetch first (free, fast)
  • Fallback: Whisper (local RTX 3090 / OpenAI API)
    │
    ▼
[Segmentation Agent — Haiku T=0.4]
  • Split transcript into logical sections
  • Tag sections by topic
  • Identify speaker turns (if multi-speaker)
    │
    ▼
[Insight Extraction Agent — Sonnet T=0.3]
  • Extract: key claims, frameworks, named concepts, citations, speakers
  • Generate structured summary (TL;DR + bullet insights)
  • Propose Neo4j nodes: Speaker, Talk, Concept, Citation
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge extractions — flag vague or unsupported claims
  • Verify speaker attribution where possible
    │
    ├──▶ [Obsidian Write]
    │      • /knowledge/ai-talks/YYYYMMDD-{slug}.md
    │      • Frontmatter: date, speaker, source_url, youtube_url (fixed field)
    │      • Body: summary, insights, transcript segments
    │
    └──▶ [UC-01 Knowledge Graph ingest]
           • Speaker, Talk, Concept nodes + relationships
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author full pipeline |
| `n8n-mcp` · `search_nodes` | RSS, HTTP, YouTube nodes |
| YouTube transcript API (HTTP node) | Caption fetch (free path) |
| yt-dlp (Execute Command node) | Audio extraction fallback |
| Whisper API / local (HTTP node) | Transcription |
| Neo4j (HTTP node) | Graph write |
| Obsidian URI / webhook | Vault write |
| UC-01 webhook | Knowledge graph ingest |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| RSS Feed Trigger node | Monitor AI talk feeds |
| Webhook trigger | URL submission from Ayla |
| HTTP Request node | Transcript API, Whisper, Neo4j, Obsidian |
| Execute Command node | yt-dlp audio extraction |
| Switch node | Route by source type |
| AI Agent node (Haiku) | Segmentation + critical review |
| AI Agent node (Sonnet) | Insight extraction |
| Code node (JS) | Frontmatter construction, Cypher prep |
| Set / Merge nodes | Assemble final payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — sequential pipeline with source-type routing (Switch pattern)
- **Expression Syntax** — binary data for audio, URL parsing
- **Validation Expert** — `youtube_url` field (not `url`) — known bug, already fixed in UC-01
- **Tools Expert** — Execute Command node for yt-dlp

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-01 Knowledge Graph (downstream) | 🟡 In Progress |
| n8n (local Docker) | ✅ Live |
| Whisper (OpenAI API — interim) | ✅ Available |
| Local Whisper / RTX 3090 | 🔴 Hardware not yet acquired |
| yt-dlp installed on n8n host | 🔴 Needs install + test |
| YouTube transcript API access | 🟡 Public API available, rate limits apply |
| Obsidian vault + write pipeline | 🟡 URI live |
| Curated AI talk feed list | 🔴 Not yet defined |

---

## Known Issues / Watch Items
- YouTube caption quality varies — auto-generated captions on technical talks often mangle terminology; Whisper fallback is important
- yt-dlp in Execute Command node has path/permissions gotchas in Docker — test early
- Feed list curation is an ongoing task; consider storing in Neo4j or an Obsidian note as a managed resource
- `youtube_url` field fix already applied in UC-01 — propagate same schema to this UC from the start

---

## Related UCs
- UC-01 Knowledge Graph (primary consumer)
- UC-02 Voice-to-Knowledge (shared Whisper infrastructure)
- UC-32 Automated Briefing Generation (AI Talks summaries as briefing source)
