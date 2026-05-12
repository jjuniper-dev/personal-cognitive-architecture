---
type: architecture
version: Phase-2
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [runtime, topology, deployment, docker, networking, infrastructure]
---

# PCA Runtime Topology

## Executive Summary

The Runtime Topology defines how PCA components are deployed, networked, and orchestrated across local and cloud infrastructure in each phase.

This document specifies:

- **Component Deployment** — What runs where (Docker containers, local processes, cloud services)
- **Network Architecture** — Local subnet, internet gateway, security boundaries
- **Data Flow** — How data moves between components
- **Phase-Based Evolution** — Topology changes from Phase 1 (cloud-heavy) through Phase 3 (hybrid local-first)
- **Resilience & Failover** — Backup strategies when components fail

The topology ensures **Obsidian remains canonical** while supporting multiple derived indices and inference layers.

---

## Phase 1: Cloud Jumpstart Topology

### Component Inventory

| Component | Technology | Deployment | Purpose |
|-----------|-----------|-----------|---------|
| **Obsidian Vault** | Markdown files | Local filesystem | Canonical knowledge store |
| **n8n Orchestrator** | Docker container | Local network | Workflow engine for validation pipeline |
| **Claude Sonnet Agent** | Anthropic API | Cloud (AWS/Anthropic) | Conservative scoring (T=0.3) |
| **Claude Haiku Agent** | Anthropic API | Cloud (Anthropic) | Exploratory scoring (T=0.8) |
| **Neo4j Database** | Docker container | Local network | Validation results + relationships |
| **FastAPI Backend** | Docker container | Local network | Helper APIs (deduplication, note generation) |
| **Redis Cache** | Docker container | Local network | Session state (optional Phase 1) |
| **PostgreSQL Logs** | Docker container | Local network | Execution logs + audit trail |

### Phase 1 Topology Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    Local Development Machine                   │
│  (MacBook/Linux with Docker, RTX 3060 optional)                │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Docker Network (bridge)                      │ │
│  │              172.17.0.0/16 (docker0)                      │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │   n8n       │  │   Neo4j      │  │  FastAPI     │    │ │
│  │  │ (8080)      │  │  (7474/7687) │  │  (8000)      │    │ │
│  │  │             │  │              │  │              │    │ │
│  │  │ Workflow    │  │ Video schema │  │ Dedup check  │    │ │
│  │  │ Webhook     │  │ Storage      │  │ Note gen     │    │ │
│  │  │             │  │              │  │              │    │ │
│  │  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  │         │                │                  │             │ │
│  └─────────┼────────────────┼──────────────────┼─────────────┘ │
│            │                │                  │                │
│  ┌─────────┴────────────────┴──────────────────┴─────────────┐ │
│  │        Filesystem (Obsidian Vault)                         │ │
│  │   /Users/[user]/Documents/Obsidian/pca-vault/             │ │
│  │   ├─ videos/                                              │ │
│  │   ├─ assessments/                                         │ │
│  │   ├─ knowledge-graph/                                     │ │
│  │   └─ config/                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          │ Internet
                          │
         ┌────────────────┴────────────────┐
         │                                 │
    ┌────▼──────────────┐        ┌────────▼──────┐
    │ Anthropic Cloud   │        │ GitHub        │
    │ API Service       │        │ (Obsidian     │
    │                  │        │  Git Backup)  │
    │ • Claude Sonnet  │        │               │
    │ • Claude Haiku   │        │               │
    └───────────────────┘        └───────────────┘
```

### Phase 1 Docker Compose

```yaml
version: '3.8'

services:
  # n8n Workflow Orchestration
  n8n:
    image: n8nio/n8n:latest
    container_name: pca-n8n
    ports:
      - "8080:3000"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=127.0.0.1
      - N8N_PORT=3000
      - N8N_PROTOCOL=http
      - WEBHOOK_TUNNEL_URL=http://127.0.0.1:8080/
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_POSTGRESDB_DATABASE=n8n
    depends_on:
      - postgres
      - neo4j
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - pca-network
    restart: unless-stopped

  # Neo4j Graph Database
  neo4j:
    image: neo4j:latest
    container_name: pca-neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_dbms_default__listen__address=0.0.0.0
    volumes:
      - neo4j_data:/var/lib/neo4j/data
      - neo4j_logs:/var/lib/neo4j/logs
    networks:
      - pca-network
    restart: unless-stopped

  # PostgreSQL for n8n + Audit Logs
  postgres:
    image: postgres:15-alpine
    container_name: pca-postgres
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - pca-network
    restart: unless-stopped

  # FastAPI Helper Backend
  fastapi:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: pca-fastapi
    ports:
      - "8000:8000"
    environment:
      - NEO4J_HOST=neo4j
      - NEO4J_PORT=7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - OBSIDIAN_VAULT_PATH=/vault
    volumes:
      - ${OBSIDIAN_VAULT_PATH}:/vault:ro
    depends_on:
      - neo4j
    networks:
      - pca-network
    restart: unless-stopped

volumes:
  n8n_data:
  neo4j_data:
  neo4j_logs:
  postgres_data:

networks:
  pca-network:
    driver: bridge
```

### Phase 1 Data Flow

```
1. Input → n8n Webhook
   User captures: "New YouTube video: https://youtube.com/watch?v=..."
   POST /webhook/youtube-validation
   
2. n8n Fetches Video Metadata
   → Get transcript, duration, channel info
   
3. Deduplication Check (FastAPI)
   FastAPI → Neo4j query: "Does video_id exist with validated=true?"
   If found: SKIP dual-agent evaluation
   If not found: PROCEED to agents
   
4. Dual-Agent Evaluation (Anthropic Cloud API)
   Node 4: POST /v1/messages (Sonnet, T=0.3)
   Node 5: POST /v1/messages (Haiku, T=0.8)
   Both agents score 4 dimensions (JSON response)
   
5. Compare & Calculate (n8n JavaScript)
   Compare per-dimension: difference > 15? → disagreement
   Confidence: all agree (95%) → 3 agree (70%) → 2 agree (40%) → 1/0 agree (20%)
   Composite score: average of 4 dimensions
   Routing: PROMOTE (>80) | INBOX (60-80) | ARCHIVE (<60)
   
6. Create Obsidian Note (n8n JavaScript)
   Generate markdown:
   # [Video Title]
   - Channel: [name]
   - Credibility: [score]
   - Quality: [score]
   - Relevance: [score]
   - Alignment: [score]
   - Recommendation: [PROMOTE/INBOX/ARCHIVE]
   Write to: /vault/assessments/[date]/[video-id].md
   
7. Persist to Neo4j (n8n)
   UPSERT VideoCapture node:
   - Properties: all scores, routing, timestamp
   - Relationships: ASSESSED_BY → Screening Agent/Critical Agent
   
8. Summary
   Video validated and indexed in Neo4j, note in Obsidian.
   Cost: ~CAD $0.018 per video
```

### Phase 1 Resilience

**Component Failures:**

| Component | Impact | Recovery |
|-----------|--------|----------|
| **n8n down** | Webhooks not processed | Restart container; queue fills automatically |
| **Anthropic API timeout** | Agents don't respond | n8n retry logic (3x with backoff) |
| **Neo4j down** | Can't persist results | In-memory queue in n8n; resume when Neo4j online |
| **Obsidian vault locked** | Can't write notes | Queue notes in PostgreSQL; flush when vault available |
| **Network offline** | All cloud services blocked | Local queue fills; sync when online |

---

## Phase 2: Self-Hosted Hybrid Topology

### Component Inventory (Additions)

| Component | Technology | Deployment | Purpose |
|-----------|-----------|-----------|---------|
| **Qwen2.5-7B** | Ollama | Local GPU (RTX 3090) | Fast inference (real-time chat) |
| **Qwen2.5-32B** | Ollama | Local GPU (RTX 3090) | Deep inference (synthesis) |
| **BGE-M3 Embeddings** | Ollama | Local GPU | Semantic search (no external API) |
| **ChromaDB** | Vector DB | Local container | Semantic index + RAG retrieval |
| **Redis Cache** | Docker container | Local network | Session context cache |
| **Prometheus** | Docker container | Local network | Metrics collection |
| **Grafana** | Docker container | Local network | Observability dashboards |

### Phase 2 Topology Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    Homelab Hardware                              │
│  (Sovereign Edge Runtime)                                        │
│  ┌────────────────────┐         ┌──────────────────────────────┐ │
│  │  Docker Network    │         │   GPU Hardware               │ │
│  │  172.17.0.0/16     │         │   RTX 3090 24GB VRAM         │ │
│  │                    │         │                              │ │
│  │ ┌─────────────────┐│         │ ┌────────────────────────┐   │ │
│  │ │ n8n             ││         │ │ Ollama Container       │   │ │
│  │ │ (8080)          ││         │ │ (11434)                │   │ │
│  │ │                 ││         │ │                        │   │ │
│  │ │ + orchestration ││         │ │ • Qwen2.5-7B (16GB)   │   │ │
│  │ │ + webhooks      ││         │ │ • Qwen2.5-32B (24GB)  │   │ │
│  │ │                 ││         │ │ • BGE-M3 embeddings   │   │ │
│  │ └────────┬────────┘│         │ └────────┬───────────────┘   │ │
│  │          │         │         │          │                   │ │
│  │ ┌────────▼────────┐│    ┌────▼──────────▼───┐              │ │
│  │ │ Neo4j   (7687)  ││    │ ChromaDB (8000)   │              │ │
│  │ │ Reconciliation  ││    │ Semantic index    │              │ │
│  │ │ engine state    ││    │ RAG retrieval     │              │ │
│  │ └────────────────┬┘│    └───────┬──────────┘               │ │
│  │                  │ │            │                           │ │
│  │ ┌────────────────▼┐│  ┌─────────▼──────────┐               │ │
│  │ │ PostgreSQL      ││  │ Redis Cache        │               │ │
│  │ │ (5432)          ││  │ (6379)             │               │ │
│  │ │ Run logs        ││  │ Session context    │               │ │
│  │ │ Audit trail     ││  │ In-context cache   │               │ │
│  │ └─────────────────┘│  └────────────────────┘               │ │
│  │                    │                                        │ │
│  │ ┌─────────────────┐│  ┌──────────────────┐                │ │
│  │ │ Prometheus      ││  │ Grafana (3000)   │                │ │
│  │ │ (9090)          ││  │ Dashboards       │                │ │
│  │ │ Metrics         ││  │ Alerting         │                │ │
│  │ └─────────────────┘│  └──────────────────┘                │ │
│  │                    │                                        │ │
│  └────────────────────┴────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │            Filesystem (SSD Array)                          │ │
│  │  /nvme0n1/pca/                                            │ │
│  │  ├─ obsidian-vault/                                       │ │
│  │  ├─ ollama-models/                                        │ │
│  │  ├─ chroma-indexes/                                       │ │
│  │  ├─ postgresql-data/                                      │ │
│  │  └─ neo4j-graph/                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                    Internet (Optional)
                         │
         ┌───────────────┴──────────────┐
         │                              │
    ┌────▼────────────┐        ┌────────▼─────┐
    │ Anthropic API   │        │ GitHub Backup│
    │ (Fall-through   │        │ (Vault sync) │
    │  if needed)     │        │              │
    └─────────────────┘        └──────────────┘
```

### Phase 2 Docker Compose (Additions)

```yaml
  # Ollama GPU Inference
  ollama:
    image: ollama/ollama:latest
    container_name: pca-ollama
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_MODELS=/models
    volumes:
      - ollama_models:/models
      - ollama_cache:/root/.ollama
    devices:
      - /dev/nvidia0:/dev/nvidia0  # RTX 3090
      - /dev/nvidiactl:/dev/nvidiactl
      - /dev/nvidia-uvm:/dev/nvidia-uvm
    networks:
      - pca-network
    restart: unless-stopped

  # ChromaDB Vector Store
  chromadb:
    image: ghcr.io/chroma-core/chroma:latest
    container_name: pca-chromadb
    ports:
      - "8001:8000"
    environment:
      - CHROMA_DB_IMPL=duckdb+parquet
      - PERSIST_DIRECTORY=/chroma/data
      - ANONYMIZED_TELEMETRY=false
    volumes:
      - chromadb_data:/chroma/data
    networks:
      - pca-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: pca-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --maxmemory 4gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - pca-network
    restart: unless-stopped

  # Prometheus Metrics
  prometheus:
    image: prom/prometheus:latest
    container_name: pca-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - pca-network
    restart: unless-stopped

  # Grafana Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: pca-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=redis-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana-dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml
    depends_on:
      - prometheus
    networks:
      - pca-network
    restart: unless-stopped

volumes:
  ollama_models:
  ollama_cache:
  chromadb_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Phase 2 Data Flow

Phase 2 adds **local inference** and **reconciliation engine** to Phase 1:

```
Phase 1 flow + additions:

8. Semantic Indexing (New)
   Obsidian note → ChromaDB
   • Generate embeddings (BGE-M3)
   • Store in vector index
   • Enables semantic search + RAG

9. Knowledge Reconciliation (New)
   New VideoCapture → Reconciliation Engine (Qwen2.5-32B local)
   • Compare against existing Neo4j nodes
   • Detect: Reinforce | Contradict | Expand | Ignore
   • Update confidence via Bayesian logic
   • Flag contradictions for HITL review

10. Semantic Search (New)
    User query → ChromaDB (BGE-M3 embeddings)
    → Top K similar Obsidian notes
    → Return with relevance scores

11. Real-Time Chat (New)
    User message → Qwen2.5-7B (local)
    → Fast response (~500ms latency)
    → Context from Redis cache
    → No cloud cost

12. Observability (New)
    All components → Prometheus metrics
    → Grafana dashboards
    → Track: latency, costs, GPU utilization, model quality
```

### Phase 2 Inference Routing

```
Request arrives → Model Router (deterministic)

IF latency_requirement < 100ms:
  use Qwen2.5-7B (local, ~80ms)
  
ELIF input_size < 5KB AND decision_type = scoring:
  use Haiku via Anthropic API (cost optimization)
  
ELIF latency_requirement < 5s:
  use Qwen2.5-7B (local, low cost)
  
ELIF latency_flexible AND quality_critical:
  use Qwen2.5-32B (local, best quality)
  
ELSE:
  use Claude Sonnet (cloud, highest quality, if needed)
```

---

## Phase 3+: Enterprise Topology

### Component Inventory (Phase 3+)

| Component | Technology | Deployment | Purpose |
|-----------|-----------|-----------|---------|
| **Azure Cloud Infrastructure** | Azure VMs | Cloud (GC-approved) | Enterprise compliance, scale |
| **Microsoft Fabric** | Azure Lakehouse | Cloud | Data governance, enterprise data management |
| **Power Automate** | Azure Automation | Cloud | Enterprise workflow orchestration |
| **Azure OpenAI** | LLM Service | Cloud | Compliant inference (Claude Sonnet) |
| **Azure Key Vault** | Secrets | Cloud | Credential management |
| **Azure Purview** | Governance | Cloud | Policy enforcement, audit |
| **Power BI** | BI Platform | Cloud | Executive dashboards |
| **FastAPI Output Engine** | Python Framework | Cloud | Report generation |

### Phase 3 Topology (Conceptual)

```
Enterprise Tenant (Azure)
├─ Identity & Access (Azure AD)
├─ Data Lakehouse (Microsoft Fabric)
│  ├─ Knowledge Graph (migrated from Neo4j)
│  ├─ Reconciliation State
│  └─ Audit Trail
├─ Integration Layer
│  ├─ Power Automate (orchestration)
│  ├─ Azure OpenAI (reasoning)
│  └─ Azure Purview (governance)
└─ Output Engine
   ├─ PowerPoint Generation
   ├─ Word Reports
   ├─ Power BI Dashboards
   └─ Audio (Kokoro TTS)
```

---

## Network Segmentation

### Phase 1-2 Local Network

```
                    🔒 Firewall
                        │
     Host Network: 192.168.1.x (WiFi/Ethernet)
                        │
            ┌───────────┴───────────┐
            │                       │
       Docker0 (Bridge)         Host System
       172.17.0.0/16           (Obsidian vault)
            │
      ┌─────┼─────┬─────────┬─────────┐
      │     │     │         │         │
    n8n  Neo4j  FastAPI  PostgreSQL  Redis
  :8080 :7687  :8000     :5432      :6379
```

**Security Rules:**

- Only n8n and FastAPI expose ports on localhost:8080, 8000
- Neo4j, PostgreSQL, Redis only accessible within Docker network
- Obsidian vault mounted read-only where needed (ChromaDB during Phase 2)
- Anthropic API calls go through n8n HTTP client (supports proxies)

### Phase 1-2 Internet Gateway

```
┌──────────────────────────────────┐
│  Local Machine (Homelab)         │
│  Docker containers               │
└──────────────────┬───────────────┘
                   │
              🔒 Firewall
                   │
        ┌──────────┴──────────┐
        │                     │
    Anthropic API       GitHub
    (HTTPS/TLS)        (HTTPS/TLS)
```

**Principles:**

- All cloud API calls: HTTPS/TLS
- No credential storage in containers (use .env, mounted secrets)
- API keys: never logged, never committed to git
- Backup: Obsidian vault synced to GitHub (private repo)

---

## Data Durability

### Phase 1 Backup Strategy

**Obsidian Vault (Canonical):**
```
Local SSD (primary)
  ↓
Git (local repo) → Push to GitHub (private)
  └─ Daily automated backup via GitHub Actions
```

**Neo4j Database:**
```
PostgreSQL backup (n8n stores backups)
  ↓
Daily dumps to local filesystem
  ↓
Sync to GitHub Gists (encrypted, if needed)
```

**PostgreSQL Logs:**
```
Persistent Docker volume
  ↓
Daily compressed backup
  ↓
Sync to external drive or S3 (Phase 3)
```

### Phase 2 Backup Strategy (Additions)

**ChromaDB Indexes:**
```
Ephemeral (non-critical)
  ↓
Rebuilt from Obsidian on startup
  └─ No separate backup needed
```

**Ollama Models:**
```
Downloaded once, cached locally
  ↓
Can be re-downloaded if lost
  └─ No backup needed (just time to re-pull)
```

**Redis Cache:**
```
Ephemeral session state
  ↓
Persisted to disk (RDB dump)
  └─ Optional: backup for fast recovery
```

---

## Deployment & Startup

### Phase 1 Local Setup (45 minutes)

```bash
# 1. Clone repo
git clone https://github.com/jjuniper-dev/personal-cognitive-architecture
cd personal-cognitive-architecture

# 2. Create .env file
cat > .env << EOF
N8N_USER=admin
N8N_PASSWORD=$(openssl rand -base64 12)
NEO4J_PASSWORD=$(openssl rand -base64 12)
POSTGRES_USER=pca_user
POSTGRES_PASSWORD=$(openssl rand -base64 12)
ANTHROPIC_API_KEY=sk-ant-...
OBSIDIAN_VAULT_PATH=/Users/[user]/Documents/Obsidian/pca-vault
EOF

# 3. Create Obsidian vault structure
mkdir -p $OBSIDIAN_VAULT_PATH/{videos,assessments,knowledge-graph,config}

# 4. Start Docker containers
docker-compose up -d

# 5. Initialize Neo4j schema
docker exec pca-neo4j cypher-shell << EOF
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
EOF

# 6. Configure n8n workflow
# - Login to http://localhost:8080
# - Import workflow from docs/SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md
# - Set environment variables (API keys, Neo4j credentials)

# 7. Test with sample video
curl -X POST http://localhost:8080/webhook/youtube-validation \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://youtube.com/watch?v=...", "title": "Test"}'
```

### Phase 2 Additions (30 minutes)

```bash
# 1. Pull Ollama models (first time: ~20 minutes for 32B)
docker exec pca-ollama ollama pull qwen2.5:7b
docker exec pca-ollama ollama pull qwen2.5:32b
docker exec pca-ollama ollama pull bgem3:latest

# 2. Initialize ChromaDB
# - Creates Chroma directory
# - Ready for embeddings on startup

# 3. Update n8n workflows
# - Add embedding step: POST to ChromaDB
# - Add reconciliation: Call Ollama Qwen2.5-32B

# 4. Configure monitoring
# - Copy prometheus.yml to ./monitoring/
# - Copy grafana-datasources.yml to ./monitoring/
# - Create Grafana dashboards (import templates)

# 5. Verify all services
docker-compose ps
# All containers should be "Up"
```

---

## Monitoring & Observability

### Key Metrics (Phase 2+)

| Metric | Source | Purpose |
|--------|--------|---------|
| **GPU Utilization** | Ollama + nvidia-smi | Detect bottlenecks |
| **Inference Latency** | Prometheus | Model performance |
| **API Cost** | n8n logs | Budget tracking |
| **Error Rate** | PostgreSQL logs | System health |
| **Cache Hit Rate** | Redis | Optimization opportunity |
| **Validation Quality** | Neo4j stats | Agent agreement rate |

### Dashboards (Grafana)

1. **System Health** — GPU, memory, disk, container status
2. **Inference Performance** — Latency by model, cost/video
3. **Validation Metrics** — Agent agreement, routing distribution
4. **Cost Tracking** — API spend vs. budget

---

## Failover & Recovery

### Component Failure Recovery

| Scenario | Impact | Recovery Time | Action |
|----------|--------|---------------|--------|
| **Docker container crashes** | Service unavailable | < 5s | Auto-restart (unless-stopped) |
| **Ollama OOM (out of memory)** | Local inference blocked | 10-30s | Kubernetes pod restart or manual restart |
| **Neo4j data corruption** | Can't persist results | 30-60s | Restore from backup |
| **Obsidian vault locked** | Can't write notes | Variable | Queue in PostgreSQL, flush later |
| **Network offline** | API calls fail | Variable | Retry with exponential backoff |
| **GPU memory exhausted** | Inference timeout | 10-30s | Kill inference process, restart model |

---

## Integration Points

### Control Plane Integration

This topology implements the **Execution Authorization** and **Inference Execution** layers from the Cognitive Control Plane:

```
Request → Policy Gate ✅
        ↓
Execution Authorization:
  - Model Router selects: Qwen2.5-7B | Qwen2.5-32B | Haiku | Sonnet
  - Output Constraints prepared (token limits, format)
  - Monitoring enabled (Prometheus metrics)
        ↓
Inference Execution:
  - n8n calls selected model (local via Ollama or cloud via API)
  - Result captured with metadata
        ↓
Output Validation:
  - Check sensitivity level matches request
  - Verify confidence sufficient
  - Create audit record
        ↓
Return Result
```

---

## Revision History

- **2026-05-12:** Initial version. Specified Phase 1-3 topology, Docker Compose structures, data flow, networking, and failover strategies.

