# UC-31 · Architecture Governance Support
**Cluster:** Data & Platform Strategy  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime / L1 Knowledge & Control

---

## Purpose
Provide AI-assisted support for the architecture governance process — ARB preparation, submission drafting, risk profiling, and decision documentation. The operational governance layer that ties the EA practice deliverables to the four-body governance structure (OCDO, TPO, ARB, DTB).

---

## Trigger
| Type | Source |
|------|--------|
| Manual | ARB submission preparation, governance query |
| Event-driven | UC-24 screening flags ARB-bound use case → initiate ARB prep |
| Schedule | Weekly governance status review |

---

## Agent Flow

```
[ARB Prep / Governance Query]
    │
    ▼
[Governance Context Assembler — n8n]
  • Pull: use case profile from UC-26 tracker
  • Pull: screening assessment from UC-24
  • Pull: relevant capability rows from UC-25
  • Pull: applicable GC frameworks (DADM, AIA, PIA, SA&A, GBA+)
  • Pull: current PATH/HAIL platform status
    │
    ▼
[ARB Submission Agent — Sonnet T=0.3]
  • Draft or review ARB submission sections:
    - Business context and rationale
    - Technical architecture summary
    - Platform alignment (PATH/HAIL/Purview)
    - Risk identification and mitigation
    - Governance gate completion status
    - Recommendation for disposition
  • Apply known ARB risk profile:
    - PATH/HAIL convergence unresolved
    - SIG is a pattern not a capability
    - Governance is project-level not enterprise
    - Rubric lacks GC endorsement
    - Timeline estimates likely 2–5× optimistic
    │
    ▼
[Critical Review Agent — Haiku T=0.8]
  • Challenge: is anything being oversold?
  • Flag: missing governance gates, missing PIA triggers
  • Verify: correct framing ("structured decision framework pending alignment")
    │
    ▼
[Decision Documentation Agent — Sonnet T=0.3]
  • Document ADR (Architecture Decision Record) for approved decisions
  • Update: UC-26 tracker with ARB disposition
  • Generate: ADM-ready briefing note if required
    │
    ▼
[Output]
  ├──▶ Google Drive: ARB submission draft / ADR
  ├──▶ Neo4j: GovernanceDecision node + ARB disposition
  ├──▶ Obsidian: /ea/governance/ARB-UCNAME.md
  └──▶ `jjuniper-dev/status-site`: ARB status dashboard update
```

---

## MCP Tools

| Tool | Role |
|------|------|
| Google Drive MCP | ARB document read/write |
| GitHub API (HTTP + PAT) | Status-site ARB status update |
| Neo4j (HTTP node) | Governance decision graph |
| UC-23 EA Agent | Framework knowledge |
| UC-24 screening output | Use case risk profile |
| UC-26 tracker | Use case status |
| Obsidian URI / webhook | ADR note write |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | ARB prep initiation |
| Schedule trigger | Weekly governance status |
| AI Agent node (Sonnet) | ARB drafting + ADR documentation |
| AI Agent node (Haiku) | Critical review |
| HTTP Request node | Google Drive, Neo4j, GitHub, Obsidian |
| Code node (JS) | Governance gate completion matrix |
| Set node | ARB submission payload |

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| Google Drive MCP | ✅ Connected |
| UC-24 Strategic Screening | 🔴 Not Started |
| UC-25 AI Capability Framework | 🟡 In Progress |
| UC-26 AI Use Case Tracker | 🔴 Not Started |
| `jjuniper-dev/status-site` | ✅ Live |
| TBS governance briefing package (9 decision gates) | ✅ Produced |
| Four-body governance structure knowledge | ✅ Known (OCDO, TPO, ARB, DTB) |

---

## Known Issues / Watch Items
- The ARB risk profile is well-understood and must be hardcoded as a standing check: PATH/HAIL convergence, SIG framing, project-level governance, rubric endorsement gap, timeline optimism
- "Structured decision framework pending platform/governance alignment" is the correct framing for all ARB submissions in the current state — enforce this in every draft
- AutoResearch for autonomous compliance validation: explicitly excluded from ARB submissions without human review — this agent assists, does not replace the EA

---

## Related UCs
- UC-23 Virtual EA Agent (knowledge foundation)
- UC-24 Strategic Screening (intake)
- UC-25 AI Capability Framework (capability reference)
- UC-26 AI Use Case Tracker (disposition tracking)
- UC-32 Automated Briefing Generation (governance briefings)
