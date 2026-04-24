# Personal Cognitive Architecture

A local-first, governed cognitive architecture for capture, validation, reconciliation, retrieval, agent orchestration, and structured output generation.

## Core design

- Obsidian remains the canonical knowledge store.
- Automation and orchestration are handled through n8n and lightweight scripts.
- Agents are modular and replaceable.
- Services abstract external infrastructure such as models, vector stores, graph databases, and storage.
- Reconciliation is explicit, governed, and toggleable.

## Repository structure

```text
config/       System, model, routing, and scoring configuration
agents/       Modular cognitive agents
services/     Infrastructure abstraction layer
workflows/    n8n exports and executable scripts
knowledge/    Obsidian vault link area and schemas
data/         Local runtime data, inboxes, logs, embeddings
prompts/      System prompts, task prompts, reusable templates
outputs/      Generated reports, diagrams, audio, and artifacts
tests/        Unit and scenario tests
docs/         Architecture notes, decisions, and operating model
```

## Current status

Initial scaffold for PCA v1.
