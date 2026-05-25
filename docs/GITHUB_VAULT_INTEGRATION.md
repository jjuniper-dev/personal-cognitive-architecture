# GitHub Vault Integration

This document describes the GitHub connector integration for accessing your Obsidian vault as a backup source for the Cognitive Operations Dashboard.

## Overview

The GitHub Vault Connector provides read-only access to your Obsidian vault stored in the `jjuniper-dev/Obsidian` GitHub repository. This allows the dashboard to:

- Display your vault structure and folder organization
- Read canonical knowledge from the 04_Concepts folder
- Access notes from all vault sections (Inbox, Daily, Projects, Research, etc.)
- Search across your entire vault
- Parse YAML frontmatter metadata
- Infer note types based on folder location

## Architecture

### Components

1. **GitHubVaultConnector** (`server/github-connector.ts`)
   - Core connector class for GitHub API integration
   - Handles authentication, file retrieval, and metadata parsing
   - Supports recursive folder traversal and markdown parsing

2. **Vault Router** (`server/vault-router.ts`)
   - tRPC procedures for vault operations
   - Public endpoints for vault structure, metadata, and search
   - Folder-specific endpoints (Concepts, Inbox, Daily, Research, Projects)

3. **Tests** (`server/github-connector.test.ts`)
   - Comprehensive test suite validating GitHub authentication
   - Tests for vault structure retrieval and metadata
   - Tests for note parsing and frontmatter extraction
   - Tests for folder-specific operations

## Setup

### 1. Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "PCA Dashboard"
4. Select scope: `repo` (full control of private repositories)
5. Generate and copy the token

### 2. Add Token to Environment

The token is stored as `GITHUB_TOKEN` environment variable and is automatically injected by the Manus platform.

### 3. Verify Connection

Run the test suite to verify the connector is working:

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

### Via tRPC Client (Frontend)

```typescript
import { trpc } from "@/lib/trpc";

// Get vault structure
const { data: structure } = await trpc.vault.structure.useQuery();

// Get vault metadata
const { data: metadata } = await trpc.vault.metadata.useQuery();

// List notes in a folder
const { data: notes } = await trpc.vault.listNotes.useQuery({ 
  folderPath: "04_Concepts" 
});

// Get a specific note
const { data: note } = await trpc.vault.getNote.useQuery({ 
  path: "04_Concepts/AI-Safety.md" 
});

// Search notes
const { data: results } = await trpc.vault.search.useQuery({ 
  query: "cognitive architecture" 
});

// Get canonical notes
const { data: canonical } = await trpc.vault.getCanonicalNotes.useQuery();

// Get inbox notes
const { data: inbox } = await trpc.vault.getInboxNotes.useQuery();

// Get daily notes
const { data: daily } = await trpc.vault.getDailyNotes.useQuery();

// Get research notes
const { data: research } = await trpc.vault.getResearchNotes.useQuery();

// Get project notes
const { data: projects } = await trpc.vault.getProjectNotes.useQuery();
```

### Direct Server Usage

```typescript
import { GitHubVaultConnector } from "./github-connector";

const connector = new GitHubVaultConnector(
  process.env.GITHUB_TOKEN!,
  "jjuniper-dev",
  "Obsidian"
);

// Get vault structure
const folders = await connector.getVaultStructure();

// Get vault metadata
const metadata = await connector.getVaultMetadata();

// List notes in folder
const notes = await connector.listNotesInFolder("04_Concepts");

// Get specific note
const note = await connector.getNote("04_Concepts/AI-Safety.md");

// Search notes
const results = await connector.searchNotes("cognitive");
```

## Vault Structure

The connector recognizes the following PCA vault structure:

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

## Frontmatter Support

The connector parses YAML frontmatter from markdown files:

```yaml
---
type: concept
status: stable
created: 2026-01-15
updated: 2026-05-25
themes: [AI, cognition, architecture]
source: https://example.com
confidence: 0.95
---
```

Supported frontmatter fields:
- `type`: Note type (concept, daily, project, research, output, reference, template)
- `status`: Note status (candidate, structured, trusted, canonical)
- `created`: Creation date
- `updated`: Last update date
- `themes`: Array of theme tags
- `source`: Source URL or reference
- `confidence`: Confidence score (0-1)

## Note Type Inference

The connector automatically infers note types based on folder location:

- `00_Inbox` → `reference`
- `01_Daily` → `daily`
- `02_Projects` → `project`
- `03_Research` → `research`
- `04_Concepts` → `concept`
- `07_Outputs` → `output`
- `30_Templates` → `template`
- Other → `reference`

## Performance Considerations

### Caching

For better performance, consider implementing caching:

```typescript
const cache = new Map<string, VaultNote[]>();

async function getCachedNotes(folder: string) {
  if (cache.has(folder)) {
    return cache.get(folder)!;
  }
  
  const notes = await connector.listNotesInFolder(folder);
  cache.set(folder, notes);
  return notes;
}
```

### Rate Limiting

GitHub API has rate limits:
- Authenticated requests: 5,000 per hour
- The connector respects these limits automatically

### Search Optimization

For large vaults, search can be slow. Consider:
- Limiting search scope to specific folders
- Implementing full-text search indexing
- Caching search results

## Error Handling

The connector includes comprehensive error handling:

```typescript
try {
  const notes = await connector.listNotesInFolder("04_Concepts");
} catch (error) {
  console.error("[GitHub Connector] Failed to list notes:", error);
  // Returns empty array on error
}
```

All methods return empty arrays or null on error, never throwing exceptions.

## Testing

Run the full test suite:

```bash
pnpm test -- github-connector.test.ts
```

Run with verbose output:

```bash
pnpm test -- github-connector.test.ts --reporter=verbose
```

Run with coverage:

```bash
pnpm test -- github-connector.test.ts --coverage
```

## Integration with Dashboard

The vault integration is used by:

1. **CanonicalKnowledgeBrowser** - Displays vault structure and canonical notes
2. **KnowledgeGraphExplorer** - Shows relationships between notes
3. **ReconciliationDecisions** - Maps decisions to canonical knowledge
4. **CognitiveOperations** - Main dashboard showing vault statistics

## Future Enhancements

- [ ] Implement vault change detection and webhooks
- [ ] Add support for vault syncing and updates
- [ ] Implement full-text search indexing
- [ ] Add support for note linking and graph visualization
- [ ] Implement caching layer for performance
- [ ] Add support for vault statistics and analytics
- [ ] Implement conflict resolution for vault updates
- [ ] Add support for collaborative editing

## Troubleshooting

### "GITHUB_TOKEN environment variable not set"

Ensure the token is properly set in your environment:

```bash
echo $GITHUB_TOKEN
```

### "Failed to retrieve vault structure"

Check that:
1. The token has `repo` scope
2. The repository is accessible (not archived or deleted)
3. GitHub API is not rate-limited

### "Timeout retrieving notes"

Large vaults may timeout. Try:
1. Increasing timeout in tests
2. Searching specific folders instead of entire vault
3. Implementing caching

## Support

For issues or questions, refer to:
- GitHub Connector: `server/github-connector.ts`
- Vault Router: `server/vault-router.ts`
- Tests: `server/github-connector.test.ts`
