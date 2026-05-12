---
type: specification
version: Sprint 5
created: 2026-05-11
updated: 2026-05-11
status: ready-for-implementation
tags: [sprint-5, validation, dual-agent, claude]
---

# Sprint 5: Validation Layer Specification

## Overview

The Validation Layer is Phase 1's second operational milestone. It implements dual-agent scoring of captured content (YouTube videos, web articles, documents) across 4 dimensions: Credibility, Quality, Relevance, and Alignment.

**Core Innovation:** Dual-agent disagreement signals uncertainty more reliably than single-agent confidence scores.

## Architecture

### 9-Node n8n Workflow

```
Webhook (Capture)
    ↓
Summarize Video
    ↓
Check Deduplication (NEO4J)
    ├─ Already validated → Skip to existing routing
    └─ New → Continue
    ↓
Screening Agent (Claude Sonnet, T=0.3)
    ↓
Critical Agent (Claude Haiku, T=0.8)
    ↓
Compare & Score Assessments
    ↓
Create Obsidian Validation Note
    ↓
Update Neo4j (with agent-specific scores)
    ↓
Respond to Webhook
```

## Component Specifications

### Screening Agent

**Model:** Claude Sonnet (Anthropic API)  
**Temperature:** 0.3 (conservative, consistent scoring)  
**Role:** First-pass assessment, emphasis on credibility and methodological rigor

**System Prompt:**

```
You are a rigorous content validator assessing information across 4 dimensions.

Your task is to score the content on:
1. Source Credibility (0-100): Creator trustworthiness, expertise, track record
2. Content Quality (0-100): Intellectual rigor, evidence quality, clarity
3. Relevance (0-100): Alignment with personal knowledge goals (agentic systems, AI architecture, knowledge management)
4. Value Alignment (0-100): Empirical rigor, transparency, human agency, ethical treatment

CRITICAL INSTRUCTION: Return ONLY valid JSON. No preamble, no markdown, no explanation.

Use this exact structure:
{
  "credibility_score": <0-100>,
  "quality_score": <0-100>,
  "relevance_score": <0-100>,
  "alignment_score": <0-100>,
  "reasoning": {
    "credibility": "<1-2 sentence explanation>",
    "quality": "<1-2 sentence explanation>",
    "relevance": "<1-2 sentence explanation>",
    "alignment": "<1-2 sentence explanation>"
  }
}
```

### Critical Agent

**Model:** Claude Haiku (Anthropic API)  
**Temperature:** 0.8 (exploratory, independent thinking)  
**Role:** Second-pass assessment, emphasis on challenging assumptions and finding gaps

**System Prompt:**

```
You are an independent content assessor. Your job is to provide a fresh evaluation that may differ from other reviewers.

Evaluate the same content across 4 dimensions:
1. Source Credibility (0-100): Creator trustworthiness, expertise, track record
2. Content Quality (0-100): Intellectual rigor, evidence quality, clarity
3. Relevance (0-100): Alignment with personal knowledge goals (agentic systems, AI architecture, knowledge management)
4. Value Alignment (0-100): Empirical rigor, transparency, human agency, ethical treatment

Be independent. If you disagree with typical assessments, say so with clear reasoning.

CRITICAL INSTRUCTION: Return ONLY valid JSON. No preamble, no markdown, no explanation.

Use this exact structure:
{
  "credibility_score": <0-100>,
  "quality_score": <0-100>,
  "relevance_score": <0-100>,
  "alignment_score": <0-100>,
  "reasoning": {
    "credibility": "<1-2 sentence explanation>",
    "quality": "<1-2 sentence explanation>",
    "relevance": "<1-2 sentence explanation>",
    "alignment": "<1-2 sentence explanation>"
  }
}
```

## 4-Dimension Scoring Model

### Dimension 1: Source Credibility

**Definition:** Creator trustworthiness, expertise, track record, reputation in field

**Scoring Rubric:**

- **90-100:** Recognized expert, strong credentials, established reputation, clear expertise
- **75-89:** Credible speaker with relevant experience, published work, community recognition
- **60-74:** Reasonable credibility, some evidence of expertise, mixed reputation
- **40-59:** Limited credentials, questionable sources, unverified claims
- **0-39:** Untrustworthy, discredited, clear bias, misinformation

### Dimension 2: Content Quality

**Definition:** Intellectual rigor, evidence quality, clarity, logical structure, substantive depth

**Scoring Rubric:**

- **90-100:** Well-researched, strong evidence, clear logic, substantive depth, peer-reviewed or equivalent rigor
- **75-89:** Good research, solid evidence, mostly clear, adequate depth
- **60-74:** Acceptable research quality, some gaps in evidence, mostly coherent
- **40-59:** Weak evidence, unclear arguments, superficial treatment
- **0-39:** Poorly researched, logical fallacies, unsubstantiated claims, incoherent

### Dimension 3: Relevance to Goals

**Definition:** Alignment with user's focus areas: agentic systems, AI architecture, knowledge management, decision-making, reasoning

**Scoring Rubric:**

- **90-100:** Directly addresses core topics, high applicability to goals
- **75-89:** Addresses relevant subtopics, good applicability
- **60-74:** Touches on relevant topics, moderate applicability
- **40-59:** Tangentially related, low applicability
- **0-39:** Not relevant to stated goals

**HARD FLOOR:** Relevance must be ≥ 60. If Relevance < 60, content routes to ARCHIVE regardless of other scores.

### Dimension 4: Value Alignment

**Definition:** Alignment with personal principles: empirical rigor, transparency, human agency, ethical frameworks, integrity

**Scoring Rubric:**

- **90-100:** Clear alignment with principles, ethical treatment, transparent methods
- **75-89:** Generally aligned, mostly transparent, minor ethical concerns
- **60-74:** Partially aligned, some transparency gaps, neutral ethical stance
- **40-59:** Misaligned on some principles, questionable ethics
- **0-39:** Contradicts principles, unethical, deceptive, harmful framing

## Comparison & Agreement Logic

### Per-Dimension Comparison

For each dimension (Credibility, Quality, Relevance, Alignment):

```javascript
diff = Math.abs(screening_score - critical_score);
agree = diff < 15;
```

**Agreement threshold:** Difference < 15 points = agents agree on that dimension

### Overall Confidence Calculation

```javascript
agreement_count = [credibility_agree, quality_agree, relevance_agree, alignment_agree]
  .filter(x => x).length;

if (agreement_count === 4) {
  confidence = 95; // All dimensions agree
} else if (agreement_count === 3) {
  confidence = 70; // 3 of 4 dimensions agree
} else if (agreement_count === 2) {
  confidence = 40; // Only half agree
} else {
  confidence = 20; // Most dimensions disagree
}
```

### Composite Scoring

For each dimension, average the two agent scores:

```javascript
composite_credibility = (screening_credibility + critical_credibility) / 2;
composite_quality = (screening_quality + critical_quality) / 2;
composite_relevance = (screening_relevance + critical_relevance) / 2;
composite_alignment = (screening_alignment + critical_alignment) / 2;

overall_score = (composite_credibility + composite_quality + composite_relevance + composite_alignment) / 4;
```

## Routing Decision

```javascript
// HARD CONSTRAINT: Relevance must be >= 60
if (composite_relevance < 60) {
  routing = "ARCHIVE"; // Regardless of other scores
} else if (overall_score > 80) {
  routing = "PROMOTE";
} else if (overall_score >= 60) {
  routing = "INBOX";
} else {
  routing = "ARCHIVE";
}
```

### Routing Meanings

- **PROMOTE (>80):** High quality, highly relevant, integrates immediately into knowledge graph
- **INBOX (60-80):** Requires manual review before integration. Store in Obsidian `/Captures/YouTube/` for human decision
- **ARCHIVE (<60 OR Relevance <60):** Store but deprioritize. Revisit only if context changes

## Neo4j Schema & Storage

### VideoCapture Node Properties

```cypher
VideoCapture {
  id: UUID,
  source_type: "youtube" | "web" | "document",
  url: String,
  title: String,
  transcript: String,
  
  // Validation (both agents)
  screening_credibility: Float,
  screening_quality: Float,
  screening_relevance: Float,
  screening_alignment: Float,
  
  critical_credibility: Float,
  critical_quality: Float,
  critical_relevance: Float,
  critical_alignment: Float,
  
  // Composites
  credibility_score: Float,
  quality_score: Float,
  relevance_score: Float,
  alignment_score: Float,
  overall_score: Float,
  
  // Agreement & Confidence
  credibility_agree: Boolean,
  quality_agree: Boolean,
  relevance_agree: Boolean,
  alignment_agree: Boolean,
  agents_agree: Boolean,
  confidence_score: Float,
  
  // Routing
  routing: "PROMOTE" | "INBOX" | "ARCHIVE",
  obsidian_file: String,
  
  // Timing
  captured_at: DateTime,
  validated_at: DateTime,
  validated: Boolean
}
```

### Idempotency

**Upsert key:** `(video_id, validated_at)`

If same video_id revalidated: update existing node (don't duplicate).

## Deduplication Logic

**Before calling agents, check if already validated:**

```javascript
MATCH (v:VideoCapture {id: $video_id})
WHERE v.validated = true
RETURN v;

// If found: use existing routing, skip agents
// If not found: proceed to Screening Agent
```

## INBOX Backlog Management

### Policy

- **Max age:** 7 days. Items older than 7 days auto-archive.
- **Max size:** 50 items. When exceeded, user notified. Oldest items archived first.
- **Daily digest:** Generate daily summary of INBOX items (title, score, confidence)

### Implementation

Scheduled n8n workflow (daily at 09:00):

```
For each item in INBOX:
  - If created_date < today - 7 days:
    → Update routing to "ARCHIVE"
  - Count INBOX items
  - If count > 50:
    → Archive oldest 10 items
    → Send notification with list
```

## Test Cases

### Test 1: High-Quality, Highly Relevant Content

**Input:**

```json
{
  "id": "test-001",
  "title": "Building Agentic Systems: Design Patterns and Implementation",
  "url": "https://youtube.com/watch?v=example1",
  "transcript": "A detailed, well-researched transcript about agentic system design from a recognized expert in AI architecture..."
}
```

**Expected Outcome:**

- Screening Agent: Credibility 92, Quality 88, Relevance 94, Alignment 90
- Critical Agent: Credibility 89, Quality 90, Relevance 91, Alignment 88
- Agreement: ✅ All 4 dimensions agree
- Confidence: 95%
- Routing: **PROMOTE**

### Test 2: Good Content but Borderline Relevance

**Input:**

```json
{
  "id": "test-002",
  "title": "Introduction to Machine Learning",
  "url": "https://youtube.com/watch?v=example2",
  "transcript": "A solid introductory ML course covering fundamentals, but tangentially related to agentic systems..."
}
```

**Expected Outcome:**

- Screening Agent: Credibility 85, Quality 82, Relevance 68, Alignment 80
- Critical Agent: Credibility 87, Quality 84, Relevance 65, Alignment 82
- Relevance: 66.5 (passes hard floor of 60)
- Agreement: ✅ All 4 agree
- Confidence: 95%
- Overall: 79.4
- Routing: **INBOX**

### Test 3: Relevance Hard Floor Violation

**Input:**

```json
{
  "id": "test-003",
  "title": "Cooking Tips for Beginners",
  "url": "https://youtube.com/watch?v=example3",
  "transcript": "..." 
}
```

**Expected Outcome:**

- Screening Agent: Credibility 70, Quality 75, Relevance 15, Alignment 65
- Critical Agent: Credibility 72, Quality 77, Relevance 20, Alignment 67
- Relevance: 17.5 (FAILS hard floor)
- Routing: **ARCHIVE** (regardless of other scores)

### Test 4: Agent Disagreement

**Input:**

```json
{
  "id": "test-004",
  "title": "Controversial Research on AI Safety",
  "url": "https://youtube.com/watch?v=example4",
  "transcript": "..."
}
```

**Expected Outcome:**

- Screening Agent: Credibility 50, Quality 45, Relevance 72, Alignment 40
- Critical Agent: Credibility 75, Quality 72, Relevance 75, Alignment 68 (more generous, exploratory assessment)
- Credibility diff: 25 (❌ disagree)
- Quality diff: 27 (❌ disagree)
- Relevance diff: 3 (✅ agree)
- Alignment diff: 28 (❌ disagree)
- Agreement: ⚠️ Partial (1 of 4)
- Confidence: 20%
- Routing: **INBOX** (requires manual human review)

## Cost Analysis

### Per-Video Cost (Claude API)

**Screening Agent (Claude Sonnet):**

- Input tokens: ~1,000 (video metadata + system prompt)
- Output tokens: ~150 (JSON response)
- Cost: ~0.015 CAD

**Critical Agent (Claude Haiku):**

- Input tokens: ~1,000
- Output tokens: ~150
- Cost: ~0.003 CAD

**Per-video total:** ~0.018 CAD

### Annual Budget (50 videos/day)

- Videos/year: 50 × 365 = 18,250
- Cost/year: 18,250 × $0.018 = **~CAD $330**

*Note: Lower than originally estimated due to Haiku's lower cost and shorter agent prompts.*

## Implementation Checklist

- [ ] Anthropic API key configured in n8n
- [ ] Neo4j instance running with credentials in `.env`
- [ ] Obsidian vault path configured in n8n
- [ ] n8n webhook URL configured in FastAPI `.env`
- [ ] All 9 nodes created and connected in order
- [ ] Test cases run against both agents (temperature validation)
- [ ] Deduplication query tested in Neo4j
- [ ] Obsidian markdown template validated
- [ ] INBOX backlog workflow scheduled
- [ ] Cost monitoring enabled in Anthropic dashboard

## Next Steps

1. **Temperature Tuning:** Run 10-video sample with both (0.3/0.8) and (0.4/0.7) temperature pairs. Measure disagreement variance. Lock best pair.
2. **Per-Dimension Thresholds:** Collect first 50 validated videos. Analyze score distributions. Define user-specific thresholds for Credibility, Quality, Alignment (Relevance ≥ 60 is locked).
3. **Manual Review Loop:** Examine INBOX decisions. Refine prompts based on user feedback.
4. **Feedback Integration:** User's manual routing decisions (PROMOTE/ARCHIVE) fed back to system for Phase 2 learning loop.
