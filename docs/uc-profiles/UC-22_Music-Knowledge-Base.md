# UC-22 · Music Knowledge Base
**Cluster:** Open Source  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control / L3 Workflow & Integration

---

## Purpose
Build and maintain a structured knowledge base of music — focused on deep house (late 1980s–early 1990s Chicago/New York sound), vinyl records, labels, producers, and tracks. Personal passion project and open-source resource for the deep house community. Feeds UC-04 preferences and UC-06 music recommendations.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | User adds track, artist, or record to the knowledge base via Ayla |
| Schedule | Weekly enrichment run — pull new data for existing entries |
| Import | Discogs collection export → bulk ingest |
| Event-driven | New UC-05 AI Talks on music history → extract music entities |

---

## Agent Flow

```
[Input — manual / import / enrichment trigger]
    │
    ▼
[Source Router — Switch]
    │
    ├──▶ [Discogs API — collection / release data]
    │      • Track details, label, year, format, matrix number
    │      • Artist credits, genre/style tags
    │
    ├──▶ [MusicBrainz API — canonical metadata]
    │      • Canonical IDs (MBIDs) for artists, releases, labels
    │      • Relationships: produced by, remixed by, released on
    │
    ├──▶ [Last.fm API — listening data + tags]
    │      • Community tags, similar artists
    │
    └──▶ [Manual input — free text via Ayla]
           • Parse artist, track, label, year, notes
    │
    ▼
[Enrichment Agent — Sonnet T=0.3]
  • Cross-reference sources
  • Identify era (Chicago house / NY house / UK acid / etc.)
  • Extract notable production techniques, equipment, studio
  • Link to related tracks, artists, labels in graph
    │
    ▼
[Knowledge Graph Writer]
  • Neo4j: MERGE Artist, Release, Track, Label, Studio, Producer nodes
  • Relationships: PRODUCED_BY, RELEASED_ON, REMIXED_BY, PLAYED_AT
  • Properties: year, bpm, key, mood_tag, format, matrix, personal_rating
    │
    ▼
[Output]
  ├──▶ Neo4j graph (canonical store)
  ├──▶ Obsidian: /music/artists/ and /music/releases/ notes
  └──▶ Optional: public API endpoint for community access
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author music KB ingestion workflow |
| `n8n-mcp` · `search_nodes` | HTTP, schedule, code nodes |
| Discogs API (HTTP node) | Collection and release data |
| MusicBrainz API (HTTP node) | Canonical music metadata |
| Last.fm API (HTTP node) | Tags and listening data |
| Neo4j (HTTP node) | Graph write |
| Obsidian URI / webhook | Vault note generation |
| GitHub API (HTTP node + PAT) | Optional: publish KB data to public repo |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Manual entry from Ayla |
| Schedule trigger | Weekly enrichment |
| HTTP Request node | Discogs, MusicBrainz, Last.fm, Neo4j |
| Switch node | Source routing |
| AI Agent node (Sonnet) | Enrichment and cross-referencing |
| Code node (JS) | Discogs import parsing, MBID resolution, frontmatter generation |
| Loop / Split In Batches node | Batch Discogs collection import |
| Merge node | Combine multi-source enrichment |
| Set node | Assemble Neo4j node payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — fan-out enrichment (multiple APIs → merge → write)
- **Expression Syntax** — API response normalisation, MBID handling
- **Validation Expert** — multi-API merge conflict resolution (Discogs vs MusicBrainz disagreements)
- **Tools Expert** — Loop node for batch Discogs import

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Neo4j (local Docker) | ✅ Live |
| Discogs API token | 🟡 Easy to obtain (personal token) |
| MusicBrainz API | 🟡 Public, no key required — rate limit 1 req/sec |
| Last.fm API key | 🟡 Free — easy to obtain |
| Discogs collection export | 🔴 Need to export current collection |
| Music KB schema (Neo4j) | 🔴 Not yet defined |
| UC-04 Likes/Dislikes Graph (preference link) | 🔴 Not Started |
| UC-05 AI Talks (music entity source) | 🔴 Not Started |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Open Source Considerations
- The music knowledge graph data itself could be valuable to the deep house community — consider publishing a sanitised (no personal ratings) graph snapshot
- MusicBrainz rate limit (1 req/sec) requires a polite batch loop — build this in from the start
- Discogs terms of service: personal use of API is fine; public redistribution of Discogs data requires compliance with their terms
- Deep house era taxonomy (Chicago 1986–1992, NYC 1988–1994, UK acid 1988–1991, etc.) should be defined upfront as a controlled vocabulary in Neo4j

---

## Known Issues / Watch Items
- Schema design is the critical first step — Neo4j music graph schema must be defined before any writes
- MusicBrainz MBID as canonical ID: always use MBIDs as primary keys where available to avoid artist/release name collisions
- Personal vinyl collection vs. general knowledge: track which nodes come from personal collection (with personal ratings) vs. general knowledge (community data) — use a `source` property
- BPM and key data: Discogs doesn't provide this; consider Tunebat API or manual entry as supplementary source

---

## Related UCs
- UC-04 Likes/Dislikes Graph (music preferences)
- UC-05 AI Talks (music history content as source)
- UC-06 Ayla Assistant (music queries and recommendations)
- UC-01 Knowledge Graph (music entities as subgraph)
