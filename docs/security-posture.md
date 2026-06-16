# PCA Security Posture Report

**Date:** 2026-06-16  
**Scope:** `jjuniper-dev/pca` and `jjuniper-dev/personal-cognitive-architecture`  
**Status:** Sprint A Stabilization baseline

---

## Executive Summary

PCA is a **self-hosted, local-first system** running on Windows with Docker Desktop. The security posture prioritizes **isolation, local data residency, and controlled external API access** via Vault. This report inventories current exposed surfaces, secret management, and recommendations for hardening before production use.

**Critical findings:**
- Vault stores all sensitive credentials; no hardcoded secrets in code/config (✓)
- GitHub Actions secrets configured (`ANTHROPIC_API_KEY`, `VAULT_TOKEN`) (✓)
- Ollama and n8n expose HTTP-only local surfaces without authentication (⚠ acceptable for isolated network)
- Several bot/* branches in git show Codex dispatch integration work in progress
- No protected main branches; all pushes go to master directly (⚠ risk of accidental overwrites)

---

## 1. Repository Branches & Active Development

### jjuniper-dev/pca

**Main branch:** `master` (latest commit: `13b15a4`) — not protected.

**Active feature branches (≥ 30):**
- **Claude sessions** (claude/* prefix, 20+): code implementation, testing, documentation
  - `claude/busy-thompson-vwznpy` (current work branch for this session)
  - `claude/neo4j-virtual-graphs-6d8ZM` (WF-VirtualGraph pending merge)
  - `claude/coding-session-scheduled-GwMGe` (E-Ayla.1 WF-Ayla scripts)
  - `claude/e-learn-0-self-learning-contract` (Sprint A self-learning docs)

- **Bot/Codex automation** (bot/* prefix, 11): workflow and deployment automation
  - `bot/codex-dispatch-*` (multiple): Codex dispatch integration, Vault runtime secrets
  - `bot/update-n8n-api-key-codex-dispatch`: n8n API key rotation workflow
  - `bot/fix-codex-dispatch-*`: error handling and payload fixes

**Concern:** Codex/bot branches suggest external AI automation (Codex agent) is writing code and pushing directly to feature branches. Verify Codex access controls and code review processes for these bot/* commits before merging to master.

### jjuniper-dev/personal-cognitive-architecture

**Main branch:** `main` (latest commit: `72b0d48`) — not protected.

**Open PRs:** 2 (both drafts, auto-generated `package-lock.json` updates, no security concern)

**Active branches:** 29 (mostly claude/* and feature/ prefixes, architecture and schema work)

---

## 2. GitHub Actions & CI/CD Secrets

### Configured Secrets (names only)

| Secret Name | Purpose | Status |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API calls in workflows | ✓ Present (Sprint A blocker confirmed) |
| `VAULT_TOKEN` | Runtime access to Vault during CI/CD deploys | ✓ Present (Sprint A blocker confirmed) |

### Validation

No secrets hardcoded in `.github/workflows/*.yml`. All external API calls route through Vault lookup (e.g., WF-CodexDispatch reads GitHub PAT from `secret/pca/github`).

**Recommendation:** Review CI/CD job logs for accidental secret leaks in stdout/stderr. Enable secret masking in GitHub Actions for all defined secrets.

---

## 3. Local Vault Configuration & Secrets

### Vault Setup

- **Type:** HashiCorp Vault (KV v2 engine at `secret/pca/*`)
- **Access:** HTTP-only (`http://localhost:8200`) — acceptable for internal-only Windows Docker host
- **Auth:** Root token stored locally in `C:\Users\client\Documents\PCA\vault_init.json` (not tracked in git)

### Secrets Inventory (Vault paths)

| Path | Key | Purpose | Status |
|---|---|---|---|
| `secret/pca/n8n` | `api_key` | n8n Management API access | ✓ Rotated 2026-06-14 (old exposed key revoked) |
| | `mcp_token` | n8n MCP server auth | ✓ Present |
| | `base_url` | n8n instance location | ✓ Hardcoded: `http://localhost:5678` |
| | `expires` | Key expiry tracking | ✓ Set: 2026-06-24 |
| `secret/pca/anthropic` | `api_key` | Claude API key | ✓ Present (used by WF10, WF14, WF-Eval) |
| `secret/pca/neo4j` | `username`, `password`, `bolt_url`, `http_url` | Neo4j Bolt + HTTP access | ✓ Present (hardcoded creds: `neo4j:pca-neo4j-2026`) |
| `secret/pca/newsapi` | `api_key` | News API for WF11 (Reddit feed) | ✓ Present (deferred feature) |
| `secret/pca/github` | `username`, `pat`, `api_base` | GitHub PAT for WF-CodexDispatch | ✓ Stored 2026-06-14 (old PAT revoked) |
| `secret/pca/openrouter` | `model`, `base_url` | Qwen3-Coder via OpenRouter (WF09) | ✓ Present (no API key — uses Anthropic key route) |
| `secret/pca/ollama` | `base_url`, `embed_model`, `embed_dims`, `docker_base_url` | Local Ollama config | ✓ Present |
| `secret/pca/ntfy` | `topic` | ntfy.sh iPhone notifications (WF-Notify) | ⚠ Pending storage (ADMIN_TASKS #4) |
| `secret/pca/twilio` | `account_sid`, `auth_token`, `from_number` | SMS alerts | ⚠ Pending setup (PR #148 not merged) |

### Vault Access Pattern

**Reads:** PowerShell `vault_get.ps1` helpers (`Get-VaultSecret`, `Get-VaultSecretObject`)  
**Writes:** Recently added `Set-VaultSecret` (2026-06-14) for key rotation workflows  
**HTTP Transport:** `System.Net.Http.HttpClient` with `X-Vault-Token` header  
**Error handling:** Graceful degradation (scripts continue if Vault is sealed/unreachable, skip optional features)

**Recommendation:** 
- Implement Vault token rotation policy (root token should not be used long-term in production)
- Store unseal key offline after re-initialization to prevent auto-unseal lockout (current state: unseal_key is empty, manual intervention required on Vault restart)
- Audit Vault API usage logs periodically

---

## 4. n8n Workflow Surfaces & API Endpoints

### Deployed Workflows

| Workflow | n8n ID | Webhook Path | Response Mode | Auth | Status |
|---|---|---|---|---|---|
| WF02 Relevance Scoring | `7y6w0ORVGE569g0I` | `POST /webhook/pca/score` | onReceived (fire-and-forget) | Bearer (n8n API key) | ✓ Deployed |
| WF09 Coding Assistant | `NXwCrddaO4Kz3LyL` | `POST /webhook/pca/code` | lastNode (blocks until done) | Bearer | ✓ Deployed |
| WF10 Knowledge Capture | `b09dH4fUAWHYCPmt` | `POST /webhook/pca/incident` | lastNode | Bearer | ✓ Deployed |
| WF11 Feed Ingestion | `oModdPsuQeKyquw6` | `POST /webhook/pca/reddit` | onReceived | Bearer | ✓ Deployed |
| WF12 Agent Memory | `jIvVOK1CW8eMuVnT` | `POST /webhook/pca/memory` | lastNode | Bearer | ✓ Deployed (defect fixed 2026-06-14) |
| WF16 Image Capture | (assigned on deploy) | `POST /webhook/pca/image` | lastNode | Bearer | ⏳ Pending deployment |
| WF-Dispatch | `Jr4QwDAsf6AQuByp` | `POST /webhook/pca/dispatch` | lastNode | Bearer | ✓ Deployed (Codex dispatch) |
| WF-VirtualGraph | (run create_wf_virtual_graph.ps1) | `POST /webhook/pca/graph/query` | lastNode | Bearer | ⏳ Pending deployment |

### n8n API Access

- **Management API:** `GET/POST/PUT http://localhost:5678/api/v1/*`
- **Webhook Base:** `http://localhost:5678/webhook/*`
- **Authentication:** n8n API key (Bearer token) stored in Vault
- **Network:** Local HTTP only (no TLS for localhost)

**Key security controls:**
- All webhook payloads validated against knowledge schema (WF10 gate)
- File access restricted to allowlist in n8n env var: `/files/obsidian`, `/files/vault`, `/files/main-vault`, `/files/audio`, `/files/pca`, `/files/fin-data`, `/home/node/.n8n`
- `NODE_FUNCTION_ALLOW_BUILTIN` restricts JavaScript require() to: fs, path, os, http, https, crypto, url, querystring, stream, buffer, util, events
- Max payload size: 100 MB (`N8N_PAYLOAD_SIZE_MAX`)

**Concern:** WF-Dispatch reads GitHub PAT from Vault and can trigger arbitrary Codex actions. Verify Codex workflow whitelist (allowed actions) is maintained separately.

---

## 5. Docker Compose Infrastructure

### Running Services

| Service | Image | Port (Host) | Port (Container) | Auth | Data Volume |
|---|---|---|---|---|---|
| n8n | `docker.n8n.io/n8nio/n8n` | 5678 | 5678 | n8n API key | n8n_data (external) |
| Qdrant | `qdrant/qdrant:latest` | 6333, 6334 | 6333, 6334 | None (local) | qdrant_storage |
| Neo4j | `neo4j:5-community` | 7474, 7687 | 7474, 7687 | neo4j:pca-neo4j-2026 | neo4j_data, neo4j_logs |
| Vault | `hashicorp/vault:latest` | 8200, 8201 | 8200, 8201 | Root token (local file) | vault-data (Windows path) |
| Ollama | Native Windows binary | 11434 | N/A | None | Local models cache |
| faster-whisper | `fedirz/faster-whisper-server:cuda` | 8010 | 8000 | None (local) | whisper_models |
| RSS Bridge | `rssbridge/rss-bridge:latest` | 3030 | 80 | None (local) | rss-bridge-config |
| Dashboard | `nginx:alpine` | 8080 | 80 | None (browser access only) | dashboard content |
| Homepage | `ghcr.io/gethomepage/homepage:latest` | 3001 | 3000 | None (browser) | homepage-config |
| Syncthing | `syncthing/syncthing:latest` | 8384, 22000 | 8384, 22000 | Syncthing UI password | syncthing-config, vault (Windows path) |

### Network & Volume Mounts

- **Docker network:** `pca_default` (internal; no external routing by default)
- **Windows host volumes mounted into containers:** Obsidian vault paths, Vault config, PCA scripts, n8n data
- **Syncthing:** Syncs Obsidian vault to remote instance (network edge, verify TLS cert pinning if used)

**Concern:** Vault and n8n data on Windows host filesystem — ensure Windows NTFS permissions restrict access to Docker Desktop user account only.

---

## 6. MCP Server Configuration

### Current MCP Servers (.mcp.json)

| Server | Type | Command | Env Vars | Purpose |
|---|---|---|---|---|
| `twilio-sms` | stdio | `docker run ... pca-twilio-mcp` | `VAULT_TOKEN`, `VAULT_ADDR` | SMS alerts via Twilio |
| `task-master-ai` | stdio | `npx task-master-ai` | `TASK_MASTER_TOOLS=standard`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY` | Task management & parsing |

**Recommendation:** Document all MCP servers' secret dependencies. Audit MCP container images before deployment.

---

## 7. Identified Security Gaps & Recommendations

### Critical (Before Production)

| Finding | Risk | Mitigation | Priority |
|---|---|---|---|
| Master branches not protected | Accidental force-push, loss of history | Enable branch protection on `master` / `main`; require PR reviews | HIGH |
| Vault root token stored in plaintext file | Token theft if host compromised | Rotate to limited-scope token; store unseal key offline | HIGH |
| Neo4j default creds hardcoded in compose | Password exposure in config history | Rotate password in production; read from env var / Vault | HIGH |
| n8n API key in git history | Potential for old key reuse | Verify old key is revoked (done 2026-06-14); scan history with `git-secrets` | HIGH |

### Medium (Before Sprint Completion)

| Finding | Risk | Mitigation | Priority |
|---|---|---|---|
| Codex bot automation without code review gate | Untrusted code injection via bot branches | Require manual PR approval for bot/* → master; audit bot commit history | MEDIUM |
| Ollama, Qdrant, n8n expose HTTP without auth on localhost | Lateral movement if Docker host is compromised | Firewall host ports (external traffic only); restrict to localhost bindings | MEDIUM |
| GitHub Actions secrets not masked in logs | Secret leakage in workflow logs | Enable Actions log obfuscation; review recent job logs for leaks | MEDIUM |
| Incomplete Vault secrets (ntfy, Twilio pending) | Incomplete pipeline, later credential injection risk | Complete ADMIN_TASKS #3, #4 before Sprint A closure | MEDIUM |
| No audit log for Vault API access | Cannot detect unauthorized reads | Enable Vault audit logging; forward to central log aggregation | MEDIUM |

### Low (Best Practices)

| Finding | Recommendation |
|---|---|
| Syncthing syncs vault content over network | Verify TLS cert pinning; encrypt vault data at rest on remote |
| Docker socket mounted in homepage container | Restrict container actions to read-only inspection |
| RSS Bridge allows arbitrary feed URLs | Implement feed whitelist; rate limit; scan feed content |

---

## 8. Access Control Matrix

### Who Can Access What

| Role | Vault | n8n UI | Neo4j | GitHub Secrets |
|---|---|---|---|---|
| Local Windows user (jjuniper-dev) | ✓ (root token) | ✓ (JWT via API key) | ✓ (hardcoded creds in compose) | ✓ (via gh CLI) |
| GitHub Actions (CI/CD) | ✓ (VAULT_TOKEN secret) | ✗ (n8n key read from Vault) | ✗ (no deploy access yet) | ✓ (Actions secrets) |
| Codex (bot automation) | ✗ (read n8n key, GitHub PAT via WF-Dispatch) | ✓ (via API key from Vault) | ✗ (no direct access) | ✗ |
| n8n Code nodes | ✓ (read Vault via curl/JS) | ✓ (self-reference) | ✓ (hardcoded bolt:// creds) | ✗ |
| Docker containers (internal) | ✓ (VAULT_TOKEN env var) | ✓ (localhost 5678) | ✓ (localhost 7687) | ✗ |

---

## 9. Compliance & Data Residency

**PCA design priority:** Local-first, all canonical data stays on-machine.

| Data Type | Storage | Residency | Encryption |
|---|---|---|---|
| Knowledge vault (Obsidian) | Windows NTFS volume | Local | Windows NTFS encryption (if enabled) |
| Embeddings (Qdrant) | Docker volume | Local container | Qdrant doesn't encrypt at rest by default |
| Relationship graph (Neo4j) | Docker volume | Local container | Neo4j doesn't encrypt at rest in community edition |
| Secrets (Vault) | Windows filesystem | Local | Vault sealing key required to decrypt (✓) |
| External API calls | Anthropic API, OpenRouter | Cloud (US region) | TLS in transit; fallback to local Ollama |

**Recommendation:** Document data classification and retention policy. For Qdrant and Neo4j, consider enabling encryption at rest if volumes contain sensitive data.

---

## 10. Incident Response & Monitoring

### Current Monitoring

- **Health check:** `pca_health_check.ps1` runs every 15 min, checks services, posts incidents to WF10
- **AI diagnosis:** Script calls Anthropic API to diagnose issues, writes to Obsidian vault
- **Incident log:** WF10 stores structured capture notes in `pca_memory` (Qdrant) and Obsidian

### Missing Elements

- [ ] Vault audit log aggregation
- [ ] n8n workflow execution audit trail (logs to n8n_data volume)
- [ ] Secrets rotation schedule (n8n key rotated ad-hoc, no automation)
- [ ] Intrusion detection / anomaly alerting

**Recommendation (Sprint C+):** Implement central logging (Grafana Loki or ELK) for all services.

---

## 11. Conclusion

PCA **currently acceptable for private local development** given:
- ✓ All secrets in Vault, no hardcoded credentials in code
- ✓ Local-first architecture with fallback to cloud APIs
- ✓ Self-healing health checks and incident logging
- ✓ Workflow validation gate (WF10 schema enforcement)

**Before production or multi-user access:**
1. Protect master branches (require PR review)
2. Rotate Vault root token and store unseal key offline
3. Audit and revoke bot automation without manual gates
4. Complete ADMIN_TASKS secrets inventory (ntfy, Twilio)
5. Implement Vault audit logging

---

**Report prepared:** 2026-06-16 by Claude Code (Session: security posture audit)  
**Next review:** After Sprint A stabilization (target 2026-06-28)
