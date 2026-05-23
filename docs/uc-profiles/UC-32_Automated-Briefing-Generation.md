# UC-32 · Automated Briefing Generation
**Cluster:** Knowledge Publishing  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime / L3 Workflow & Integration

---

## Purpose
Automate the generation of structured briefing documents — for senior leadership (ADM/DM level), ARB, and TPO audiences — drawing from the EA knowledge base, use case tracker, platform status, and governance gate data. Reduces manual briefing prep time significantly.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Weekly — generate status briefing for Chad / leadership |
| Manual | On-demand briefing for specific topic or audience |
| Event-driven | Major governance decision → generate decision brief |

---

## Agent Flow

```
[Briefing Request — scheduled or manual]
  Parameters: audience (ADM / ARB / TPO), topic, time period
    │
    ▼
[Context Assembler — n8n]
  • UC-26 Use Case Tracker: status updates, new submissions, dispositions
  • UC-25 Capability Framework: capability changes
  • UC-31 Governance Support: recent ARB decisions, gate completions
  • UC-07 News Briefing: relevant AI policy / tech developments
  • UC-05 AI Talks: relevant insights from recent talks
    │
    ▼
[Briefing Agent — Sonnet T=0.3]
  • Select relevant content for specified audience
  • Apply briefing format:
    ADM: 1-page, terse, risk-flagged, action items
    ARB: structured submission format, technical depth
    TPO: operational status, platform alignment, dependencies
  • Apply HC/PHAC EA style (Arial, professional, neutral tone)
  • Apply correct framing (no overselling, "pending alignment" language)
    │
    ▼
[Review Agent — Haiku T=0.8]
  • Check: audience-appropriate depth
  • Flag: any optimistic framing
  • Verify: factual consistency with source data
    │
    ▼
[Output]
  ├──▶ Google Drive: briefing document (DOCX via python-docx or Google Docs API)
  ├──▶ Obsidian: /ea/briefings/YYYYMMDD-AUDIENCE.md
  └──▶ UC-06 Ayla: confirm generation and share link
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Upload briefing document |
| `n8n-mcp` · `create_workflow` | Author briefing pipeline |
| UC-26 tracker data | Use case status |
| UC-31 governance data | ARB decisions |
| UC-25 capability data | Capability updates |
| Neo4j (HTTP node) | Aggregate status queries |
| Obsidian URI / webhook | Briefing note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Weekly briefing run |
| Webhook trigger | On-demand briefing request |
| AI Agent node (Sonnet) | Briefing generation |
| AI Agent node (Haiku) | Review |
| HTTP Request node | All data sources, Google Drive, Obsidian |
| Code node (JS) | Audience-specific format selection, content filtering |
| Switch node | Route by audience type |
| Set node | Briefing payload assembly |

---

## Claude Skills (n8n-skills)

- **Patterns** — context-gather → audience-filter → generate → review → publish
- **Expression Syntax** — conditional content selection by audience parameter
- **Validation Expert** — briefing format compliance, factual cross-check

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-26 AI Use Case Tracker | 🔴 Not Started |
| UC-31 Architecture Governance Support | 🔴 Not Started |
| UC-25 AI Capability Framework | 🟡 In Progress |
| UC-07 News Briefing (personal — AI policy feed) | 🟡 Migration in progress |
| Google Drive MCP | ✅ Connected |
| HC/PHAC DOCX template / style | ✅ Arial, teal/green — known |
| python-pptx limitation | ⚠️ Cannot reliably edit existing PPTX — use Google Docs API or Markdown for briefings |

---

## Known Issues / Watch Items
- python-pptx cannot reliably edit existing PPTX — generate briefings as Google Docs or Markdown; convert manually if PPTX needed
- ADM briefings are highest-stakes output — always route through human review before delivery; agent generates draft only
- Framing discipline: briefing agent must have the ARB risk profile and "pending alignment" framing hardcoded in its system prompt
- Weekly cadence: align with Chad's reporting rhythm — confirm preferred delivery day/format

---

## Related UCs
- UC-26 AI Use Case Tracker (primary data source)
- UC-31 Architecture Governance Support (governance data)
- UC-25 AI Capability Framework (capability data)
- UC-07 News Briefing (AI policy feed)
- UC-33 Presentation & Diagram Generation (visual output complement)
