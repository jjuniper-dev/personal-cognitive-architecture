# Model Evaluation Rubric Integration

## Purpose

Define how external model benchmarks and internal PCA evaluations are combined into a structured decision framework.

---

## Core Concept

The PCA does not select models based on preference.

It uses a **rubric-driven evaluation system** combining:
- external benchmarks
- internal testing
- architectural fit

---

## Evaluation Dimensions

Each model is evaluated across the following:

### 1. Capability
- reasoning quality
- instruction following
- structured output ability

### 2. Performance
- latency
- throughput
- local feasibility

### 3. Cost
- API cost
- local compute cost

### 4. Architectural Fit
- aligns with PCA roles (Gwen, GPT, Claude, Azure)
- supports routing model
- replaceability

### 5. Governance
- data residency
- auditability
- enterprise alignment

---

## Evidence Sources

| Source | Type |
|------|------|
| Open VLM Leaderboard | External benchmark |
| Internal tests | Empirical |
| Vendor docs | Claimed capability |

---

## Scoring Model (v0.1)

Each dimension scored 1–5:

```text
Total Score = Weighted Sum
```

Example weights:

- Capability: 30%
- Performance: 20%
- Cost: 20%
- Architectural Fit: 20%
- Governance: 10%

---

## Output

Rubric produces:

- suitability score
- recommended role (Gwen / GPT / Claude / Azure)
- escalation rules

---

## Integration with PCA

Outputs from rubric feed into:

- config/models.yaml
- config/routing.yaml

This ensures:
- model decisions are explainable
- changes are traceable

---

## Future Enhancements

- automated benchmark ingestion
- dynamic routing adjustments
- scenario-based evaluation
