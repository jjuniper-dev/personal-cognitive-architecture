---
type: architecture
created: 2026-04-24
updated: 2026-05-11
tags: [pca, technology, stack, deprecated]
status: DEPRECATED
superseded_by: docs/TECHNOLOGY_STACK.md
---

# ⚠️ DEPRECATED — DO NOT USE

> **This document is superseded by [`TECHNOLOGY_STACK.md`](TECHNOLOGY_STACK.md).**
> Pre-remediation stack decisions (April 2026) that conflict with current locked decisions.
> **For authoritative technology decisions, always read [`TECHNOLOGY_STACK.md`](TECHNOLOGY_STACK.md).**

## What changed
| Decision | Deprecated | Current |
|----------|-----------|----------|
| Phase 1 LLM | OpenAI GPT-4 | Claude Sonnet + Haiku |
| Phase 2 Local LLM | Mistral 7B | Qwen2.5-7B + 32B |
| Embeddings | all-MiniLM-L6-v2 | BGE-M3 |
| Cost | Not stated | ~CAD $330/year |

Per architectural review by Claude Opus 4.7 (2026-05-11): recommendation #1.

---

## ⚠️ HISTORICAL CONTENT (DO NOT USE) ⚠️

*[Content truncated. See TECHNOLOGY_STACK.md for current decisions.]*

## Revision History
- **2026-05-11:** ⚠️ DEPRECATED. Superseded by `TECHNOLOGY_STACK.md`.
- **2026-04-24:** Initial version (pre-remediation decisions)