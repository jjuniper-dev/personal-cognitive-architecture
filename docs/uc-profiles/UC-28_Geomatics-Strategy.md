# UC-28 · Geomatics Strategy
**Cluster:** Enterprise Architecture  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control

---

## Purpose
Support the development and maintenance of HC/PHAC's geomatics and GeoAI strategy — tracking spatial data assets, geomatics platform options, GeoAI capability mapping, and alignment with the broader data architecture. Specialist EA domain within the HC/PHAC portfolio.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | Geomatics strategy document authoring or review |
| Event-driven | New spatial platform or GeoAI capability identified |
| Schedule | Quarterly geomatics landscape scan |

---

## Agent Flow

```
[Geomatics Input / Strategy Query]
    │
    ▼
[Geomatics Context Assembler — n8n]
  • Pull relevant HC/PHAC spatial data assets from CORE / Google Drive
  • Pull GeoAI capability rows from UC-25 framework
  • Pull platform options: ArcGIS Online, Azure Maps, QGIS, StatCan geodata
    │
    ▼
[Strategy Agent — Sonnet T=0.3]
  • Analyse: current state vs. target state for spatial capabilities
  • Identify: GeoAI opportunities (epidemiological signal mapping,
    environmental health surveillance, facility proximity analysis)
  • Align to: HC/PHAC data architecture, PATH/HAIL stack, Protected B requirements
  • Generate: strategy brief, capability gap analysis, platform recommendation
    │
    ▼
[Review Agent — Haiku T=0.8]
  • Challenge platform recommendations against GC procurement constraints
  • Flag: SSC dependency, Protected B data residency, licensing risks
    │
    ▼
[Output]
  ├──▶ Google Drive: strategy document or brief update
  ├──▶ Obsidian: /ea/geomatics/TOPIC.md
  └──▶ UC-25 Capability Framework: update GeoAI capability rows
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Strategy document read/write |
| `n8n-mcp` · `create_workflow` | Author geomatics research pipeline |
| UC-25 capability reference | GeoAI capability rows |
| UC-23 EA Agent | Framework alignment check |
| Obsidian URI / webhook | Strategy note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Strategy query input |
| AI Agent node (Sonnet) | Strategy analysis and document generation |
| AI Agent node (Haiku) | Critical review |
| HTTP Request node | Google Drive, Neo4j, Obsidian |
| Code node (JS) | Capability gap matrix assembly |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| Google Drive MCP | ✅ Connected |
| UC-25 AI Capability Framework (GeoAI rows) | 🟡 In Progress |
| UC-23 Virtual EA Agent | 🔴 Not Started |
| Geomatics platform landscape research | 🔴 Not yet done |

---

## Known Issues / Watch Items
- GeoAI + Protected B: spatial data often includes sensitive health or location data — Protected B classification requirements apply; flag in every capability row
- ArcGIS Online: ESRI's GC licensing through SSC; procurement path is known but slow — document current state clearly
- StatCan geodata: excellent free source for Canadian spatial reference data — incorporate as a standard source
- This UC has direct overlap with UC-29 AI-Enabled Surveillance & GeoAI — coordinate scope boundaries

---

## Related UCs
- UC-25 AI Capability Framework (GeoAI capability rows)
- UC-23 Virtual EA Agent (framework context)
- UC-29 AI-Enabled Surveillance & GeoAI (data & platform strategy counterpart)
