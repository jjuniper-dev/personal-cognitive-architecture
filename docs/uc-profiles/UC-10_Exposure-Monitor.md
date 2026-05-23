# UC-10 · Exposure Monitor
**Cluster:** Automation  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Monitor personal digital exposure — data breaches, OSINT footprint, leaked credentials, public data aggregator listings — and surface alerts when new exposure is detected. Privacy and personal security use case.

---

## Trigger
| Type | Source |
|------|--------|
| Schedule | Weekly batch (breach monitoring), daily (news/paste monitoring) |
| Event-driven | HaveIBeenPwned webhook / API alert |
| Manual | On-demand audit via Ayla |

---

## Agent Flow

```
[Schedule / HIBP Webhook]
    │
    ▼
[Exposure Data Collector — n8n]
  • HaveIBeenPwned API — breach check on monitored emails
  • Google Alerts RSS — name / alias monitoring
  • Pastebin monitor (via third-party API or scrape)
  • Data broker opt-out status tracker (manual list)
    │
    ▼
[New Exposure Detector — Code node]
  • Compare against known exposure baseline (Neo4j)
  • Flag net-new breaches or mentions
    │
    ▼
[Risk Classifier — Haiku T=0.3]
  • Severity: low (old breach, already known) / medium / high (credential exposure)
  • Tag: breach / mention / data-broker / doxxing-risk
    │
    ├─[Low]──▶ [Neo4j update — log only]
    │
    └─[Medium / High]──▶ [Response Advisor — Sonnet T=0.3]
                            • Explain what was exposed
                            • Recommend specific actions (password reset, opt-out, etc.)
                            │
                            ▼
                          [Output]
                            ├──▶ Obsidian: /security/exposure/YYYYMMDD.md
                            └──▶ UC-06 Ayla: push high-severity alert immediately
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author exposure monitoring workflow |
| `n8n-mcp` · `search_nodes` | HTTP, webhook, schedule nodes |
| HaveIBeenPwned API (HTTP node) | Breach monitoring |
| Google Alerts RSS (HTTP node) | Name/alias monitoring |
| Neo4j (HTTP node) | Exposure baseline storage |
| Obsidian URI / webhook | Alert note write |
| UC-06 Ayla webhook | High-severity push alert |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Schedule trigger | Batch runs |
| Webhook trigger | HIBP real-time alerts |
| HTTP Request node | HIBP, Google Alerts, Neo4j |
| RSS Feed Read node | Google Alerts RSS |
| Code node (JS) | Baseline diff, exposure deduplication |
| AI Agent node (Haiku) | Risk classification |
| AI Agent node (Sonnet) | Response advice generation |
| If / Switch node | Severity routing |
| Set node | Structure alert payload |

---

## Claude Skills (n8n-skills)

- **Patterns** — monitor-detect-alert (same structural pattern as UC-08, UC-09)
- **Expression Syntax** — baseline comparison, date-keyed Neo4j lookups
- **Validation Expert** — HIBP API response schema, rate limit handling

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| HaveIBeenPwned API key | 🔴 Needs subscription (HIBP v3 monitoring API is paid) |
| Google Alerts RSS feeds | 🟡 Set up Google Alerts for monitored terms |
| Neo4j (exposure baseline) | ✅ Live |
| Monitored email/alias list | 🔴 Not yet defined — sensitive, store encrypted |
| UC-06 Ayla (alert surface) | 🟡 Planned |
| Obsidian vault write pipeline | 🟡 URI live |

---

## Known Issues / Watch Items
- Sensitive data: monitored emails and aliases must not be stored in plain text in n8n workflow definitions — use n8n credentials store or environment variables
- HIBP monitoring API (v3) requires a paid subscription for real-time breach notifications — evaluate cost vs. polling approach
- Pastebin monitoring is legally and technically complex — consider deprioritising or using a managed service (e.g. SpyCloud, DeHashed) via API instead of DIY scrape
- This UC has partial overlap with UC-19 AliasGuard OSINT — coordinate on shared monitored identity schema
- Data broker opt-out tracker is manual state — simplest implementation is an Obsidian table, not Neo4j, at least initially

---

## Related UCs
- UC-06 Ayla Assistant (alert delivery)
- UC-19 AliasGuard OSINT (open-source counterpart — shared identity schema)
- UC-01 Knowledge Graph (exposure events as nodes)
