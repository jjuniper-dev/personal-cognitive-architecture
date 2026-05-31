# Repo Activity Worker

**Layer**: L1 Knowledge & Control — inspection and audit tooling  
**Type**: worker (bounded task execution)  
**Owner**: PCA

---

## Purpose

Inspect the three PCA GitHub repositories and emit a structured activity report covering:

- Branch inventory grouped by type: `claude/`, `codex/`, `feat/fix/chore`, default
- Age and last-commit date per branch
- Open PR status per branch
- Recent commits to default branches
- Stale branch flagging (no open PR and age > threshold)

The report supports operator review of AI-assisted development activity and facilitates branch hygiene decisions.

---

## Inputs

| Input | Source | Required |
|---|---|---|
| `GITHUB_TOKEN` | environment / `.env` | yes |
| `STALE_DAYS` | environment (default `14`) | no |
| `RECENT_DAYS` | environment (default `30`) | no |

---

## Output

Markdown report printed to stdout. Structure per repo:

```
## <repo-name>
Branches: N  Open PRs: N  Stale: N

### claude
### codex
### feat/fix/chore
### other
### default

### Open PRs
### Recent commits to default branch (last Nd)
### Stale branches flagged for cleanup
```

---

## Invocation

```bash
# Direct
GITHUB_TOKEN=<token> node scripts/repo-activity-check.js

# With custom thresholds
GITHUB_TOKEN=<token> STALE_DAYS=7 RECENT_DAYS=14 node scripts/repo-activity-check.js

# Via npm
npm run repo-activity-check

# Capture to file
npm run repo-activity-check > reports/repo-activity-$(date +%Y-%m-%d).md
```

---

## Scope

Repos checked:

- `jjuniper-dev/pca`
- `jjuniper-dev/personal-cognitive-architecture`
- `jjuniper-dev/Obsidian`

---

## PCA Primitive Chain Mapping

```
Input (GITHUB_TOKEN) → Query (GitHub REST API) → Validate (none) → Route (none) → Store (none) → Retrieve (branches/PRs/commits) → Act (print report) → Audit (report is the artifact)
```

This worker is **read-only**. It makes no writes to GitHub, vault, graph, or any other state.

---

## Degraded Behaviour

- `GITHUB_TOKEN` missing: exits immediately with an error, no network calls made.
- Single repo fetch fails: error is printed to stderr and remaining repos are still checked.
- GitHub API rate limit hit: Octokit handles 429/403 retry for authenticated requests; the run will slow but complete for small repo sets.

---

## Removal

Delete `scripts/repo-activity-check.js` and `agents/repo-activity-worker.md`, then remove the `repo-activity-check` entry from `package.json` scripts.
