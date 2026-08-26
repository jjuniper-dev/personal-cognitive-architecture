# Cline Configuration Reference

This repo now includes the two Cline config files that can actually live in version control.
The remaining Cline config surfaces are extension-level (stored outside the repo, in VS Code's
global state / Cline's extension storage) and must be configured per-machine through the Cline
panel UI. This doc records where each surface lives and what it's for, so the setup is
reproducible without committing machine-specific or secret data.

## 1. `.clinerules` (repo file — created)

- Location: `./.clinerules` (root of this workspace).
- Loaded automatically by Cline as custom instructions for every task in this repo.
- Currently encodes the PCA governance rules from `AGENTS.md` (mission, layers, PCA/Ayla naming,
  canonical memory rules, event backbone rules, security, testing/verification, completion output
  format).
- `AGENTS.md` remains the authoritative source; if `.clinerules` and `AGENTS.md` disagree, treat
  `AGENTS.md` as correct and update `.clinerules` to match.

## 2. `.clineignore` (repo file — created)

- Location: `./.clineignore` (root of this workspace).
- Works like `.gitignore` but scoped to Cline's file reads, search, and context-building.
- Currently excludes: `.git/`, build artifacts, `node_modules/`, `.env*` (except `.env.example`),
  the two personal-profile JSON files under `data/`, `outputs/`, binary Office docs, and
  `package-lock.json`.
- Excluded files can still be read explicitly with `read_file` when a task genuinely requires it
  — `.clineignore` only affects broad/implicit context scans, not deliberate reads.

## 3. Cline VS Code sidebar extension — installed, machine-local config

- Extension ID: `saoudrizwan.claude-dev`.
- Installed in VS Code as the Cline sidebar extension.
- Open it from the Activity Bar Cline icon, or via Command Palette → **Cline: Open In New Tab**.
- Provider/API settings for the sidebar extension are machine-local. Configure OpenRouter through
  the Cline sidebar settings UI; do not commit API keys to this repo.

## 4. MCP settings (`cline_mcp_settings.json`) — machine-local, not in repo

- This file is **not** stored in the workspace. It lives in the Cline extension's global storage,
  e.g. on macOS:
  `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Configure it via VS Code: Cline panel → **MCP Servers** icon → **Configure MCP Servers**, which
  opens this file directly for editing.
- Each entry defines a server's launch command/args, environment variables (for API keys/tokens),
  and optional per-tool auto-approve lists.
- No MCP servers are currently configured for this repo. If PCA later needs one (e.g. a Neo4j MCP
  server or a GitHub MCP bridge — see `docs/github-mcp-operating-model.md`), document the required
  env var names here without real values before wiring it up.

## 5. Global Custom Instructions — machine-local, not in repo

- Configured via VS Code: Cline panel → gear icon → **Custom Instructions**.
- Applies across *all* workspaces, unlike `.clinerules` which is per-project.
- Not currently set for this environment; per-project rules are handled entirely by
  `.clinerules` + `AGENTS.md`/`CLAUDE.md`, which is the preferred approach for PCA so that rules
  travel with the repo rather than living only on one operator's machine.

## 6. Auto-approve / permissions settings — machine-local, not in repo

- Configured via VS Code: Cline panel → gear icon → **Auto-Approve** settings.
- Lets you control, per tool category (reads, edits, commands, browser, MCP), whether Cline can
  proceed without an explicit approval click.
- Recommendation for this repo: keep **write/edit and command execution** on manual approval given
  the canonical-memory and security rules in `AGENTS.md` (no unreviewed writes to Obsidian/graph
  state, no unreviewed secret handling). Read-only operations (read_file, search_files, list_files)
  can reasonably be auto-approved.

## 7. Workspace VS Code wiring for the `cline` CLI — `.vscode/settings.json`, `.vscode/tasks.json`

- Note: this is the standalone `cline` CLI, not the Cline VS
  Code *extension* (`saoudrizwan.claude-dev`) referenced elsewhere in this doc. The CLI reads its
  own config from `~/.cline` (machine-local, not in this repo), where an `openrouter` provider is
  already authenticated for `z-ai/glm-5.3`.
- `.vscode/settings.json` adds a **"Cline (OpenRouter)"** integrated-terminal profile that opens
  `cline -i -P openrouter --auto-approve false` (the interactive TUI, pinned to the openrouter
  provider but not to a model). It does not change `terminal.integrated.defaultProfile`, so
  existing shells are untouched.
- `.vscode/tasks.json` adds a **"Cline: OpenRouter prompt"** task for one-off act-mode prompts. It
  prompts for any OpenRouter model id (via an `inputs` promptString) and a prompt string, then runs
  `cline -P openrouter -m <model> --thinking low --auto-approve false -c ${workspaceFolder}
  <prompt>`.
- No API keys live in either file — both only reference the `openrouter` provider id, which
  resolves against the machine-local `~/.cline` auth.

## Summary Table

| # | Surface | Repo file? | Status |
|---|---|---|---|
| 1 | `.clinerules` | Yes | Created — encodes AGENTS.md rules |
| 2 | `.clineignore` | Yes | Created — secrets/build/data exclusions |
| 3 | Cline sidebar extension | No (VS Code extension install) | Installed — `saoudrizwan.claude-dev` |
| 4 | MCP settings | No (global storage) | Not configured — no MCP servers in use yet |
| 5 | Global custom instructions | No (global state) | Not set — handled via `.clinerules` instead |
| 6 | Auto-approve settings | No (global state) | Not set — recommend manual approval for writes/commands |
| 7 | Workspace VS Code wiring for `cline` CLI | Yes (`.vscode/settings.json`, `.vscode/tasks.json`) | Created — terminal profile + prompt task, both openrouter-scoped |
