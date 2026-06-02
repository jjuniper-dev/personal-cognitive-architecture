# GitHub MCP Operating Model

> **Work package:** PCA-WP-GITHUB-ACCESS-001
> **Status:** pending — setup requires manual steps on target machine
> **Backlog reference:** `pca/BACKLOG.md` → PCA-WP-GITHUB-ACCESS-001

## Role

The GitHub MCP server is an **agent convenience bridge**, not the authoritative Git execution path.

```
Claude / local agent
   ↓
GitHub MCP server
   ↓
GitHub API
   ↓
pca + personal-cognitive-architecture repos
```

MCP sits behind the Runtime Policy Gate concept:

```
low-risk read        → allowed
issue creation       → allowed with summary
file write           → branch + PR required
workflow edit        → explicit approval
secret touch         → blocked
force push / delete  → blocked
```

---

## Allowed Uses

- Read repository files
- Inspect issues and PRs
- Create issues
- Create branches
- Create small documentation PRs
- Comment on PRs
- Fetch PR diffs

---

## Restricted Uses

- No direct commits to `master` or `main`
- No force pushes
- No branch deletion
- No secret modification
- No production workflow modification without explicit approval
- No repository-wide refactors through MCP alone

---

## Required Write Pattern

All writes must follow:

```
branch → commit → PR → human review → merge
```

---

## PCA Authority Hierarchy

| Resource | Authority |
|----------|-----------|
| `jjuniper-dev/pca/BACKLOG.md` | Single authoritative backlog for all PCA work |
| `jjuniper-dev/pca` | Operational and runtime repo (scripts, workflows, schemas) |
| `jjuniper-dev/personal-cognitive-architecture` | Architecture and agent-definition repo |
| PCA | Platform / system name |
| Ayla | Persona / interface only — not the infrastructure |

---

## Phased Permission Rollout

### Phase 1 — Read-Only Validation

Verify MCP server stability before granting write access.

**PAT permissions:**
- Contents: Read-only
- Issues: Read-only
- Pull requests: Read-only
- Metadata: Read-only

### Phase 2 — Controlled Write

Enable issue creation and branch/PR workflows.

**Add:**
- Contents: Read and write
- Issues: Read and write
- Pull requests: Read and write

All writes still require branch → PR → human merge.

### Phase 3 — Automation (deferred)

Only add when workflow automation is explicitly needed and reviewed.

**Add (with care):**
- Actions: Read and write
- Workflows: Read and write

Workflow write access is powerful. Delay until there is a clear, scoped need.

---

## Token Governance

- Use a **fine-grained PAT** scoped to `jjuniper-dev/pca` and `jjuniper-dev/personal-cognitive-architecture` only
- Token name: `pca-local-github-mcp`
- Do not grant organization-wide or account-wide access
- Store token in Vault at `secret/pca/github_mcp` and inject at runtime
- Do not hardcode token in config files committed to the repo

**Recommended permissions for Phase 2:**
- Contents: Read and write
- Pull requests: Read and write
- Issues: Read and write
- Metadata: Read-only
- Actions: Read-only

---

## Architecture Position

```
Human request
   ↓
Agent / Claude / GPT
   ↓
MCP policy boundary (this document)
   ↓
GitHub MCP server
   ↓
GitHub issues / PRs / files
   ↓
Backlog / docs / audit artifacts
```

Local Git and GitHub Actions remain the stable execution and control layers. MCP is the standardized tool interface for agents.

---

## Setup Reference

See `PCA-WP-GITHUB-ACCESS-001` in `pca/BACKLOG.md` for the full setup checklist:

1. Create fine-grained PAT on GitHub
2. Store token in Vault (`secret/pca/github_mcp`)
3. Run official MCP server via Docker: `ghcr.io/github/github-mcp-server`
4. Register in Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json`
5. Register in Claude Code: `claude mcp add github -- docker run ...`
6. Validate Phase 1 (read-only) before enabling writes

---

## First Use Cases (in order)

1. Read `pca/BACKLOG.md` and list active items — validate read access
2. Create a small issue via MCP — validate write access
3. Create a branch and draft PR adding a doc file — validate branch/PR workflow
4. Only then use MCP for regular agent-driven development work
