# Ayla UC Profiles — Index
**Generated:** 2026-05-23  
**Scope:** All 34 UCs across 8 clusters  
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

## Cluster 3 · Lifestyle

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-11_Weekend-Events-Ottawa]] | Weekend Events Ottawa | 🔴 Not Started | Eventbrite API + UC-04 |
| [[UC-12_Event-Voting]] | Event Voting | 🔴 Not Started | UC-11 live |
| [[UC-13_Lifestyle-Concierge]] | Lifestyle Concierge | 🔴 Not Started | UC-04 + UC-11 + UC-03 |
| [[UC-14_Birthday-Planning]] | Birthday Planning | 🔴 Not Started | UC-01 person data |

---

## Cluster 4 · Finance

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-15_Budget-Automation]] | Budget Automation | 🔴 Not Started | UC-16 (gating) |
| [[UC-16_Transaction-Import]] | Transaction Import | 🔴 Not Started | Bank connectivity decision |
| [[UC-17_Financial-Alerts]] | Financial Alerts | 🔴 Not Started | UC-16 (gating) |
| [[UC-18_Net-Worth-Tracking]] | Net Worth Tracking | 🔴 Not Started | UC-16 + investment APIs |

---

## Cluster 5 · Open Source

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-19_AliasGuard-OSINT]] | AliasGuard OSINT | 🔴 Not Started | UC-10 as POC first |
| [[UC-20_State-of-Democracy-Tracker]] | State of Democracy Tracker | 🔴 Not Started | UC-08 + shared schema |
| [[UC-21_Agent-Ecosystem-Framework]] | Agent Ecosystem Framework | 🔴 Not Started | Ayla stack stable |
| [[UC-22_Music-Knowledge-Base]] | Music Knowledge Base | 🔴 Not Started | Neo4j schema design |

---

## Cluster 6 · Enterprise Architecture

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-23_Virtual-EA-Agent]] | Virtual EA Agent | 🔴 Not Started | CORE reference folder |
| [[UC-24_Strategic-Screening]] | Strategic Screening | 🔴 Not Started | CORE + UC-23 |
| [[UC-25_AI-Capability-Framework]] | AI Capability Framework | 🟡 In Progress | Spreadsheet v2.x active |
| [[UC-26_AI-Use-Case-Tracker-HC]] | AI Use Case Tracker HC | 🔴 Not Started | UC-24 + UC-25 |
| [[UC-27_AI-Learning-Path]] | AI Learning Path | 🔴 Not Started | MS Learn MCP + feeds |
| [[UC-28_Geomatics-Strategy]] | Geomatics Strategy | 🔴 Not Started | UC-25 GeoAI rows |

---

## Cluster 7 · Data & Platform Strategy

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-29_Data-Architecture-Playbook]] | Data Architecture Playbook | 🔴 Not Started | CORE + MS Learn MCP |
| [[UC-30_AI-Enabled-Surveillance-GeoAI]] | AI-Enabled Surveillance & GeoAI | 🔴 Not Started | UC-28 + UC-29 |
| [[UC-31_Architecture-Governance-Support]] | Architecture Governance Support | 🔴 Not Started | UC-24 + UC-26 |

---

## Cluster 8 · Knowledge Publishing

| UC | Name | Status | Key Dependency |
|----|------|--------|---------------|
| [[UC-32_Automated-Briefing-Generation]] | Automated Briefing Generation | 🔴 Not Started | UC-26 + UC-31 |
| [[UC-33_Presentation-Diagram-Generation]] | Presentation & Diagram Generation | 🔴 Not Started | Mermaid MCP + UC-23 |
| [[UC-34_Content-Conversion-SharePoint-Web]] | Content Conversion for SharePoint/Web | 🔴 Not Started | M365 MCP + UC-32 |

---

## Cross-Cutting Observations

### Shared Infrastructure (all UCs)
- n8n (local Docker) ✅
- Neo4j (local Docker) ✅
- Obsidian vault `050926_vault` ✅
- Tailscale mesh ✅
- iOS capture pipeline 🔴 (gating UC-01, 02, 03)

### Connected MCP Tools (ready now)
| MCP | Connected UCs |
|-----|--------------|
| Google Drive MCP | UC-23–26, 28–34 |
| Microsoft 365 MCP | UC-34 |
| Microsoft Learn MCP | UC-27, 29 |
| Google Calendar MCP | UC-13, 14 |
| Mermaid Chart MCP | UC-33 |

### Dominant Agent Patterns
| Pattern | UCs |
|---------|-----|
| Orchestrator-Worker (Sonnet → Haiku) | UC-01, 06, 23, 24, 31 |
| Scheduled batch digest | UC-07, 11, 27, 32 |
| Monitor-detect-alert | UC-08, 09, 10, 15, 17 |
| Fan-out collect → aggregate → enrich | UC-05, 19, 20, 22 |
| Context-gather → generate → publish | UC-13, 21, 29, 33, 34 |
| Sequential pipeline | UC-02, 16 |
| Stateful lifecycle tracker | UC-14, 18, 26 |

### Personal → Open Source Pairs
| Personal | Open Source | Shared Concern |
|----------|-------------|----------------|
| UC-08 Democracy Monitor | UC-20 State of Democracy Tracker | Schema — define once |
| UC-10 Exposure Monitor | UC-19 AliasGuard OSINT | Identity model |
| UC-06 Ayla Architecture | UC-21 Agent Ecosystem Framework | Documentation |

### Finance Cluster Critical Path
UC-16 Transaction Import is the single gating dependency for the entire Finance cluster. Bank connectivity method decision (SimpleFIN / Flinks / CSV) must be made before any Finance UC can be built.

### EA Cluster Data Sensitivity
UCs 23–34 operate on HC/PHAC professional data. All EA UCs must remain within the Claude.ai HC/PHAC EA Practice Project boundary until SA&A is complete. No HC/PHAC data through personal n8n instance.

### Recommended Build Order (full stack)
**Phase 1 — Infrastructure & quick wins**
1. iOS capture pipeline (unblocks UC-01, 02, 03)
2. UC-07 News Briefing Zapier → n8n migration
3. UC-16 Transaction Import (bank connectivity decision first)

**Phase 2 — Personal core**
4. UC-01 Knowledge Graph (stable)
5. UC-06 Ayla Assistant routing layer
6. UC-17 Financial Alerts (simplest Finance UC)
7. UC-15 Budget Automation

**Phase 3 — Personal enrichment**
8. UC-02 Voice-to-Knowledge
9. UC-04 Likes/Dislikes Graph
10. UC-11 Weekend Events Ottawa
11. UC-22 Music Knowledge Base (parallel)

**Phase 4 — Personal completion**
12. UC-03 Life Memory Archive
13. UC-05 AI Talks
14. UC-08 Democracy Monitor + UC-10 Exposure Monitor
15. UC-12, 13, 14 Lifestyle cluster
16. UC-18 Net Worth Tracking

**Phase 5 — EA practice**
17. UC-25 AI Capability Framework (automation layer)
18. UC-23 Virtual EA Agent + CORE
19. UC-24 Strategic Screening → UC-26 Use Case Tracker
20. UC-31 Governance Support → UC-32 Briefing Generation

**Phase 6 — Open source & publishing**
21. UC-19 AliasGuard, UC-20 Democracy Tracker
22. UC-21 Agent Ecosystem Framework
23. UC-33 Diagram Generation → UC-34 Content Conversion
24. UC-27 AI Learning Path, UC-28 Geomatics, UC-29–30 Platform Strategy
