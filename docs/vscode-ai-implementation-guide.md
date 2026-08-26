# VS Code AI Implementation Guide

This guide provides step-by-step instructions for implementing the simplified AI development setup in VS Code.

## Prerequisites

- VS Code version 1.122 or higher
- Valid subscriptions for Claude Pro/Max and ChatGPT
- OpenRouter API key

## Implementation Steps

### 1. OpenRouter Setup

#### Step 1.1: Access Language Models Manager
1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) to open Command Palette
3. Type "Chat: Manage Language Models" and select it

#### Step 1.2: Add OpenRouter Models
1. Click "Add Models"
2. Select "OpenRouter"
3. Enter your OpenRouter API key when prompted
4. Select specific models to enable:
   - `qwen/qwen3-coder` (cost-effective coding)
   - `openai/gpt-5.2-codex` (for benchmarking, if needed)

#### Step 1.3: Verify OpenRouter Setup
1. Open a new chat window in VS Code
2. Click on the model selector dropdown
3. Confirm that OpenRouter models appear in the list

### 2. Claude Code Setup

#### Step 2.1: Install Claude Code Extension
1. Open VS Code Extensions Marketplace (`Cmd+Shift+X`)
2. Search for "Claude Code" or "Claude for VS Code"
3. Install the official Anthropic extension

#### Step 2.2: Install Claude CLI
1. Visit https://claude.ai/download to download the Claude CLI
2. Follow installation instructions for your OS

#### Step 2.3: Authenticate with Claude Subscription
1. Open Claude Code extension in VS Code
2. Sign in using your Claude account credentials (Pro/Max subscription)
3. **Important**: Do NOT set `ANTHROPIC_API_KEY` as a global environment variable

#### Step 2.4: Verify Claude Code Setup
1. Open a new chat with Claude Code
2. Ask a simple architectural question to confirm it's working
3. Check that it's using your subscription (not API credits)

### 3. Codex Setup

#### Step 3.1: Install Codex Extension
1. Open VS Code Extensions Marketplace (`Cmd+Shift+X`)
2. Search for "Codex" or "OpenAI Codex"
3. Install the official OpenAI extension

#### Step 3.2: Install Codex CLI (if needed)
1. Visit https://openai.com/blog/openai-codex for CLI installation
2. Follow installation instructions for your OS

#### Step 3.3: Authenticate with ChatGPT Subscription
1. Open Codex extension in VS Code
2. Sign in using your ChatGPT account credentials
3. Confirm that your subscription includes Codex access

#### Step 3.4: Verify Codex Setup
1. Open a new chat with Codex
2. Ask it to generate a simple function to confirm it's working
3. Check that it's using your ChatGPT subscription

### 4. Environment Variable Setup (Optional)

If you need to set environment variables for any services:

#### 4.1: Create .env file
Create a `.env` file in your project root with:
```
OPENROUTER_API_KEY=your_openrouter_key_here
```

#### 4.2: Add to .gitignore
Ensure `.env` is in your `.gitignore` file to prevent credential leakage

### 5. Testing the Setup

#### 5.1: Test Each Model Lane
1. Create a simple test project or open an existing one
2. Try each model for different tasks:
   - **Codex**: Implementation task ("Create a function to calculate fibonacci numbers")
   - **Claude Code**: Architecture task ("Design a REST API for a todo application")
   - **OpenRouter**: Experimental task ("Try to explain this code in simple terms")

#### 5.2: Verify Independence
Confirm that each model works independently without affecting the others.

### 6. Troubleshooting Common Issues

#### Issue: Models not appearing in chat
- Solution: Restart VS Code and reopen the Language Models manager

#### Issue: Authentication failing
- Solution: Ensure you're signing in with the correct account (subscription account, not API key)

#### Issue: PAYG charges for Claude
- Solution: Check that `ANTHROPIC_API_KEY` is not set globally in your environment

#### Issue: Limited model selection
- Solution: In Language Models manager, click "Refresh" to update the model list

### 7. Recommended Workflow

```
Development Process:
1. Use Codex for primary implementation
2. Use Claude Code for architecture review
3. Use OpenRouter models for experimentation
4. Commit code with clear messages
5. Document any model-specific insights
```

### 8. Security Best Practices

1. Never commit API keys or credentials to version control
2. Use environment variables for local development
3. Regularly rotate API keys
4. Monitor usage to detect anomalies

### 9. Performance Optimization

1. Use appropriate models for tasks:
   - Lightweight tasks → Qwen3 Coder
   - Complex tasks → GPT-5.2 Codex (when needed)
   - Architecture → Claude Code

2. Monitor response times and costs
3. Cache responses when appropriate
4. Use local models for repetitive tasks

## Completion Checklist

- [ ] OpenRouter configured with selected models
- [ ] Claude Code extension installed and authenticated
- [ ] Codex extension installed and authenticated
- [ ] All three model lanes tested independently
- [ ] Environment variables secured
- [ ] Basic troubleshooting performed
- [ ] Security best practices implemented

## Next Steps

Once implementation is complete:
1. Begin using the setup for daily development
2. Document any issues or improvements
3. Share feedback with the team
4. Consider integrating usage analytics if needed