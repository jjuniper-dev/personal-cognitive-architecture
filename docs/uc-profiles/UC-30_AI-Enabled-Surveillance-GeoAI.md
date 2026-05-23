# UC-30 · AI-Enabled Surveillance & GeoAI
**Cluster:** Data & Platform Strategy  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control / L3 Workflow & Integration

---

## Purpose
Define and document the AI-enabled public health surveillance and GeoAI architecture for HC/PHAC — covering epidemiological signal detection, spatial analytics, environmental health surveillance, and the platform architecture to support it. Bridges data architecture (UC-29) and geomatics strategy (UC-28) with operational surveillance systems.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | Surveillance architecture question or design session |
| Event-driven | New surveillance use case submitted (UC-24/26) → assess platform fit |
| Schedule | Quarterly surveillance platform landscape review |

---

## Agent Flow

```
[Surveillance Architecture Query / Design Input]
    │
    ▼
[Surveillance Context Assembler — n8n]
  • Pull: current HC/PHAC surveillance systems inventory (CORE / Google Drive)
  • Pull: GeoAI capability rows from UC-25
  • Pull: epidemiological signal detection patterns from UC-22 / literature
  • Pull: PATH/HAIL platform capabilities relevant to surveillance
    │
    ▼
[Architecture Agent — Sonnet T=0.3]
  • Map surveillance use cases to platform capabilities
  • Document: data flows (ingestion → signal detection → alert → response)
  • Identify: AI/ML components (anomaly detection, NLP on case reports,
    geospatial clustering, time-series forecasting)
  • Assess: Protected B data handling requirements per data type
  • Generate: architecture pattern or decision brief
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge: data sovereignty and residency assumptions
  • Flag: any AI component lacking SA&A, PIA, or AIA
  • Verify: GBA+ considerations for surveillance data populations
    │
    ▼
[Output]
  ├──▶ Google Drive: surveillance architecture brief
  ├──▶ Neo4j: SurveillanceSystem and GeoAICapability nodes
  ├──▶ Obsidian: /ea/surveillance/TOPIC.md
  └──▶ UC-25 Capability Framework: update relevant capability rows
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Document read/write |
| Microsoft Learn MCP | Azure health data, Maps, Synapse patterns |
| Neo4j (HTTP node) | Surveillance and GeoAI graph |
| UC-25 capability reference | Capability row updates |
| UC-28 Geomatics Strategy | Spatial platform alignment |
| Obsidian URI / webhook | Pattern note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Architecture query input |
| AI Agent node (Sonnet) | Architecture analysis and documentation |
| AI Agent node (Haiku) | Compliance and critical review |
| HTTP Request node | Google Drive, MS Learn, Neo4j, Obsidian |
| Code node (JS) | Data flow diagram generation, capability matrix |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| Google Drive MCP | ✅ Connected |
| Microsoft Learn MCP | ✅ Connected |
| UC-28 Geomatics Strategy | 🔴 Not Started |
| UC-25 AI Capability Framework | 🟡 In Progress |
| Surveillance systems inventory | 🔴 Not yet compiled in CORE |

---

## Known Issues / Watch Items
- Epidemiological signal detection is listed as an HC-specific net-new capability in UC-25 — this UC defines the platform architecture to deliver it
- PMRA as PATH second use case: surveillance/data platform alignment is directly relevant
- Protected B: all surveillance data involving identifiable health information is Protected B minimum — every architecture pattern must reflect this
- GBA+: surveillance population data has significant GBA+ implications — flag in every pattern that touches demographic or geographic data

---

## Related UCs
- UC-28 Geomatics Strategy (spatial platform)
- UC-29 Data Architecture Playbook (platform foundation)
- UC-25 AI Capability Framework (capability mapping)
- UC-31 Architecture Governance Support (governance overlay)
