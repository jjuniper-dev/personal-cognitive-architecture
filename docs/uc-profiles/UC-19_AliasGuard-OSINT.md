# UC-19 · AliasGuard OSINT
**Cluster:** Open Source  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration / L1 Knowledge & Control

---

## Purpose
Open-source OSINT tool for monitoring digital identity exposure across aliases, emails, and usernames. Surfaces public data aggregator listings, breach appearances, and social footprint — designed for individual privacy protection. Personal use case (UC-10) as the closed variant; AliasGuard is the public/open-source release.

---

## Trigger
| Type | Source |
|------|--------|
| API call | External user submits alias/email for OSINT scan |
| Schedule | Automated monitoring run for registered identities |
| Manual | Direct invocation for one-off audit |

---

## Agent Flow

```
[Identity Input — alias / email / username]
    │
    ▼
[OSINT Collector — n8n]
  • HaveIBeenPwned API — breach check
  • Sherlock-style username search (HTTP calls to known platforms)
  • Google dorking via SerpAPI (limited, controlled scope)
  • Data broker listing check (Spokeo, Whitepages — public endpoints)
  • Social platform existence check
    │
    ▼
[Result Aggregator — Code node]
  • Deduplicate findings
  • Normalise source, exposure type, date
  • Build exposure profile object
    │
    ▼
[Risk Assessor — Sonnet T=0.3]
  • Categorise findings: breach / social-footprint / data-broker / doxxing-risk
  • Assign risk tier: Low / Medium / High / Critical
  • Generate plain-language explanation of each finding
    │
    ▼
[Report Generator — Sonnet T=0.3]
  • Produce structured OSINT report (Markdown + JSON)
  • Include remediation recommendations per finding
    │
    ▼
[Output]
  ├──▶ API response (JSON) — for programmatic consumers
  └──▶ Markdown report — for direct user delivery
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author OSINT scan workflow |
| `n8n-mcp` · `search_nodes` | HTTP, aggregation, code nodes |
| HaveIBeenPwned API (HTTP node) | Breach lookup |
| SerpAPI (HTTP node) | Controlled Google dork queries |
| HTTP Request node (multi) | Platform existence checks, data broker endpoints |
| Code node (JS) | Deduplication, normalisation, report assembly |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | API entry point for scan requests |
| HTTP Request node | All external OSINT sources |
| Code node (JS) | Aggregation, deduplication, normalisation |
| AI Agent node (Sonnet) | Risk assessment + report generation |
| Aggregate / Merge nodes | Combine multi-source results |
| Respond to Webhook node | Return JSON report to caller |
| Loop / Split In Batches | Handle multi-alias scans |

---

## Claude Skills (n8n-skills)

- **Patterns** — fan-out collection → aggregate → enrich (parallel source collection)
- **Expression Syntax** — multi-source result merging, array manipulation
- **Validation Expert** — HTTP error handling (many OSINT endpoints return 404 for not-found vs. error)
- **Tools Expert** — Loop node for multi-alias iteration

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker for dev) | ✅ Live |
| HaveIBeenPwned API key | 🔴 Paid subscription needed |
| SerpAPI key | 🟡 Needs key — free tier limited |
| Platform check endpoint list | 🔴 Not yet defined |
| Data broker endpoint research | 🔴 Not yet done |
| GitHub repo (public release) | 🔴 Not yet created |
| UC-10 Exposure Monitor (personal variant) | 🔴 Not Started — build UC-10 first, extract reusable components |

---

## Open Source Considerations
- Must be designed for public release: no hardcoded credentials, all secrets via env vars
- Rate limiting and ethical scope must be built in — no aggressive crawling, respect robots.txt
- Legal disclaimer required: OSINT on third parties without consent may have legal implications depending on jurisdiction
- Consider GitHub Actions–based deployment option (serverless, no n8n required for end users) as an alternative delivery to the n8n workflow

---

## Known Issues / Watch Items
- Overlap with UC-10: build UC-10 first as the private proof-of-concept, then extract the workflow logic into AliasGuard as the open-source variant
- Sherlock-style checks: doing this properly requires maintaining a list of platform URL templates — this is ongoing maintenance work
- SerpAPI Google dorking: implement strict query limits and scope controls to avoid ToS issues

---

## Related UCs
- UC-10 Exposure Monitor (personal variant — build first)
- UC-06 Ayla Assistant (may surface AliasGuard results in conversation)
- UC-01 Knowledge Graph (OSINT findings as identity exposure nodes)
