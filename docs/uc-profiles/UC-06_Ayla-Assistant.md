# UC-06 · Ayla Assistant
**Cluster:** Automation  
**Status:** 🟡 Architecture defined — orchestrator-worker pattern established  
**Layer:** L2 Agent Runtime (primary) / L1 / L3

---

## Purpose
The primary conversational interface to the Ayla ecosystem. Ayla receives natural language requests, routes them to the appropriate worker agents or n8n workflows, and returns synthesised responses. Functions as the inner orchestrator for the entire UC stack.

---

## Trigger
| Type | Source |
|------|--------|
| Chat message | Claude.ai (current), future: custom front-end or iOS Shortcut |
| Webhook | External trigger → Ayla processing pipeline |
| Scheduled prompt | Proactive check-in (e.g. morning briefing delivery) |

---

## Agent Flow

```
[User Input]
    │
    ▼
[Ayla Orchestrator — Sonnet T=0.3]
  • Intent classification
  • Route to worker or respond directly
  • Maintain conversation context (window-based, no persistent memory in flight)
    │
    ├──▶ [Knowledge Query Worker — Haiku]
    │      • Query Neo4j for entities / relationships
    │      • Return structured context to orchestrator
    │
    ├──▶ [Memory Recall Worker — Haiku]
    │      • Search Obsidian vault (UC-03)
    │      • Return relevant memory snippets
    │
    ├──▶ [Preference Lookup Worker — Haiku]
    │      • Query UC-04 Likes/Dislikes Graph
    │      • Return preference context for recommendations
    │
    ├──▶ [Workflow Trigger Worker]
    │      • Invoke n8n webhook (any UC pipeline)
    │      • Return execution status
    │
    ├──▶ [Web Search Worker — Haiku]
    │      • Tavily / SerpAPI search
    │      • Return summarised results
    │
    └──▶ [Direct Response]
           • Orchestrator synthesises and replies
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` / `update_workflow` | Author Ayla routing workflows |
| `n8n-mcp` · `execute_workflow` | Trigger UC pipelines from conversation |
| Neo4j MCP / HTTP node | Knowledge graph queries |
| Obsidian URI / HTTP | Vault read/write |
| Tavily / SerpAPI (HTTP node) | Web search worker |
| MCP Server Trigger (n8n) | Expose n8n workflows as MCP tools to Claude |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive Ayla requests |
| AI Agent node (Sonnet) | Orchestrator |
| AI Agent node (Haiku) | Worker agents (multiple instances) |
| HTTP Request node | Neo4j, Obsidian, search APIs |
| Switch / Router node | Intent-based routing |
| Sub-workflow / Execute Workflow node | Invoke other UC pipelines |
| Respond to Webhook node | Return response to caller |
| Window Buffer Memory node | Conversation context |

---

## Claude Skills (n8n-skills)

- **Patterns** — orchestrator-worker (canonical Ayla pattern)
- **Tools Expert** — Sub-workflow execution, MCP Server Trigger
- **Expression Syntax** — passing context between orchestrator and workers via `$json`
- **Validation Expert** — routing logic, worker tool definitions

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Neo4j (UC-01) | 🟡 In Progress |
| Obsidian vault (UC-03) | 🟡 Partial |
| UC-04 Likes/Dislikes Graph | 🔴 Not Started |
| OpenClaw / NanoClaw (L2 gateway) | 🟡 OpenClaw provisional — NanoClaw under eval |
| Tailscale mesh | ✅ Live |
| iOS front-end (future) | 🔴 Not planned yet |

---

## Known Issues / Watch Items
- Worker-as-tool pattern (not worker-as-agent): workers are n8n sub-workflows exposed as tools to the orchestrator, not autonomous agents — this is the confirmed architectural decision
- DeerFlow explicitly excluded — provenance concerns, not suitable for any Ayla or HC/PHAC data
- Context window management: orchestrator cannot hold long conversation history across sessions — UC-03 and UC-01 serve as the persistent layer; design prompts accordingly
- NanoClaw assessment pending — may supersede OpenClaw as L2 gateway

---

## Related UCs
- UC-01 through UC-05 (knowledge layer — Ayla's read/write targets)
- UC-07 through UC-10 (Ayla triggers automation UCs)
- UC-11 through UC-14 (Ayla surfaces lifestyle recommendations)
- All UCs (Ayla is the primary interaction surface)
