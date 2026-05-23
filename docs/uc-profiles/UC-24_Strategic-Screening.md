# UC-24 · Strategic Screening
**Cluster:** Enterprise Architecture  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime / L3 Workflow & Integration

---

## Purpose
Automated screening of incoming IT investment proposals, project requests, and architectural submissions against HC/PHAC EA principles, GC frameworks, and the AI governance decision gates. Produces structured intake assessments for the ARB / TPO / CDO audiences.

---

## Trigger
| Type | Source |
|------|--------|
| Document upload | IT investment proposal or project brief submitted |
| Manual | James submits a document for screening via Claude Project |
| Schedule | Batch processing of 26-27 IT investment cycle submissions |

---

## Agent Flow

```
[Document Input — PDF / DOCX / text]
    │
    ▼
[Screening Agent — Sonnet T=0.3]
  • Extract: project name, branch, cluster, spend estimate, technology stack
  • Map to 9-cluster IT investment taxonomy
  • Identify: AI components, data handling, cloud services, vendor lock-in risk
    │
    ▼
[Framework Alignment Checker — Sonnet T=0.3]
  • Check against: DADM, AIA, PIA, SA&A, GBA+, Privacy Act
  • Check against: 9 AI governance decision gates
  • Check against: PATH/HAIL platform alignment
  • Identify gaps and compliance risks
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge screening conclusions
  • Flag: optimistic assumptions, missing frameworks, timeline compression
  • Apply ARB risk lens (known risk profile: PATH/HAIL, SIG pattern, governance gaps)
    │
    ▼
[Assessment Report Generator — Sonnet T=0.3]
  • Produce structured ARB intake assessment:
    - Executive summary (2–3 sentences)
    - Cluster classification
    - Framework gap analysis
    - Risk flags
    - Recommended ARB disposition
  • Output in HC/PHAC EA style (Arial, professional tone)
    │
    ▼
[Output]
  ├──▶ Obsidian: /ea/screening/PROJECT-NAME.md
  └──▶ Google Drive: upload assessment to CORE folder
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Upload assessment, read submission docs |
| Neo4j (HTTP node) | Framework and taxonomy reference |
| UC-23 EA Agent (internal) | Framework lookup worker |
| Obsidian URI / webhook | Assessment note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Document submission |
| AI Agent node (Sonnet) | Screening + alignment check + report generation |
| AI Agent node (Haiku) | Critical review |
| HTTP Request node | Neo4j, Google Drive, Obsidian |
| Code node (JS) | Cluster classification logic, report formatting |
| Set node | Assessment payload assembly |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| CORE project reference (taxonomy, frameworks) | 🟡 In Progress |
| Google Drive MCP | ✅ Connected |
| 9-cluster IT investment taxonomy (finalised) | ✅ Cluster Dictionary finalised |
| 9 AI governance decision gates | ✅ Defined in TBS governance briefing |
| Neo4j (framework reference store) | 🟡 Shared stack |

---

## Known Issues / Watch Items
- 63-row IT investment review already completed manually — this UC automates future cycles
- Timeline estimate accuracy: current ARB submissions tend to be 2–5× optimistic — screening agent must apply a correction heuristic
- AutoResearch for autonomous compliance validation is explicitly flagged as lacking formal assurance alignment — do not auto-publish screening assessments without human review

---

## Related UCs
- UC-23 Virtual EA Agent (framework knowledge source)
- UC-25 AI Capability Framework (platform alignment reference)
- UC-26 AI Use Case Tracker HC (tracks screened projects)
