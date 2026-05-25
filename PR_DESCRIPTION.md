# GitHub Vault Connector for Obsidian Integration

## Overview

This PR introduces a GitHub Vault Connector that enables the Cognitive Operations Dashboard to read your Obsidian vault directly from GitHub as a backup source. This integration allows the dashboard to display canonical knowledge, vault structure, and note metadata in real-time.

## What's New

### Components Added

1. **GitHubVaultConnector** (`src/ui-dashboard/server/github-connector.ts`)
   - Core connector class for GitHub API integration
   - Retrieves vault structure and folder organization
   - Parses YAML frontmatter from markdown files
   - Infers note types based on folder location
   - Implements full-text search across vault
   - Handles GitHub API authentication and rate limiting

2. **Vault Router** (`src/ui-dashboard/server/vault-router.ts`)
   - tRPC procedures for vault operations
   - Public endpoints for vault structure, metadata, and search
   - Folder-specific endpoints (Concepts, Inbox, Daily, Research, Projects)
   - Type-safe API with full TypeScript support

3. **Comprehensive Tests** (`src/ui-dashboard/server/github-connector.test.ts`)
   - 7 passing tests validating GitHub authentication
   - Tests for vault structure retrieval and metadata
   - Tests for note parsing and frontmatter extraction
   - Tests for folder-specific operations
   - Proper timeout handling for API calls

4. **Documentation** (`docs/GITHUB_VAULT_INTEGRATION.md`)
   - Complete setup and usage guide
   - API reference with examples
   - Vault structure documentation
   - Frontmatter support details
   - Performance considerations
   - Troubleshooting guide

## Features

✅ **Vault Structure Retrieval** - Display folder organization and metadata
✅ **Note Parsing** - Read and parse markdown files with YAML frontmatter
✅ **Type Inference** - Automatically determine note types from folder location
✅ **Full-Text Search** - Search across entire vault
✅ **Folder-Specific Endpoints** - Quick access to Concepts, Inbox, Daily, Research, Projects
✅ **Error Handling** - Comprehensive error handling with graceful fallbacks
✅ **GitHub API Integration** - Authenticated access via Personal Access Token
✅ **Rate Limiting** - Respects GitHub API rate limits

## Supported Vault Structure

The connector recognizes the PCA vault structure:

| Folder | Type | Purpose |
|--------|------|---------|
| `00_Inbox` | Ingestion | Temporary ingestion zone for new captures |
| `01_Daily` | Temporal | Daily cognitive snapshots and reflections |
| `02_Projects` | Execution | Active execution-oriented work |
| `03_Research` | Exploration | Exploration and investigation space |
| `04_Concepts` | Knowledge | Stable knowledge primitives and frameworks |
| `05_Themes` | Thematic | Cross-cutting domains and recurring patterns |
| `06_People` | Context | Relationship and context layer |
| `07_Outputs` | Publication | Finalized artifacts and publications |
| `08_Media` | Assets | Non-text supporting material |
| `20_MOCs` | Navigation | Maps of Content for navigation |
| `30_Templates` | Reusable | Reusable cognitive structures |
| `40_References` | External | External source preservation |
| `_system` | Machine | Machine-operated infrastructure |
| `90_Archive` | Historical | Archived and historical content |

## Setup Instructions

### 1. Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "PCA Dashboard"
4. Select scope: `repo` (full control of private repositories)
5. Generate and copy the token

### 2. Add Token to Environment

Set the `GITHUB_TOKEN` environment variable with your PAT token.

### 3. Verify Connection

Run the test suite:

```bash
pnpm test -- github-connector.test.ts
```

Expected output:
```
✓ GitHub Vault Connector (7 tests)
  ✓ should authenticate with GitHub API
  ✓ should retrieve vault structure
  ✓ should have canonical folders in vault structure
  ✓ should retrieve vault metadata
  ✓ should list notes in Concepts folder
  ✓ should parse note frontmatter correctly
  ✓ should infer note types correctly
```

## API Usage

### Frontend (tRPC)

```typescript
import { trpc } from "@/lib/trpc";

// Get vault structure
const { data: structure } = await trpc.vault.structure.useQuery();

// Get vault metadata
const { data: metadata } = await trpc.vault.metadata.useQuery();

// List notes in folder
const { data: notes } = await trpc.vault.listNotes.useQuery({ 
  folderPath: "04_Concepts" 
});

// Get canonical notes
const { data: canonical } = await trpc.vault.getCanonicalNotes.useQuery();

// Search notes
const { data: results } = await trpc.vault.search.useQuery({ 
  query: "cognitive architecture" 
});
```

### Backend (Direct)

```typescript
import { GitHubVaultConnector } from "./github-connector";

const connector = new GitHubVaultConnector(
  process.env.GITHUB_TOKEN!,
  "jjuniper-dev",
  "Obsidian"
);

const folders = await connector.getVaultStructure();
const metadata = await connector.getVaultMetadata();
const notes = await connector.listNotesInFolder("04_Concepts");
```

## Integration with Dashboard

The vault integration is used by:

1. **CanonicalKnowledgeBrowser** - Displays vault structure and canonical notes
2. **KnowledgeGraphExplorer** - Shows relationships between notes
3. **ReconciliationDecisions** - Maps decisions to canonical knowledge
4. **CognitiveOperations** - Main dashboard showing vault statistics

## Testing

All tests pass successfully:

```bash
pnpm test -- github-connector.test.ts
```

Tests cover:
- GitHub API authentication
- Vault structure retrieval
- Vault metadata retrieval
- Note listing in folders
- Frontmatter parsing
- Note type inference

## Performance Considerations

- GitHub API rate limit: 5,000 requests/hour for authenticated requests
- Large vault searches may timeout (30s default)
- Caching recommended for frequently accessed folders
- Full-text search can be optimized with indexing

## Future Enhancements

- [ ] Implement vault change detection and webhooks
- [ ] Add support for vault syncing and updates
- [ ] Implement full-text search indexing
- [ ] Add support for note linking and graph visualization
- [ ] Implement caching layer for performance
- [ ] Add support for vault statistics and analytics
- [ ] Implement conflict resolution for vault updates
- [ ] Add support for collaborative editing

## Files Changed

```
src/ui-dashboard/server/
├── github-connector.ts          (NEW) - Core GitHub API integration
├── vault-router.ts             (NEW) - tRPC vault procedures
└── github-connector.test.ts     (NEW) - Comprehensive test suite

docs/
└── GITHUB_VAULT_INTEGRATION.md  (NEW) - Complete documentation
```

## Related Issues

This PR enables:
- Display of canonical knowledge from Obsidian vault
- Real-time vault structure visualization
- Integration with reconciliation engine
- Knowledge graph population from vault

## Checklist

- [x] Code follows project conventions
- [x] Tests pass (7/7)
- [x] TypeScript compilation clean
- [x] Documentation complete
- [x] GitHub authentication tested
- [x] Vault structure validated
- [x] Error handling implemented
- [x] Performance optimized for API limits

## Questions?

Refer to `docs/GITHUB_VAULT_INTEGRATION.md` for detailed setup and troubleshooting.
