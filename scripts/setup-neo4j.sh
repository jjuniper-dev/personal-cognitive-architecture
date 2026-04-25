#!/bin/bash

# Neo4j Personal Graph Setup Script

echo "🚀 Setting up Neo4j Personal Cognitive Architecture Graph"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Please install Docker to run Neo4j."
    echo "Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Neo4j container already exists
if docker ps -a --format '{{.Names}}' | grep -q '^neo4j-personal$'; then
    echo "📦 Stopping existing Neo4j container..."
    docker stop neo4j-personal 2>/dev/null || true
    docker rm neo4j-personal 2>/dev/null || true
fi

echo "📦 Starting Neo4j container..."
docker run -d \
  --name neo4j-personal \
  --publish 7474:7474 \
  --publish 7687:7687 \
  --env NEO4J_AUTH=neo4j/password \
  --env NEO4J_PLUGINS='["apoc"]' \
  neo4j:latest

echo ""
echo "⏳ Waiting for Neo4j to start (30 seconds)..."
sleep 30

echo ""
echo "✅ Neo4j is running!"
echo ""
echo "📍 Neo4j Browser: http://localhost:7474"
echo "🔌 Connection URI: bolt://localhost:7687"
echo "👤 Username: neo4j"
echo "🔐 Password: password"
echo ""
echo "Next steps:"
echo "1. Install neo4j-driver: npm install neo4j-driver"
echo "2. Run: node scripts/populate-graph.js"
echo ""
