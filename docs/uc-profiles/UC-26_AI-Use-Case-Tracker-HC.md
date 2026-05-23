# UC-26 · AI Use Case Tracker (HC)
**Cluster:** Enterprise Architecture  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control / L3 Workflow & Integration

---

## Purpose
Track AI use cases across HC/PHAC branches — intake, classification, governance status, platform alignment, and disposition. Provides visibility into the 8-team AI demand currently approaching API endpoints independently, and supports ADM-level reporting.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | New use case submitted or identified |
| Event-driven | UC-24 Strategic Screening completes → register screened use case |
| Schedule | Weekly status update run |

---

## Agent Flow

```
[New Use Case Input]
    │
    ▼
[Use Case Intake Agent — Sonnet T=0.3]
  • Extract: branch, use case name, description, requestor, AI type, data sensitivity
  • Assign: cluster (9-cluster taxonomy), risk tier, governance gates required
  • Map to: HC/PHAC AI Capabilities Framework (UC-25)
    │
    ▼
[Status Tracker — Code node]
  • Maintain lifecycle state machine:
    Identified → Screened → ARB Submitted → ARB Approved →
    Platform Assigned → SA&A In Progress → Live → Deprecated
  • Compute: governance gate completion per use case
    │
    ▼
[Reporting Agent — Sonnet T=0.3]
  • Generate: weekly status summary for Chad / senior leadership
  • Format: ADM-ready, terse, risk-flagged
  • Highlight: stalled use cases, governance blockers, litigation risk items
    │
    ▼
[Output]
  ├──▶ Neo4j: UseCase node + status + relationships
  ├──▶ Google Drive: update tracker spreadsheet / CORE folder
  ├──▶ `jjuniper-dev/status-site`: dashboard update (PATH/HAIL tracking)
  └──▶ Obsidian: /ea/use-cases/BRANCH-UCNAME.md
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | Read/write tracker |
| GitHub API (HTTP + PAT) | Push status-site updates |
| Neo4j (HTTP node) | Use case graph |
| UC-24 webhook | Receive screened use cases |
| UC-25 capability reference | Map use cases to capabilities |
| Obsidian URI / webhook | Use case note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | New use case intake |
| Schedule trigger | Weekly status run |
| AI Agent node (Sonnet) | Intake classification + reporting |
| Code node (JS) | State machine logic, governance gate tracking |
| HTTP Request node | Neo4j, Google Drive, GitHub, Obsidian |
| Set node | Use case payload assembly |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| 9-cluster IT taxonomy | ✅ Finalised |
| UC-24 Strategic Screening | 🔴 Not Started |
| UC-25 AI Capability Framework | 🟡 In Progress |
| Google Drive MCP | ✅ Connected |
| `jjuniper-dev/status-site` | ✅ Live (IBM Plex / dark teal) |
| GitHub PAT (status-site updates) | 🟡 Single-use PAT pattern |
| Neo4j (use case graph) | 🟡 Shared stack |

---

## Known Issues / Watch Items
- 8 teams currently seeking API endpoints independently (flagged by FATAC as litigation risk) — this UC provides the visibility layer to manage that demand
- ADM reserve funding (Dan's push) and external implementer procurement: use case tracker data should inform that business case
- Radar 2.0 replacement (Isaac): flag as a tracked use case in this system
- Medical Device Shortages re-platforming: tracked use case
- VIAP: tracked use case through July 1 daily scrum
- ClamAV/Alinea stall: flag as governance-blocked use case

---

## Related UCs
- UC-23 Virtual EA Agent (knowledge consumer)
- UC-24 Strategic Screening (intake source)
- UC-25 AI Capability Framework (capability mapping)
- UC-32 Automated Briefing Generation (use case tracker as briefing source)
