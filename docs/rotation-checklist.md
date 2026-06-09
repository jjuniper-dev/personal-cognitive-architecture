# Credential Rotation Checklist

**Version:** 0.1  
**Date:** 2026-06-09  
**Owner:** PCA runtime  
**Classification:** Internal — do not commit credential values  

Execute this checklist whenever:
- A credential is approaching its rotation frequency (see column in `docs/security-posture.md`)
- A credential may have been exposed (leaked URL, lost device, repo incident)
- A team member's access is revoked

After completing each section, record the rotation in the audit log at the bottom of this document.

---

## 1. GitHub Personal Access Token (PAT)

**Rotation frequency:** 90 days  
**Used by:** GitHub MCP server, Obsidian Git plugin, Codex API calls, GitHub vault connector

### Steps

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Locate the current PCA token (named "PCA Dashboard" or similar)
3. Click **Regenerate** — copy the new token immediately (it will not be shown again)
4. Update the token in every location it is stored:
   - Local `.env` file (`GITHUB_TOKEN=<new-token>`)
   - n8n credential store: **Credentials → GitHub → update token field**
   - Obsidian Git plugin settings: **Settings → Obsidian Git → Authentication → update token**
5. Restart any running n8n workflows that use the GitHub credential
6. Verify: trigger a vault structure check or run `pnpm test -- github-connector.test.ts` — confirm no 401 errors
7. Revoke the old token in GitHub settings

**Verification:** GitHub API returns 200 for an authenticated request. No 401 in n8n workflow logs.

---

## 2. Anthropic API Key

**Rotation frequency:** 90 days  
**Used by:** Claude Code CLI, n8n Claude nodes

### Steps

1. Go to **console.anthropic.com → API keys**
2. Click **Create key** — name it with the date: `pca-YYYY-MM-DD`
3. Copy the new key immediately
4. Update in every location:
   - Local `.env` file (`ANTHROPIC_API_KEY=<new-key>`)
   - n8n credential store: **Credentials → Anthropic → update key field**
   - Claude Code CLI: update via `claude config set apiKey <new-key>` or update the env var Claude Code reads
5. Run a test prompt via Claude Code to confirm the key works
6. Delete the old key in the Anthropic console
7. Verify: `claude -p "say ok"` returns a response with no auth error

**Verification:** Successful Claude Code response. No 401 in n8n logs.

---

## 3. OpenAI API Key

**Rotation frequency:** 90 days  
**Used by:** Event concierge PoC, Responses API calls in n8n

### Steps

1. Go to **platform.openai.com → API keys**
2. Click **Create new secret key** — name it `pca-YYYY-MM-DD`
3. Copy the new key immediately
4. Update in every location:
   - Local `.env` file (`OPENAI_API_KEY=<new-key>`)
   - n8n credential store: **Credentials → OpenAI → update key field**
5. Trigger a test call in n8n (any workflow using OpenAI) and confirm success
6. Delete the old key in the OpenAI dashboard
7. Verify: n8n workflow using OpenAI completes without auth error

**Verification:** Successful OpenAI API response. No 401 in n8n logs.

---

## 4. n8n Webhook Secrets

**Rotation frequency:** 180 days  
**Used by:** WF10, WF12, WF15 inbound triggers; iOS shortcut mobile capture

### Steps

1. Generate a new secret: `openssl rand -hex 32`
2. In n8n: **Workflows → open each webhook-triggered workflow → Webhook node → update the path or add/update the header secret**
3. Update the secret in the iOS Shortcut:
   - Open **Shortcuts app → PCA Capture shortcut → Edit**
   - Find the HTTP request action → update the `X-Webhook-Secret` header value (or equivalent)
4. Update in local `.env` if the secret is referenced there (`N8N_WEBHOOK_SECRET=<new-secret>`)
5. Send a test capture from the iOS shortcut and confirm it reaches n8n successfully
6. Confirm the old secret is no longer accepted (send a request with the old value — expect rejection)

**Verification:** Test capture arrives in n8n. Replay with old secret is rejected.

---

## 5. Neo4j Credentials

**Rotation frequency:** 180 days  
**Used by:** WF10 knowledge graph queries, direct Cypher access

### Steps

1. Connect to the Neo4j instance: `docker exec -it <neo4j-container> cypher-shell -u neo4j -p <current-password>`
2. Run: `ALTER USER neo4j SET PASSWORD '<new-password>';`
3. Update in every location:
   - Local `.env` file (`NEO4J_PASSWORD=<new-password>`)
   - n8n credential store: **Credentials → Neo4j → update password**
   - `docker-compose.yml` or `.env.docker` if Neo4j password is set there
4. Restart n8n to reload credentials
5. Trigger a test workflow that queries Neo4j and confirm success
6. Verify: n8n Neo4j node returns results without auth error

**Verification:** n8n workflow completes a graph query. No auth error in logs.

---

## 6. Obsidian Vault GitHub Token

**Rotation frequency:** 90 days (shares lifecycle with GitHub PAT — rotate together)  
**Used by:** Obsidian Git plugin for vault backup to GitHub

If this uses the same PAT as section 1, rotating the PAT and updating Obsidian Git covers this section. If a separate fine-grained PAT is used:

1. Go to **GitHub → Settings → Developer settings → Fine-grained tokens**
2. Generate a new token scoped to the Obsidian vault repo only (Contents: read/write)
3. Update in **Obsidian → Settings → Obsidian Git → Authentication/token field**
4. Trigger a manual git push from Obsidian and confirm success
5. Revoke the old token

**Verification:** Obsidian Git push completes. No auth error in Obsidian Git status bar.

---

## 7. Ollama Local Runtime

**No credentials to rotate** — Ollama runs without authentication on the local network by default.

**Review trigger:** If Ollama is ever exposed beyond the local network (e.g. via ngrok, tailscale, or port-forwarding), add authentication at that point and add a new checklist section here.

Current posture: acceptable for local-only deployment. See risk R7 in `docs/security-posture.md`.

---

## Audit Log

Record each rotation here. Do not record credential values — record class, date, and rotator only.

| Date | Credential Class | Rotated By | Notes |
|---|---|---|---|
| — | — | — | Initial checklist created; no rotations yet performed |

---

## Related

- `docs/security-posture.md` — full surface inventory and risk register (Sec.0)
- `docs/runtime-policy-gate.md` — runtime governance controls
