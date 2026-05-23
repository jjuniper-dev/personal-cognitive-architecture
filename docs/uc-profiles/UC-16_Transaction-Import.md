# UC-16 · Transaction Import
**Cluster:** Finance  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Ingest financial transactions from Canadian bank and credit card accounts into the Ayla data layer. The foundational data pipeline for all finance UCs — without this, UC-15, UC-17, and UC-18 have no data.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Daily — pull new transactions from all accounts |
| Manual | On-demand sync via Ayla |
| File drop | CSV export from bank dropped to watched folder |

---

## Agent Flow

```
[Schedule / File Drop / Manual Trigger]
    │
    ▼
[Source Router — Switch]
    │
    ├──▶ [Canadian Bank API / Aggregator]
    │      • Option A: Flinks (Canadian open banking aggregator — paid)
    │      • Option B: Plaid (limited Canadian coverage — evaluate)
    │      • Option C: Manual CSV export → watched folder → n8n file read
    │      • Option D: SimpleFIN Bridge (self-hosted, OFX-based)
    │
    └──▶ [Credit Card — same options as above]
    │
    ▼
[Transaction Normaliser — Code node]
  • Map to canonical schema:
    { id, date, amount, merchant, account, currency, raw_description }
  • Deduplicate against existing transactions (by id or date+amount+merchant)
  • Flag: credit vs. debit, CAD vs. foreign currency
    │
    ▼
[Enrichment Agent — Haiku T=0.3]
  • Clean merchant name (strip terminal IDs, location suffixes)
  • Detect: recurring transaction, subscription, refund
    │
    ▼
[Write]
  ├──▶ Neo4j: MERGE Transaction node (idempotent)
  └──▶ Emit event → UC-15 Budget Automation webhook
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author transaction import workflow |
| `n8n-mcp` · `search_nodes` | File, HTTP, schedule, code nodes |
| Flinks API (HTTP node) | Canadian bank data aggregation |
| SimpleFIN Bridge (HTTP node) | Self-hosted OFX aggregation alternative |
| Read Binary Files / Watch Folder node | CSV export ingestion |
| Neo4j (HTTP node) | Transaction write |
| UC-15 webhook (internal) | Emit new transaction event |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Daily sync |
| Watch Folder / Read File node | CSV drop ingestion |
| HTTP Request node | Bank API, Neo4j |
| Code node (JS) | Schema normalisation, deduplication, currency handling |
| AI Agent node (Haiku) | Merchant name cleaning, pattern detection |
| Switch node | Source routing (API vs. CSV) |
| Split In Batches node | Process large transaction sets |
| Set node | Canonical transaction object |

---

## Claude Skills (n8n-skills)

- **Patterns** — ingest → normalise → deduplicate → enrich → emit
- **Expression Syntax** — binary file reading, CSV parsing
- **Validation Expert** — deduplication logic, schema consistency across sources

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| Canadian bank API access | 🔴 Critical decision — Flinks vs. SimpleFIN vs. CSV |
| Flinks account (if chosen) | 🔴 Paid — evaluate cost |
| SimpleFIN Bridge (if chosen) | 🔴 Self-hosted setup needed |
| Neo4j (transaction store) | ✅ Live |
| Transaction schema defined | 🔴 Not yet defined |
| UC-15 Budget Automation (consumer) | 🔴 Not Started |

---

## Known Issues / Watch Items
- **Critical design decision: bank connectivity method.** Canadian banks have poor open banking support vs. EU. Options ranked by preference:
  1. **SimpleFIN Bridge** — self-hosted, OFX-based, works with many Canadian institutions via screen-scraping; local-first philosophy compatible
  2. **CSV export + file drop** — most reliable, most manual; acceptable for weekly sync cadence
  3. **Flinks** — best API coverage for Canadian banks, but paid and involves third-party data handling (privacy consideration)
  4. **Plaid** — limited Canadian coverage, US-focused
- Make this decision before building anything else in the Finance cluster
- All transaction data must remain local — no third-party cloud storage of financial records
- CAD-first: handle USD and other foreign currency transactions as a special case with exchange rate lookup (Bank of Canada exchange rate API — free)

---

## Related UCs
- UC-15 Budget Automation (primary consumer)
- UC-17 Financial Alerts (alert trigger source)
- UC-18 Net Worth Tracking (account balance consumer)
- UC-06 Ayla Assistant (on-demand sync trigger)
