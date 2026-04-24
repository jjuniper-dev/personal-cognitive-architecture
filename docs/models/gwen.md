# Gwen — Local Model Abstraction

## Purpose
Gwen represents the PCA’s local-first reasoning capability.

## Design Principles
- Runs locally by default
- Lowest cost execution path
- Used for lightweight cognitive tasks
- Must be replaceable without affecting system logic

## Current Implementation
- Backend: Qwen2.5-7B-Instruct
- Runtime: Ollama

## Responsibilities
- Validation scoring
- Classification
- Lightweight reasoning
- Pre-filtering before escalation

## Non-Responsibilities
- Deep synthesis
- Complex architecture reasoning
- High-precision structured output

## Evolution Path
- v0: Qwen2.5-7B via Ollama
- v1: Optimized local model (quantized)
- v2: Multi-model local ensemble (optional)
