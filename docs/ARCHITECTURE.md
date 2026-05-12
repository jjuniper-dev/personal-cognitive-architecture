---
type: architecture
version: Phase-1
created: 2026-05-11
updated: 2026-05-11
tags: [architecture, 9-layer, pca]
---

# PCA Architecture — 9-Layer System Design

**A comprehensive breakdown of the Personal Cognitive Architecture system, layer by layer.**

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                                    │
│  YouTube │ Web │ Chat │ Voice │ Documents │ Files │ Shortcuts      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│                    CAPTURE LAYER                                    │
│  Whisper │ Playwright │ Custom Parsers │ Normalization             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│              VALIDATION LAYER (Dual-Agent)                          │
│  Screening Agent (Sonnet) │ Critical Agent (Haiku)                  │
│  Credibility • Quality • Relevance • Alignment                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│        COGNITIVE RECONCILIATION ENGINE (Phase 2)                    │
│  Graph Comparison │ Relationship Detection │ Confidence Update      │
│  Model Evolution │ Contradiction Detection                          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│           KNOWLEDGE INTEGRATION LAYER                               │
│  Obsidian (Canonical) │ Neo4j (Graph) │ Chroma (Vector)             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│        REASONING & AGENTS LAYER (Phase 3)                          │
│  LLMs (Tiered) │ Agent Framework (MCP) │ RAG │ Tools                │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│           EXECUTION & AUTOMATION LAYER                              │
│  n8n Workflows │ Task Management │ API Integrations │ Schedules     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│          OUTPUT GENERATION LAYER (Phase 3)                          │
│  Presentations │ Documents │ Dashboards │ Audio Summaries            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│        INFRASTRUCTURE & DEPLOYMENT                                  │
│  Docker │ Compose │ GitLab CI/CD │ Backup (Restic + B2)             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                    GOVERNANCE & ETHICS
           Privacy • Bias Detection • Human-in-Loop • Audit
```

## Layer-by-Layer Breakdown

### Layer 1: Input Sources 🔵

**Purpose:** Multi-modal, low-friction ingestion from diverse sources

**Components:**

- **YouTube** → Video capture via iPhone Shortcuts
- **Web** → Browser bookmarks, shared links, web articles
- **Chat** → Messages, Slack, Teams, Discord
- **Voice** → Voice memos, transcribed calls
- **Documents** → PDFs, research papers, books
- **Files** → Local files, notes, Markdown
- **iPhone Shortcuts** → One-tap capture from any app

**Design Principle:** Minimize friction. Users should be able to capture from anywhere in <5 seconds.

**Status:** ✅ Partially Complete (FastAPI endpoints ready, Shortcuts UX to improve)

### Layer 2: Capture Layer 🔵

**Purpose:** Normalize and structure raw inputs into canonical format

**Components:**

- **Whisper API** — Transcribe audio (voice memos, video audio)
- **Playwright** — Extract web content (articles, metadata)
- **Custom Parsers** — Handle specific formats (PDFs, emails, Markdown)
- **Normalization** — Standardize metadata (timestamps, authors, sources)

**Flow:**

```
Raw Input → Extraction → Parsing → Normalization → Structured Data
```

**Output Format:**

```json
{
  "id": "capture-uuid",
  "source_type": "youtube",
  "content": "full text or transcript",
  "metadata": {
    "title": "...",
    "author": "...",
    "url": "...",
    "captured_at": "ISO8601",
    "duration": "minutes"
  }
}
```

**Status:** ✅ Sprint 1 Complete (FastAPI endpoints, Neo4j storage)

**Implementation:** `backend/app/services/` and n8n workflows

### Layer 3: Validation Layer 🟢

**Purpose:** Intelligently filter content before integration into knowledge system

**Key Innovation:** Dual-agent screening with agreement-driven confidence

**Components:**

1. **Screening Agent** (Claude Sonnet, T=0.3)
   - Conservative assessment
   - Consistent scoring

2. **Critical Agent** (Claude Haiku, T=0.8)
   - Independent assessment
   - Exploratory thinking

3. **4-Dimension Scoring:**
   - **Source Credibility** (0-100): Creator trustworthiness
   - **Content Quality** (0-100): Intellectual rigor
   - **Relevance** (0-100): Alignment with user goals
   - **Alignment** (0-100): Ethical & methodological alignment

4. **Agreement Gate:**
   - Difference <15 points per dimension = agreement
   - All 4 dimensions agree = high confidence (95%)
   - Partial disagreement = medium confidence (40-70%)
   - Most disagree = low confidence (20%)

5. **3-Tier Routing:**
   - **PROMOTE** (>80): Integrate immediately
   - **INBOX** (60-80): Manual review required
   - **ARCHIVE** (<60): Store but don't prioritize

**Why Dual Agents (not single + confidence)?**

- Model confidence is unreliable (overconfident on easy, underconfident on hard)
- Agent disagreement is interpretable (tells us WHERE confidence is low)
- Asymmetric models (Sonnet + Haiku) naturally integrate human review patterns

**Status:** ✅ Sprint 5 Complete (ready to build in n8n)

**Implementation:** 9-node n8n workflow (see `SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md`)

### Layer 4: Cognitive Reconciliation Engine 🟣

**Purpose:** THE CORE DIFFERENTIATOR — Compare new knowledge against existing knowledge graph

**Components:**

1. **Graph Comparison**
   - Compare new content against existing Neo4j nodes
   - Detect: exact duplicates, near-duplicates, derivatives

2. **Relationship Detection**
   - **Reinforce:** Strengthens existing knowledge
   - **Contradict:** Challenges existing beliefs
   - **Expand:** Adds new dimensions or examples
   - **Ignore:** Irrelevant to existing graph

3. **Confidence Update**
   - Bayesian inference: combine new evidence with prior belief
   - Formula: P(knowledge | new evidence) = P(evidence | knowledge) × P(knowledge) / P(evidence)
   - Heuristics: agreement from multiple sources increases confidence

4. **Model Evolution**
   - When inconsistencies detected: flag for review
   - When gaps detected: suggest new research areas
   - Trigger restructuring: merge, split, or reorganize concepts

**Flow:**

```
New Content
    ↓
Compare against Neo4j
    ↓
Detect relationship type (R/C/E/I)
    ↓
Update confidence via Bayesian
    ↓
Trigger action if needed
    ├─ Flag for manual review (contradiction)
    ├─ Update existing node (reinforce)
    ├─ Link new node (expand)
    └─ Archive (ignore)
```

**Status:** 🔲 Phase 2 (planned but not yet implemented)

**Why Phase 2?** Need validation layer (Layer 3) complete first. Phase 2 will consume validation signals and training data from user's INBOX decisions.

### Layer 5: Knowledge Integration Layer 🔵

**Purpose:** Store knowledge in multiple formats optimized for different use cases

**Triple-Layer Storage:**

#### 5a. Obsidian Knowledge Graph

- **Format:** Markdown with YAML front matter
- **Structure:** Nodes (documents), links (relationships), backlinks (reverse links), tags, properties
- **Use Case:** Human-readable knowledge, navigation, editing
- **Location:** `/Captures/` folder in Obsidian vault
- **Example Node:**

```markdown
---
title: "Agentic System Design Patterns"
tags: [architecture, agents, design-patterns]
created: 2026-05-11
confidence: 95
routing: PROMOTE
---

# Agentic System Design Patterns

[Link to related concept](concept-link)
[Reference to source](youtube-capture)

## Key Ideas
- Agent disagreement signals uncertainty better than confidence scores
- Human-in-the-loop gates ensure accountability
- ...
```

#### 5b. Neo4j Graph Database

- **Format:** Property graph (nodes + relationships + properties)
- **Structure:** Semantic relationships, indexes, constraints
- **Use Case:** Machine-readable knowledge, graph queries, pattern matching
- **Schema:**

```cypher
(VideoCapture {
  id, title, url, source,
  created_at, validated_at,
  screening_credibility, screening_quality, screening_relevance, screening_alignment,
  critical_credibility, critical_quality, critical_relevance, critical_alignment,
  credibility_score, quality_score, relevance_score, alignment_score,
  overall_score, confidence, routing, agents_agree
})

(Concept {
  id, name, definition,
  created_at, updated_at,
  confidence_score
})

(Author {
  id, name, expertise_areas,
  credibility_score
})

RELATIONSHIPS:
- (VideoCapture)-[:CAPTURES]->(Concept)
- (VideoCapture)-[:CREATED_BY]->(Author)
- (Concept)-[:RELATES_TO]->(Concept)
- (Concept)-[:REINFORCED_BY]->(VideoCapture)
- (Concept)-[:CONTRADICTED_BY]->(VideoCapture)
```

#### 5c. Vector Database (Chroma)

- **Format:** Embeddings + metadata
- **Structure:** Semantic vectors (BGE-M3 embeddings, local via Ollama), similarity indices
- **Use Case:** Semantic search ("find similar ideas"), RAG retrieval
- **Flow:** Document → BGE-M3 embedding (local) → Chroma index → Similarity search

**Synchronization:**

- **Obsidian ← (Canonical):** Source of truth, human-edited
- **Neo4j ← Obsidian (Phase 2):** One-way ingestion from Obsidian
- **Chroma ← Neo4j:** Vector index from Neo4j nodes (derived, ephemeral)

**Rule: Obsidian is always authoritative. Neo4j and Chroma are derived indices, rebuildable from Obsidian.**

**Status:** ✅ Obsidian vault ready, 🔲 Neo4j schema prepared, 🔲 Chroma integration (Phase 2)

### Layer 6: Reasoning & Agents Layer 🔵

**Purpose:** Intelligent reasoning over knowledge graph, answer questions, generate insights

**Components:**

1. **LLMs (Tiered)**
   - **Claude Sonnet** (cloud): Complex reasoning, generation, orchestration
   - **Claude Haiku** (cloud): Fast, simple tasks, validation
   - **Qwen2.5-7B** (Ollama local): Fast reasoning, real-time tasks, privacy-critical
   - **Qwen2.5-32B** (Ollama local): Deep analysis, reconciliation, synthesis

2. **Agent Framework (MCP-based)**
   - Agents can query Neo4j as tools via MCP
   - Agents can execute functions: search, create notes, schedule tasks
   - Natural language control of system

3. **Retrieval (RAG)**
   - LlamaIndex for semantic retrieval
   - Query Neo4j + Chroma for context
   - Inject retrieved context into LLM prompts

4. **Tools & Integrations**
   - Custom API calls (GitHub, Slack, etc.)
   - File system access (read/write Obsidian)
   - Database queries (Neo4j Cypher)

**Example Agentic Flow:**

```
User Question: "What are the key design patterns for agentic systems?"
    ↓
Agent routes to RAG system
    ↓
RAG queries Neo4j: MATCH (c:Concept {tags: "agents"}) RETURN c
    ↓
RAG queries Chroma: semantic search "agentic design patterns"
    ↓
Combines results → injects into Claude Sonnet
    ↓
Claude synthesizes answer from retrieved context
    ↓
Output: Comprehensive answer with citations
```

**Status:** 🔲 Phase 3 (planned after validation + reconciliation)

### Layer 7: Execution & Automation Layer 🔵

**Purpose:** Trigger workflows, run tasks, integrate with external systems

**Components:**

1. **n8n Workflows**
   - Event-driven: webhooks, schedules, API triggers
   - Multi-lane architecture (Lane A + Lane B for parallelization)
   - YouTube processor, Voice processor, Chat processor (see Sprint 5, 6, 7)

2. **Task Management**
   - Create tasks from captured content ("Action items extracted")
   - Schedule follow-ups
   - Integrate with calendar, to-do apps

3. **API Integrations**
   - Slack: Post summaries, request input
   - Microsoft Teams: Notifications, approval workflows
   - Notion/Linear: Sync tasks

4. **Schedules & Triggers**
   - Periodic reconciliation (5-min sync cycle)
   - Nightly summary generation
   - Weekly review prompts

**Status:** ✅ FastAPI webhooks ready (Sprint 1), 🔧 n8n setup in progress (Sprint 5+)

### Layer 8: Output Generation Layer 🔵

**Purpose:** Create polished, multi-format artifacts for consumption and sharing

**Components:**

1. **Presentations** (PowerPoint)
   - Key insights summarized in slides
   - Automated via python-pptx + n8n

2. **Documents** (Word/PDF)
   - Long-form summaries, research synthesis
   - Automated via python-docx + n8n

3. **Dashboards** (Web)
   - Real-time knowledge graphs
   - Query interface for graph exploration
   - Built with React/D3.js

4. **Audio Summaries** (MP3 via Kokoro TTS)
   - High-quality text-to-speech synthesis
   - Podcast-style weekly recaps
   - Local generation (privacy-preserving)

**Status:** 🔲 Phase 3 (planned)

### Layer 9: Infrastructure & Deployment 🔵

**Purpose:** Reliable, secure, scalable hosting on home PC with cloud backup

**Components:**

1. **Docker Containers**
   - FastAPI service
   - Neo4j database
   - n8n orchestration
   - Each isolated, reproducible

2. **Docker Compose**
   - Orchestrates all containers
   - Network management, volume mounts
   - Easy start/stop: `docker-compose up/down`

3. **Version Control (GitLab)**
   - All code, workflows, configs
   - CI/CD pipelines for testing, building
   - Branching for feature development

4. **Backup Strategy**
   - Restic for encrypted backups
   - Backblaze B2 for Canadian cloud storage
   - Automated daily backups
   - Point-in-time recovery

**Deployment Architecture:**

```
Home PC
├── Docker Desktop
│   ├── FastAPI Container
│   │   └── Python, uvicorn, app code
│   ├── Neo4j Container
│   │   └── Graph DB, 7687 (bolt), 7474 (HTTP)
│   ├── n8n Container
│   │   └── Workflow automation
│   ├── Ollama Container (Phase 2)
│   │   └── Qwen2.5-7B, Qwen2.5-32B, BGE-M3 on RTX 3090
│   ├── ChromaDB Container (Phase 2)
│   │   └── Vector store
│   ├── PostgreSQL Container (Phase 2)
│   │   └── Run logs, session history
│   └── Redis Container (Phase 2)
│       └── Session cache
├── Obsidian Vault
│   └── `/Captures/` markdown files
├── Restic + Backblaze B2
│   └── Encrypted daily backups
└── GitLab CI/CD
    └── Automated tests, builds
```

**Status:** ✅ Docker Compose working (Sprint 1), 🔲 Backup automation, 🔲 GitLab CI/CD

## Governance & Ethics (Integrated)

**Privacy & Data Protection**

- All processing on home PC (no cloud upload except encrypted backups)
- Canadian data residence (Backblaze B2)
- Encrypted backups via Restic
- Local embeddings (BGE-M3) — no external embedding API

**Bias Detection & Mitigation**

- Validate source credibility (filter misinformation)
- Dual-agent disagreement flags potential bias
- User manual review of INBOX items
- Agent-specific scores enable bias analysis

**Human-in-the-Loop Gates**

- Borderline content (INBOX) requires human review
- Agent disagreements escalate to user
- User decisions train system (RLHF-Lite)
- Hard floors (e.g., Relevance ≥ 60) enforce non-negotiable criteria

**Auditability & Logging**

- All decisions logged with reasoning
- Obsidian provides audit trail (timestamped, versioned)
- Neo4j stores full provenance graph
- Agent-specific scores enable traceability

## Data Flow Examples

### Example 1: YouTube Video → Integration

```
1. YouTube Shortcut
   User taps "Capture" in YouTube app
   Sends: {url, title, transcript} to FastAPI

2. FastAPI (Capture Layer)
   Creates VideoCapture node in Neo4j
   Returns immediately with capture ID (low latency)
   Async: sends webhook to n8n

3. n8n (Validation Layer)
   Screening Agent (Claude Sonnet) scores video
   Critical Agent (Claude Haiku) scores video
   Compares scores, determines confidence
   Routes to PROMOTE/INBOX/ARCHIVE

4. n8n (Integration)
   If PROMOTE: creates Obsidian note
   Updates Neo4j with validation fields (agent-specific + composite scores)
   Indexes in Chroma (semantic search)

5. Neo4j Graph
   VideoCapture node now has:
   - screening_credibility: 92
   - critical_credibility: 89
   - credibility_score: 90.5
   - overall_score: 89
   - routing: PROMOTE
   - agents_agree: true
   - obsidian_file: path

6. User
   Opens Obsidian, sees new note with validation report
   Knowledge integrated into existing graph
```

### Example 2: Reconciliation (Phase 2)

```
1. New VideoCapture scored as PROMOTE

2. Reconciliation Engine (Phase 2)
   Query Neo4j: "Similar concepts?"
   Find existing Concept: "Agentic Systems"

3. Relationship Detection
   New video reinforces existing concept
   Increases confidence: 85% → 92%

4. User Review
   Sees suggestion: "This reinforces 'Agentic Systems' concept"
   Approves or provides feedback

5. Model Evolution
   If 10+ videos REINFORCE same concept:
   Suggest: "Time to synthesize research into major paper?"
```

## Design Trade-offs

| Decision | Pro | Con |
|----------|-----|-----|
| **Dual agents (Sonnet + Haiku)** | Interpretable uncertainty, asymmetric thinking | Higher cost (~CAD $0.018/item) |
| **Obsidian + Neo4j + Chroma** | Best of each (human + machine + semantic) | More complex sync, extra infrastructure |
| **Local processing (Ollama)** | Privacy, no latency, cost reduction | Requires GPU, inference time |
| **3-tier routing (PROMOTE/INBOX/ARCHIVE)** | Explicit human review, quality control | Manual effort required |
| **Agreement threshold <15 points** | Conservative (fewer false positives) | May be too strict, needs tuning |
| **Relevance hard floor ≥60** | Non-negotiable quality gate | May filter valuable borderline content |
| **MCP agents** | Standardized tool use, interoperability | Still early technology, limited maturity |

## Roadmap

| Phase | Sprints | Focus | Status |
|-------|---------|-------|--------|
| **1** | 1-5 | Input capture, basic validation | ✅ Sprint 5 Ready |
| **2** | 6-10 | Reconciliation, local inference, semantic indexing | 🔲 Planned |
| **3** | 11-15 | Reasoning agents, RAG, MCP, output generation | 🔲 Planned |
| **4** | 16-20 | Enterprise compliance, governance, scaling | 🔲 Planned |
| **5+** | 21+ | Outcome measurement, RLHF, system evolution | 🔲 Future |

## Key References

- **SPRINT_5_VALIDATION_LAYER.md** — Validation layer specification (scoring rubric, dual-agent logic, Neo4j schema)
- **SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md** — Step-by-step n8n build guide (45–90 min)
- **TECHNOLOGY_STACK.md** — Technology decisions, migration path
- **README.md** — Project overview, vision, principles

## Revision History

- **2026-05-11:** Updated to Claude Sonnet + Haiku, Qwen2.5 (Phase 2), BGE-M3 embeddings, Kokoro TTS, one-way sync, agent-specific scores in Neo4j
- **2026-04-24:** Initial version
