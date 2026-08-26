# Claude and Codex Configuration Reference

This repo tracks the safe workspace-level wiring for Claude Code and Codex on the primary
development machine. Secrets, OAuth tokens, provider credentials, and account state remain
machine-local.

## 1. VS Code Sidebar Extensions

Recommended extensions live in `.vscode/extensions.json`:

- `anthropic.claude-code` — Claude Code sidebar extension.
- `openai.chatgpt` — OpenAI / ChatGPT / Codex VS Code extension surface.
- `saoudrizwan.claude-dev` — Cline sidebar extension.

Open Claude from the Activity Bar Spark icon, the status bar, or Command Palette → **Claude Code:
Open in New Tab**. Claude's official VS Code integration also supports the CLI from the integrated
terminal and shares conversation history between the extension and CLI.

Open Codex from the OpenAI/ChatGPT extension surface if available in the Activity Bar or Command
Palette. The same local setup also exposes the `codex` CLI in VS Code's integrated terminal.

## 2. Terminal Profiles

`.vscode/settings.json` adds dedicated terminal profiles without changing the default shell:

- **Claude Code** runs `claude --ide --permission-mode manual`.
- **Cline (OpenRouter)** runs `cline -i -P openrouter --auto-approve false`.
- **Codex** runs `codex --cd ${workspaceFolder} --sandbox workspace-write --ask-for-approval
  on-request`.

These profiles are for interactive work. They do not pin a model, so model selection remains with
the tool's own account, config, and model picker.

## 3. VS Code Tasks

`.vscode/tasks.json` adds prompt-driven tasks:

- **Claude Code: prompt** starts Claude with IDE integration and manual permissions.
- **Cline: OpenRouter prompt** prompts for any OpenRouter model id and runs Cline with manual tool
  approval.
- **Codex: read-only prompt** runs `codex exec` in read-only sandbox mode for analysis and
  questions.

Use the interactive **Codex** terminal profile for implementation work. The read-only task is
intentionally conservative so a quick prompt cannot mutate the repository.

## 4. Machine-Local State

Claude state lives outside this repo, primarily under `~/.claude/`, plus VS Code extension global
storage. This repository's `.claude/settings.json` only configures the project SessionStart hook.
Do not commit `.claude/settings.local.json`; it is machine-local.

Codex state lives outside this repo, primarily under `~/.codex/`, plus VS Code extension global
storage. Keep credentials and account state there, not in repo files.

## 5. Guardrails

- Keep Claude permission mode on `manual` for PCA work.
- Keep Codex on `workspace-write` plus `on-request` approval for interactive work.
- Use Codex read-only task for quick inspections.
- Do not add API keys, OAuth tokens, provider credentials, or personal data to repo-tracked config.
