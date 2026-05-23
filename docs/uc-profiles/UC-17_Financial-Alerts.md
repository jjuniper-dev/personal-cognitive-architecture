# UC-17 · Financial Alerts
**Cluster:** Finance  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Real-time and near-real-time financial alerts — unusual spending, large transactions, recurring charge changes, low balance warnings, and foreign currency activity. The reactive monitoring layer on top of the transaction pipeline.

---

## Trigger
| Type | Source |
|------|--------|
| Event-driven | UC-16 Transaction Import → new transaction detected |
| Schedule | Daily balance check |
| Manual | On-demand alert status via Ayla |

---

## Agent Flow

```
[New Transaction Event from UC-16]
    │
    ▼
[Alert Rule Engine — Code node]
  Rules evaluated per transaction:
  • Large transaction: amount > $CAD threshold (configurable, e.g. $200)
  • Foreign currency: non-CAD transaction
  • Unusual merchant: first-time merchant above $50
  • Subscription change: recurring amount differs from last period by > 5%
  • Potential duplicate: same merchant + amount within 24 hours
  • Low balance: account balance below threshold (daily check)
    │
    ├─[No rules triggered]──▶ [Log only — no alert]
    │
    └─[Rule triggered]──▶ [Alert Composer — Haiku T=0.3]
                            • Generate concise alert message
                            • Include: amount, merchant, account, rule triggered
                            • Suggest action if relevant (e.g. "verify this charge")
                            │
                            ▼
                          [Delivery]
                            ├──▶ UC-06 Ayla: immediate push
                            └──▶ Neo4j: log alert (for pattern analysis)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author alert workflow |
| `n8n-mcp` · `search_nodes` | Webhook, code, HTTP nodes |
| UC-16 webhook (event trigger) | New transaction input |
| Neo4j (HTTP node) | Alert log, recurring transaction history |
| UC-06 Ayla webhook | Alert delivery |
| Bank of Canada exchange rate API (HTTP node) | CAD equivalent for foreign transactions |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive transaction events from UC-16 |
| Code node (JS) | Alert rule engine — all rules evaluated here |
| AI Agent node (Haiku) | Alert message composition |
| If / Switch node | Route triggered vs. clean transactions |
| HTTP Request node | Neo4j, Ayla webhook, BoC exchange rate |
| Set node | Alert payload assembly |

---

## Claude Skills (n8n-skills)

- **Patterns** — event-driven rule engine → conditional alert
- **Expression Syntax** — amount comparison, date arithmetic for duplicate detection
- **Validation Expert** — rule threshold config schema, alert deduplication

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-16 Transaction Import | 🔴 Not Started — gating dependency |
| n8n (local Docker) | ✅ Live |
| Neo4j (alert log, transaction history) | ✅ Live |
| UC-06 Ayla (delivery) | 🟡 Planned |
| Alert thresholds config | 🔴 Not yet defined |
| Bank of Canada API | 🟡 Free, no key needed |

---

## Known Issues / Watch Items
- Alert fatigue: keep default thresholds high enough that only genuinely notable events trigger alerts; make all thresholds configurable via a Neo4j config node or Obsidian config note
- Subscription change detection: requires storing last-seen amount per recurring merchant — Neo4j `RecurringTransaction` node pattern
- This is the simplest Finance UC to build — pure rule engine, minimal LLM involvement; build immediately after UC-16

---

## Related UCs
- UC-16 Transaction Import (data source — build first)
- UC-15 Budget Automation (complementary — budget tracks trends, alerts track events)
- UC-06 Ayla Assistant (delivery)
- UC-18 Net Worth Tracking (balance alerts overlap)
