# Model Benchmark Sources

## Open VLM Leaderboard
Source: https://huggingface.co/spaces/opencompass/open_vlm_leaderboard

### Purpose
- Track performance of multimodal models
- Provide comparative evaluation across model families
- Support evidence-based model selection decisions

### Usage in PCA
- Not used at runtime
- Used as an input into the Model Intelligence and Evaluation layer
- Feeds into rubric-based assessment and vendor comparison

### Relevance to PCA
- Phase 2+: model evaluation discipline
- Phase 3+: multimodal expansion (Gwen-M concept)

---

## Integration with Rubric System

This benchmark source feeds into the PCA evaluation rubric as:

- Evidence input for capability scoring
- External validation for model performance claims
- Comparative baseline for:
  - reasoning
  - multimodal capability
  - efficiency tradeoffs

---

## Interpretation Guidance

Do not:
- Treat leaderboard rank as final decision criteria
- Assume top-ranked models fit PCA architecture

Do:
- Map benchmark strengths to PCA task roles
- Combine with:
  - cost analysis
  - local feasibility
  - governance constraints

---

## Future Direction

This source will support:

- Gwen evolution decisions
- Introduction of multimodal agents
- Expansion of the PCA model routing system
