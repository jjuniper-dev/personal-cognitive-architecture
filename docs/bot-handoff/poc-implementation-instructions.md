# POC Implementation Instructions

This handoff tells a coding bot how to get the PCA POC usable without expanding the system.

The goal is to make the current app install, run, and demonstrate the core flows without crashing or misleading the user.

---

## POC Definition

A POC is acceptable when all of the following are true:

- the app installs from a clean checkout
- the app builds without errors
- the main UI launches locally
- the quiz flow completes end to end
- the state tracker dashboards do not crash
- the export actions work in the supported runtime
- the iPhone capture path can hand off a capture event into the POC flow
- the code changes are small, explainable, and easy to roll back

Do not expand this into a full platform build.

---

## Required Reading

Read these files before editing anything:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/REPO-AUTHORITY.md`
4. `README.md`
5. `package.json`
6. `src/App.jsx`
7. `src/components/Quiz.jsx`
8. `src/components/QuestionCard.jsx`
9. `src/components/SchemaOutput.jsx`
10. `src/components/StateTrackerDashboard.jsx`
11. `src/components/ADHDTrackerDashboard.jsx`
12. `src/markov/StateTracker.js`
13. `src/markov/ADHDStateTracker.js`
14. `docs/pca-iphone-to-obsidian-workflow.md`
15. `docs/mobile-capture-setup.md`

If something is unclear, document the ambiguity instead of inventing new architecture.

---

## Scope

Focus on the existing prototype app:

- React/Vite frontend
- quiz flow
- profile/schema generation
- state tracker dashboards
- basic export helpers
- iPhone capture intake path

If backend or runtime services are missing, keep the app usable by degrading gracefully rather than blocking startup.

### iPhone Capture Integration

The POC must include a minimal mobile capture path that can receive or represent iPhone-originated input.

Use the repository’s existing capture model:

- the iPhone side is the source of capture
- the runtime side accepts or stages the capture event
- the capture should be represented as a structured payload, not an untyped note blob

Align with these existing references instead of inventing a new capture contract:

- `docs/pca-iphone-to-obsidian-workflow.md`
- `docs/mobile-capture-setup.md`
- `docs/REPO-AUTHORITY.md`

The bot should prefer the smallest useful integration:

- build the webhook intake contract first
- accept text payloads first
- add voice capture only after the text path is stable
- keep audio transcription optional if it blocks the POC
- preserve an audit trail for the incoming capture

Recommended order:

1. webhook-based capture endpoint
2. text-only payload
3. structured storage or staging
4. voice upload and transcription later

If the current repo only has the UI prototype, the bot should still add the minimal intake surface or stub that lets an iPhone capture event enter the flow cleanly.

---

## Part One: Webhook Intake Contract

This is the first implementation slice.

Build only enough to prove that an iPhone Shortcut or equivalent client can send a structured capture into the system.

### Contract

Accept a `POST` request with a JSON body shaped like this:

```json
{
  "source": "iphone",
  "capture_type": "text",
  "timestamp": "2026-06-20T12:34:56Z",
  "text": "short capture text",
  "context_note": "optional context",
  "location": "optional location",
  "tags": ["optional", "tags"]
}
```

### Minimum behavior

- validate that `source` is present
- validate that `capture_type` is present
- validate that `timestamp` is present and parseable
- accept `text` as the primary payload for POC
- store or stage the capture in a visible, inspectable form
- return a deterministic success response
- write an audit record or log entry

### Minimum success response

Return something like:

```json
{
  "ok": true,
  "capture_id": "generated-id",
  "received_at": "2026-06-20T12:34:56Z",
  "status": "staged"
}
```

### POC acceptance criteria for part one

- an iPhone-originated text capture can be submitted
- the capture is accepted and validated
- the capture is recorded somewhere inspectable
- the bot can show where the capture landed
- the response is stable and repeatable

### Keep out of scope for part one

- voice transcription
- audio file uploads
- semantic routing
- graph enrichment
- Obsidian write automation beyond a simple staging handoff
- UI redesign

---

## Non-Goals

Do not use this POC pass to:

- redesign the architecture
- move files between directories
- introduce new infrastructure
- add a backend unless it is required to make the app run
- rename concepts broadly
- refactor unrelated code
- add speculative features

The bot should keep the diff as small as possible.

---

## Priority Fix Order

Fix issues in this order:

1. Make the app build and launch cleanly
2. Add the minimal iPhone capture intake path
3. Fix quiz state that leaks between questions
4. Fix tracker timing logic so alerts reflect the active state
5. Fix Node-side export helpers in the ESM module setup
6. Add or update tests that prove the POC flow works

If a lower-priority issue blocks the build, fix the blocker first.

---

## Known Defects To Address First

These are the highest-value POC defects already identified:

- `iPhone capture path`
  - there is no minimal intake surface wired into the POC flow yet
- `src/components/QuestionCard.jsx`
  - local `selected` state does not reset when the question changes
- `src/components/ADHDTrackerDashboard.jsx`
  - time-blindness checks use completed history instead of active elapsed time
- `src/markov/StateTracker.js`
  - `exportDailyLog()` uses `require('fs')` in an ESM repo
- `src/markov/ADHDStateTracker.js`
  - `exportADHDLog()` uses `require('fs')` in an ESM repo

Treat these as first-pass POC blockers.

---

## Implementation Rules

Follow these rules while editing:

- keep changes surgical
- prefer plain code over abstractions
- avoid hidden state
- do not claim success without verification
- do not touch unrelated files
- do not move files
- do not rewrite docs unless the change requires it
- do not introduce secrets or live credentials

If you need a new helper, keep it local to the component or module that needs it.

---

## Suggested Implementation Path

1. Get the app running locally from a clean install.
2. Add the minimal iPhone capture intake path so a mobile-originated capture can enter the flow.
3. Fix the question card state reset so each quiz question starts clean.
4. Fix the tracker timing model so it measures the active session, not just completed history.
5. Replace CommonJS-only filesystem calls with ESM-compatible imports.
6. Run the available tests or add minimal tests if the repo currently lacks coverage for the changed behavior.
7. Verify the app still renders the dashboard, can complete the quiz flow, and can accept the capture handoff.

Do not move on to broader cleanup until this path is stable.

---

## Verification Checklist

At minimum, verify:

- `npm install`
- `npm run build`
- `npm test -- --run`
- the app launches in the browser
- the quiz can be completed end to end
- the dashboard views render without runtime errors
- the export buttons work in the intended environment
- the iPhone capture handoff can be represented or received in the POC path

If one of those checks cannot be run, state exactly why.

---

## Acceptance Criteria

The POC is done when:

- the main app renders without crashing
- the quiz flow produces a schema output
- the state tracker views are interactive
- the export helpers work without Node ESM errors
- the mobile capture path is integrated at a POC level
- the bot can summarize what changed, what was verified, and what remains out of scope

That is enough for handoff.

---

## Output Format For The Bot

When the bot finishes, it should report:

```md
## Summary
- what changed

## Files Changed
- path: why it changed

## Verification
- checks run
- checks not run

## Risks
- remaining issues or follow-up items
```

Keep the final report concise.
