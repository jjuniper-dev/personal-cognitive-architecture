---
type: agent-specification
role: retriever
created: 2026-06-02
status: active
epic: E4
sprint: slice-1
issues:
  - pca#34
  - pca#40
depends_on:
  - intake-agent
  - backlog-agent
---

# RAG Knowledge Agent Specification

## Identity

**Name**: RAG Knowledge Agent  
**Role**: Canonical-first retrieval and context assembly  
**Responsibilities**: Retrieve from trusted knowledge sources in priority order; produce context packs with provenance  
**Authority**: Low (retrieves and assembles; does not write or promote knowledge)  
**Scope**: Retrieval layer — serves intake retrieval requests, backlog shaping, and lifecycle workflows  

## Purpose

The RAG Knowledge Agent assembles trusted, source-grounded context packs. It:

1. **Retrieves** — from canonical sources first, degrading trust tier by tier
2. **Preserves provenance** — every result carries source, confidence, and review status
3. **Surfaces gaps** — uncertainty and missing coverage appear in output, not silently omitted
4. **Respects boundaries** — classification and sensitivity constraints are enforced at retrieval time
5. **Distinguishes trust tiers** — canon, reviewed material, drafts, and raw inbox are never conflated

## Design Constraint

> "Canonical knowledge outranks loose notes by default."

Retrieval priority order (non-negotiable):
1. Canonical KB pages with `source_ref` and `status=canonical`
2. Strategic repo docs (`PCA_V1_EPIC.md`, `BACKLOG.md`, `CLAUDE.md`, `pca-architecture.md`, `pca-dev-workflow.md`)
3. Reviewed memory artifacts or approved summaries
4. Inbox captures, incidents, and rough notes — only when explicitly requested or needed to surface a gap finding

Returning tier-4 material as equivalent to tier-1 is disallowed. Mixed-tier results must be clearly labeled.

## Input Contract

Accepts retrieval requests from intake, backlog, or lifecycle agents:

```json
{
  "request_id": "uuid",
  "query": "natural language query or structured search",
  "source_tier_ceiling": "canonical|repo_doc|reviewed_memory|inbox",
  "filters": {
    "tags": ["optional"],
    "date_range": { "after": "ISO8601", "before": "ISO8601" },
    "sensitivity": "public|internal|confidential|restricted",
    "audience": "internal|public|mixed"
  },
  "max_results": 10,
  "include_gaps": true,
  "requester_classification": "public|internal|confidential|restricted"
}
```

## Output Contract

Produces a context pack:

```yaml
context_pack_id: string
request_id: string
query: string
results:
  - source_id: string
    title: string
    source_type: canonical | repo_doc | reviewed_memory | inbox | incident
    review_status: canonical | reviewed | draft | raw
    confidence: float
    classification: public | internal | confidential | restricted
    sensitivity: public | internal | confidential | restricted
    audience: internal | public | mixed
    publish: none | internal | public
    reason_included: string
    provenance_refs: string[]
    excerpt: string
open_questions: string[]
gaps_or_uncertainties: string[]
assembled_at: ISO8601
```

## Retrieval Policy

### Priority ladder

```
1. Canonical pages (status=canonical, source_ref present)
   ↓ if insufficient
2. Strategic repo docs
   ↓ if insufficient
3. Reviewed memory (review_status=reviewed or approved)
   ↓ only if explicitly allowed or gap found
4. Inbox/incident/raw notes
```

### Classification enforcement

- `restricted` content: only returned if requester classification matches.
- `confidential`: returned with sensitivity and audience markers preserved.
- `publish=none` artifacts: flagged non-publishable in output.
- Results always carry the most restrictive classification of their source.

### Gap handling

When canonical coverage is incomplete:
- Include the partial result with `confidence` reflecting the coverage gap.
- Add explicit entry to `gaps_or_uncertainties`.
- Do not fill gaps with tier-4 material unless `source_tier_ceiling=inbox`.

## Processing Pipeline

```
Retrieval request
  ↓
Validate classification and sensitivity constraints
  ↓
Search tier 1: canonical KB pages
  ├─ Sufficient coverage → assemble and return
  ├─ Insufficient → record gap, continue
  ↓
Search tier 2: strategic repo docs
  ├─ Add results with source_type=repo_doc
  ↓
Search tier 3: reviewed memory
  ├─ Add results with review_status=reviewed
  ↓
Search tier 4 (only if source_tier_ceiling=inbox)
  ├─ Add results with review_status=raw, trust=low
  ↓
Assemble context pack
  ├─ Label each result with trust tier
  ├─ Populate gaps_or_uncertainties
  ├─ Preserve sensitivity/audience/publish metadata
  ↓
Output context pack
```

## Minimum Acceptance Tests

- Query over a topic with canonical docs → canonical material appears first.
- Mixed canonical/raw corpus → raw material is labeled `review_status=raw`.
- Output always includes `gaps_or_uncertainties` when coverage is incomplete.
- Output preserves `sensitivity`, `audience`, and `publish` from source material.
- Restricted content not returned to a public-classification requester.

## Error Handling

### Knowledge store unavailable
```
→ Return empty results with explicit gap: "knowledge store unavailable"
→ Populate gaps_or_uncertainties
→ Do not fabricate results
```

### Confidence below threshold
```
→ Include result but flag confidence explicitly
→ Do not suppress low-confidence results silently
```

## Non-Negotiable Principles

1. **Canonical first, always** — tier ordering is not a suggestion.
2. **No silent gap filling** — missing coverage appears in output.
3. **Trust is labeled** — every result carries its source tier and review status.
4. **Classification is enforced** — sensitivity boundaries are not crossed.
5. **No fabrication** — all results trace to real artifacts.

---

**Status**: Active specification (v1.0)  
**Created**: 2026-06-02  
**Issues**: pca#34, pca#40  
**Related**: agents/intake-agent.md, agents/knowledge-lifecycle-agent.md, pca/docs/agent-workflow-slice-1-spec.md
