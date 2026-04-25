---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [iphone, shortcut, obsidian, capture, mobile, setup]
status: active
---

# iPhone Capture → Obsidian → PCA Pipeline

Mobile-first knowledge capture with Apple Shortcuts, flowing through Obsidian into the PCA ingestion system.

## Architecture

```
iPhone Shortcut
    ↓
Capture (text, voice, photo, metadata)
    ↓
Format as Markdown frontmatter
    ↓
Obsidian iCloud Sync
    ↓
~/obsidian-vault/20-Ideas/Unstructured/[timestamp].md
    ↓
n8n watches folder for new captures
    ↓
Classification → Validation → Routing
    ↓
Final destination (Project, Inbox, Archive)
```

## Prerequisites

1. **iPhone Setup**
   - iOS 15+ (Shortcuts app pre-installed)
   - iCloud Drive enabled
   - Obsidian for iOS installed

2. **Obsidian Setup**
   - iCloud Sync enabled in Obsidian settings
   - Vault location: `~/obsidian-vault/`
   - Mobile app folder: `~/obsidian-vault/`

3. **n8n Automation**
   - Folder watch trigger configured
   - Watch path: `~/obsidian-vault/20-Ideas/Unstructured/`

## Step 1: Configure Obsidian for iCloud Sync

### iOS App Setup
```
Obsidian > Settings (gear icon)
  → Sync
    → iCloud Sync
      ✓ Enable iCloud Sync
      → Select vault: "personal-cognitive-architecture"
```

### Mac Desktop Setup (for verification)
```
Obsidian > Settings > Sync
  → iCloud Sync
    ✓ Enable
    ✓ Sync at startup
    ✓ Sync on file change
```

Verify sync is working:
```bash
# Check vault directory exists
ls -la ~/obsidian-vault/20-Ideas/Unstructured/

# Watch for new files
fswatch -r ~/obsidian-vault/20-Ideas/Unstructured/
```

## Step 2: Create iPhone Shortcut

### Option A: Quick Capture (Text + Voice)

In Apple Shortcuts app on iPhone:

```
1. Create new shortcut
   Shortcuts app > "+" > Create Shortcut

2. Add "Ask for Text" action
   Search: Ask for [Text]
   Question: "What's on your mind?"
   Save to variable: note_text

3. Add "Ask for [Audio]" action
   Request: "Record voice note? (or Skip)"
   Save to variable: voice_recording

4. Add "Get current date/time"
   Save to variable: timestamp

5. Add "Format timestamp"
   Format: "yyyy-MM-dd'T'HHmmss"
   Save to variable: formatted_time

6. Get current location (optional)
   Ask for Location
   Save to variable: location

7. Format markdown with frontmatter
   Set variable markdown_content:
   
   ---
   type: capture
   source_type: voice
   created: {formatted_time}
   confidence: 0.5
   domain: ""
   tags: []
   ---
   
   # Quick Note
   
   {note_text}
   
   ## Location
   {location}
   
   ---

8. Save to Obsidian file
   Set variable filename: 
   "capture-{formatted_time}.md"
   
9. Use "Save File to Obsidian"
   Action: Save file to Obsidian
   Vault: personal-cognitive-architecture
   Folder: 20-Ideas/Unstructured/
   Filename: {filename}
   Text: {markdown_content}
   Replace existing: No

10. Show completion dialog
    Show result: "Saved to Inbox"
```

### Option B: Screenshot + Context

```
1. Take Screenshot
   Action: Take Screenshot
   Save to variable: screenshot

2. Ask "What's the context?"
   Save to variable: context_text

3. Ask "Which domain?"
   Options: 
   - AI-Safety
   - Research
   - Projects
   - Ideas
   - Other
   Save to variable: domain

4. Format markdown (same as above, add image)

5. Save image to Obsidian
   Save {screenshot} as attachment

6. Save note with image reference:
   ![Screenshot](attachments/screenshot-{timestamp}.png)
```

### Option C: Complete Shortcut (Text/Voice/Photo)

**Name**: "📸 Capture to PCA"

**Structure**:

```swift
// 1. Main menu
Choose from list:
  - Text Note
  - Voice Note  
  - Photo + Context
  - Quick Thought
  Save to: capture_type

// 2. Based on selection, capture data
If capture_type = "Text Note"
  Ask for text: "What's the note?"
  Save to: content

If capture_type = "Voice Note"
  Ask for audio: "Record note"
  Save to: voice_file
  transcribe: false (let n8n handle transcription)

If capture_type = "Photo + Context"
  Take screenshot
  Ask for context
  Save both

// 3. Get metadata
Current date/time → timestamp
Current location → location (optional)
Ask "Domain?" → domain
Ask "Sensitivity?" → sensitivity (public/private/sensitive)
Ask "Tags?" (comma-separated) → tags

// 4. Format frontmatter
Create markdown with:
```yaml
---
type: capture
source_type: {capture_type}
created: {timestamp}
location: {location}
domain: {domain}
sensitivity: {sensitivity}
tags: {tags}
confidence: 0.5
---
```

// 5. Create filename
Format: "capture-{timestamp}-{domain}.md"

// 6. Save to Obsidian
Obsidian action: Save file
  Vault: personal-cognitive-architecture
  Folder: 20-Ideas/Unstructured
  Filename: {filename}
  Content: {markdown_with_frontmatter}

// 7. Show success
Display: "✅ Captured to inbox"
```

## Step 3: Shortcut JSON Export/Import

Export shortcut for sharing:

1. In Shortcuts app, long-press the shortcut
2. Select "Share"
3. Share as "Shortcut File"
4. Save to Files or email

To import:
1. Receive shortcut file
2. Open in Shortcuts app
3. Tap "Add Shortcut"

## Step 4: Configure n8n Folder Watch

In n8n workflow, add trigger:

```json
{
  "type": "filesystem",
  "event": "fileCreated",
  "path": "~/obsidian-vault/20-Ideas/Unstructured/",
  "filter": "*.md",
  "action": "trigger_pca_ingest"
}
```

When files appear in this folder:
1. n8n reads the file
2. Parses frontmatter
3. Extracts content
4. Creates capture document
5. Routes through validation pipeline

## Step 5: Verify End-to-End Flow

### On iPhone
```
1. Open Shortcuts app
2. Tap "📸 Capture to PCA"
3. Select capture type
4. Fill in details
5. Tap "Done"
6. ✅ "Captured to inbox" appears
```

### On Mac
```
# Watch for new captures
cd ~/obsidian-vault/20-Ideas/Unstructured/
ls -ltr

# Should see:
# capture-2026-04-25T143000-AI-Safety.md

# Tail n8n logs to verify processing
tail -f ~/n8n/logs/pca-ingest.log
```

### In Chainlit Dashboard
```
Run dashboard:
chainlit run dashboards/chainlit-pca-monitor.py

Commands:
/status       ← Shows capture in queue
/traces       ← Shows latest capture being processed
/watch        ← Live updates as capture flows through
```

## Frontmatter Schema

Captures must match `schemas/ingest-capture.schema.json`:

```yaml
---
type: capture
source_type: voice|text|photo|article|signal  # Required
created: ISO-8601 timestamp                   # Required
location: lat,lng or location name            # Optional
domain: string (AI-Safety, Research, etc)     # Optional
sensitivity: public|private|sensitive         # Default: public
tags: [comma-separated list]                  # Optional
confidence: 0.0-1.0                          # Default: 0.5 for human capture
---

# Content
Your markdown content here...
```

## iPhone Shortcut: Complete URL Scheme

If you prefer URL scheme (for iOS automation):

```
From external automation (e.g., web clipping, email), use:

shortcuts://open-shortcut/
  ?name=📸 Capture to PCA
  &input=text
  &text={captured_text}
```

## Sync Troubleshooting

### Captures not appearing in Obsidian

**Check iCloud Sync**:
```bash
# Mac: Verify iCloud Drive is syncing
ls ~/Library/Mobile\ Documents/iCloud\~md\~obsidian/Documents/personal-cognitive-architecture/

# Should see vault files
```

**Check Obsidian permissions**:
- iOS Settings > Obsidian > iCloud Drive → ON
- Restart Obsidian app
- Force sync: Obsidian > Settings > Sync > Sync now

### n8n not detecting new files

**Check folder watcher**:
```bash
# Verify folder exists
test -d ~/obsidian-vault/20-Ideas/Unstructured/ && echo "✅ Folder exists"

# Check file permissions
ls -la ~/obsidian-vault/20-Ideas/Unstructured/

# Verify n8n can read it
# In n8n workflow, test folder watch trigger manually
```

### iCloud Sync conflicts

If files get duplicated with " 2" suffix:
```bash
# Remove duplicates
rm ~/obsidian-vault/20-Ideas/Unstructured/*\ 2.md

# Restart sync on both iPhone and Mac
```

## Advanced: Custom iOS Shortcut

For full control, create shortcut with these variables:

```swift
Variables:
- note_type: text|voice|photo
- note_text: string
- voice_url: file path
- screenshot_url: file path
- timestamp: ISO-8601
- domain: string
- tags: array
- location: string
- confidence: 0.0-1.0

Actions:
1. Ask user for input
2. Format markdown frontmatter
3. Save to iCloud Drive → Obsidian folder
4. Trigger n8n webhook (optional, for immediate processing)
```

## Dashboard Integration

After capture appears in vault:

1. **Real-time visibility**: `/watch` shows capture flowing through pipeline
2. **Stage tracking**: `/traces` shows each stage (capture → validate → classify → route)
3. **Quality metrics**: `/metrics` shows capture success rate
4. **Graph visualization**: `/graph` shows capture added to knowledge network

## Next Steps

1. ✅ Set up Obsidian iCloud Sync
2. ✅ Create iPhone Shortcut
3. ✅ Configure n8n folder watch
4. ✅ Test capture → Obsidian sync
5. ✅ Verify n8n ingestion
6. ✅ Monitor dashboard
7. Optional: Add voice transcription to shortcut
8. Optional: Create multiple shortcuts for different capture types

---

**Status**: Ready for implementation
**Last Updated**: 2026-04-25
**Related**: ../schemas/ingest-capture.schema.json, ../workflows/n8n/README.md
