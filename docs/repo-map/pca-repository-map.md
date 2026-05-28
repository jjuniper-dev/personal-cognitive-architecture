# PCA Repository Map

Status: draft  
Created: 2026-05-28  
Purpose: define how the PCA repositories relate so humans and LLM code bots do not treat them as competing sources of truth.

---

## Repository Roles

| Repository | Visibility | Default Branch | Canonical Role |
|---|---:|---|---|
| `jjuniper-dev/personal-cognitive-architecture` | public | `main` | Architecture, planning, decisions, use cases, epics, bot instructions, branch reconciliation |
| `jjuniper-dev/pca` | private | `master` | Local runtime implementation: Docker, n8n, Qdrant, Neo4j, Vault, Whisper/Ollama-adjacent services, dashboards, operations |

Working rule:

```text
personal-cognitive-architecture defines.
pca implements.
```

---

## Source-of-Truth Split

### `personal-cognitive-architecture` owns

- PCA vision and principles
- PCA/Ayla naming rules
- capability model
- use cases and epics
- architecture decision records
- branch reconciliation
- Claude/Codex/local-agent instructions
- MVP definition
- event/backbone design
- governance and audit model
- runtime requirements

### `pca` owns

- `docker-compose.yml`
- runtime service configuration
- local runbooks
- `.env.example`
- Vault configuration templates
- n8n workflow exports
- local dashboard assets
- service health checks
- backup/restore procedures
- operational scripts

---

## What Each Repo Should Not Own

### `personal-cognitive-architecture` should not own

- live secrets
- machine-local credentials
- host-specific runtime paths except examples
- production `.env` files
- operational state
- local data volumes
- large generated runtime artifacts

### `pca` should not own

- long-form architecture debate
- canonical epics
- system-wide architecture decisions without links back to the architecture repo
- broad PCA/Ayla naming changes
- conceptual experiments not tied to runtime implementation

---

## Architecture-to-Runtime Traceability

| Architecture Concept | Architecture Repo Location | Runtime Repo Location | Status |
|---|---|---|---|
| Capture pipeline | `docs/delivery/`, iOS capture docs, use cases | n8n workflows, mounted vault paths | Needs reconciliation |
| Canonical memory | Obsidian/vault architecture docs | mounted vault volumes in `docker-compose.yml` | Active but needs documentation |
| Vector retrieval | architecture docs / future event model | Qdrant service | Runtime exists; integration status unclear |
| Graph memory | architecture docs / graph model | Neo4j service | Runtime exists; schema status unclear |
| Secrets management | governance/security docs | Vault service | Runtime exists; hardcoded credential cleanup needed |
| Transcription | capture/multimodal docs | `faster-whisper` service | Runtime exists; workflow status unclear |
| Weak-signal capture | future capability/prototype branch | RSS Bridge / weak signal branch | Future capability, not MVP core |
| Dashboard | architecture/runtime topology docs | `dashboard`, `homepage` services | Runtime exists; role needs docs |

---

## Bot Operating Model

Claude, Codex, Cursor, and local coding agents should read this map before making cross-repo changes.

If a task asks for architecture, design, planning, reconciliation, or decision framing, work in:

```text
jjuniper-dev/personal-cognitive-architecture
```

If a task asks for Docker, service config, runtime health, workflows, or local operations, work in:

```text
jjuniper-dev/pca
```

If a task spans both, produce a two-part plan first.

---

## Cross-Repo Change Rule

Before changing both repos, state:

```text
Architecture change:
Runtime change:
Traceability link:
Verification path:
Rollback path:
```

Do not silently implement runtime behaviour that contradicts architecture docs.

Do not update architecture docs to match accidental runtime state without calling out the decision.

---

## Current Cleanup Priority

1. Make `personal-cognitive-architecture` canonical for repo map, branch reconciliation, and PCA V1 definition.
2. Make `pca` self-documenting as the runtime repo.
3. Externalize hardcoded credentials from `pca/docker-compose.yml`.
4. Extract high-value architecture documents from old branches into `main` through reviewable PRs.
5. Quarantine prototype branches until PCA V1 loop is stable.

---

## Principle

The two repos should behave like a small enterprise architecture/control-plane split:

```text
Architecture repo = control and intent
Runtime repo = execution and operations
```

This is the same PCA pattern applied to the PCA project itself.
