# UC-23 · Virtual EA Agent
**Cluster:** Enterprise Architecture  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime

---

## Purpose
A conversational EA assistant for HC/PHAC work — answers questions about architecture decisions, GC frameworks, platform status, and ARB submission requirements. Draws from the CORE project reference folders, Obsidian EA vault, and Neo4j architecture graph. The professional counterpart to UC-06 Ayla.

---

## Trigger
| Type | Source |
|------|--------|
| Chat | Claude.ai (HC/PHAC EA Practice Project) |
| Manual | Document or decision query |

---

## Agent Flow

```
[EA Query — chat or document request]
    │
    ▼
[EA Orchestrator — Sonnet T=0.3]
  • Classify: ARB query / platform query / framework query / document request
  • Route to appropriate worker
    │
    ├──▶ [CORE Reference Worker — Haiku]
    │      • Search CORE project folders (HTML viewer + structured JSON)
    │      • Return relevant project context
    │
    ├──▶ [GC Framework Worker — Haiku]
    │      • Query: DADM, AIA, PIA, SA&A, GBA+, Privacy Act
    │      • Return applicable framework requirements
    │
    ├──▶ [Architecture Graph Worker — Haiku]
    │      • Query Neo4j: capabilities, platforms, decisions, risks
    │      • Return structured EA context
    │
    ├──▶ [ARB Submission Worker — Sonnet]
    │      • Draft or review ARB submission sections
    │      • Apply HC/PHAC ARB framing and risk language
    │
    └──▶ [Direct Response]
           • Synthesise and reply
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author EA agent routing workflows |
| Neo4j (HTTP node) | Architecture graph queries |
| Google Drive MCP | CORE project folder access |
| GitHub MCP (read) | EA repo reference |
| HC/PHAC EA Practice Claude Project | Primary interface (existing) |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Query routing from Claude Project |
| AI Agent node (Sonnet) | EA orchestrator |
| AI Agent node (Haiku) | Specialist workers |
| HTTP Request node | Neo4j, Google Drive, GitHub |
| Switch node | Query type routing |
| Respond to Webhook node | Return EA response |

---

## Claude Skills (n8n-skills)

- **Patterns** — orchestrator-worker (same as UC-06, EA domain)
- **Tools Expert** — Google Drive MCP integration
- **Validation Expert** — GC framework citation accuracy

---

## Dependencies

| Dependency | Status |
|------------|--------|
| HC/PHAC EA Practice Claude Project | ✅ Exists |
| CORE project reference folder | 🟡 In Progress (GEAkr evolution) |
| Neo4j (EA architecture graph) | 🟡 Shared with personal stack |
| Google Drive MCP | ✅ Connected |
| GitHub MCP (read-only) | ✅ Available via OAuth |
| GC framework knowledge base | 🟡 Partially built via Claude Project context |

---

## Governance / Data Sensitivity Notes
- This UC operates on HC/PHAC professional data — must be scoped to Claude.ai (not self-hosted) for Protected B compatibility until SA&A is complete
- No HC/PHAC data should flow through personal n8n instance — keep EA agent within Claude Project boundary
- AutoResearch framework for compliance validation: flagged as lacking formal assurance alignment — do not deploy without ARB sign-off
- DeerFlow: explicitly excluded from any EA or personal vault work

---

## Known Issues / Watch Items
- ARB risk profile: PATH/HAIL convergence unresolved; Secure Inference Gateway is a pattern not a capability; governance is project-level not enterprise — EA Agent must reflect this uncertainty, not paper over it
- The correct ARB framing remains: "structured decision framework pending platform/governance alignment" — not "ready for implementation"
- CORE HTML viewer + React/Neo4j/GraphQL backend: build this as the knowledge layer before the agent layer

---

## Related UCs
- UC-24 Strategic Screening (ARB intake counterpart)
- UC-25 AI Capability Framework (capabilities data consumer)
- UC-27 AI Learning Path (EA professional development)
- UC-28 Geomatics Strategy (domain-specific EA work)
