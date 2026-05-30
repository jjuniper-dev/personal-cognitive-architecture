# Virtual Graph Layer

> Added: 2026-05-30
> Status: Implemented in pca repo (branch claude/neo4j-virtual-graphs-6d8ZM)
> Ref: neo4j.com/blog/graph-database/introducing-neo4j-virtual-graph-graph-reasoning-on-the-data-you-already-have/

## Problem: Siloed Knowledge Stores

PCA writes knowledge to three stores simultaneously (WF10), but each store is
only queryable on its own terms:

| Store   | Query capability        | Blind spot                              |
|---------|-------------------------|-----------------------------------------|
| Neo4j   | Structural relationships | Cannot weight by semantic relevance     |
| Qdrant  | Semantic similarity      | Cannot traverse structural connections  |
| DuckDB  | SQL aggregations         | Cannot participate in graph reasoning   |

This creates a retrieval ceiling: the best answer to most queries lives at the
intersection of semantic relevance (Qdrant) and structural context (Neo4j),
but no single query can reach both.

## Solution: Virtual Graph Projection

Inspired by Neo4j Virtual Graph (announced May 2026), PCA implements a local
bridge pattern called WF-VirtualGraph:

1. **Embed** the query via Ollama
2. **Search Qdrant** for semantically similar nodes across collections
3. **Anchor** each hit in Neo4j by matching on title/name
4. **Traverse** the graph 1-2 hops from each anchor
5. **Return** a unified context block combining both layers

No data is moved between stores. No permanent cross-store edges are written.
The virtual subgraph exists only for the duration of the query.

## Architectural Position

```
Layer 5 (Agentic Runtime)
  |
  v
Layer 4 (Retrieval)
  |
  +-- WF12: Agent Memory (Qdrant pca_memory + Neo4j Memory nodes)
  +-- WF-VirtualGraph: Cross-store graph reasoning          <-- this layer
  +-- embed_vault.ps1: Vault embedding into Qdrant pca_vault
  |
  v
Layer 3 (Knowledge Stores)
  +-- Neo4j (structural graph)
  +-- Qdrant (semantic vectors)
  +-- DuckDB (financial data)
```

WF-VirtualGraph sits at Layer 4 (Retrieval), above the stores and below
the agentic runtime. It produces the same context-block format as WF12,
so agents can use either interchangeably.

## Data Flow

```
GET /webhook/pca/graph/query
  { query, hops, min_score, collections }
         |
         v
    Ollama embed
         |
         v
    Qdrant search          Neo4j MATCH
    pca_vault      ---->   (n) WHERE n.title = $t
    pca_memory             -[r*1..2]->(m)
         |
         v
    Score fusion + context assembly
         |
         v
    { context, stats, raw }
```

## Deployment

See `pca` repo:
- `virtual-graphs.md` — full design doc with known limits and future path
- `create_wf_virtual_graph.ps1` — deploys WF-VirtualGraph to n8n
- `test_wf_virtual_graph.ps1` — 3-case verification script
- `BACKLOG.md` E9.1 — tracks deploy + verify on target machine

## Future: Official Neo4j Virtual Graph Integration

The official Neo4j Virtual Graph product (private preview as of May 2026)
connects Neo4j to Snowflake and Databricks via zero-copy Cypher queries.
When it reaches GA, PCA could expose:

- **DuckDB** financial data as a virtual graph: `(:Transaction)-[:SAME_MERCHANT]->(:Transaction)`
- **PostgreSQL** n8n execution log as a Cypher-queryable workflow graph
- All without ETL — data stays in its native store

This is the longer-term convergence point for PCA's multi-store knowledge architecture.
