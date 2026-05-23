# UC-15 · Budget Automation
**Cluster:** Finance  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration / L1 Knowledge & Control

---

## Purpose
Automate personal budget tracking — ingest transactions, categorise spending, compare against budget targets, and surface variance alerts. Replaces manual spreadsheet tracking with an always-current picture of financial position.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily — pull new transactions, update budget state |
| Event-driven | UC-16 Transaction Import → new transactions detected |
| Manual | On-demand budget status via Ayla ("how am I doing this month?") |

---

## Agent Flow

```
[Daily Schedule / Transaction Event]
    │
    ▼
[Transaction Ingester — n8n]
  • UC-16 Transaction Import (primary source)
  • Supplementary: manual entry via Ayla
    │
    ▼
[Categorisation Agent — Haiku T=0.3]
  • Assign spending category: Housing / Food / Transport / Entertainment /
    Health / Personal / Savings / Misc
  • Use merchant name + amount heuristics
  • Flag uncategorised for review
    │
    ▼
[Budget Comparator — Code node]
  • Load monthly budget targets (from Neo4j / Obsidian config note)
  • Compute: spent vs. budgeted per category
  • Compute: days remaining in month, projected end-of-month spend
  • Identify: over-budget categories, under-budget (potential savings)
    │
    ▼
[Alert Evaluator — Haiku T=0.3]
  • Trigger alert if: category > 80% of budget with > 7 days remaining
  • Trigger alert if: total spend on pace to exceed budget by > 10%
    │
    ├─[No alert]──▶ [Neo4j update — log daily state]
    │
    └─[Alert]──▶ [Summary Agent — Sonnet T=0.3]
                    • Generate budget status brief
                    • Suggest specific adjustments
                    │
                    ▼
                  [Output]
                    ├──▶ UC-06 Ayla: alert + brief
                    └──▶ Obsidian: /finance/budget/YYYY-MM.md (monthly tracker)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author budget automation workflow |
| `n8n-mcp` · `search_nodes` | Schedule, HTTP, code nodes |
| UC-16 Transaction Import webhook | Transaction data source |
| Neo4j (HTTP node) | Budget state, category totals, targets |
| Obsidian URI / webhook | Monthly budget note write |
| UC-06 Ayla webhook | Alert and status delivery |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily run |
| Webhook trigger | Transaction event from UC-16 |
| AI Agent node (Haiku) | Transaction categorisation |
| AI Agent node (Sonnet) | Budget brief generation |
| Code node (JS) | Budget math, projection, variance calculation |
| If / Switch node | Alert threshold routing |
| HTTP Request node | Neo4j, Obsidian, Ayla webhook |
| Set node | Budget state payload assembly |

---

## Claude Skills (n8n-skills)

- **Patterns** — ingest → categorise → compare → alert (stateful financial pipeline)
- **Expression Syntax** — date arithmetic (days in month, days remaining), percentage calc
- **Validation Expert** — categorisation consistency, budget config schema

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| UC-16 Transaction Import | 🔴 Not Started — gating dependency |
| Neo4j (budget state store) | ✅ Live |
| Budget targets defined | 🔴 Not yet configured |
| UC-06 Ayla (alert delivery) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Known Issues / Watch Items
- Build UC-16 Transaction Import first — this UC is entirely dependent on it
- Budget targets: store in a config note in Obsidian OR a Neo4j `Budget` node — Obsidian config note is simpler to edit manually
- Categorisation accuracy: Haiku at T=0.3 should be reliable for common merchants; build a merchant→category lookup table (Code node) as a fast-path before hitting the LLM
- Canadian tax year considerations: budget month = calendar month is fine; ensure GST/HST is not double-counted in categorised amounts
- Privacy: all financial data stays local — Neo4j and Obsidian only, no cloud sync for finance notes

---

## Related UCs
- UC-16 Transaction Import (primary data source — build first)
- UC-17 Financial Alerts (threshold alerting counterpart)
- UC-18 Net Worth Tracking (balance sheet counterpart)
- UC-06 Ayla Assistant (delivery interface)
- UC-14 Birthday Planning (budget context for gift spending)
