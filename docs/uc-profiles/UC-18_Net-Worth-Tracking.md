# UC-18 · Net Worth Tracking
**Cluster:** Finance  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration / L1 Knowledge & Control

---

## Purpose
Track personal net worth over time — assets (chequing, savings, investments, property, vehicle) minus liabilities (credit card balances, loans) — updated regularly and visualised as a trend. The financial balance sheet layer of Ayla.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Weekly — update all account balances and compute net worth |
| Manual | On-demand via Ayla ("what's my net worth?") |
| Event-driven | UC-16 Transaction Import → balance update detected |

---

## Agent Flow

```
[Weekly Schedule / Manual / Balance Event]
    │
    ▼
[Balance Collector — n8n]
  Assets:
  • Bank account balances (via UC-16 / Flinks / SimpleFIN)
  • Investment accounts (Questrade API / Wealthsimple API / manual)
  • Property value estimate (manual — update quarterly via MPAC/Zolo)
  • Vehicle value (manual — update annually; 2019 Mazda CX-3 current value)
  
  Liabilities:
  • Credit card balances (via UC-16 pipeline)
  • Any outstanding loans (manual entry)
    │
    ▼
[Net Worth Calculator — Code node]
  • Total assets − total liabilities = net worth
  • Delta vs. last week / last month / YTD
  • Category breakdown: liquid / invested / property / vehicle / debt
    │
    ▼
[Trend Analyser — Haiku T=0.3]
  • Characterise trend: growing / flat / declining
  • Flag significant changes (>2% week-over-week)
  • Note driver of change if identifiable
    │
    ▼
[Write]
  ├──▶ Neo4j: NetWorthSnapshot node (date, total, breakdown)
  ├──▶ Obsidian: /finance/net-worth/YYYY-WXX.md
  └──▶ UC-06 Ayla: weekly summary (notable changes only)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author net worth tracking workflow |
| `n8n-mcp` · `search_nodes` | Schedule, HTTP, code nodes |
| UC-16 Transaction Import (balance data) | Bank + credit card balances |
| Questrade API (HTTP node) | Investment account balance |
| Wealthsimple API (HTTP node) | Investment account balance (if used) |
| Neo4j (HTTP node) | Snapshot storage, trend queries |
| Obsidian URI / webhook | Weekly net worth note |
| UC-06 Ayla webhook | Summary delivery |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Weekly run |
| Webhook trigger | Balance update event from UC-16 |
| HTTP Request node | Investment APIs, Neo4j, Obsidian, Ayla |
| Code node (JS) | Net worth calculation, delta computation, category breakdown |
| AI Agent node (Haiku) | Trend characterisation |
| Set node | Snapshot payload assembly |
| Merge node | Combine asset and liability sources |

---

## Claude Skills (n8n-skills)

- **Patterns** — scheduled aggregate → calculate → trend → store
- **Expression Syntax** — financial arithmetic, percentage delta, YTD calculations
- **Validation Expert** — multi-account balance schema consistency

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-16 Transaction Import (bank balances) | 🔴 Not Started — gating dependency |
| n8n (local Docker) | ✅ Live |
| Neo4j (snapshot store) | ✅ Live |
| Questrade API access | 🔴 Needs API key registration |
| Wealthsimple API access | 🔴 Unofficial API — evaluate reliability |
| Property value source (MPAC / Zolo) | 🔴 Manual update — define cadence |
| Vehicle value (2019 Mazda CX-3) | 🔴 Manual — annual update via AutoTrader |
| Obsidian vault write pipeline | 🟡 URI live |
| UC-06 Ayla (delivery) | 🟡 Planned |

---

## Known Issues / Watch Items
- Investment APIs: Questrade has an official API; Wealthsimple does not (unofficial community API only — fragile). Consider manual CSV export for Wealthsimple as a more reliable path
- Property and vehicle values are inherently manual and infrequent — design the workflow to handle missing/stale values gracefully (use last known value with a staleness flag)
- All financial data stays local — no third-party cloud storage
- Visualisation: net worth trend chart would be valuable — consider a simple Obsidian Dataview table or a Chart.js n8n output for local dashboard

---

## Related UCs
- UC-16 Transaction Import (balance data source — build first)
- UC-15 Budget Automation (spending context)
- UC-17 Financial Alerts (balance threshold alerts)
- UC-06 Ayla Assistant (query and delivery)
