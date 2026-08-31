# SEC-001: Remove Personal Profile Data from Public Repository

- **ID**: SEC-001
- **Date**: 2026-08-31
- **Severity**: High (live personal data in public repository)
- **Status**: Removed from tracking. History rewrite pending operator decision.
- **Authority**: PCA security rules + canonical memory separation. Governing
  principle (ratified 2026-08-31, now codified in `AGENTS.md` → Canonical
  Memory Rules → Public Repository Boundary): *public repositories must not
  become canonical storage for personal identity, personal cognitive state,
  journals, or governed memory. Such information belongs in the PCA Knowledge
  Layer and may only appear in the repository as intentionally sanitized
  fixtures or test data.*

## Finding

Two files containing genuine personal data (psychological profile, anxiety
triggers, social/energy patterns) were committed to this public repository in
April 2026:

| File | Added | Commits touching it | Content |
|---|---|---|---|
| `data/personal-profile.json` | `a75b5e8` 2026-04-26 (PR #14) | 1 (never modified) | Personal/psychological profile: values, learning style, introversion, work challenges |
| `data/personal-os-profile.json` | `37c71e2` 2026-04-25 | 4 (2026-04-25) | Meeting-anxiety triggers, social bandwidth, attention/decision patterns |

Both are canonical personal memory, not system configuration. Their presence in
the public repo violates the PCA architectural separation between canonical
memory (governed, local-first) and the public git repository (system
architecture only).

## Remediation (this change)

- Removed both files from git tracking on `main`.
- No code depends on them: the only reference is a download filename constant
  in `src/components/SchemaOutput.jsx` (cosmetic, unaffected).
- `data/.gitkeep` retained so the governed data directory still exists locally.
- **Operator action required**: before purging history, ensure a copy of both
  files exists in governed local storage (vault or local-first PCA store,
  outside any git repository). The working-tree copies remain on disk in
  existing clones until deleted manually, but this must not be the system of
  record.

## History rewrite evaluation

Purge is feasible and low-risk:

- `personal-profile.json`: single originating commit — one commit to drop.
- `personal-os-profile.json`: 4 commits from 2026-04-25 — same commit range.
- Recommended tool: `git filter-repo --path data/personal-profile.json --path data/personal-os-profile.json --invert-paths`.
- Consequences: all commit SHAs after 2026-04-25 change; requires force-push
  and re-clone of every working copy; forks/clones outside operator control
  retain the data regardless.

**Decision deferred to operator.** Not executed in this change because history
rewriting a public repository is destructive and irreversible.

## Follow-ups

1. Operator confirms governed local copy exists, then approves history rewrite.
2. Execute `git filter-repo` purge + force-push, re-clone working copies.
3. Confirm `data/markov-cognitive-states.json` (generic state definitions, low
   sensitivity) and `data/routing-rules.json` / `data/signal-sources.json` need
   no equivalent treatment — assessed 2026-08-31, no action taken.
4. Add a pre-commit/CI guard preventing `data/*.json` personal-profile patterns
   from re-entering the repository (future hardening item).
