# UC-21 · Agent Ecosystem Framework
**Cluster:** Open Source  
**Status:** 🔴 Not Started — conceptual  
**Layer:** L2 Agent Runtime / L3 Workflow & Integration

---

## Purpose
Open-source reference framework for building personal AI agent ecosystems — documenting the Ayla architecture, patterns, tooling choices, and lessons learned. Designed to be a community resource for individuals building local-first, self-hosted agent stacks. The public expression of the PCA (Personal Cognitive Architecture) system.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | Author (James) publishes new pattern or architectural decision |
| Schedule | Periodic automated doc generation from Ayla stack state |
| Event-driven | New UC completed → auto-generate UC profile doc |

---

## Agent Flow

```
[Authoring Trigger — manual or automated]
    │
    ▼
[Context Collector — n8n]
  • Pull current UC status from Neo4j
  • Pull recent architectural decisions from Obsidian ADR notes
  • Pull n8n workflow inventory (list_workflows via n8n-mcp)
    │
    ▼
[Documentation Agent — Sonnet T=0.3]
  • Generate / update framework documentation:
    - Architecture overview (5-layer model)
    - UC catalogue with status
    - Pattern library (orchestrator-worker, monitor-alert, etc.)
    - Tooling choices and rationale
    - Lessons learned log
    │
    ▼
[Review Agent — Haiku T=0.8]
  • Check for inconsistencies with known architectural decisions
  • Flag outdated references
  • Validate that rejected tools (DeerFlow, MongoDB, etc.) are correctly documented as exclusions
    │
    ▼
[Output]
  ├──▶ GitHub repo markdown (via GitHub API / MCP)
  │      • README, /docs/, /patterns/, /uc-catalogue/
  ├──▶ Obsidian vault sync (personal reference copy)
  └──▶ Optional: static site generation (GitHub Pages)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `list_workflows` | Pull current workflow inventory for UC status |
| `n8n-mcp` · `create_workflow` | Author documentation pipeline |
| GitHub MCP (read) | Pull current repo state |
| GitHub API (HTTP node + PAT) | Write docs to repo (PAT-based HTTPS — OAuth write limitation) |
| Neo4j (HTTP node) | Pull UC status, architectural decisions |
| Obsidian URI / webhook | Sync to personal vault |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Manual / Webhook trigger | Doc generation trigger |
| Schedule trigger | Periodic automated refresh |
| HTTP Request node | GitHub API (PAT), Neo4j, Obsidian |
| AI Agent node (Sonnet) | Documentation generation |
| AI Agent node (Haiku) | Consistency review |
| Code node (JS) | Markdown assembly, frontmatter, GitHub API payload |
| Set / Merge nodes | Combine context sources |

---

## Claude Skills (n8n-skills)

- **Patterns** — context-gather → generate → review → publish
- **Expression Syntax** — GitHub API payload construction
- **Validation Expert** — doc consistency checking against decision log

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| GitHub repo (`jjuniper-dev/personal-cognitive-architecture`) | ✅ Exists |
| GitHub PAT (HTTPS write access) | ✅ Workaround confirmed |
| Neo4j (UC status store) | 🟡 In Progress |
| Obsidian vault | ✅ Live |
| UC profiles (this document set) | 🟡 In Progress (current session) |
| Architectural decision log in Obsidian | 🔴 Not yet formalised |

---

## Open Source Considerations
- The framework docs must be honest about rejected tools and why — the exclusion rationale (DeerFlow, MongoDB, etc.) is as valuable as the inclusion choices
- Versioning: tag framework releases to match Ayla sprint milestones
- Community contribution model: define before opening to PRs — likely "reference implementation only, forks encouraged" model to avoid scope creep

---

## Known Issues / Watch Items
- This UC is self-referential — it documents the system that generates it. Prioritise getting Ayla stable before investing in framework publishing
- GitHub OAuth write limitation is already documented and worked around (PAT-based HTTPS) — apply same pattern here
- Static site generation: `jjuniper-dev/status-site` (IBM Plex / dark teal) could serve as companion dashboard — link from framework README

---

## Related UCs
- All UCs (framework documents the entire stack)
- UC-01 Knowledge Graph (UC status as graph data)
- UC-06 Ayla Assistant (Ayla is the primary subject of the framework)
- UC-32 Automated Briefing Generation (framework updates as briefing items)
