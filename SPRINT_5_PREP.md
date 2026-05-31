# Sprint 5 Pre-Sprint Prep
**For: June 1, 2026 — 7:00 AM (2-hour block)**

Do these tonight to be ready to execute at 7 AM.

---

## Pre-Sprint Checklist (Tonight: ~10 min)

- [ ] **1. Gather credentials**
  - [ ] Anthropic API key (from console.anthropic.com)
  - [ ] Obsidian vault path (e.g., `/Users/[you]/Documents/Obsidian/pca-vault`)

- [ ] **2. Set up environment**
  ```bash
  cd /home/user/personal-cognitive-architecture
  cp .env.example .env
  
  # Edit .env:
  nano .env
  # Add:
  # ANTHROPIC_API_KEY=sk-ant-your-actual-key
  # OBSIDIAN_VAULT_PATH=/your/obsidian/path
  # Save: Ctrl+X → Y → Enter
  ```

- [ ] **3. Create Obsidian vault directories**
  ```bash
  VAULT_PATH=$(grep OBSIDIAN_VAULT_PATH .env | cut -d '=' -f 2 | tr -d ' ')
  mkdir -p "$VAULT_PATH/videos"
  mkdir -p "$VAULT_PATH/assessments"
  mkdir -p "$VAULT_PATH/knowledge-graph"
  ```

- [ ] **4. Quick Docker check**
  ```bash
  docker --version
  docker-compose --version
  # Both should be available
  ```

---

## Tomorrow Morning (7:00 AM): Sprint Execution

**Timeline: 60–90 minutes**

### ⏱️ 7:00–7:20 AM — Phase 1: Environment Setup

```bash
cd /home/user/personal-cognitive-architecture

# Start Docker containers
docker-compose up -d

# Wait 60 seconds
sleep 60

# Initialize Neo4j schema
NEO4J_PASSWORD=$(grep NEO4J_PASSWORD .env | cut -d '=' -f 2 | tr -d ' ')
docker exec pca-neo4j cypher-shell -u neo4j -p "$NEO4J_PASSWORD" << 'EOF'
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
CREATE INDEX idx_validated IF NOT EXISTS FOR (v:VideoCapture) ON (v.validated);
CREATE INDEX idx_routing IF NOT EXISTS FOR (v:VideoCapture) ON (v.routing);
EOF

# Verify containers running
docker-compose ps
```

**Expected:** All 3 containers show "Up" ✓

### ⏱️ 7:20–7:30 AM — Phase 2: n8n Setup

1. Open: http://localhost:5678
2. Login: `admin` / (your `N8N_PASSWORD` from `.env`)
3. Create **Anthropic credential:**
   - Settings → Credentials → New → HTTP
   - Name: `Anthropic API`
   - URL: `https://api.anthropic.com`
   - Headers: `x-api-key: [your-key-from-.env]`
   - Save ✓

4. Create **Neo4j credential:**
   - Settings → Credentials → New → HTTP Basic Auth
   - Name: `Neo4j Local`
   - Username: `neo4j`
   - Password: (your `NEO4J_PASSWORD`)
   - Save ✓

**Expected:** 2 credentials visible in list ✓

### ⏱️ 7:30–8:15 AM — Phase 3: Build Workflow

Follow **SPRINT_5_IMPLEMENTATION_GUIDE.md**:
- Sections 3.1 → 3.10
- Build nodes 1–8 in order
- Test each node before connecting next

**Critical nodes:**
- Node 3 & 4: Claude API calls (Sonnet + Haiku)
- Node 5: Scoring logic (JavaScript)
- Node 6: Obsidian note generation
- Node 7: Neo4j persistence

**Reference:** `SPRINT_5_IMPLEMENTATION_GUIDE.md` has full code for each node

### ⏱️ 8:15–8:30 AM — Phase 4: Test

```bash
# Create test.json with sample video
cat > /tmp/test.json << 'EOF'
{
  "id": "test-video-001",
  "title": "Understanding Climate Science",
  "url": "https://youtube.com/watch?v=test123",
  "transcript": "Climate science is the study of Earth's climate system, including the atmosphere, oceans, ice sheets, and biosphere. A changing climate is already having far-reaching effects on the Earth's ecosystems and human societies. [Add more realistic transcript here - at least 500 words]"
}
EOF

# Send test request
WEBHOOK_URL="http://localhost:5678/webhook/youtube-validation"
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @/tmp/test.json

# Check results:
# 1. n8n workflow execution log (all green ✓)
# 2. Neo4j: docker exec pca-neo4j cypher-shell ... "MATCH (v:VideoCapture) RETURN v;"
# 3. Obsidian: check assessments/ folder for generated note
```

**Expected:** 
- ✓ n8n workflow shows 8 nodes executed
- ✓ Neo4j contains VideoCapture with routing + scores
- ✓ Obsidian note created in assessments/2026-06-01/

**Cost:** Should see ~$0.018 in API calls

---

## Success Criteria

✅ **Sprint 5 Complete when:**
- [ ] Docker containers running
- [ ] n8n credentials configured
- [ ] 8-node workflow built and tested
- [ ] Sample video processed end-to-end
- [ ] Neo4j node created with scores
- [ ] Obsidian note generated
- [ ] Total execution time: 60–90 min
- [ ] Cost: ~$0.018/video

---

## Troubleshooting Quicklinks

| Issue | Fix |
|-------|-----|
| Neo4j won't start | Check port 7687 not in use: `lsof -i :7687` |
| Anthropic API 401 | Verify API key in `.env` and n8n credential |
| n8n webhook 404 | Restart n8n: `docker restart pca-n8n` |
| Node execution fails | Check node configuration matches guide exactly |

---

## After Sprint 5

**Celebrate!** You've built:
- ✓ Automated video capture workflow
- ✓ Dual-agent validation (Sonnet 0.3 + Haiku 0.8)
- ✓ Neo4j knowledge graph foundation
- ✓ Obsidian vault integration
- ✓ 4-dimension scoring system

**Next:** Collect 50 INBOX decisions (users routing videos) → Phase 2 reconciliation engine

---

**Questions before 7 AM?** Reference the full guide: `SPRINT_5_IMPLEMENTATION_GUIDE.md`

**Go time: June 1, 7:00 AM** ⏰

