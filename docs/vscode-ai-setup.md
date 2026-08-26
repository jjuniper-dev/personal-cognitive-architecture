# VS Code AI Development Setup (Simple Approach)

This guide explains how to set up the best MacBook development environment using your paid AI models (Claude, ChatGPT, and OpenRouter) while avoiding Microsoft Copilot or GitHub Copilot.

## Three Independent Model Lanes

### 1. OpenRouter - Direct VS Code Integration

**Setup:**
1. Open VS Code
2. Press `Cmd+Shift+P` to open Command Palette
3. Type "Chat: Manage Language Models" and select it
4. Click "Add Models" → "OpenRouter"
5. Enter your OpenRouter API key
6. Select specific models like `qwen/qwen3-coder` for cost-effective coding tasks

**Best Use Cases:**
- Model experimentation
- Cheap workers (Qwen, Kimi, DeepSeek, etc.)
- Benchmarking routing/provider behavior

### 2. Claude Code - Architecture & Complex Reasoning

**Setup:**
1. Install the official Claude Code extension from VS Code marketplace
2. Install the Claude CLI
3. Authenticate with your Claude subscription (Pro/Max)
4. **Important:** Do NOT globally export `ANTHROPIC_API_KEY` to avoid PAYG charges

**Best Use Cases:**
- Architecture design
- Difficult debugging
- Repo reasoning
- Second opinions on complex problems

### 3. Codex - Primary Implementation Work

**Setup:**
1. Install the official Codex IDE extension from VS Code marketplace
2. Install the Codex CLI
3. Sign in using your ChatGPT subscription (not API key)
4. Your ChatGPT subscription already includes Codex access

**Best Use Cases:**
- Implementation tasks
- Writing tests
- Refactoring code
- PR-ready coding

## Key Benefits

- **No GitHub Copilot subscription required**
- **No Microsoft-hosted model dependency**
- **No PCA runtime coupling**
- **Independent model lanes for different tasks**
- **Cost optimization using existing subscriptions**
- **Clean evidence generation for PCA Model Lab comparisons**

## Current Limitation

Inline/ghost-text completion still requires GitHub Copilot. However, agentic coding with Codex + Claude Code is more valuable than predictive autocomplete.

## Recommended Workflow

```
VS Code
│
├── Codex
│   └── ChatGPT subscription
│       └── primary implementation
│
├── Claude Code
│   └── Claude subscription
│       └── architecture / review / difficult reasoning
│
└── VS Code Local Agent
    └── OpenRouter BYOK
        ├── Qwen
        ├── Kimi
        ├── DeepSeek
        ├── GLM
        └── experimental models
```

This setup gives you a clean, modular development environment that aligns with PCA principles of separation of concerns while leveraging your existing paid subscriptions effectively.