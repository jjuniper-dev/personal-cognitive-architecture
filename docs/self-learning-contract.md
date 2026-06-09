# Self-Learning Agent Contract

**Version:** 0.1  
**Owner:** PCA runtime  
**Status:** Draft — pending human review  

---

## Purpose

This contract defines how Ayla captures and promotes learning from interactions. It governs trigger conditions, learning categories, output targets, and governance rules. It does not define event schema, storage format, or distillation logic — those are covered in E-Learn.4.

---

## Trigger Conditions

A self-learning event is initiated by any of the following:

| Trigger | Description |
|---|---|
| Session end | Ayla detects a natural session boundary (user signs off, inactivity threshold reached) |
| Explicit user signal | User explicitly requests a learning capture (e.g. "remember this", "note that preference") |
| Reconciliation completion | The PCA reconciliation engine finalises a batch and flags candidate learning signals |

Multiple triggers in a single session produce one consolidated learning candidate, not one per trigger.

---

## Learning Categories

Each learning event must be tagged with at least one of:

- **Behaviour correction** — a change to how Ayla responds, routes, or prioritises (e.g. tone, format, refusal pattern)
- **User preference** — a durable signal about what the user wants, avoids, or values
- **Domain knowledge** — a factual or conceptual update relevant to PCA, the user's work, or their context

A single event may carry items from multiple categories.

---

## Output Targets

Validated learning events are written to:

- **Vault note** — a structured note in the `_system/learning/` folder of the Obsidian vault, following the canonical knowledge schema
- **Memory file** — the active memory file for the relevant agent or context layer, updated with the new signal

Writes to both targets are atomic: either both succeed or neither is committed.

---

## Governance Rule

All learning candidates are **flagged for human review** before becoming canonical.

No self-learning event modifies vault or memory automatically. The review queue surfaces candidates with their source trigger, category tags, and proposed write targets. The human approves, rejects, or edits before promotion.

This rule may not be overridden by Ayla or any downstream workflow without an explicit governance change recorded in this document.

---

## Out of Scope

- Event schema and field definitions → E-Learn.4
- Storage format and versioning rules → E-Learn.4
- Distillation triggers and batch logic → E-Learn.4
- UI for the review queue → separate delivery
