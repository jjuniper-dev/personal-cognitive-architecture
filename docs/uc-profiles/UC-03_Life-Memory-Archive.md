# UC-03 · Life Memory Archive
**Cluster:** Personal Knowledge  
**Status:** 🔴 Not Started — depends on UC-01 and UC-02 being stable  
**Layer:** L1 Knowledge & Control

---

## Purpose
Build a searchable, time-indexed personal memory archive — a structured record of life events, decisions, relationships, and experiences drawn from all capture sources. The long-term episodic memory layer of the Ayla ecosystem, distinct from the semantic knowledge graph (UC-01).

---

## Trigger
| Type | Source |
|------|--------|
| Event-driven | UC-01 graph write → emits memory-candidate event |
| Schedule | Nightly batch — promote high-significance nodes to archive |
| Manual | Direct Obsidian note tagged `#memory` → webhook pickup |

---

## Agent Flow

```
[Memory Candidate Input]
  (from UC-01 graph events, UC-02 transcripts, manual tags)
    │
    ▼
[Significance Scorer — Haiku T=0.5]
  • Score 1–10 on personal significance
  • Classify: event / decision / relationship / milestone / reflection
  • Check for duplicates against archive index
    │
    ├─[Score < 4]──▶ [Discard / tag as ephemeral in graph]
    │
    └─[Score ≥ 4]──▶ [Memory Structuring Agent — Sonnet T=0.3]
                        • Generate memory record:
                          - date, location (if known)
                          - people involved
                          - summary narrative
                          - emotion/tone tag
                          - linked Neo4j node IDs
                        │
                        ▼
                      [Obsidian Write]
                        • /memory/YYYY/MM/YYYYMMDD-{slug}.md
                        • Frontmatter: date, type, people, significance
                        • Body: narrative + linked entities
                        │
                        ▼
                      [Neo4j — update node]
                        • Mark source node as archived
                        • Add `memory_id` property linking back to note
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author archive pipeline |
| `n8n-mcp` · `search_nodes` | Find scheduling, webhook, Neo4j nodes |
| Neo4j (HTTP node) | Read candidate nodes, write archive links |
| Obsidian URI / webhook | Write memory notes to vault |
| UC-01 webhook (internal) | Receive memory candidate events |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive candidates from UC-01 |
| Schedule trigger | Nightly batch run |
| AI Agent node (Haiku) | Significance scoring |
| AI Agent node (Sonnet) | Memory record structuring |
| Code node (JS) | Frontmatter generation, date formatting, path construction |
| If / Switch nodes | Route by significance score |
| HTTP Request node | Neo4j REST, Obsidian URI |
| Set node | Assemble final memory record payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — event-driven with scoring gate (filter → enrich → write)
- **Validation Expert** — frontmatter schema consistency
- **Expression Syntax** — date/time formatting in `$json`, path construction

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-01 Knowledge Graph (event emitter) | 🟡 In Progress |
| UC-02 Voice-to-Knowledge (input source) | 🔴 Not Started |
| Neo4j (local Docker) | ✅ Live |
| Obsidian vault + write pipeline | 🟡 URI live, webhook planned |
| n8n (local Docker) | ✅ Live |
| Archive schema / note template defined | 🔴 Not yet defined |

---

## Known Issues / Watch Items
- Significance scoring is subjective — prompt needs calibration with real examples before relying on Haiku
- Deduplication against existing archive needs a fast index (consider a Neo4j `Archive` node type as lookup before vault write)
- Privacy consideration: archive notes contain personal episodic data — ensure vault encryption and no cloud sync of `/memory/` path beyond Obsidian Sync (E2E encrypted)

---

## Related UCs
- UC-01 Knowledge Graph (primary source)
- UC-02 Voice-to-Knowledge (input)
- UC-04 Likes/Dislikes Graph (emotional/preference layer feeds archive context)
- UC-06 Ayla Assistant (queries archive for personal context in conversations)
