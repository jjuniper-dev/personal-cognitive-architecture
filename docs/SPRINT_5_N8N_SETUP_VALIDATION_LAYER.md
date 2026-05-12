---
type: implementation
version: Sprint 5
status: ready-for-build
tags: [n8n, validation, setup, claude]
---

# Sprint 5: n8n Setup Guide — Validation Layer Workflow

**Goal:** Build the dual-agent validation workflow that scores captured content across 4 dimensions and routes to PROMOTE/INBOX/ARCHIVE.

**Timeline:** 60–90 minutes

**Cost:** ~CAD $0.018 per video (~CAD $330/year at 50 videos/day)

## Prerequisites

1. **n8n running** locally or accessible (default: http://localhost:5678)
2. **Anthropic API key** with Claude Sonnet and Claude Haiku access
3. **Neo4j running** with credentials from `.env`
4. **Obsidian vault** with `/Captures/YouTube/` folder created
5. **FastAPI backend running** with n8n webhook URL configured

## Step 1: Create Credentials

### Anthropic Credential

1. **Settings → Credentials → New**
2. **Choose:** HTTP
3. **Name:** "Anthropic API"
4. **URL:** `https://api.anthropic.com`
5. **Headers:**
   - Key: `x-api-key`
   - Value: `${ANTHROPIC_API_KEY}` (from your `.env`)
6. **Save**

### Neo4j Credential (HTTP Basic Auth)

1. **Settings → Credentials → New**
2. **Choose:** HTTP Basic Auth
3. **Name:** "Neo4j Local"
4. **Username:** `neo4j`
5. **Password:** (from `.env`)
6. **Save**

## Step 2: Create the Workflow

### 1️⃣ Webhook Trigger Node

1. **Add Node → Trigger → Webhook**
2. **Configuration:**
   - **Path:** `youtube-validation`
   - **Method:** POST
   - **Response Mode:** On Received
   - **Auto-respond:** YES
3. **Save and copy the webhook URL**
   - Example: `http://localhost:5678/webhook/youtube-validation`
   - Update FastAPI `.env` with this URL

### 2️⃣ Summarize Video Node

1. **Add Node → Helpers → Code**
2. **Language:** JavaScript
3. **Code:**

```javascript
// Prepare video data for validation assessment
const payload = $input.first().json;

// For very long transcripts, truncate to first 2000 chars
const transcript = payload.transcript || '';
const summary = transcript.length > 2000 
  ? transcript.substring(0, 2000) + "\n[...transcript truncated for length...]"
  : transcript;

return {
  video_title: payload.title,
  video_url: payload.url,
  summary,
  full_transcript: transcript,
  video_id: payload.id,
  captured_at: new Date().toISOString()
};
```

### 3️⃣ Check Deduplication Node

**NEW NODE** — Skip agents if already validated.

1. **Add Node → Request → HTTP Request**
2. **Method:** POST
3. **URL:** `http://localhost:7474/db/neo4j/tx/commit`
4. **Authentication:** Basic Auth with Neo4j credentials
5. **Headers:** `Content-Type: application/json`
6. **Body (JSON):**

```json
{
  "statements": [
    {
      "statement": "MATCH (v:VideoCapture {id: $id}) WHERE v.validated = true RETURN v.routing as routing, v.overall_score as score, v.obsidian_file as file",
      "parameters": {
        "id": "{{$node['Summarize Video'].json.video_id}}"
      }
    }
  ]
}
```

7. **Add Conditional Logic:**
   - If result.length > 0 → Skip to "Create Validation Note" with existing data
   - If result.length = 0 → Proceed to Screening Agent

### 4️⃣ Screening Agent Assessment Node

1. **Add Node → Request → HTTP Request**
2. **Method:** POST
3. **URL:** `https://api.anthropic.com/v1/messages`
4. **Authentication:** Custom — use "Anthropic API" credential
5. **Headers:**
   - `Content-Type: application/json`
   - `anthropic-version: 2023-06-01`
6. **Body (JSON):**

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 500,
  "temperature": 0.3,
  "system": "You are a rigorous content validator assessing information across 4 dimensions.\n\nYour task is to score the content on:\n1. Source Credibility (0-100): Creator trustworthiness, expertise, track record\n2. Content Quality (0-100): Intellectual rigor, evidence quality, clarity\n3. Relevance (0-100): Alignment with personal knowledge goals (agentic systems, AI architecture, knowledge management)\n4. Value Alignment (0-100): Empirical rigor, transparency, human agency, ethical treatment\n\nCRITICAL INSTRUCTION: Return ONLY valid JSON. No preamble, no markdown, no explanation.\n\nUse this exact structure:\n{\n  \"credibility_score\": <0-100>,\n  \"quality_score\": <0-100>,\n  \"relevance_score\": <0-100>,\n  \"alignment_score\": <0-100>,\n  \"reasoning\": {\n    \"credibility\": \"<1-2 sentence explanation>\",\n    \"quality\": \"<1-2 sentence explanation>\",\n    \"relevance\": \"<1-2 sentence explanation>\",\n    \"alignment\": \"<1-2 sentence explanation>\"\n  }\n}",
  "messages": [
    {
      "role": "user",
      "content": "Assess this YouTube video:\n\n**Title:** {{$node['Summarize Video'].json.video_title}}\n\n**Content Summary:**\n{{$node['Summarize Video'].json.summary}}\n\nEvaluate and score across the 4 dimensions. Be rigorous but fair."
    }
  ]
}
```

### 5️⃣ Critical Agent Assessment Node

1. **Add Node → Request → HTTP Request**
2. **Same configuration as Screening Agent, EXCEPT:**
3. **Temperature:** 0.8 (more exploratory)
4. **System Prompt:**

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

### 6️⃣ Compare Assessments & Calculate Scores

1. **Add Node → Helpers → Code**
2. **Language:** JavaScript
3. **Code:**

```javascript
const screeningRaw = $node["Screening Agent Assessment"].json;
const criticalRaw = $node["Critical Agent Assessment"].json;

// Parse response from Claude API
const screening = typeof screeningRaw.content === 'string' 
  ? JSON.parse(screeningRaw.content[0].text)
  : screeningRaw;

const critical = typeof criticalRaw.content === 'string' 
  ? JSON.parse(criticalRaw.content[0].text)
  : criticalRaw;

// Calculate per-dimension differences
const credibility_diff = Math.abs(screening.credibility_score - critical.credibility_score);
const quality_diff = Math.abs(screening.quality_score - critical.quality_score);
const relevance_diff = Math.abs(screening.relevance_score - critical.relevance_score);
const alignment_diff = Math.abs(screening.alignment_score - critical.alignment_score);

// Agreement threshold: <15 point difference
const credibility_agree = credibility_diff < 15;
const quality_agree = quality_diff < 15;
const relevance_agree = relevance_diff < 15;
const alignment_agree = alignment_diff < 15;

// All dimensions must agree for overall agreement
const agents_agree = credibility_agree && quality_agree && relevance_agree && alignment_agree;

// Count agreeing dimensions
const agreement_count = [credibility_agree, quality_agree, relevance_agree, alignment_agree]
  .filter(x => x).length;

// Composite scores (average of both agents)
const composite_credibility = (screening.credibility_score + critical.credibility_score) / 2;
const composite_quality = (screening.quality_score + critical.quality_score) / 2;
const composite_relevance = (screening.relevance_score + critical.relevance_score) / 2;
const composite_alignment = (screening.alignment_score + critical.alignment_score) / 2;

// Overall score: average of all 4 dimensions
const overall_score = (composite_credibility + composite_quality + composite_relevance + composite_alignment) / 4;

// Confidence: based on agent agreement
let confidence_score;
if (agents_agree) {
  confidence_score = 95; // All dimensions agree
} else if (agreement_count === 3) {
  confidence_score = 70; // 3 of 4 dimensions agree
} else if (agreement_count === 2) {
  confidence_score = 40; // Only half agree
} else {
  confidence_score = 20; // Most dimensions disagree
}

// HARD FLOOR: Relevance must be >= 60
// Routing decision
let routing;
if (composite_relevance < 60) {
  routing = "ARCHIVE"; // Hard floor violation
} else if (overall_score > 80) {
  routing = "PROMOTE";
} else if (overall_score >= 60) {
  routing = "INBOX";
} else {
  routing = "ARCHIVE";
}

return {
  agents_agree,
  agreement_count,
  confidence_score,
  overall_score: Math.round(overall_score * 10) / 10,
  routing,
  relevance_hard_floor_passed: composite_relevance >= 60,
  scores: {
    credibility: {
      screening: screening.credibility_score,
      critical: critical.credibility_score,
      composite: Math.round(composite_credibility * 10) / 10,
      agree: credibility_agree,
      diff: Math.round(credibility_diff * 10) / 10
    },
    quality: {
      screening: screening.quality_score,
      critical: critical.quality_score,
      composite: Math.round(composite_quality * 10) / 10,
      agree: quality_agree,
      diff: Math.round(quality_diff * 10) / 10
    },
    relevance: {
      screening: screening.relevance_score,
      critical: critical.relevance_score,
      composite: Math.round(composite_relevance * 10) / 10,
      agree: relevance_agree,
      diff: Math.round(relevance_diff * 10) / 10
    },
    alignment: {
      screening: screening.alignment_score,
      critical: critical.alignment_score,
      composite: Math.round(composite_alignment * 10) / 10,
      agree: alignment_agree,
      diff: Math.round(alignment_diff * 10) / 10
    }
  },
  reasoning: {
    screening: screening.reasoning,
    critical: critical.reasoning
  }
};
```

### 7️⃣ Create Validation Note

1. **Add Node → Helpers → Code**
2. **Language:** JavaScript
3. **Code:**

```javascript
const comparison = $node["Compare Assessments"].json;
const video = $node["Summarize Video"].json;
const now = new Date();
const dateStr = now.toISOString().split('T')[0];

const routingColor = {
  'PROMOTE': '🟢',
  'INBOX': '🟡',
  'ARCHIVE': '🔴'
};

const validationReport = `# ${video.video_title}

**Source:** [Watch on YouTube](${video.video_url})  
**Assessment Date:** ${now.toLocaleString()}  
**Video ID:** ${video.video_id}

---

## 📊 Validation Summary

| Metric | Score |
|--------|-------|
| **Overall Score** | ${comparison.overall_score}/100 |
| **Routing Decision** | ${routingColor[comparison.routing]} ${comparison.routing} |
| **Confidence** | ${comparison.confidence_score}% |
| **Agent Agreement** | ${comparison.agents_agree ? '✅ YES' : '⚠️ DISAGREEMENT'} |
| **Relevance Hard Floor** | ${comparison.relevance_hard_floor_passed ? '✅ PASSED (≥60)' : '❌ FAILED (<60)'} |

---

## 🎯 Dimension Scores

### 1️⃣ Source Credibility: ${comparison.scores.credibility.composite}/100
\`\`\`
Screening Agent: ${comparison.scores.credibility.screening}/100
Critical Agent:  ${comparison.scores.credibility.critical}/100
Difference:      ${comparison.scores.credibility.diff} points
Agreement:       ${comparison.scores.credibility.agree ? '✅' : '❌'}
\`\`\`

**Evaluation:**
- Screening: ${comparison.reasoning.screening.credibility}
- Critical: ${comparison.reasoning.critical.credibility}

### 2️⃣ Content Quality: ${comparison.scores.quality.composite}/100
\`\`\`
Screening Agent: ${comparison.scores.quality.screening}/100
Critical Agent:  ${comparison.scores.quality.critical}/100
Difference:      ${comparison.scores.quality.diff} points
Agreement:       ${comparison.scores.quality.agree ? '✅' : '❌'}
\`\`\`

**Evaluation:**
- Screening: ${comparison.reasoning.screening.quality}
- Critical: ${comparison.reasoning.critical.quality}

### 3️⃣ Relevance to Goals: ${comparison.scores.relevance.composite}/100
\`\`\`
Screening Agent: ${comparison.scores.relevance.screening}/100
Critical Agent:  ${comparison.scores.relevance.critical}/100
Difference:      ${comparison.scores.relevance.diff} points
Agreement:       ${comparison.scores.relevance.agree ? '✅' : '❌'}
Hard Floor:      ${comparison.relevance_hard_floor_passed ? '✅ PASSED' : '❌ FAILED'}
\`\`\`

**Evaluation:**
- Screening: ${comparison.reasoning.screening.relevance}
- Critical: ${comparison.reasoning.critical.relevance}

### 4️⃣ Value Alignment: ${comparison.scores.alignment.composite}/100
\`\`\`
Screening Agent: ${comparison.scores.alignment.screening}/100
Critical Agent:  ${comparison.scores.alignment.critical}/100
Difference:      ${comparison.scores.alignment.diff} points
Agreement:       ${comparison.scores.alignment.agree ? '✅' : '❌'}
\`\`\`

**Evaluation:**
- Screening: ${comparison.reasoning.screening.alignment}
- Critical: ${comparison.reasoning.critical.alignment}

---

## 📋 Assessment Summary

${comparison.agents_agree ? 
  `✅ **Agents Agree** — Assessment is highly reliable (${comparison.confidence_score}%)` :
  `⚠️ **Agent Disagreement** — Flagged for manual review (${comparison.confidence_score}% confidence, ${4-comparison.agreement_count} dimension(s) misaligned)`
}

### Routing Decision

${!comparison.relevance_hard_floor_passed ?
  `**🔴 ARCHIVE (Relevance Hard Floor Violation):** Relevance score ${comparison.scores.relevance.composite} is below the mandatory floor of 60. Content archived regardless of quality or other scores.` :
comparison.routing === 'PROMOTE' ?
  `**🟢 PROMOTE:** Integrate into knowledge graph and semantic index. High quality content aligned with goals.` :
comparison.routing === 'INBOX' ?
  `**🟡 INBOX:** Requires manual review before integration. Review reasoning above and decide:
  - Keep for integration → Move to \`PROMOTE\` folder
  - Discard → Move to \`ARCHIVE\` folder` :
  `**🔴 ARCHIVE:** Store for later reference. Low relevance or quality score, but may be useful in different context.`
}

---

## 🏷️ Tags & Metadata

- Status: #validation #${comparison.routing.toLowerCase()}
- Confidence: #confidence-${comparison.confidence_score}
- Video ID: \`${video.video_id}\`
- Assessed: ${now.toISOString()}
`;

const filename = `${dateStr}-${video.video_id}-validation.md`;

return {
  filename,
  filepath: `Captures/YouTube/${filename}`,
  content: validationReport,
  video_id: video.video_id,
  routing: comparison.routing,
  confidence: comparison.confidence_score,
  overall_score: comparison.overall_score,
  agents_agree: comparison.agents_agree,
  // Agent-specific scores for Neo4j
  screening_credibility: comparison.scores.credibility.screening,
  screening_quality: comparison.scores.quality.screening,
  screening_relevance: comparison.scores.relevance.screening,
  screening_alignment: comparison.scores.alignment.screening,
  critical_credibility: comparison.scores.credibility.critical,
  critical_quality: comparison.scores.quality.critical,
  critical_relevance: comparison.scores.relevance.critical,
  critical_alignment: comparison.scores.alignment.critical,
  // Composites
  credibility_score: comparison.scores.credibility.composite,
  quality_score: comparison.scores.quality.composite,
  relevance_score: comparison.scores.relevance.composite,
  alignment_score: comparison.scores.alignment.composite
};
```

### 8️⃣ Write to Obsidian

1. **Add Node → Files → Write Binary File**
2. **File Path:**
   ```
   /path/to/vault/{{$node["Create Validation Note"].json.filepath}}
   ```
   Replace `/path/to/vault` with your actual Obsidian vault path
3. **File Content:**
   ```
   {{$node["Create Validation Note"].json.content}}
   ```

### 9️⃣ Update Neo4j

1. **Add Node → Request → HTTP Request**
2. **Method:** POST
3. **URL:** `http://localhost:7474/db/neo4j/tx/commit`
4. **Authentication:** Basic Auth with Neo4j credentials
5. **Headers:** `Content-Type: application/json`
6. **Body (JSON):**

```json
{
  "statements": [
    {
      "statement": "MATCH (v:VideoCapture {id: $id}) SET v.validated = true, v.validated_at = datetime(), v.screening_credibility = $scr_cred, v.screening_quality = $scr_qual, v.screening_relevance = $scr_rel, v.screening_alignment = $scr_align, v.critical_credibility = $crit_cred, v.critical_quality = $crit_qual, v.critical_relevance = $crit_rel, v.critical_alignment = $crit_align, v.credibility_score = $cred, v.quality_score = $qual, v.relevance_score = $rel, v.alignment_score = $align, v.overall_score = $overall, v.confidence = $conf, v.routing = $route, v.agents_agree = $agree, v.obsidian_file = $file RETURN v",
      "parameters": {
        "id": "{{$node['Create Validation Note'].json.video_id}}",
        "scr_cred": {{$node['Create Validation Note'].json.screening_credibility}},
        "scr_qual": {{$node['Create Validation Note'].json.screening_quality}},
        "scr_rel": {{$node['Create Validation Note'].json.screening_relevance}},
        "scr_align": {{$node['Create Validation Note'].json.screening_alignment}},
        "crit_cred": {{$node['Create Validation Note'].json.critical_credibility}},
        "crit_qual": {{$node['Create Validation Note'].json.critical_quality}},
        "crit_rel": {{$node['Create Validation Note'].json.critical_relevance}},
        "crit_align": {{$node['Create Validation Note'].json.critical_alignment}},
        "cred": {{$node['Create Validation Note'].json.credibility_score}},
        "qual": {{$node['Create Validation Note'].json.quality_score}},
        "rel": {{$node['Create Validation Note'].json.relevance_score}},
        "align": {{$node['Create Validation Note'].json.alignment_score}},
        "overall": {{$node['Create Validation Note'].json.overall_score}},
        "conf": {{$node['Create Validation Note'].json.confidence}},
        "route": "{{$node['Create Validation Note'].json.routing}}",
        "agree": {{$node['Create Validation Note'].json.agents_agree}},
        "file": "{{$node['Create Validation Note'].json.filepath}}"
      }
    }
  ]
}
```

### 🔟 Respond to Webhook

1. **Add Node → Request → Respond to Webhook**
2. **Response Code:** 200
3. **Response Data:**

```json
{
  "status": "success",
  "message": "YouTube video validated",
  "validation": {
    "overall_score": "{{$node['Compare Assessments'].json.overall_score}}/100",
    "routing": "{{$node['Compare Assessments'].json.routing}}",
    "confidence": "{{$node['Compare Assessments'].json.confidence_score}}%",
    "agents_agree": {{$node['Compare Assessments'].json.agents_agree}},
    "manual_review_required": {{!$node['Compare Assessments'].json.agents_agree}}
  },
  "obsidian_file": "{{$node['Create Validation Note'].json.filename}}",
  "neo4j_updated": true
}
```

## Connect Nodes in Order

```
Webhook 
  ↓
Summarize Video
  ↓
Check Deduplication
  ├─ If duplicate → Create Validation Note (with cached data)
  └─ If new → Screening Agent
       ↓
Critical Agent
  ↓
Compare Assessments
  ↓
Create Validation Note
  ↓
(both in parallel)
├─ Write to Obsidian
└─ Update Neo4j
  ↓
Respond to Webhook
```

## Test the Workflow

### Update FastAPI `.env`

```bash
N8N_WEBHOOK_URL=http://localhost:5678/webhook/youtube-validation
```

### Test with curl

```bash
curl -X POST http://localhost:8000/api/capture/youtube \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=test001",
    "title": "Building Agentic Systems: Design Patterns",
    "transcript": "This is a detailed, well-researched transcript about agentic system design patterns from a recognized expert in AI architecture...",
    "id": "test-001"
  }'
```

### Verify Results

1. **Check n8n Executions:**
   - Go to Executions tab
   - Should see green execution (all nodes passed)
   - Review Screening & Critical Agent outputs
2. **Check Obsidian:**
   - Navigate to `/Captures/YouTube/`
   - Should see new markdown file with validation report
   - Verify scores, agent agreement, routing decision
3. **Check Neo4j:**
   - Query: `MATCH (v:VideoCapture {id: "test-001"}) RETURN v`
   - Verify: `validated=true`, all agent-specific scores present, routing decision

## Troubleshooting

### "Invalid JSON" error in agent nodes

**Solution:** Claude may be including extra text. Add stricter system prompt constraint:

```
You MUST respond ONLY with valid JSON object. Nothing else. No markdown, no explanation, no preamble.
```

### Agents always agree (no variation expected)

**Solution:** This is OK if both agents legitimately agree. If testing, try an ambiguous piece of content. Temperature difference (0.3 vs 0.8) should show variation on controversial material.

### File write fails

**Solution:** Verify Obsidian vault path is correct and n8n process has write permissions:

```bash
ls -la /path/to/vault/Captures/YouTube/
chmod -R 755 /path/to/vault/Captures/YouTube/
```

### Neo4j connection fails

**Solution:** Verify credentials match `.env` and Neo4j is running:

```bash
curl http://localhost:7474/
```

### Deduplication node returns empty but should match

**Solution:** Check that the first VideoCapture node was created with `validated=true`. Query:

```bash
MATCH (v:VideoCapture) RETURN v.id, v.validated
```

## Next Steps

1. **Temperature Tuning:** Run 10-video sample with both (0.3/0.8) and (0.4/0.7) pairs. Measure disagreement variance. Lock best pair.
2. **Per-Dimension Thresholds:** Collect first 50 validated videos. Analyze distributions. Define user-specific thresholds for Credibility, Quality, Alignment.
3. **INBOX Backlog Automation:** Set up daily scheduled workflow for 7-day auto-archive and 50-item limit enforcement.
4. **Manual Review Loop:** User examines INBOX decisions, refines prompts based on feedback.
5. **Phase 2 Preparation:** Save agent-specific scores from Neo4j for RLHF-lite training in reconciliation engine.
