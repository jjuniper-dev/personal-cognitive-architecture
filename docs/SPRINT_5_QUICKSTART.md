# Sprint 5: Validation Layer — Quick Start

**What changed:** Rebuilt from task extraction to **dual-agent validation** with agreement-driven confidence scoring.

**What it does:** 
- Two independent AI agents score each YouTube video across 4 dimensions
- If agents **agree** → high confidence → automatic routing (PROMOTE/INBOX/ARCHIVE)
- If agents **disagree** → flag for manual review
- Your decisions train future assessments

## Architecture at a Glance

```
YouTube Video Captured
    ↓
Screening Agent                Critical Agent
  (temp 0.5)     →→→    Assessment    ←←←   (temp 0.7)
Scores on:
• Source Credibility (0-100)
• Content Quality (0-100)  
• Relevance to Goals (0-100)
• Value Alignment (0-100)
    ↓
Compare Scores → Agreement?
    ├─ YES (all 4 dimensions align) → Confidence 95% → AUTO-ROUTE
    └─ NO (disagreement) → Confidence 20-70% → FLAG FOR REVIEW
    ↓
Route based on Overall Score
    ├─ >80 → PROMOTE (integrate into knowledge)
    ├─ 60-80 → INBOX (needs your review)
    └─ <60 → ARCHIVE (low relevance)
    ↓
Create Obsidian validation report + Update Neo4j
```

## 3-Step Setup

### Step 1: Read the Architecture
**File:** `SPRINT_5_VALIDATION_LAYER.md`
- 4 scoring dimensions explained
- n8n workflow node-by-node breakdown
- Sample test cases
- Neo4j schema changes

**Time:** 15 min

### Step 2: Build in n8n
**File:** `SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md`
- Create OpenAI + Neo4j credentials
- Add 9 nodes to n8n workflow (copy/paste code)
- Connect nodes in order
- Update FastAPI `.env` with webhook URL

**Time:** 30-45 min

### Step 3: Test
```bash
curl -X POST http://localhost:8000/api/capture/youtube \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Test Video Title",
    "transcript": "Your video transcript or summary here...",
    "id": "test-001"
  }'
```

## Source

Migrated from `jjuniper-dev/Obsidian/SPRINT_5_QUICKSTART.md`.
