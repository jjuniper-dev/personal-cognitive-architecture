# Gwen-VL — Multimodal Model Abstraction

## Purpose
Gwen-VL represents the PCA’s multimodal perception and reasoning capability.

## Design Principles
- Extends Gwen into vision-language domain
- Used for interpreting diagrams, documents, and visual inputs
- Supports structured extraction from images
- Must remain replaceable (backend-agnostic)

## Current Implementation
- Backend: Qwen2.5-VL
- Runtime: Ollama (target)

## Responsibilities
- Diagram interpretation
- Document parsing
- Visual-to-structure extraction
- Input transformation for downstream models (Claude, GPT)

## Non-Responsibilities
- Diagram generation (Claude)
- Deep reasoning (GPT)
- UI reconstruction (GLM-V)

## Role in PCA
Gwen-VL acts as the **perception layer**, enabling:
- image → structured data
- diagram → architecture model

## Evolution Path
- v0: Qwen2.5-VL
- v1: optimized multimodal pipeline
- v2: multi-model perception layer
