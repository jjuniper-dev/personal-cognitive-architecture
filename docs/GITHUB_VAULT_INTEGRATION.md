# GitHub Vault Integration

This document describes the GitHub connector integration for accessing your Obsidian vault through GitHub as a synchronization and backup source for the Cognitive Operations Dashboard.

## Architectural Positioning

The GitHub repository is NOT the canonical cognitive authority.

Canonical authority remains:
- Local-first Obsidian vault
- Human-governed knowledge lifecycle
- PCA reconciliation and validation workflows

GitHub serves as:
- Synchronization layer
- Backup and recovery source
- Remote retrieval surface for dashboard and agents
- Read-side integration boundary

This aligns with PCA architectural principles around:
- Local-first execution
- Human-in-the-loop governance
- Structured knowledge authority
- Separation of concerns

## Overview

The GitHub Vault Connector provides read-only access to your Obsidian vault stored in the `jjuniper-dev/Obsidian` GitHub repository.

This allows the dashboard to:

- Display vault structure and folder organization
- Read canonical knowledge from the 04_Concepts folder
- Access notes from all vault sections
- Search across the vault
- Parse YAML frontmatter metadata
- Infer note types based on folder location

## Security Guidance

Use a Fine-Grained Personal Access Token whenever possible.

Recommended permissions:
- Repository access: ONLY the Obsidian repository
- Contents: Read-only
- Metadata: Read-only

Avoid using classic PATs with broad `repo` scope unless absolutely necessary.

## Setup

### 1. Create GitHub Personal Access Token

Preferred approach:

1. Go to https://github.com/settings/personal-access-tokens
2. Create a Fine-grained Personal Access Token
3. Restrict repository access to the Obsidian repository only
4. Grant:
   - Contents: Read-only
   - Metadata: Read-only
5. Generate and copy the token

### 2. Add Token to Environment

Set the `GITHUB_TOKEN` environment variable.

### 3. Verify Connection

```bash
pnpm test -- github-connector.test.ts
```

## Performance Considerations

- GitHub API authenticated limit: 5,000 requests/hour
- Large vault searches may timeout
- Caching is strongly recommended
- Full-text indexing should eventually replace recursive brute-force search

## Operational Guidance

This connector should be treated as:
- Read-only
- Non-authoritative
- Eventually consistent
- Supportive to the PCA knowledge lifecycle

It should NOT:
- Become the primary editing surface
- Bypass reconciliation workflows
- Replace local vault governance
- Introduce direct agent write-back without approval controls
