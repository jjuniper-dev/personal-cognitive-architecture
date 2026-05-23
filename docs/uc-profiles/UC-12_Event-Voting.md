# UC-12 · Event Voting
**Cluster:** Lifestyle  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Collaborative shortlisting tool for weekend events — share a curated event list with a partner or friends, collect votes/preferences, and surface the consensus top picks. Closes the loop from UC-11 discovery to actual decision.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | Triggered after UC-11 digest is generated — "send this week's events for voting" |
| Schedule | Auto-send Thursday evening after UC-11 runs |

---

## Agent Flow

```
[UC-11 Digest Available]
    │
    ▼
[Voting Package Builder — Code node]
  • Format top events as numbered list with brief description
  • Generate unique voting session ID
  • Store session + event list in Neo4j (or simple JSON in n8n static data)
    │
    ▼
[Delivery — Switch]
    │
    ├──▶ [iMessage / Signal — via webhook or shortcut]
    │      • Send formatted event list to contacts
    │      • Include simple reply instruction ("reply 1,3,5")
    │
    └──▶ [Simple web form — n8n Form trigger]
           • Hosted voting page (n8n native form)
           • Each event as checkbox
    │
    ▼
[Vote Collector — Webhook / Form response]
  • Receive votes from each participant
  • Tally results per event
    │
    ▼
[Results Agent — Haiku T=0.4]
  • Rank events by vote count
  • Identify consensus picks vs. split votes
  • Generate summary ("3 votes for Glebe Garage Sale, 2 for Jazz Festival")
    │
    ▼
[Output]
  ├──▶ UC-06 Ayla: deliver results
  └──▶ Obsidian: /lifestyle/events/YYYY-WXX-votes.md
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author voting workflow |
| `n8n-mcp` · `search_nodes` | Form trigger, webhook, HTTP nodes |
| n8n Form Trigger node | Hosted voting form (no external service needed) |
| Neo4j / static data (HTTP node) | Session + results storage |
| UC-11 webhook (internal) | Receive event digest as input |
| UC-06 Ayla webhook | Deliver results |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Form Trigger node | Hosted voting interface |
| Webhook trigger | Receive UC-11 output |
| Code node (JS) | Vote tallying, ranking, session management |
| AI Agent node (Haiku) | Results summary generation |
| HTTP Request node | Neo4j session store, Ayla webhook |
| Wait node | Hold open for vote collection period |
| Set node | Structure voting session payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — request-wait-collect-summarise (async collection pattern)
- **Expression Syntax** — session ID generation, vote tally aggregation
- **Tools Expert** — Form Trigger node, Wait node for async collection

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-11 Weekend Events (event source) | 🔴 Not Started |
| n8n (local Docker) | ✅ Live |
| n8n Form Trigger (native) | ✅ Available in n8n |
| UC-06 Ayla (results delivery) | 🟡 Planned |
| Participant contact list | 🔴 Define — SMS vs. form link |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Known Issues / Watch Items
- Keep it simple: n8n native Form Trigger is the right tool — no external voting service needed
- SMS/iMessage delivery is complex on a self-hosted stack; simplest path is sharing a form URL via any messaging app manually
- Vote collection window: define a cutoff (e.g. Friday noon) after which results are finalised — use n8n Wait node with timeout
- This UC has very low complexity relative to others — can be built quickly once UC-11 is live

---

## Related UCs
- UC-11 Weekend Events Ottawa (event source)
- UC-06 Ayla Assistant (results delivery)
- UC-13 Lifestyle Concierge (broader lifestyle planning context)
