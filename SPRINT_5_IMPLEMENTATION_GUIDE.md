---
type: implementation-guide
version: 1.0
created: 2026-05-12
status: ready
tags: [sprint-5, validation, n8n, implementation]
---

# Sprint 5 Implementation Guide

**Timeline:** 60–90 minutes  
**Goal:** Build and test the dual-agent validation workflow  
**Cost:** ~CAD $0.018 per video  

## Phase 1: Environment Setup (20 min)

### 1.1 Create .env File

```bash
cd /home/user/personal-cognitive-architecture
cp .env.example .env
```

Edit `.env` with your actual credentials:

```bash
# Required credentials
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Directory path to your Obsidian vault
# Adjust to your system (macOS example shown)
OBSIDIAN_VAULT_PATH=/Users/[your-username]/Documents/Obsidian/pca-vault

# Custom passwords (change from defaults!)
N8N_PASSWORD=your-secure-password
NEO4J_PASSWORD=your-secure-password
POSTGRES_PASSWORD=your-secure-password
```

### 1.2 Create Obsidian Vault Structure

```bash
VAULT_PATH=$(grep OBSIDIAN_VAULT_PATH .env | cut -d '=' -f 2 | tr -d ' ')
mkdir -p "$VAULT_PATH/videos"
mkdir -p "$VAULT_PATH/assessments"
mkdir -p "$VAULT_PATH/knowledge-graph"
mkdir -p "$VAULT_PATH/config"

echo "✓ Vault structure created at: $VAULT_PATH"
```

### 1.3 Start Docker Containers

```bash
docker-compose up -d

# Wait for services to initialize (60 seconds)
sleep 60

# Verify all containers are running
docker-compose ps
```

**Expected output:**
```
NAME           COMMAND                 STATE      PORTS
pca-n8n        docker-entrypoint.sh    Up         5678->3000/tcp
pca-neo4j      /sbin/tini -- /docker  Up         7474->7474/tcp, 7687->7687/tcp
pca-postgres   docker-entrypoint.sh    Up         5432->5432/tcp
```

### 1.4 Initialize Neo4j Schema

```bash
NEO4J_PASSWORD=$(grep NEO4J_PASSWORD .env | cut -d '=' -f 2 | tr -d ' ')

docker exec pca-neo4j cypher-shell -u neo4j -p "$NEO4J_PASSWORD" << 'EOF'
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
CREATE INDEX idx_validated IF NOT EXISTS FOR (v:VideoCapture) ON (v.validated);
CREATE INDEX idx_routing IF NOT EXISTS FOR (v:VideoCapture) ON (v.routing);
EOF

echo "✓ Neo4j schema initialized"
```

---

## Phase 2: n8n Credential Setup (10 min)

### 2.1 Log in to n8n

1. Open browser: **http://localhost:5678**
2. Login with credentials from `.env`:
   - Username: `admin`
   - Password: (your `N8N_PASSWORD`)
3. Click **Settings** → **Credentials**

### 2.2 Create Anthropic API Credential

1. Click **New** button
2. Choose **HTTP**
3. Configure:
   - **Name:** `Anthropic API`
   - **URL:** `https://api.anthropic.com`
   - **Headers:**
     - Key: `x-api-key`
     - Value: `${ANTHROPIC_API_KEY}` (paste from `.env`)
4. Click **Save**

### 2.3 Create Neo4j Credential

1. Click **New** button
2. Choose **HTTP Basic Auth**
3. Configure:
   - **Name:** `Neo4j Local`
   - **URL:** `http://neo4j:7687` (Docker internal hostname)
   - **Username:** `neo4j`
   - **Password:** (your `NEO4J_PASSWORD` from `.env`)
4. Click **Save**

---

## Phase 3: Build n8n Workflow (30–45 min)

### 3.1 Create New Workflow

1. Click **Workflows** → **Create**
2. Name: `Validation Layer - YouTube`
3. Start building nodes (see below)

### 3.2 Node 1: Webhook Trigger

1. Add Node → **Trigger** → **Webhook**
2. Configure:
   - **Path:** `youtube-validation`
   - **Method:** `POST`
   - **Response Mode:** `On Received`
   - **Auto-respond:** ✓
3. **Save and copy webhook URL:**
   - Example: `http://localhost:5678/webhook/youtube-validation`
   - Note this for testing

### 3.3 Node 2: Summarize Video

1. Connect Webhook → Add Node
2. Choose **Helpers** → **Code**
3. **Language:** JavaScript
4. **Code:**

```javascript
const payload = $input.first().json;
const transcript = payload.transcript || '';
const summary = transcript.length > 2000 
  ? transcript.substring(0, 2000) + "\n[...truncated...]"
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

5. Click **Execute Node** to test

### 3.4 Node 3: Screening Agent Evaluation

1. Connect Summarize → Add Node
2. Choose **Request** → **HTTP Request**
3. Configure:
   - **Method:** `POST`
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Authentication:** Use credential `Anthropic API`
   - **Body (JSON):**

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 500,
  "temperature": 0.3,
  "messages": [
    {
      "role": "user",
      "content": "You are a conservative content evaluator. Score this on 4 dimensions (0-100): Credibility, Quality, Relevance, Alignment. Return ONLY valid JSON.\n\nTitle: {{ $json.summary }}\n\nRespond with:\n{\"credibility\": X, \"quality\": X, \"relevance\": X, \"alignment\": X}"
    }
  ]
}
```

4. Add Post-processing:
   - Extract JSON from response: `$json.content[0].text`

### 3.5 Node 4: Critical Agent Evaluation

1. Connect Summarize → Add Node
2. **Duplicate Node 3** (HTTP Request for Screening)
3. **Change only:**
   - **Temperature:** `0.8` (exploratory)
   - Rename to "Critical Agent"
   - Body text: same prompt (exploratory perspective)

### 3.6 Node 5: Compare Assessments & Calculate Scores

1. Connect both agents → Add Node
2. Choose **Helpers** → **Code**
3. **Language:** JavaScript

```javascript
const inputs = $input.all();
const screening = JSON.parse(inputs[0].json.screening_result);
const critical = JSON.parse(inputs[1].json.critical_result);

// Calculate per-dimension agreement
const dimensions = ['credibility', 'quality', 'relevance', 'alignment'];
let agreed = 0;

for (const dim of dimensions) {
  const diff = Math.abs(screening[dim] - critical[dim]);
  if (diff <= 15) agreed++;
}

// Confidence calculation
const confidence_map = { 4: 0.95, 3: 0.70, 2: 0.40, 1: 0.20 };
const confidence = confidence_map[agreed] || 0.20;

// Composite scores
const scores = {};
for (const dim of dimensions) {
  scores[dim] = Math.round((screening[dim] + critical[dim]) / 2);
}

const overall_score = Math.round(
  Object.values(scores).reduce((a, b) => a + b) / 4
);

// Routing decision
let routing = 'ARCHIVE';
if (scores.relevance < 60) {
  routing = 'ARCHIVE';  // Hard floor
} else if (overall_score > 80) {
  routing = 'PROMOTE';
} else if (overall_score >= 60) {
  routing = 'INBOX';
} else {
  routing = 'ARCHIVE';
}

return {
  screening_scores: screening,
  critical_scores: critical,
  agreement_count: agreed,
  confidence,
  composite_scores: scores,
  overall_score,
  routing
};
```

4. Click **Execute Node** to test with sample data

### 3.7 Node 6: Create Obsidian Note

1. Connect scoring logic → Add Node
2. Choose **Filesystem** → **Write Binary File**
3. Configure:
   - **Path:** `{{ $json.video_id }}.md`
   - **Filename:** `{{ $json.routing }}_{{ $json.overall_score }}_{{ $json.video_id }}.md`
   - **Data:** (markdown template below)

```javascript
`---
video_id: {{ $json.video_id }}
routing: {{ $json.routing }}
overall_score: {{ $json.overall_score }}
confidence: {{ $json.confidence }}
assessed_at: {{ $now.toISOString() }}
---

# Video Assessment

## Scores
| Dimension | Value |
|-----------|-------|
| Credibility | {{ $json.composite_scores.credibility }} |
| Quality | {{ $json.composite_scores.quality }} |
| Relevance | {{ $json.composite_scores.relevance }} |
| Alignment | {{ $json.composite_scores.alignment }} |

**Overall:** {{ $json.overall_score }}/100  
**Confidence:** {{ ($json.confidence * 100).toFixed(0) }}%  
**Decision:** {{ $json.routing }}
`
```

### 3.8 Node 7: Update Neo4j

1. Connect note creation → Add Node
2. Choose **Request** → **HTTP Request**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://neo4j:7474/db/neo4j/tx/commit`
   - **Authentication:** Use credential `Neo4j Local`
   - **Body (JSON):**

```json
{
  "statements": [
    {
      "statement": "MERGE (v:VideoCapture {video_id: $video_id}) SET v += $properties RETURN v",
      "parameters": {
        "video_id": "{{ $json.video_id }}",
        "properties": {
          "title": "{{ $json.video_title }}",
          "routing": "{{ $json.routing }}",
          "overall_score": "{{ $json.overall_score }}",
          "confidence": "{{ $json.confidence }}",
          "screening_credibility": "{{ $json.screening_scores.credibility }}",
          "critical_credibility": "{{ $json.critical_scores.credibility }}",
          "validated": true,
          "validated_at": "{{ $now.toISOString() }}"
        }
      }
    }
  ]
}
```

### 3.9 Node 8: Success Response

1. Connect Neo4j update → Add Node
2. Choose **Helpers** → **Code**
3. Return success message:

```javascript
return {
  success: true,
  message: "Video validated and recorded",
  video_id: $json.video_id,
  routing: $json.routing,
  timestamp: new Date().toISOString()
};
```

### 3.10 Save Workflow

Click **Save** button. Name: `Validation Layer - YouTube`

---

## Phase 4: Testing & Validation (10–15 min)

### 4.1 Test with Sample Video

**Create test.json:**

```json
{
  "id": "test-video-001",
  "title": "Understanding Climate Science",
  "url": "https://youtube.com/watch?v=test123",
  "transcript": "Climate science is the study of... [paste a real transcript here, at least 500 words]"
}
```

### 4.2 Send Test Request

```bash
WEBHOOK_URL="http://localhost:5678/webhook/youtube-validation"

curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @test.json
```

### 4.3 Verify Results

1. **Check n8n:** Workflow execution log should show all 8 nodes ✓
2. **Check Neo4j:**
   ```bash
   NEO4J_PASSWORD=$(grep NEO4J_PASSWORD .env | cut -d '=' -f 2)
   docker exec pca-neo4j cypher-shell -u neo4j -p "$NEO4J_PASSWORD" \
     "MATCH (v:VideoCapture) RETURN v LIMIT 1;"
   ```
   Should show: VideoCapture node with routing, scores, confidence

3. **Check Obsidian:** Navigate to `assessments/` folder
   Should see: `PROMOTE_85_test-video-001.md` (or appropriate routing)

### 4.4 Cost Check

View n8n logs:
```bash
docker logs pca-n8n | grep -i anthropic
```

Should show: ~$0.015–0.020 per video (Sonnet + Haiku)

---

## Phase 5: Next Steps (After Testing)

### Ready for Phase 2?

Once you have **50+ videos validated** (50 INBOX decisions):
1. Begin Phase 2: Cognitive Reconciliation Engine
2. Design: Bayesian confidence updates, contradiction detection
3. Implementation: Qwen2.5-32B local model for reconciliation

### Monitoring (Optional Phase 2)

Set up Prometheus + Grafana for:
- Request volume (videos/day)
- Agent agreement rate (%)
- Cost tracking (CAD/day)
- Latency by stage (ms)

---

## Troubleshooting

### Issue: Neo4j connection fails

```bash
# Check if Neo4j is running
docker exec pca-neo4j cypher-shell -u neo4j -p <password> "RETURN 1;"
```

### Issue: Anthropic API errors

- Verify API key in `.env`
- Check rate limits: `https://console.anthropic.com`
- Test directly:
  ```bash
  curl -X POST https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "content-type: application/json" \
    -d '{"model": "claude-3-5-sonnet-20241022", "max_tokens": 100, "messages": [{"role": "user", "content": "test"}]}'
  ```

### Issue: n8n webhook not responding

```bash
# Check n8n logs
docker logs pca-n8n | tail -20

# Restart if needed
docker restart pca-n8n
```

---

## Success Criteria

✅ **Complete when:**
- [ ] Docker containers running (n8n, Neo4j, PostgreSQL)
- [ ] n8n credentials configured (Anthropic, Neo4j)
- [ ] 8-node workflow built and saved
- [ ] Test video processed successfully
- [ ] Validation result appears in Neo4j
- [ ] Obsidian note generated with correct routing
- [ ] Cost is ~CAD $0.018–0.020 per video

**Expected time: 60–90 minutes**

---

**Questions?** See `docs/SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md` for detailed node specifications.

