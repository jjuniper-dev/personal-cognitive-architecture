# Personal Cognitive Architecture - Neo4j Graph Setup

This guide walks you through setting up and populating your personal cognitive architecture as a Neo4j graph database.

## Quick Start

### 1. Start Neo4j with Docker

```bash
chmod +x scripts/setup-neo4j.sh
./scripts/setup-neo4j.sh
```

This will:
- Start a Neo4j container with default credentials
- Expose Neo4j Browser at `http://localhost:7474`
- Open the Bolt connection on `bolt://localhost:7687`

### 2. Install Dependencies

```bash
npm install neo4j-driver dotenv
```

### 3. Populate the Graph

```bash
node scripts/populate-graph.js
```

This will create all nodes and relationships representing your personal profile.

## Connection Details

- **Browser UI**: http://localhost:7474
- **Bolt URI**: bolt://localhost:7687
- **Username**: neo4j
- **Password**: password

## Graph Schema

### Node Types

- **Self**: Core node representing you
- **Value**: Core values (Contribution, Growth, Autonomy, Authenticity)
- **LearningStyle**: How you learn (Visual, Auditory, Trial & Error, Teaching)
- **WorkContext**: Work environment and preferences
- **Relationship**: Relationship types and preferences
- **Energy**: Energy patterns and rhythm
- **Challenge**: Development challenges

### Relationship Types

```
Self -[HAS_LEARNING_STYLE]-> LearningStyle
Self -[VALUES]-> Value
Self -[WORKS_IN]-> WorkContext
Self -[HAS_RELATIONSHIP_STYLE]-> Relationship
Self -[OPERATES_WITH_ENERGY]-> Energy
Self -[FACES_CHALLENGE]-> Challenge

LearningStyle -[SHAPES]-> WorkContext
LearningStyle -[ENERGIZED_BY]-> Relationship

Relationship -[ROOTED_IN]-> Value
```

## Useful Cypher Queries

### View Your Complete Profile
```cypher
MATCH (self:Self)-[r]->(node)
RETURN self, type(r) as relationshipType, node
```

### Find What Energizes You
```cypher
MATCH (self:Self)-[:HAS_RELATIONSHIP_STYLE]->(rel:Relationship {preference: 'Energizing'})
RETURN rel.type, rel.preference
```

### View Your Core Values
```cypher
MATCH (self:Self)-[:VALUES]->(v:Value)
RETURN v.name, v.description
```

### See Your Learning Style
```cypher
MATCH (self:Self)-[:HAS_LEARNING_STYLE]->(ls:LearningStyle)
RETURN ls.modality, ls.description
```

### Find What's Connected to Your Work
```cypher
MATCH (self:Self)-[:WORKS_IN]->(wc:WorkContext)
RETURN wc.aspect, wc.description
ORDER BY wc.aspect
```

### Understand Your Energy Patterns
```cypher
MATCH (self:Self)-[:OPERATES_WITH_ENERGY]->(e:Energy)
RETURN e.aspect, e.description
```

### See What Challenges You Face
```cypher
MATCH (self:Self)-[:FACES_CHALLENGE]->(c:Challenge)
RETURN c.name, c.impact
```

### Map Learning Style to Work Context
```cypher
MATCH (ls:LearningStyle)-[:SHAPES]->(wc:WorkContext)
RETURN ls.modality, wc.aspect
```

### Find Shared Values in Relationships
```cypher
MATCH (rel:Relationship)-[:ROOTED_IN]->(v:Value)
RETURN rel.type, v.name
```

## Expanding Your Graph

### Add New Learning Modalities
```cypher
MATCH (self:Self {name: 'Self'})
CREATE (ls:LearningStyle {modality: 'Your New Style', description: 'Description'})
CREATE (self)-[:HAS_LEARNING_STYLE]->(ls)
```

### Add New Values
```cypher
MATCH (self:Self {name: 'Self'})
CREATE (v:Value {name: 'New Value', description: 'Description'})
CREATE (self)-[:VALUES]->(v)
```

### Add Relationships Between Nodes
```cypher
MATCH (source:LearningStyle {modality: 'Teaching Others'})
MATCH (target:WorkContext {aspect: 'Value: Impact'})
CREATE (source)-[:INFLUENCES]->(target)
```

## Environment Variables

Create a `.env` file in the root directory:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j
```

## Troubleshooting

### Container Won't Start
```bash
# Check if port is in use
lsof -i :7687
lsof -i :7474

# Remove old container and try again
docker rm neo4j-personal
./scripts/setup-neo4j.sh
```

### Connection Refused
- Make sure the container is running: `docker ps`
- Wait 30+ seconds for Neo4j to fully initialize
- Check the container logs: `docker logs neo4j-personal`

### Permission Denied on Script
```bash
chmod +x scripts/setup-neo4j.sh
./scripts/setup-neo4j.sh
```

## Next Steps

1. Explore your graph in Neo4j Browser
2. Run Cypher queries to understand connections
3. Add new insights as you discover patterns
4. Build visualizations of your cognitive architecture
