# UC-01 · Knowledge Graph
**Cluster:** Personal Knowledge  
**Status:** 🟡 In Progress — Neo4j live, Sprint 5 validation layer active  
**Layer:** L1 Knowledge & Control / L2 Agent Runtime

---

## Purpose
Build and maintain a persistent, queryable knowledge graph of entities, concepts, and relationships extracted from all ingested content (voice notes, Obsidian captures, web clips, documents). The canonical memory layer for the Ayla ecosystem.

---

## Trigger
| Type | Source |
|------|--------|
| Webhook (primary) | n8n webhook node — receives payloads from Obsidian URI capture pipeline, iOS Shortcuts |
| Schedule (secondary) | Nightly batch — re-processes unlinked nodes, runs graph maintenance |
| Manual | Claude chat → n8n MCP tool call |

---

## Agent Flow

```
[Capture Input]
    │
    ▼
[Preprocessor Agent — Sonnet T=0.3]
  • Normalize payload (text, metadata, source type)
  • Detect entity candidates
  • Classify content type (concept / event / person / resource)
    │
    ▼
[Extraction Agent — Sonnet T=0.3]
  • Named entity extraction
  • Relationship inference
  • Deduplication check against existing Neo4j nodes
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge low-confidence extractions
  • Flag ambiguous relationships for human review
    │
    ├─[Approved]──▶ [Neo4j Write]
    │                 • MERGE node (avoid duplicates)
    │                 • CREATE relationships
    │                 • Tag with source, timestamp, confidence score
    │
    └─[Flagged]───▶ [Obsidian Note — Review Queue]
                      • Write to /inbox/kg-review/ via Obsidian URI
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` / `update_workflow` | Author and maintain the ingestion workflow |
| `n8n-mcp` · `validate_workflow` | Pre-flight before activation |
| `n8n-mcp` · `search_nodes` | Discover Neo4j, webhook, HTTP nodes |
| Neo4j MCP (custom / self-hosted) | `cypher_query`, `merge_node`, `create_relationship` |
| Obsidian URI scheme (via n8n HTTP node) | Write review-queue notes to vault |
| `czlonkowski/n8n-mcp` · `get_node_essentials` | Node config reference during authoring |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Entry point for iOS / Obsidian payloads |
| HTTP Request node | Obsidian URI write, external lookups |
| Code node (JS) | Payload normalization, Cypher query construction |
| Neo4j community node | Graph writes |
| AI Agent node (Sonnet) | Extraction and preprocessing |
| AI Agent node (Haiku) | Critical review |
| Set / Merge nodes | Data shaping between steps |
| Error Trigger | Route failures to Obsidian inbox |

---

## Claude Skills (n8n-skills)

- **Patterns** — orchestrator-worker pattern (Sonnet → Haiku)
- **Validation Expert** — catch Cypher field mismatches (known bug: `url` vs `youtube_url`)
- **Expression Syntax** — `$json`, `$node` variable access across agents
- **Tools Expert** — Neo4j node configuration

---

## Dependencies

| Dependency | Status |
|------------|--------|
| Neo4j (local Docker) | ✅ Live |
| n8n (local Docker) | ✅ Live |
| Obsidian vault `050926_vault` | ✅ Live |
| iOS Shortcut → Obsidian URI pipeline | 🔴 Gating dependency — not yet complete |
| Webhook pipeline (n8n) | 🟡 Planned next after iOS pipeline |
| Sprint 5 dual-agent validation layer | 🟡 Active, Cypher bugs recently fixed |
| `youtube_url` field fix | ✅ Fixed |
| `#` comment syntax fix | ✅ Fixed |

---

## Known Issues / Watch Items
- Deduplication logic needs tuning — MERGE on name alone risks false collapses
- Review queue in Obsidian needs a triage workflow (UC-1 feeds UC-3 Life Memory Archive)
- Neo4j MCP server: no production-ready public option — likely needs custom n8n HTTP node wrappers against the Neo4j REST/Bolt API

---

## Related UCs
- UC-2 Voice-to-Knowledge (primary ingest source)
- UC-3 Life Memory Archive (consumer of graph)
- UC-4 Likes/Dislikes Graph (specialised subgraph)
- UC-6 Ayla Assistant (queries graph at runtime)
