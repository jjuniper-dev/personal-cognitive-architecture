# UC-25 · AI Capability Framework
**Cluster:** Enterprise Architecture  
**Status:** 🟡 In Progress — spreadsheet v2.x active  
**Layer:** L1 Knowledge & Control

---

## Purpose
Maintain the HC/PHAC AI Capabilities Mapping — a structured taxonomy of AI capabilities aligned to the GC ACM taxonomy, BCM anchoring, and HC-specific additions. The canonical reference for AI capability classification across the organisation.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | New capability identified → add to mapping |
| Schedule | Quarterly review — validate and update capability statuses |
| Event-driven | New AI use case screened (UC-24) → check capability coverage |

---

## Agent Flow

```
[Capability Input / Review Trigger]
    │
    ▼
[Capability Classifier — Sonnet T=0.3]
  • Map to GC ACM taxonomy (L1/L2/L3)
  • Assign BCM anchor
  • Classify: existing / draft / net-new HC-specific
  • Apply EU AI Act risk class attribute
  • Check: governance horizontal row applicable?
    │
    ▼
[Gap Analyser — Haiku T=0.8]
  • Compare against existing 224-row mapping
  • Identify: duplicate, overlap, or genuine new capability
  • Flag: missing GBA+, missing PIA trigger, missing SA&A flag
    │
    ▼
[Spreadsheet Updater — Code node]
  • Generate row update for capability spreadsheet
  • Maintain: 29 Draft AI L3 capabilities placed
  • Maintain: Horizontal Governance section
  • Maintain: HC-specific capabilities
    (NLP redaction, regulatory submission intelligence,
     scientific literature triage, epidemiological signal detection,
     workforce analytics)
    │
    ▼
[Output]
  ├──▶ Google Drive: update capabilities spreadsheet
  ├──▶ Neo4j: MERGE Capability node with taxonomy attributes
  └──▶ Obsidian: /ea/capabilities/change-log.md
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Read/write capabilities spreadsheet |
| Neo4j (HTTP node) | Capability graph store |
| UC-23 EA Agent | Framework alignment check |
| Obsidian URI / webhook | Change log write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | New capability input |
| Schedule trigger | Quarterly review |
| AI Agent node (Sonnet) | Capability classification |
| AI Agent node (Haiku) | Gap analysis / critical review |
| HTTP Request node | Google Drive, Neo4j, Obsidian |
| Code node (JS) | Spreadsheet row generation, taxonomy mapping |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| AI Capabilities Mapping spreadsheet v2.x | ✅ Active — 224 rows, 29 Draft L3 |
| Google Drive MCP | ✅ Connected |
| GC ACM taxonomy | ✅ Reference available |
| BCM taxonomy | ✅ Anchored |
| EU AI Act risk-class attribute | ✅ Added to framework |
| HC-specific capability set | ✅ Defined (5 net-new) |
| Neo4j (capability graph) | 🟡 Shared stack |

---

## Known Issues / Watch Items
- python-pptx cannot reliably edit existing PPTX files — for PowerPoint output use claude.ai/design
- GC ACM taxonomy rubric lacks formal GC endorsement — note this explicitly in capability records
- ISO 42001 as QMS spine: recommended but not yet adopted — flag capabilities requiring QMS alignment
- EU AI Act August 2026 deadline: Article 27 FRIA should be integrated into AIA/PIA/GBA+ stack for applicable capabilities

---

## Related UCs
- UC-23 Virtual EA Agent (framework consumer)
- UC-24 Strategic Screening (platform alignment reference)
- UC-26 AI Use Case Tracker HC (use case to capability mapping)
