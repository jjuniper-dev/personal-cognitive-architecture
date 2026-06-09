# PCA Security Posture Report

**Version:** 0.1  
**Date:** 2026-06-09  
**Owner:** PCA runtime  
**Status:** Point-in-time baseline  
**Classification:** Internal  

---

## Purpose

This report inventories every credential surface, data sensitivity surface, and runtime control in the PCA system. It produces a prioritised risk register. It is a baseline — not a threat model and not a penetration test.

Update this document whenever a new credential class is introduced, a surface changes, or a risk is resolved.

---

## 1. Credential and Secret Surface Inventory

| Credential Class | Where It Lives | Used By | Rotation Frequency | Current Control |
|---|---|---|---|---|
| GitHub Personal Access Token (PAT) | Local env / n8n credentials store | GitHub MCP, vault connector, Codex API calls | 90 days | Manual rotation; no expiry enforcement |
| Anthropic API key | Local env / n8n credentials store | Claude Code CLI, n8n Claude nodes | 90 days | Manual rotation; no expiry enforcement |
| OpenAI API key | Local env / n8n credentials store | Event concierge PoC, Responses API calls | 90 days | Manual rotation; no expiry enforcement |
| n8n webhook secrets | n8n credential store (encrypted at rest) | WF10, WF12, WF15 inbound triggers | 180 days | Stored in n8n encrypted store; not in repo |
| Obsidian vault GitHub token | Local env | Obsidian Git plugin | 90 days | Manual; same PAT class as GitHub PAT above |
| Neo4j credentials (username + password) | Local env / Docker compose env | WF10, knowledge graph queries | 180 days | Local only; not exposed externally |
| Ollama runtime | Local network only | All local model calls | N/A — no credential | No auth by default; access by network isolation |
| Claude Code session tokens | Ephemeral — not persisted | Active sessions only | Per-session | Auto-expired; no durable storage |

**Critical gap:** No centralised secret manager. All credentials live in local environment variables or n8n's encrypted store. There is no rotation reminder or expiry enforcement.

---

## 2. Data Sensitivity Surface Inventory

| Surface | Data Type | Classification | Current Control |
|---|---|---|---|
| Obsidian vault | Personal knowledge, decisions, preferences, health notes | Confidential | Local filesystem; GitHub private repo backup |
| PCA GitHub repo (this repo) | Architecture docs, agent contracts, schemas | Internal | Public repo — see risk R1 |
| n8n workflow state | Captured inputs, processed events, routing decisions | Internal–Confidential | Local n8n instance; not cloud-hosted |
| Neo4j graph | Knowledge nodes, relationships, entity data | Internal–Confidential | Local Docker instance; not exposed externally |
| Session handover files | Session objectives, decisions, learning candidates | Internal | In-repo files — confirm no sensitive content before commit |
| Cloud model API calls | Prompt content sent to Anthropic/OpenAI | Confidential | Governed by runtime policy gate; restricted data must not burst to cloud |
| Voice capture pipeline | Audio transcripts from iPhone | Confidential | Local transcription via Whisper; audio not persisted after transcription |
| iOS shortcuts / mobile capture | Brief text captures from phone | Internal | Sent via HTTPS to n8n webhook; webhook secret required |

**Critical gap:** The public GitHub repo (`personal-cognitive-architecture`) currently contains personal health content (see repo audit 2026-06-03). This is classified as Confidential and must not be in a public repository.

---

## 3. Runtime Boundary Controls

| Control | Description | Status |
|---|---|---|
| Runtime Policy Gate | Governs execution authorisation, model routing, HITL escalation, memory promotion | Documented in `docs/runtime-policy-gate.md`; partially implemented in n8n |
| Human-in-the-loop (HITL) gates | Required for memory promotion, canonical writes, external communications | Defined in policy gate; n8n approval nodes partially wired |
| Cloud escalation restriction | Sensitive/confidential data must not be sent to cloud models | Policy defined; enforcement is manual — no automated classification check at API boundary |
| Data classification tagging | All captured content should be tagged with sensitivity level at ingest | Defined in schema; not consistently applied at runtime |
| Least-privilege agent tool access | Agents receive only the minimum tools required for their role | Defined in CLAUDE.md; enforced by Claude Code permission prompts per session |
| Secrets excluded from repo | `.gitignore` excludes env files and credential files | `.gitignore` exists; see risk R3 for tracked files that should be excluded |
| Audit logging | All consequential actions should produce an audit record | Defined in policy gate; not yet implemented at runtime |

---

## 4. Risk Register

| ID | Risk | Likelihood | Impact | Priority | Owner | Status |
|---|---|---|---|---|---|---|
| R1 | Personal health content (`ADHD_STATE_TRACKER_V2.md`, `STATE_TRACKER_GUIDE.md`, `meeting-anxiety-management.md`, `ADM_Accountability_Framework.pptx`) exists in a public GitHub repository | High — files are currently committed and public | High — privacy exposure | **Critical** | Repository owner | Open — delete files and move to Obsidian vault |
| R2 | No centralised secret manager; credentials stored in local env vars with no rotation enforcement or expiry alerting | High — credentials may be stale | High — stale PAT or API key could be exploited if leaked | **High** | Repository owner | Open — rotation checklist in `docs/rotation-checklist.md`; secret manager is future work |
| R3 | `vault_embed_state.json` and other files are tracked in the `pca` repo despite being listed in `.gitignore` (committed before ignore rule added) | Confirmed — files are tracked | Medium — operational state in version history | **High** | Repository owner | Open — run `git rm --cached` per repo audit findings |
| R4 | Cloud escalation restriction is policy-only; no automated enforcement at the API boundary prevents confidential content from being sent to Anthropic/OpenAI | Medium — relies on manual classification | High — confidential data sent to cloud model | **High** | PCA runtime | Open — automated classification check at policy gate is future work |
| R5 | n8n instance runs locally with no network-level authentication; any process on the local network can reach n8n UI and trigger workflows | Medium — home network only | Medium — unauthorised workflow execution | **Medium** | Repository owner | Open — add n8n basic auth or tunnel authentication |
| R6 | Webhook secrets are single-factor; a leaked webhook URL allows unauthenticated payload injection into the capture pipeline | Low — URLs not public | High — injected payloads could corrupt knowledge base | **Medium** | Repository owner | Open — add HMAC payload signing to mobile capture webhook |
| R7 | Ollama runs with no authentication by default; any local process can invoke any loaded model | Low — local only | Low — model misuse, not data exposure | **Low** | Repository owner | Open — acceptable for local-only deployment; revisit if Ollama is network-exposed |

---

## 5. Immediate Actions

In priority order:

1. **R1** — Delete personal health files from this public repo: `docs/ADHD_STATE_TRACKER_V2.md`, `docs/STATE_TRACKER_GUIDE.md`, `docs/meeting-anxiety-management.md`, `docs/ADM_Accountability_Framework.pptx`. Move content to Obsidian vault.
2. **R2** — Execute rotation checklist (`docs/rotation-checklist.md`) for all credentials. Set calendar reminders for next rotation.
3. **R3** — Run `git rm --cached vault_embed_state.json` and other tracked-but-ignored files in the `pca` repo.
4. **R4** — Add data classification check to n8n policy gate node before any cloud model call.
5. **R5** — Enable n8n basic authentication in n8n settings.

---

## 6. Out of Scope

- Threat modelling — future work
- Penetration testing — future work
- Automated secret rotation tooling — future work
- Secret manager integration (HashiCorp Vault, AWS Secrets Manager, etc.) — future work

---

## Related

- `docs/runtime-policy-gate.md` — runtime governance controls
- `docs/pca-compliance-and-governance.md` — compliance framework
- `docs/rotation-checklist.md` — executable rotation steps (Sec.1)
- `docs/repo-audit/2026-06-03-root-alignment.md` — repo audit findings
