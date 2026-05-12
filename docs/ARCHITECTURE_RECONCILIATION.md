---
type: roadmap
version: Phase-1-to-8
created: 2026-05-11
updated: 2026-05-11
tags: [roadmap, phases, reconciliation, gates]
status: active
---

# Architecture Reconciliation — Sprint 5 to 8-Phase Roadmap

## Executive Summary

Sprint 5 (Validation Layer) completes Phase 1, proving the first operational loop: **Capture → Validate → Store**.

The 8-phase roadmap maps each phase to specific sprints, deliverables, and gate criteria. Phase 2 (Cognitive Reconciliation) begins when Phase 1 produces training data (50+ INBOX decisions from users).

## 8-Phase Roadmap Overview

| Phase | Sprints | Name | Goal | Input | Output | Status |
|-------|---------|------|------|-------|--------|--------|
| **1** | 1-5 | **Capture & Validation** | Prove ingestion loop | Raw inputs (YouTube, web, voice) | Validated notes in Obsidian + Neo4j scores | ✅ Sprint 5 Ready |
| **2** | 6-8 | **Cognitive Reconciliation** | Compare new vs. existing knowledge | Phase 1 validated captures + INBOX decisions | Reinforcement/Contradiction/Expansion relationships | 🔲 Gate: 50 INBOX decisions |
| **3** | 9-12 | **Semantic Indexing & Hot/Cold** | Local inference, vector search | Neo4j graph + Phase 2 reconciliation output | ChromaDB index + Ollama inference | 🔲 Gate: GPU acquisition |
| **4** | 13-15 | **Reasoning & Agents (MCP)** | Query-driven synthesis | Indexed knowledge + user questions | Agent-generated insights, summaries, cross-domain patterns | 🔲 Gate: Phase 3 complete |
| **5** | 16-18 | **Output Generation** | Multi-modal artifact production | Reasoning engine outputs | PowerPoint, Word, dashboards, audio (Kokoro) | 🔲 Gate: Phase 4 agents stable |
| **6** | 19-21 | **Outcome Measurement** | Track impact on thinking & decisions | Generated outputs + user feedback | Health/Knowledge/Skills/Reflection dashboards | 🔲 Gate: Phase 5 artifacts in use |
| **7** | 22-24 | **Feedback & Learning (RLHF-Lite)** | System adapts to user patterns | User feedback on outcomes + agent decisions | Updated prompts, routing thresholds, agent weights | 🔲 Gate: Phase 6 measurement data |
| **8** | 25+ | **Outcome Evolution** | Continuous improvement loop | Aggregated learning from Phase 7 | New capabilities, emergent behaviors, system evolution | 🔲 Ongoing |

## Phase 1: Capture & Validation (Sprints 1-5)

### Objective

Prove the MVP loop: **n8n → Obsidian → Neo4j → structured validation**

### Deliverables

**Sprint 1-4 (Completed):**

- FastAPI capture endpoints
- Neo4j schema (VideoCapture, Concept, Author nodes)
- Obsidian vault structure
- Basic n8n webhook integration

**Sprint 5 (Now):**

- Dual-agent validation layer (Claude Sonnet + Haiku)
- 4-dimension scoring (Credibility, Quality, Relevance, Alignment)
- 3-tier routing (PROMOTE/INBOX/ARCHIVE)
- Obsidian validation notes with structured metadata
- Neo4j storage (agent-specific + composite scores)

### Outputs

1. **Obsidian Vault**: `/Captures/YouTube/` folder with markdown validation reports
2. **Neo4j Graph**: VideoCapture nodes with validation scores
3. **n8n Workflows**: 9-node dual-agent workflow tested and documented
4. **Anthropic Usage**: Track API costs (target ~CAD $330/year at 50 videos/day)

### Gate Criteria for Phase 2

✅ **Must haves:**

- [ ] 10+ successful validations in n8n workflow
- [ ] All 4 dimensions scoring consistently
- [ ] Neo4j upsert working (no duplicate nodes)
- [ ] Obsidian notes readable and timestamped
- [ ] Deduplication preventing re-scoring same video

✅ **Data collection:**

- [ ] Minimum 50 INBOX items created
- [ ] User has manually reviewed and moved 20+ to PROMOTE or ARCHIVE
- [ ] Agent disagreement patterns visible (e.g., 10+ cases where agents diverged)

## Phase 2: Cognitive Reconciliation Engine (Sprints 6-8)

### Objective

Implement the **core differentiator**: Compare new knowledge against existing knowledge, detect contradictions, update confidence via Bayesian logic.

### Inputs from Phase 1

1. **Validated Captures**: All PROMOTE/INBOX/ARCHIVE VideoCapture nodes from Sprint 5
2. **User Decisions**: INBOX items moved to PROMOTE (reinforcement signal) or ARCHIVE (rejection signal)
3. **Agent-Specific Scores**: screening_credibility, critical_credibility, etc. from Neo4j for disagreement analysis
4. **Confidence Baselines**: Overall_score and confidence_score from dual-agent assessment

### Reconciliation Logic

```
For each new PROMOTE node:
  1. Query Neo4j: "Find existing Concepts similar to this capture"
  2. Compare: 
     - Same domain? (agentic systems, knowledge management, etc.)
     - Contradictory claims? (different methodologies, conflicting results)
     - Reinforcing evidence? (same conclusion from multiple sources)
     - Expanding context? (new examples, additional dimensions)
  3. Assign relationship type:
     - REINFORCE: Increases confidence in existing concept
     - CONTRADICT: Flags for human review (belief updating required)
     - EXPAND: Links new evidence or dimensions
     - IGNORE: Not relevant to existing graph
  4. Update confidence:
     - REINFORCE: conf = conf + (new_score × 0.1)
     - CONTRADICT: conf = max(20%, conf × 0.5) + manual_flag
     - EXPAND: Add new node, link to parent
     - IGNORE: Archive capture, no graph change
  5. Store decision in Neo4j with timestamp & reasoning
```

### Deliverables

**Sprint 6:**

- Reconciliation engine design doc
- Neo4j Cypher queries for graph comparison
- Contradiction detection rules

**Sprint 7:**

- n8n reconciliation workflow (integrates validation output)
- Obsidian interface for CONTRADICT reviews
- User feedback loop (mark as "resolved" when contradiction addressed)

**Sprint 8:**

- Bayesian confidence update implementation
- Model evolution triggers (when to suggest restructuring)
- Phase 2 completion test suite

### Outputs

1. **Reconciliation Decisions**: R/C/E/I tags on all Phase 1 captures
2. **Updated Confidence Scores**: Obsidian/Neo4j both updated with reconciliation results
3. **Contradiction Queue**: Flagged beliefs requiring user review
4. **Confidence Heatmap**: Visual showing high-confidence vs. uncertain knowledge areas

### Gate Criteria for Phase 3

✅ **Must haves:**

- [ ] 100+ captures processed through reconciliation
- [ ] At least 5 contradictions detected and resolved
- [ ] Bayesian confidence updates visible in Neo4j
- [ ] User manual review loop working (INBOX → review → resolve → learn)
- [ ] No regressions: old beliefs not overwritten without human say-so

✅ **Data collection:**

- [ ] Measure agreement: how often user agrees with R/C/E/I assessment?
- [ ] Contradiction patterns: common disagreement types?
- [ ] Learning signals: which user corrections most valuable?

## Phase 3: Semantic Indexing & Hot/Cold Architecture (Sprints 9-12)

### Objective

Local inference + vector search. Reduce API costs. Enable always-on semantic recall.

### Prerequisite Gate

🔲 **RTX 3090 GPU acquired** (~CAD $800 used)

If GPU not acquired by end of Sprint 8, Phase 3 defers.

### Inputs from Phase 2

1. **Neo4j Graph**: Fully reconciled knowledge graph with confidence scores
2. **Obsidian Vault**: 200+ notes with validated metadata
3. **Agent-Specific Scores**: Full audit trail for bias analysis

### Hot Layer (Real-time, always-on)

**Components:**

- Claude Haiku (cloud) for quick tasks
- Qwen2.5-7B (local, Ollama) for fast reasoning
- Redis cache for in-session context

**Use cases:**

- Chat interface to Obsidian (sub-second response)
- Real-time relevance filtering
- Quick tag suggestions

### Cold Layer (On-demand, heavy)

**Components:**

- Claude Sonnet (cloud) for complex synthesis
- Qwen2.5-32B (local, Ollama) for deep analysis
- PostgreSQL for structured query results

**Use cases:**

- Weekly synthesis reports
- Cross-domain pattern discovery
- Long-form research summaries

### Deliverables

**Sprint 9:**

- Ollama container setup (Qwen2.5-7B + 32B models)
- BGE-M3 embedding model loaded in Ollama
- Redis cache configuration

**Sprint 10:**

- ChromaDB integration (ingest Obsidian notes → embeddings → index)
- Semantic search endpoints (n8n integration)

**Sprint 11:**

- Hot/Cold routing logic (decide which model based on query complexity)
- Latency benchmarks (hot: <100ms, cold: <2s)

**Sprint 12:**

- Observability: Prometheus metrics for inference times
- Cost comparison: Phase 1 API costs vs. Phase 3 local inference

### Outputs

1. **ChromaDB Index**: 200+ notes embedded and searchable
2. **Inference Latency Profile**: Hot vs. cold performance characteristics
3. **Cost Analysis**: API spend reduction (target 40-60% cost savings)

### Gate Criteria for Phase 4

✅ **Must haves:**

- [ ] Local inference working (Qwen models loaded, inference <2s)
- [ ] ChromaDB semantic search returning relevant results
- [ ] Hot/Cold routing logic tested on 20+ queries
- [ ] No knowledge loss (all Phase 2 reconciliation decisions preserved)

## Phase 4: Reasoning & Agents (MCP-based) (Sprints 13-15)

### Objective

Enable agents to ask questions, retrieve context, synthesize answers from the knowledge graph.

### Inputs from Phase 3

1. **Indexed Knowledge**: ChromaDB + Neo4j fully searchable
2. **Embedding Model**: BGE-M3 ready for semantic retrieval
3. **Hot/Cold Routers**: Inference routing decisions proven

### MCP Agent Framework

**Agents as MCP Servers:**

- Query Neo4j (graph search, relationship traversal)
- Retrieve from ChromaDB (semantic search)
- Call external APIs (GitHub, Slack, etc.)
- Create/update Obsidian notes
- Schedule tasks via n8n

**Example Agent Flow:**

```
User: "What are common failure modes in agentic systems?"
  ↓
Agent routes to Claude Sonnet (complex reasoning)
  ↓
Agent calls MCP Neo4j tool: MATCH (c:Concept {tags: "agents"}) RETURN c
  ↓
Agent calls MCP ChromaDB tool: semantic_search("failure modes agentic systems", top_k=10)
  ↓
Claude synthesizes retrieved context into answer
  ↓
Agent creates summary note in Obsidian
  ↓
Output: Answer + citation + saved note
```

### Deliverables

**Sprint 13:**

- MCP agent framework design
- Neo4j MCP tool (query, create, update)
- ChromaDB MCP tool (semantic search)

**Sprint 14:**

- Agent skill library (10+ reusable skills)
- n8n orchestration for agent workflows
- Multi-turn conversation support

**Sprint 15:**

- Agent evaluation (does it answer questions accurately?)
- Cross-domain reasoning tests
- Performance profiling

### Outputs

1. **Agent Library**: 10+ tested, documented agents
2. **Knowledge Retrieval Quality**: Semantic search precision/recall benchmarks
3. **Reasoning Evaluation**: Sample Q&A with annotated reasoning steps

### Gate Criteria for Phase 5

✅ **Must haves:**

- [ ] 5+ agents working independently
- [ ] Semantic retrieval returning relevant context (precision >80%)
- [ ] Agent answers grounded in knowledge graph (citations working)
- [ ] Multi-turn conversations maintaining context

## Phase 5: Output Generation (Sprints 16-18)

### Objective

Transform reasoning outputs into polished artifacts (slides, reports, dashboards, audio).

### Inputs from Phase 4

1. **Reasoning Engine Outputs**: Structured answers, insights, summaries
2. **Knowledge Graph**: Full context for generation
3. **User Preferences**: Format, tone, audience preferences

### Output Types

**Presentations (PowerPoint):**

- Auto-generated slide decks from synthesis
- Key insights, evidence, recommendations
- Speaker notes with source citations

**Documents (Word/PDF):**

- Long-form research reports
- Executive summaries
- Structured briefs

**Dashboards (Web):**

- Real-time knowledge graph visualization
- Query interface for exploration
- Confidence heatmaps

**Audio (Kokoro TTS):**

- Podcast-style weekly recaps
- High-quality voice (no robotic sound)
- 10-15 minute digestible summaries

### Deliverables

**Sprint 16:**

- PowerPoint generation (python-pptx + templating)
- Word document generation (python-docx + templating)

**Sprint 17:**

- Dashboard UI (React + D3.js)
- Kokoro TTS integration

**Sprint 18:**

- Output quality benchmarks
- User preference learning (which formats preferred?)

### Outputs

1. **Template Library**: 20+ reusable output templates
2. **Generation Pipeline**: Automated artifact creation from reasoning
3. **Quality Metrics**: User satisfaction with outputs

### Gate Criteria for Phase 6

✅ **Must haves:**

- [ ] Generated presentations readable and professional
- [ ] Documents include proper citations
- [ ] Dashboards interactive and responsive
- [ ] Audio summaries understandable and engaging

## Phase 6: Outcome Measurement (Sprints 19-21)

### Objective

Define and measure impact on human thinking and decision-making.

### Outcome Domains

**Health:**

- Sleep quality, energy levels, well-being
- Tracked: sleep app, subjective daily rating

**Knowledge:**

- Learning progress (new concepts understood, languages, research)
- Tracked: note growth, concept mastery assessment

**Skills:**

- Communication quality, systems thinking, decision-making
- Tracked: peer feedback, self-assessment

**Reflection:**

- Judgment quality, value alignment, growth direction
- Tracked: journaling, decision retrospectives

### Measurement Framework

```
Capture Phase 1: Baseline metrics
  ↓
Months 1-6: Passive observation (system running, no pressure)
  ↓
Months 7-12: Active feedback collection (rate impacts)
  ↓
Monthly Review: Trend analysis (improving, stable, declining?)
  ↓
Quarterly Synthesis: Pattern discovery (what's working?)
```

### Deliverables

**Sprint 19:**

- Measurement framework design
- Data collection infrastructure
- Baseline assessment

**Sprint 20:**

- Dashboard for outcome tracking
- Trend analysis and reporting

**Sprint 21:**

- Learning signals from outcomes
- Feedback to Phase 7 for system adaptation

### Outputs

1. **Baseline Metrics**: Starting point for each outcome domain
2. **Tracking Dashboard**: Real-time view of progress
3. **Insight Reports**: Monthly/quarterly trends

## Phase 7: Feedback & Learning (RLHF-Lite) (Sprints 22-24)

### Objective

System learns from user feedback and adapts routing, scoring, prompts.

### Learning Signals

1. **INBOX Decisions**: User move to PROMOTE/ARCHIVE = validation signal
2. **Outcome Correlation**: Which knowledge sources led to good decisions?
3. **Contradiction Resolutions**: How did user resolve conflicts?
4. **Agent Feedback**: "This answer was good/bad" annotations

### Adaptation Targets

**Scoring Thresholds:**

- Phase 1: User provides feedback on first 50 INBOX items
- Adjustment: Relevance floor stays ≥60; Credibility/Quality/Alignment tuned per user preferences

**Prompt Evolution:**

- Phase 4: Agent prompts refined based on answer quality
- Adjustment: Store good/bad examples, update system prompts

**Routing Logic:**

- Phase 2: R/C/E/I detection improved based on contradiction feedback
- Adjustment: Weight agent disagreement differently if user finds patterns

### Deliverables

**Sprint 22:**

- Feedback collection infrastructure
- RLHF-Lite training pipeline (fine-tune prompts)

**Sprint 23:**

- Prompt iteration framework
- Threshold optimization (grid search on Credibility/Quality/Alignment floors)

**Sprint 24:**

- Learning metrics (how much do adaptations improve outcomes?)
- Documentation of learned patterns

### Outputs

1. **Adapted Prompts**: Custom prompts learned from user feedback
2. **Optimized Thresholds**: Per-user scoring tuning
3. **Learned Patterns**: What types of sources most valuable to user?

## Phase 8: Outcome Evolution (Sprints 25+)

### Objective

Continuous improvement loop. System becomes a true cognitive OS.

### Ongoing Activities

**Quarterly Cycles:**

- Measure outcomes (Phase 6)
- Collect feedback (Phase 7)
- Adapt system (Phase 7)
- Deploy improvements (Phase 8)

**Emergent Capabilities:**

- Cross-domain pattern discovery (e.g., "Music theory patterns apply to system design")
- Weak signal detection (early indicators of opportunity or risk)
- Decision support (proactive suggestions when pattern matches past situations)

### Long-Term Vision

By Phase 8:

- System knows user's thinking patterns
- Proactively surfaces relevant knowledge
- Learns from user's decisions (reinforcement learning)
- Continuously improves own models through RLHF
- Feels like a true cognitive partner

## Timeline & Dependencies

### Critical Path

```
Sprint 5 (May 2026)
  ↓ Gate: 50 INBOX decisions
Sprint 6-8 (Jun-Jul 2026) — Phase 2 Reconciliation
  ↓ Gate: 100+ captures reconciled
Sprint 9-12 (Aug-Oct 2026) — Phase 3 (requires GPU)
  ↓ Gate: Vector search working
Sprint 13-15 (Nov-Dec 2026) — Phase 4 Agents
  ↓ Gate: 5+ agents tested
Sprint 16-18 (Jan-Feb 2027) — Phase 5 Output
  ↓ Gate: Output templates ready
Sprint 19-21 (Mar-May 2027) — Phase 6 Measurement
  ↓ Gate: 6 months of baseline data
Sprint 22-24 (Jun-Aug 2027) — Phase 7 Learning
  ↓ Gate: Adaptation loop working
Sprint 25+ (Sep 2027+) — Phase 8 Evolution
```

### Blocking Dependencies

- **Phase 2 blocks on:** 50 INBOX decisions (timing depends on capture rate)
- **Phase 3 blocks on:** RTX 3090 acquisition (~CAD $800)
- **Phase 4 blocks on:** Phase 3 complete (vector search must work)
- **Phase 5 blocks on:** Phase 4 agents stable
- **Phase 6 blocks on:** 6+ months of baseline (cannot rush)
- **Phase 7 blocks on:** Phase 6 outcome data
- **Phase 8:** Continuous, no blockers

## Decision Matrix

| Decision | Phase | Status | Notes |
|----------|-------|--------|-------|
| LLM stack (Claude Sonnet + Haiku) | 1 | ✅ Locked | Cost-effective, asymmetric agents |
| Knowledge store (Obsidian canonical) | 1 | ✅ Locked | Human-readable, version control |
| Validation approach (dual-agent) | 1 | ✅ Locked | Disagreement signals uncertainty |
| Local inference timing (Phase 3) | 3 | ✅ Locked | Blocked on GPU acquisition |
| Outcome domains (Health/Knowledge/Skills/Reflection) | 6 | ✅ Locked | Comprehensive human development |
| RLHF-Lite strategy (user feedback → prompts) | 7 | ✅ Locked | Lightweight, sustainable learning |
| Measurement baseline duration | 6 | ⏳ TBD | 6 months? 1 year? |
| Phase 8 automation depth | 8 | ⏳ TBD | How proactive should system be? |

## Revision History

- **2026-05-11:** Initial 8-phase roadmap mapping, Sprint 5 completion gates defined
- **2026-04-24:** Preliminary phase structure (5 phases)
