---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [iphone, shortcut, build, step-by-step, implementation]
status: active
---

# iPhone Shortcuts App: Build Guide (📸 Capture to PCA)

**Time**: ~15 minutes | **Difficulty**: Beginner | **Device**: iPhone (iOS 17+)

Follow this guide step-by-step while building in the Shortcuts app.

---

## Setup

1. Open **Shortcuts app** (purple icon)
2. Tap **"+" button** (top right) to create new shortcut
3. You'll see a blank canvas with a search bar at the top

---

## Step 1: Ask for Capture Type

**Action to add**: `Ask for [Menu]`

1. Tap search bar, search: **"ask for"**
2. Select **"Ask for [Menu]"** (blue action with menu icon)
3. Configure:
   - **Question**: `Capture type?`
   - **Options** (tap "+" to add each):
     - `Quick thought`
     - `Voice note`
     - `Screenshot`
     - `Link/Article`
   - **Default answer**: `Quick thought`
   - **Variable name** (top right): `capture_type`

**✓ Done**: Variable `capture_type` saved

---

## Step 2: Ask for Text Content

**Action to add**: `Ask for [Text]`

1. Tap **"+"** at bottom, search: **"ask for"**
2. Select **"Ask for [Text]"** (with text field icon)
3. Configure:
   - **Question**: `What's on your mind?`
   - **Variable name**: `text_content`

**✓ Done**: Variable `text_content` saved

---

## Step 3: Get Current Timestamp

**Action to add**: `Current Date and Time`

1. Tap **"+"**, search: **"current date"**
2. Select **"Current Date and Time"** (calendar icon)
3. This adds current date/time to your shortcut
4. Tap the action, look for **"Format"** option
5. Change format to: **`yyyy-MM-dd'T'HHmmss`** (or similar timestamp format)
6. **Variable name**: `timestamp`

**✓ Done**: Variable `timestamp` saved

---

## Step 4: Ask for Domain

**Action to add**: `Ask for [Text]`

1. Tap **"+"**, search: **"ask for"**
2. Select **"Ask for [Text]"**
3. Configure:
   - **Question**: `Domain? (work/personal/research/other)`
   - **Variable name**: `domain`
   - Leave default blank

**✓ Done**: Variable `domain` saved

---

## Step 5: Ask for Tags

**Action to add**: `Ask for [Text]`

1. Tap **"+"**, search: **"ask for"**
2. Select **"Ask for [Text]"**
3. Configure:
   - **Question**: `Tags? (comma-separated, or skip)`
   - **Variable name**: `tags_input`
   - Leave default blank

**✓ Done**: Variable `tags_input` saved

---

## Step 6: Ask for Sensitivity

**Action to add**: `Ask for [Menu]`

1. Tap **"+"**, search: **"ask for"**
2. Select **"Ask for [Menu]"**
3. Configure:
   - **Question**: `Sensitivity?`
   - **Options**:
     - `public`
     - `private`
     - `sensitive`
   - **Default answer**: `public`
   - **Variable name**: `sensitivity`

**✓ Done**: Variable `sensitivity` saved

---

## Step 7: Build Markdown Content

**Action to add**: `Text`

1. Tap **"+"**, search: **"text"**
2. Select **"Text"** (just shows a text field)
3. Copy and paste this exact text into the text field:

```
---
type: capture
source_type: [capture_type]
created: [timestamp]
domain: [domain]
sensitivity: [sensitivity]
tags: [tags_input]
confidence: 0.5
---

# Capture

[text_content]
```

**Important**: 
- The `[variable_name]` parts will auto-insert your variables
- Keep the `---` markers exactly as shown (front matter)

4. **Variable name**: `markdown_content`

**✓ Done**: Variable `markdown_content` saved

---

## Step 8: Generate Filename

**Action to add**: `Text`

1. Tap **"+"**, search: **"text"**
2. Select **"Text"**
3. Enter:

```
capture-[timestamp]-[domain].md
```

4. **Variable name**: `filename`

**✓ Done**: Variable `filename` saved

---

## Step 9: Save File to Obsidian

**Action to add**: `Write Text to File`

1. Tap **"+"**, search: **"write"**
2. Select **"Write Text to File"** (looks like a file/document icon)
3. Configure:
   - **File**: Tap to open file picker
     - Navigate to: **Obsidian vault** → **20-Ideas** → **Unstructured**
     - If path doesn't exist, you may need to create it on Mac first
   - **Text**: Insert variable `markdown_content`
   - **Overwrite**: Toggle to **OFF** (so it creates new file, not overwrite)

**If Obsidian option appears instead**:
- Search: **"save file to obsidian"**
- Use that action if available
- Configure:
  - **Vault**: `personal-cognitive-architecture`
  - **Path**: `20-Ideas/Unstructured/`
  - **Filename**: Insert variable `filename`
  - **Content**: Insert variable `markdown_content`

**✓ Done**: File will be saved to Obsidian

---

## Step 10: Show Confirmation

**Action to add**: `Show Result`

1. Tap **"+"**, search: **"show result"**
2. Select **"Show Result"** (speech bubble icon)
3. Configure:
   - **Text**: `✅ Captured to inbox`
   - **Show**: Select **"Briefly"** (from dropdown)

**✓ Done**: User sees confirmation message

---

## Test Your Shortcut

1. Tap **blue play button** (top right of shortcut) to run it
2. Answer prompts:
   - Capture type: Select `Quick thought`
   - Content: Type `Testing the shortcut`
   - Domain: Type `test`
   - Tags: Type `setup,test`
   - Sensitivity: Select `public`
3. Should see: **✅ Captured to inbox**

---

## Verify in Obsidian

1. Open **Obsidian** on your Mac
2. Navigate to: **20-Ideas** → **Unstructured**
3. Look for file: `capture-[timestamp]-test.md`
4. Open it - should see:
   - Frontmatter (metadata between `---` markers)
   - Your text content below

---

## Add to Home Screen (Optional)

1. In Shortcuts app, long-press the shortcut
2. Select **"Add to Home Screen"**
3. Choose icon: `📸` (camera emoji)
4. Tap shortcut from home screen anytime to capture

Now you can also:
- Use Siri: *"Hey Siri, capture to PCA"*
- Share from other apps: Safari → Share → Capture to PCA

---

## Troubleshooting

### Obsidian file location not found
- Make sure the vault folder path exists on your Mac
- Check: `~/obsidian-vault/20-Ideas/Unstructured/`
- Create folders if needed before running shortcut

### Variables not inserting (`[variable_name]` showing as literal text)
- Make sure you're using the **text field inside the action**
- Tap `[>]` or `Aa` icon to insert variables (not typing them manually)

### File saves but content is blank
- Check that `markdown_content` variable has proper content
- Verify text action in Step 7 has all variables inserted

### Shortcut runs but nothing happens
- Check file permissions for Obsidian vault folder
- Try saving to a different location first (like iCloud)

---

## Next: Connect to n8n Pipeline

Once files appear in Obsidian vault, the n8n workflow will:
1. Detect new `.md` files in `20-Ideas/Unstructured/`
2. Transcribe voice notes (if any)
3. Score and classify captures
4. Route to appropriate project folders
5. Log complete audit trail

See: `pca-iphone-to-obsidian-workflow.md`

---

**Status**: Ready to build ✓
**Time to complete**: ~15 minutes
**Next step**: Run shortcut and verify file appears in Obsidian
