# UC-29 · Data Architecture Playbook
**Cluster:** Data & Platform Strategy  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control

---

## Purpose
Develop and maintain HC/PHAC's data architecture playbook — principles, patterns, platform decisions, and implementation guidance covering the Databricks vs. Fabric question, Purview data governance, Entra ID, and the PATH + HAIL + Purview convergence target state. The canonical reference for data architecture decisions.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | New platform decision or pattern to document |
| Event-driven | ARB submission touches data architecture → update playbook |
| Schedule | Quarterly platform landscape refresh |

---

## Agent Flow

```
[Playbook Input / Platform Query]
    │
    ▼
[Platform Context Assembler — n8n]
  • Pull current platform state from CORE / Google Drive
  • Pull Neo4j: platform nodes, capability relationships, decision log
  • Pull recent Microsoft Learn content on Fabric, Purview, Entra (MS Learn MCP)
    │
    ▼
[Architecture Agent — Sonnet T=0.3]
  • Analyse: current state (Databricks vs. Fabric fragmentation)
  • Document: target state (PATH + HAIL + Purview + Entra convergence)
  • Generate: pattern documentation, decision rationale, implementation guidance
  • Apply: Azure-as-infrastructure framing (not AI platform — foundational service layer)
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge: is this a pattern or a capability? (SIG precedent — always ask)
  • Flag: coordination gaps (multiple teams, no unified execution model)
  • Verify: Protected B data residency compliance in all platform references
    │
    ▼
[Output]
  ├──▶ Google Drive: playbook document update
  ├──▶ Obsidian: /ea/data-architecture/PATTERN.md
  └──▶ Neo4j: Platform and Pattern nodes updated
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Playbook document read/write |
| Microsoft Learn MCP | Fabric, Purview, Entra documentation |
| Neo4j (HTTP node) | Platform and decision graph |
| UC-23 EA Agent | Framework alignment check |
| Obsidian URI / webhook | Pattern note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Platform query or update |
| AI Agent node (Sonnet) | Architecture documentation |
| AI Agent node (Haiku) | Critical review |
| HTTP Request node | Google Drive, MS Learn, Neo4j, Obsidian |
| Code node (JS) | Pattern template generation |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| Google Drive MCP | ✅ Connected |
| Microsoft Learn MCP | ✅ Connected |
| Neo4j (platform graph) | 🟡 Shared stack |
| CORE project reference (platform decisions) | 🟡 In Progress |

---

## Architectural Context (Critical)
- **Azure in GC/SSC context:** foundational infrastructure and service layer, not an enterprise AI platform
- **HC/PHAC consumption:** HAIL (runtime) and PATH (target control plane, Protected B)
- **Real platform:** emerges from PATH + HAIL + Purview + Entra ID convergence
- **Key gap:** Databricks vs. Fabric fragmentation; multiple teams, no unified execution model — Azure provides capability, not coordination or governance
- **Purview:** emerging as data governance layer — not yet mature in HC/PHAC deployment
- Every playbook entry must reflect this framing — no "Azure as AI platform" language

---

## Related UCs
- UC-23 Virtual EA Agent (knowledge consumer)
- UC-25 AI Capability Framework (platform-capability mapping)
- UC-30 AI-Enabled Surveillance & GeoAI (domain application)
- UC-31 Architecture Governance Support (governance overlay)
