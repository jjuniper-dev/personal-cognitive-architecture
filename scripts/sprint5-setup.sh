#!/bin/bash
# Sprint 5 Setup Script
# Sets up Docker containers and initializes databases for n8n validation workflow

set -e

echo "🚀 PCA Sprint 5 Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Create .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your actual credentials:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - OBSIDIAN_VAULT_PATH"
    echo "   - Custom passwords (N8N_PASSWORD, NEO4J_PASSWORD, etc.)"
    exit 1
fi

# Step 2: Create Obsidian vault directories
VAULT_PATH=$(grep OBSIDIAN_VAULT_PATH .env | cut -d '=' -f 2 | tr -d ' ')
if [ ! -z "$VAULT_PATH" ]; then
    echo "📁 Creating Obsidian vault structure..."
    mkdir -p "$VAULT_PATH/videos"
    mkdir -p "$VAULT_PATH/assessments"
    mkdir -p "$VAULT_PATH/knowledge-graph"
    echo "   ✓ Vault directories created at: $VAULT_PATH"
fi

# Step 3: Start Docker containers
echo ""
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready (60 seconds)..."
sleep 60

# Step 4: Initialize Neo4j schema
echo ""
echo "⚙️  Initializing Neo4j schema..."
NEO4J_PASSWORD=$(grep NEO4J_PASSWORD .env | cut -d '=' -f 2 | tr -d ' ')

docker exec pca-neo4j cypher-shell -u neo4j -p "$NEO4J_PASSWORD" << 'EOF'
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
CREATE INDEX idx_validated IF NOT EXISTS FOR (v:VideoCapture) ON (v.validated);
CREATE INDEX idx_routing IF NOT EXISTS FOR (v:VideoCapture) ON (v.routing);
EOF

echo "   ✓ Neo4j schema initialized"

# Step 5: Verify containers are healthy
echo ""
echo "✅ Container Status:"
docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Sprint 5 Setup Complete!"
echo ""
echo "📍 Access Points:"
echo "   • n8n: http://localhost:5678"
echo "   • Neo4j Browser: http://localhost:7474"
echo "   • Neo4j Bolt: bolt://localhost:7687"
echo ""
echo "🔐 Default Credentials (change these!):"
echo "   • n8n: admin / (see .env)"
echo "   • Neo4j: neo4j / (see .env)"
echo ""
echo "📋 Next Steps:"
echo "   1. Log in to n8n (http://localhost:5678)"
echo "   2. Set up Anthropic API credential with your API key"
echo "   3. Set up Neo4j credential (host: neo4j, port: 7687)"
echo "   4. Follow SPRINT_5_N8N_SETUP_VALIDATION_LAYER.md to build workflow"
echo ""
