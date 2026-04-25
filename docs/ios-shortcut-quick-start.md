---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [iphone, shortcut, obsidian, quick-start]
status: active
---

# iOS Shortcut: Quick Start (Copy-Paste)

Build this shortcut step-by-step in Apple Shortcuts app.

## The 10-Step Shortcut

### Open Shortcuts App
- iPhone: Shortcuts app (purple icon)
- Tap "+" to create new shortcut

### Step 1: Ask for Input Type
```
Search: Ask for [Text]
Question: "Capture type?"
Options:
  - Quick thought
  - Voice note
  - Screenshot
  - Link/Article
Default: Quick thought
→ Save to variable: capture_type
```

### Step 2: Ask for Content
```
Search: Ask for [Text]
Question: "What's on your mind?"
Show When: capture_type != "Voice note"
→ Save to variable: text_content
```

### Step 3: Ask for Voice (Conditional)
```
Search: Ask for [Audio]
Question: "Record voice note:"
Show When: capture_type = "Voice note"
→ Save to variable: audio_file
```

### Step 4: Get Timestamp
```
Search: Current Date [and Time]
→ Format as: "yyyy-MM-dd'T'HHmmss"
→ Save to variable: timestamp
```

### Step 5: Ask for Domain
```
Search: Ask for [Text]
Question: "Domain? (or leave blank)"
Default: ""
Options (with alphabetic input):
→ Save to variable: domain
```

### Step 6: Ask for Tags
```
Search: Ask for [Text]
Question: "Tags? (comma-separated, or skip)"
Default: ""
→ Save to variable: tags_input
```

### Step 7: Ask for Sensitivity
```
Search: Ask for [Text]
Question: "Sensitivity?"
Options:
  - public
  - private
  - sensitive
Default: public
→ Save to variable: sensitivity
```

### Step 8: Build Markdown

```
Search: Text
Paste this exact text:

---
type: capture
source_type: [capture_type]
created: [timestamp]
domain: [domain]
sensitivity: [sensitivity]
tags: [[tags_input]]
confidence: 0.5
---

# Capture

[text_content]

```

→ Save to variable: markdown_content
```

### Step 9: Generate Filename

```
Search: Text action
Enter: capture-[timestamp]-[domain].md
→ Save to variable: filename
```

### Step 10: Save to Obsidian

```
Search: "Save File to Obsidian"

If this action doesn't exist, use alternate:

Search: "Write Text to File"
  File: 
    Vault: personal-cognitive-architecture
    Path: 20-Ideas/Unstructured/[filename]
    Text: [markdown_content]
    Overwrite: No
```

### Step 11: Show Confirmation

```
Search: Show Result
Text: "✅ Captured to inbox"
Show: Briefly
```

## Testing

1. **On iPhone**:
   - Open Shortcuts app
   - Tap the shortcut (blue Run button or top-right)
   - Select capture type: "Quick thought"
   - Enter: "Testing the shortcut"
   - Domain: "test"
   - Tags: "setup"
   - Sensitivity: "public"
   - Should see: "✅ Captured to inbox"

2. **Verify on Mac**:
   ```bash
   ls ~/obsidian-vault/20-Ideas/Unstructured/
   # Should show: capture-2026-04-25T143000-test.md
   
   cat ~/obsidian-vault/20-Ideas/Unstructured/capture-*.md
   # Should show frontmatter + content
   ```

3. **In Obsidian**:
   - Wait 5-10 seconds for iCloud sync
   - Should see file appear in "20-Ideas → Unstructured"
   - File should have proper frontmatter and content

## Troubleshooting

### "Save File to Obsidian" action not found

**Solution**: Use Obsidian's native iOS Shortcuts support:

1. In Obsidian iOS settings:
   - Settings > Advanced > Obsidian URI
   - Enable Shortcuts integration

2. In shortcut, use "Open URL":
   ```
   obsidian://advanced-uri
   ?vault=personal-cognitive-architecture
   &commandid=app:new-note
   &filename=[filename]
   ```

### iCloud sync not working

**Check**:
1. iPhone Settings > [Your Name] > iCloud > iCloud Drive → ON
2. Obsidian iOS > Settings > Sync → iCloud Sync → ON
3. Restart Obsidian app
4. Force sync: Obsidian > Settings > Sync > Sync Now

### File appears but with wrong content

**Check frontmatter format**:
- Must start with `---`
- Must end with `---`
- Each field on new line: `key: value`
- No extra spaces or special characters

## Enhancement: Add Voice Transcription

After "Ask for Audio", add:

```
Search: Ask for [Text]
Question: "Summarize voice note (or skip)?"
Default: ""
→ Save to variable: voice_summary

Then in markdown, add:
## Voice Note
[voice_summary]
```

(Full transcription happens in n8n)

## Enhancement: Add Screenshot

```
Step 1A: Conditional screenshot
Search: Ask for [Image]
Show When: capture_type = "Screenshot"
→ Save to variable: screenshot

Step 8A: Save screenshot first
Search: "Save Image to Obsidian"
  Vault: personal-cognitive-architecture
  Path: 20-Ideas/Unstructured/attachments/
  Image: [screenshot]
  Filename: screenshot-[timestamp].png

Step 8B: Add image reference to markdown
Add to markdown_content:
![Screenshot](attachments/screenshot-[timestamp].png)
```

## Enhancement: Add Location

```
Step 1B: Get location
Search: "Current Location"
Show When: User says yes
→ Save to variable: location

Add to frontmatter:
location: [location]
```

## Final Shortcut Structure

```
Input Menu
  ↓
├─ Quick thought → Ask text
├─ Voice note → Ask audio + summarize
├─ Screenshot → Capture + Ask context
└─ Link → Ask URL + summarize

Metadata:
  ├─ Timestamp
  ├─ Domain (ask)
  ├─ Tags (ask)
  ├─ Sensitivity (ask)
  └─ Confidence (default 0.5)

Format:
  ├─ Build markdown frontmatter
  ├─ Add content
  └─ Generate filename

Save:
  ├─ Save to Obsidian vault
  ├─ Path: 20-Ideas/Unstructured/
  └─ Show confirmation
```

## Naming & Organization

In Shortcuts app:

1. **Shortcut name**: `📸 Capture to PCA`
2. **Shortcut color**: Blue or Purple
3. **Add to home screen**: 
   - Long-press shortcut
   - "Add to Home Screen"
   - Icon: 📸

Now you can:
- Tap widget on home screen to capture
- Use Siri: "Hey Siri, capture to PCA"
- Share from other apps:
  - Notes → Share → Shortcuts → Capture to PCA
  - Safari → Share → Capture to PCA
  - Photos → Share → Capture to PCA

## Next: Connect to n8n

Once captures appear in Obsidian vault, n8n workflow:
1. Detects new `.md` files in `20-Ideas/Unstructured/`
2. Reads file content + frontmatter
3. Parses with `ingest-capture.schema.json`
4. Sends through validation pipeline
5. Routes to destination

Configure in n8n:
```json
{
  "type": "trigger",
  "event": "fileWatcher",
  "path": "~/obsidian-vault/20-Ideas/Unstructured/",
  "pattern": "*.md"
}
```

## Done ✅

You now have:
- iPhone shortcut for mobile capture
- iCloud sync to Obsidian vault
- Ready to flow into PCA pipeline
- Real-time visibility in Chainlit dashboard

---

**Status**: Ready to implement
**Time to build**: ~15 minutes
**Related**: mobile-capture-setup.md
