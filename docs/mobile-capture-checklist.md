---
type: checklist
created: 2026-04-25
updated: 2026-04-25
tags: [mobile-capture, setup, implementation]
status: active
---

# Mobile Capture Setup Checklist

Complete this checklist to set up iPhone → Obsidian → PCA pipeline.

## Phase 1: Obsidian Setup ✅ Prerequisites

- [ ] **Obsidian installed on iPhone**
  - App Store > "Obsidian - Markdown Notes"
  - Sign in with Obsidian account (or create free account)
  - Note account: jjuniper-dev

- [ ] **iCloud Drive enabled**
  - iPhone Settings > [Your Name]
  - iCloud > iCloud Drive > ON
  - Obsidian in "Apps using iCloud Drive" list

- [ ] **Vault synced to iPhone**
  - Open Obsidian iOS
  - Tap "Open Vault"
  - Select: personal-cognitive-architecture
  - Tap "Open"
  - Wait 30-60 seconds for initial sync

- [ ] **Verify sync working**
  - Create test file in Obsidian iOS:
    - New note > Type "test" > Save as "test-sync.md"
  - On Mac, check file appears:
    ```bash
    ls ~/obsidian-vault/test-sync.md
    # Should exist
    rm ~/obsidian-vault/test-sync.md
    ```

## Phase 2: Obsidian Folder Structure

- [ ] **Inbox folder exists**
  ```bash
  mkdir -p ~/obsidian-vault/20-Ideas/Unstructured/
  ```

- [ ] **Verify folder in Obsidian iOS**
  - Open Obsidian > File explorer
  - Navigate: 20-Ideas > Unstructured
  - Should show folder (may be empty)

- [ ] **Verify folder writable from iPhone**
  - Create test file in Obsidian iOS:
    - Tap folder icon
    - Navigate to 20-Ideas/Unstructured
    - New note > Save as "test-mobile.md"
  - Check on Mac:
    ```bash
    ls ~/obsidian-vault/20-Ideas/Unstructured/test-mobile.md
    # Should exist
    rm ~/obsidian-vault/20-Ideas/Unstructured/test-mobile.md
    ```

## Phase 3: iPhone Shortcut Creation

- [ ] **Open Shortcuts app**
  - iPhone home screen > Shortcuts app (purple)
  - Tap "+" button

- [ ] **Create shortcut (follow ios-shortcut-quick-start.md)**
  - Step 1: Input menu
  - Step 2-7: Ask for metadata
  - Step 8-9: Build markdown
  - Step 10-11: Save to Obsidian

- [ ] **Name the shortcut**
  - Tap "Untitled Shortcut" at top
  - Rename: `📸 Capture to PCA`
  - Done

- [ ] **Test shortcut**
  - Tap blue play button
  - Select: "Quick thought"
  - Enter: "Testing iPhone shortcut"
  - Domain: "test"
  - Tags: "setup,test"
  - Should show: "✅ Captured to inbox"

- [ ] **Verify file created**
  - Wait 5-10 seconds for iCloud sync
  - On Mac:
    ```bash
    ls -ltr ~/obsidian-vault/20-Ideas/Unstructured/ | tail -1
    # Should see: capture-2026-04-25T[time]-test.md
    ```

- [ ] **Verify frontmatter**
  ```bash
  head -10 ~/obsidian-vault/20-Ideas/Unstructured/capture-2026-04-25T*.md
  # Should show:
  # ---
  # type: capture
  # source_type: text
  # created: [timestamp]
  # ...
  ```

## Phase 4: n8n Integration

- [ ] **Folder watcher configured**
  - Open n8n workflow: pca-ingest-loop
  - Add trigger: File Watcher or Folder Watch
  - Path: `~/obsidian-vault/20-Ideas/Unstructured/`
  - Pattern: `*.md`
  - Trigger on: File created
  - Enabled: YES

- [ ] **Workflow activated**
  - n8n: Save and activate workflow
  - Status should show "Active" (green)

- [ ] **Test end-to-end**
  - Create capture on iPhone shortcut
  - Wait 10 seconds for iCloud sync
  - Check n8n workflow execution:
    ```bash
    tail -f ~/n8n/logs/pca-ingest.log
    # Should see: "New file detected: capture-..."
    # Should see: "Processing capture..."
    ```

## Phase 5: Dashboard Verification

- [ ] **Start Chainlit dashboard**
  ```bash
  cd ~/personal-cognitive-architecture/dashboards
  chainlit run chainlit-pca-monitor.py
  ```

- [ ] **Monitor incoming capture**
  - Open Chainlit UI: http://localhost:8000
  - Type: `/watch`
  - Create new capture on iPhone
  - Should see capture appear in real-time:
    - "Queue: ⏳ 1 | 🔄 0 | ⚠️ 0"
    - Cost and success rate updating

- [ ] **Verify in /traces**
  - Command: `/traces`
  - Should show newest entry:
    ```
    📥 Captured
    ├─ ID: [capture-id]
    ├─ Type: voice (or text)
    ├─ Action: ... 
    ├─ Latency: XXms
    ├─ Cost: $0.00
    └─ Time: 2026-04-25T14:30:00Z
    ```

## Phase 6: Enhancements (Optional)

- [ ] **Add voice note support**
  - Update shortcut: Add "Ask for Audio" action
  - Test with voice capture
  - Verify audio file syncs to Obsidian
  - n8n should trigger transcription

- [ ] **Add screenshot capture**
  - Update shortcut: Add "Take Screenshot" action
  - Save image to attachments folder
  - Reference in markdown: `![screenshot](attachments/...)`

- [ ] **Add location capture**
  - Update shortcut: Add "Current Location" action
  - Include in frontmatter: `location: [lat,lng]`

- [ ] **Create home screen widget**
  - Shortcuts app > Long-press shortcut
  - "Add to Home Screen"
  - Now available from lock screen or home screen

## Phase 7: Production Readiness

- [ ] **Test multiple captures**
  - Create 5+ captures from iPhone
  - Verify all appear in Obsidian
  - Verify all processed by n8n
  - Check dashboard /metrics for success rate

- [ ] **Verify sync reliability**
  - Disable WiFi, capture with cellular
  - Re-enable WiFi, verify sync completes
  - Check Obsidian app for sync status indicator

- [ ] **Check for conflicts**
  - If duplicates appear (filename 2):
    ```bash
    # Clean up
    rm ~/obsidian-vault/20-Ideas/Unstructured/*\ 2.md
    ```
  - Force full resync: Obsidian > Settings > Sync > Full resync

- [ ] **Performance test**
  - Create capture
  - Time from creation to dashboard visibility
  - Target: <30 seconds from shortcut → dashboard
  - If slower: check iCloud, WiFi, n8n logs

## Phase 8: Documentation & Training

- [ ] **Document for personal use**
  - Screenshot shortcut flow
  - Keep ios-shortcut-quick-start.md handy
  - Pin Shortcuts widget to home screen

- [ ] **Create shortcuts for different types**
  - Optional: Create separate shortcuts for:
    - "🎤 Voice Note" → audio-first
    - "📸 Screenshot" → image-first
    - "🔗 Link" → URL capture
  - Or use single shortcut with menu

- [ ] **Backup shortcut**
  - Shortcuts app > Long-press shortcut
  - Share > "Shortcut File"
  - Save to Files or email
  - Keep backup in case of reset

## Troubleshooting

### Capture doesn't appear in Obsidian
- [ ] Check: iPhone Settings > iCloud Drive > ON
- [ ] Check: Obsidian iOS > Settings > iCloud Sync > ON
- [ ] Action: Force sync in Obsidian > Settings > Sync > Sync Now
- [ ] Action: Restart Obsidian app
- [ ] Check Mac: Does file exist in `~/obsidian-vault/20-Ideas/Unstructured/`?

### File appears but n8n doesn't process
- [ ] Check: n8n workflow status is "Active" (green)
- [ ] Check: File watcher path matches: `~/obsidian-vault/20-Ideas/Unstructured/`
- [ ] Check: File watcher pattern is `*.md`
- [ ] Action: n8n > Save and Activate workflow again
- [ ] Check logs:
  ```bash
  tail -f ~/n8n/logs/pca-ingest.log | grep "capture-"
  ```

### Dashboard doesn't show capture
- [ ] Check: Audit logs exist:
  ```bash
  ls -ltr ~/personal-cognitive-architecture/audit-logs/audit-*.jsonl | tail
  ```
- [ ] Action: Create capture, wait 10 seconds
- [ ] Check: `/status` command in dashboard
- [ ] Check: `/traces` to see last 10 operations

### iCloud sync conflicts (filename 2)
- [ ] Cause: File edited on both Mac and iPhone simultaneously
- [ ] Fix: Delete duplicates:
  ```bash
  rm ~/obsidian-vault/20-Ideas/Unstructured/*\ 2.md
  ```
- [ ] Prevent: Don't edit captures on Mac while syncing from iPhone

## Success Criteria ✅

When complete, you have:

- ✅ iPhone shortcut that captures text/voice/context
- ✅ Data syncs to Obsidian vault via iCloud
- ✅ n8n detects new captures automatically
- ✅ Captures flow through validation pipeline
- ✅ Real-time visibility in Chainlit dashboard
- ✅ End-to-end latency <30 seconds
- ✅ Reliable, conflict-free sync

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| iPhone → Obsidian sync | <10s | ___ |
| Obsidian → n8n detection | <5s | ___ |
| n8n processing | <5s | ___ |
| Dashboard visibility | <30s | ___ |
| Sync reliability | 99%+ | ___ |
| Zero conflicts | 100% | ___ |

---

**Status**: Ready to implement
**Estimated time**: 1-2 hours
**Related**: ios-shortcut-quick-start.md, mobile-capture-setup.md, ../schemas/ingest-capture.schema.json
