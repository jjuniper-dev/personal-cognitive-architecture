# UC-04 · Likes / Dislikes Graph
**Cluster:** Personal Knowledge  
**Status:** 🔴 Not Started  
**Layer:** L1 Knowledge & Control

---

## Purpose
Maintain a structured preference graph — a persistent, evolving record of personal likes, dislikes, interests, and aversions across domains (music, food, places, people, ideas, products). Feeds Ayla's personalisation layer and recommendation UCs.

---

## Trigger
| Type | Source |
|------|--------|
| Explicit capture | User statement ("I love X", "I hate Y") detected in Ayla conversation |
| Implicit signal | UC-01 entity tagged with sentiment during extraction |
| Manual | Obsidian note tagged `#preference` → webhook |
| Schedule | Weekly review — surface unconfirmed inferences for user validation |

---

## Agent Flow

```
[Preference Signal Input]
  (conversation, graph event, manual tag, scheduled review)
    │
    ▼
[Preference Classifier — Haiku T=0.4]
  • Detect polarity: like / dislike / neutral / ambivalent
  • Extract subject entity and domain
  • Confidence score (explicit statement vs inferred)
    │
    ▼
[Conflict Check — Code node]
  • Query Neo4j: does opposite preference exist for same entity?
    │
    ├─[Conflict]──▶ [Resolution Agent — Sonnet T=0.3]
    │                 • Surface conflict to user via Ayla
    │                 • Accept updated preference, deprecate old
    │
    └─[No conflict]▶ [Neo4j Write]
                        • MERGE (:Preference {entity, domain, polarity})
                        • Link to (:Person {self})
                        • Add confidence, source, timestamp
                        • Update weight if preference already exists
                          (repeated signals increase confidence)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author preference capture workflow |
| Neo4j (HTTP node) | Read/write preference nodes |
| UC-06 Ayla webhook (outbound) | Surface conflicts / confirmations to user |
| Obsidian URI / webhook | Manual preference note pickup |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive signals from UC-01, UC-06 |
| AI Agent node (Haiku) | Preference classification |
| AI Agent node (Sonnet) | Conflict resolution dialogue |
| Code node (JS) | Neo4j Cypher query construction, conflict detection |
| HTTP Request node | Neo4j REST |
| If node | Route conflict vs clean write |
| Schedule trigger | Weekly review batch |

---

## Claude Skills (n8n-skills)

- **Patterns** — event-driven with conditional branch (conflict gate)
- **Expression Syntax** — Cypher parameterisation via `$json`
- **Validation Expert** — Neo4j node schema consistency

---

## Dependencies

| Dependency | Status |
|------------|--------|
| UC-01 Knowledge Graph (signal source) | 🟡 In Progress |
| UC-06 Ayla Assistant (conversation signal source) | 🟡 Planned |
| Neo4j (local Docker) | ✅ Live |
| Preference schema defined in Neo4j | 🔴 Not yet defined |
| n8n (local Docker) | ✅ Live |

---

## Known Issues / Watch Items
- Implicit preference inference (from UC-01 sentiment) will have high false-positive rate initially — keep confidence threshold high for auto-write; route low-confidence to review queue
- Domain taxonomy needs definition (music / food / place / idea / person / product / activity) before schema can be built
- Weekly review surface mechanism depends on UC-06 Ayla being conversationally accessible

---

## Related UCs
- UC-01 Knowledge Graph (entity source + signal emitter)
- UC-06 Ayla Assistant (conversation signal + review surface)
- UC-11 Weekend Events Concierge (consumes preferences for recommendations)
- UC-13 Lifestyle Concierge (consumes preferences)
- UC-15–18 Finance UCs (spending preferences as signal)
