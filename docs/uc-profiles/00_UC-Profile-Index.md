# Ayla UC Profiles — Index
**Generated:** 2026-05-23  
**Scope:** Personal Knowledge (UC 1–5), Automation (UC 6–10), Open Source (UC 19–22)  
**Format:** Full profile per UC — trigger, agent flow, MCP tools, n8n skills, Claude skills, dependencies, known issues

---

## Status Legend
| Symbol | Meaning |
|--------|---------|
| ✅ | Live / Complete |
| 🟡 | In Progress / Partial |
| 🔴 | Not Started / Blocked |

---

## Cluster 1 · Personal Knowledge

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-01_Knowledge-Graph]] | Knowledge Graph | 🟡 In Progress | iOS capture pipeline (gating) |
| [[UC-02_Voice-to-Knowledge]] | Voice-to-Knowledge | 🔴 Not Started | iOS Shortcut → webhook |
| [[UC-03_Life-Memory-Archive]] | Life Memory Archive | 🔴 Not Started | UC-01 stable |
| [[UC-04_Likes-Dislikes-Graph]] | Likes / Dislikes Graph | 🔴 Not Started | UC-01 + UC-06 |
| [[UC-05_AI-Talks]] | AI Talks | 🔴 Not Started | Whisper + UC-01 |

---

## Cluster 2 · Automation

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-06_Ayla-Assistant]] | Ayla Assistant | 🟡 Architecture defined | OpenClaw/NanoClaw L2 gateway |
| [[UC-07_News-Briefing]] | News Briefing | 🟡 Migrating Zapier → n8n | n8n migration |
| [[UC-08_Democracy-Monitor]] | Democracy Monitor | 🔴 Not Started | Parliament API mapping |
| [[UC-09_Space-Watch]] | Space-Watch | 🔴 Not Started | UC-07 stable first |
| [[UC-10_Exposure-Monitor]] | Exposure Monitor | 🔴 Not Started | HIBP paid API |

---

## Cluster 5 · Open Source

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-19_AliasGuard-OSINT]] | AliasGuard OSINT | 🔴 Not Started | UC-10 as POC first |
| [[UC-20_State-of-Democracy-Tracker]] | State of Democracy Tracker | 🔴 Not Started | UC-08 + shared schema |
| [[UC-21_Agent-Ecosystem-Framework]] | Agent Ecosystem Framework | 🔴 Not Started | Ayla stack stable |
| [[UC-22_Music-Knowledge-Base]] | Music Knowledge Base | 🔴 Not Started | Neo4j schema design |

---

## Cross-Cutting Observations

### Shared Infrastructure
All UCs in this set depend on:
- n8n (local Docker) ✅
- Neo4j (local Docker) ✅
- Obsidian vault `050926_vault` ✅
- Tailscale mesh ✅
- iOS capture pipeline 🔴 (gating UC-01, UC-02, UC-03)

### Dominant Agent Patterns
| Pattern | UCs |
|---------|-----|
| Orchestrator-Worker (Sonnet → Haiku) | UC-01, UC-06 |
| Sequential pipeline | UC-02, UC-05, UC-07 |
| Monitor-detect-alert | UC-08, UC-09, UC-10 |
| Fan-out collection → aggregate → enrich | UC-19, UC-20, UC-22 |
| Context-gather → generate → publish | UC-21 |

### Personal → Open Source Pairs
| Personal UC | Open Source UC | Shared Concern |
|-------------|----------------|----------------|
| UC-08 Democracy Monitor | UC-20 State of Democracy Tracker | Schema — define once |
| UC-10 Exposure Monitor | UC-19 AliasGuard OSINT | Identity model |
| UC-06 Ayla Architecture | UC-21 Agent Ecosystem Framework | Documentation |

### Critical Path (recommended build order)
1. iOS capture pipeline → unblocks UC-01, UC-02, UC-03
2. UC-07 News Briefing migration (Zapier → n8n) — quick win, already partially built
3. UC-01 Knowledge Graph stable → unblocks UC-03, UC-04, UC-05
4. UC-06 Ayla Assistant routing layer → unblocks lifestyle and automation UCs
5. UC-08 + UC-10 (personal monitors) → before open-source counterparts UC-19, UC-20
6. UC-22 Music KB — independent, can be built in parallel once Neo4j schema is settled
7. UC-21 Agent Ecosystem Framework — last; documents what's been built

### MCP Tool Stack (shared across all UCs)
- `czlonkowski/n8n-mcp` — workflow authoring (primary)
- `czlonkowski/n8n-skills` — Claude Code skills for n8n pattern guidance
- Neo4j HTTP node (custom wrappers) — no production MCP server available
- Obsidian URI scheme → n8n HTTP node (vault write)
- GitHub API + PAT HTTPS (OAuth write limitation workaround)

---

## Remaining Clusters (not yet profiled)
- Lifestyle (UC 11–14)
- Finance (UC 15–18)
- Enterprise Architecture (UC 23–28)
- Data & Platform Strategy (UC 29–31)
- Knowledge Publishing (UC 32–34)
