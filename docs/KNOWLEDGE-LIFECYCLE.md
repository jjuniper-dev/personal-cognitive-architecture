# PCA Knowledge Lifecycle

**Canonical definition:** This document  
**Schema enforcement:** `schemas/canonical-metadata.schema.json` (field: `state`)  
**Last revised:** 2026-05-30

---

## The Problem

Three repos have independently named the knowledge lifecycle states. This document declares the canonical set and maps all variants to it.

| Source | States Used |
|---|---|
| `pca/BACKLOG.md` (E1.2.1 schema description, WF10) | `raw → validated → reconciled → stale → archived` |
| `schemas/canonical-metadata.schema.json` (this repo) | `captured, inbox, validated, provisional, reconciled, trusted, contested, archived, rejected, deleted, merged, superseded` |
| `obsidian/_System/Vault Schema.md` (note status field) | `inbox, draft, active, canonical, archived` |

**Canonical set:** The `canonical-metadata.schema.json` states are authoritative. The other sets are valid operational subsets or human-facing aliases.

---

## Canonical State Machine

```
captured ──→ inbox ──→ validated ──→ provisional ──→ reconciled ──→ trusted
                                                                       │
                                                                 contested
                                                                       │
                                                              (resolve) ↓
                                                              reconciled or archived
```

Terminal states: `archived`, `rejected`, `deleted`, `merged`, `superseded`

| State | Meaning | Who Transitions |
|---|---|---|
| `captured` | Raw input received; no validation yet | WF10, WF15, WF16, any capture workflow |
| `inbox` | Landed in Obsidian Inbox; awaiting triage | WF10 (note written to 00_Inbox/) |
| `validated` | Passes schema validation; required fields present | WF10 validation gate (E1.2.3) |
| `provisional` | Classified and enriched; not yet reconciled | WF-Classify / E4.1.1 (pending) |
| `reconciled` | Checked for contradictions; no active conflicts | E1.3.x (pending) |
| `trusted` | Human-reviewed or agent-confirmed; high confidence | Manual or Critical Review Agent |
| `contested` | Contradiction detected with another knowledge object | E1.3.x (pending) |
| `archived` | No longer active; retained for history | Manual or future lifecycle worker |
| `rejected` | Failed validation; not stored in knowledge layer | WF10 validation gate |
| `deleted` | Explicitly removed with governance approval | Manual |
| `merged` | Deduplicated into another knowledge object | Future deduplication worker |
| `superseded` | Replaced by a newer version | Manual or future versioning worker |

---

## Mapping: pca Labels → Canonical

`pca/BACKLOG.md` task E1.2.1 documents the WF10 schema using abbreviated labels. Mapping:

| `pca/BACKLOG.md` label | Canonical state(s) |
|---|---|
| `raw` | `captured` |
| `validated` | `validated` |
| `reconciled` | `reconciled` or `trusted` |
| `stale` | No direct equivalent — use `archived` or set `expires_at` in metadata |
| `archived` | `archived` |

When WF10 is updated in future (after E1.2.3), use the canonical state names. Current live behavior (E1.2.3, done 2026-05-30) uses pca labels; migration to canonical names is a follow-up task.

---

## Mapping: Obsidian Vault Status → Canonical

Obsidian vault notes use a human-facing `status` field in frontmatter (defined in `obsidian/_System/Vault Schema.md`). This is a human triage label, not the machine-tracked lifecycle state — but they relate.

| Obsidian `status` | Canonical lifecycle `state`(s) |
|---|---|
| `inbox` | `captured`, `inbox` |
| `draft` | `inbox`, `validated` |
| `active` | `provisional`, `reconciled` |
| `canonical` | `trusted` |
| `archived` | `archived` |

Both fields can coexist in vault frontmatter. The Obsidian `status` is for human navigation; the canonical `state` is for machine processing and should appear in Qdrant/Neo4j metadata.

---

## Reconciliation Engine Gap

The transitions `validated → reconciled`, `validated → trusted`, and `validated → contested` require the Reconciliation Engine (E1.3.x in `pca/BACKLOG.md`). This is **not yet implemented**.

Current system behavior: knowledge objects that pass WF10 validation remain in `validated` state indefinitely. No contradiction detection runs. The states `reconciled`, `trusted`, and `contested` are aspirational until E1.3.x is built.

Implementation location when built: pca WF10 extension or new WF-Reconcile workflow in n8n.

---

## Schema Authority

`schemas/canonical-metadata.schema.json` in this repository is the machine-readable contract. All capture workflows and agents should validate against it.

The `pca/BACKLOG.md` schema description (E1.2.1, pending) predates the JSON schemas and uses abbreviated field names. The JSON schema is more complete and takes precedence. When `knowledge-schema.md` is written for pca (E1.2.1), it should be a human-readable companion to these JSON schemas — not an independent definition.
