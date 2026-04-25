---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [neo4j, obsidian, knowledge-graph, setup, seeding]
status: active
---

# Neo4j Knowledge Graph Seeding from Obsidian Vault

Guide for populating Neo4j with notes, concepts, and relationships extracted from your Obsidian vault.

## Prerequisites

1. **Neo4j Installation**
   ```bash
   # Community Edition (free)
   # Download from: https://neo4j.com/download/
   
   # Or via Homebrew (macOS)
   brew install neo4j
   
   # Or via Docker
   docker run -d -p 7474:7474 -p 7687:7687 neo4j:latest
   ```

2. **Neo4j Running**
   ```bash
   # Start Neo4j
   neo4j start
   
   # Access web interface at http://localhost:7474
   # Default credentials: neo4j / neo4j
   # Change password on first login
   ```

3. **Python Dependencies**
   ```bash
   pip install neo4j python-frontmatter pyyaml
   ```

## Vault Structure Assumptions

The seeding process expects your Obsidian vault to follow this structure:

```
obsidian-vault/
├── 10-Projects/
│   ├── PROJECT-NAME/
│   │   ├── Overview.md
│   │   ├── Tasks.md
│   │   └── Notes/
│   │       └── *.md
│   └── PATH-HAIL/
│       ├── Overview.md
│       └── Notes/
│
├── 20-Ideas/
│   ├── Unstructured/
│   │   └── *.md
│   └── Concepts/
│       └── *.md
│
├── 30-Sources/
│   ├── Articles/
│   │   └── *.md
│   ├── Books/
│   │   └── *.md
│   └── Feeds/
│       └── *.md
│
└── 40-Archive/
    └── *.md
```

## Seeding Script

Create `dashboards/scripts/seed_neo4j.py`:

```python
#!/usr/bin/env python3
"""Seed Neo4j knowledge graph from Obsidian vault"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import frontmatter
from neo4j import GraphDatabase


class VaultParser:
    """Extract notes, concepts, and relationships from Obsidian vault"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.notes: Dict = {}
        self.relationships: List[Tuple] = []
        self.projects: Set[str] = set()
        self.domains: Set[str] = set()

    def parse_vault(self) -> Tuple[Dict, List]:
        """Parse all markdown files in vault"""
        print(f"📚 Parsing vault at {self.vault_path}...")

        for md_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(md_file):
                continue
            self._parse_note(md_file)

        print(
            f"✅ Parsed {len(self.notes)} notes, "
            f"{len(self.relationships)} relationships"
        )
        return self.notes, self.relationships

    def _parse_note(self, file_path: Path):
        """Parse individual note file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)

            metadata = post.metadata or {}
            content = post.content

            # Extract note ID from filename
            note_id = file_path.stem
            relative_path = file_path.relative_to(self.vault_path)

            # Determine note type and project
            path_parts = relative_path.parts
            note_type = self._get_note_type(path_parts, metadata)
            project = self._get_project(path_parts)
            domain = metadata.get("domain", "")

            # Extract wiki links and references
            links = self._extract_links(content)
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]

            note = {
                "id": note_id,
                "title": metadata.get("title", file_path.stem),
                "type": note_type,
                "project": project,
                "domain": domain,
                "path": str(relative_path),
                "tags": tags,
                "links": links,
                "confidence": float(metadata.get("confidence", 0.85)),
                "created": metadata.get("created", datetime.now().isoformat()),
                "updated": metadata.get("updated", datetime.now().isoformat()),
            }

            self.notes[note_id] = note

            # Extract relationships
            for link_target in links:
                self.relationships.append(
                    {
                        "source": note_id,
                        "target": link_target,
                        "type": "REFERENCES",
                    }
                )

            # Track projects and domains
            if project:
                self.projects.add(project)
            if domain:
                self.domains.add(domain)

        except Exception as e:
            print(f"⚠️ Error parsing {file_path}: {e}")

    def _get_note_type(self, path_parts: Tuple, metadata: Dict) -> str:
        """Determine note type from path or metadata"""
        explicit_type = metadata.get("type")
        if explicit_type:
            return explicit_type

        if len(path_parts) > 0:
            first_dir = path_parts[0]
            if first_dir.startswith("10-"):
                return "Project"
            elif first_dir.startswith("20-"):
                return "Concept" if "Concepts" in path_parts else "Idea"
            elif first_dir.startswith("30-"):
                return "Source"
            elif first_dir.startswith("40-"):
                return "Archive"

        return "Note"

    def _get_project(self, path_parts: Tuple) -> str:
        """Extract project name from path"""
        # Assumes structure: 10-Projects/PROJECT-NAME/...
        if len(path_parts) > 1 and path_parts[0].startswith("10-"):
            return path_parts[1]
        return ""

    def _extract_links(self, content: str) -> List[str]:
        """Extract wiki links from markdown content"""
        import re

        links = []
        # Match [[link]] patterns
        pattern = r"\[\[([^\[\]]+)\]\]"
        for match in re.finditer(pattern, content):
            link = match.group(1)
            # Handle [[link|display text]]
            target = link.split("|")[0].strip()
            links.append(target)

        return links


class Neo4jSeeder:
    """Seed Neo4j with knowledge graph data"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def seed_graph(self, notes: Dict, relationships: List):
        """Create nodes and relationships in Neo4j"""
        print("📝 Creating nodes...")
        for note_id, note in notes.items():
            self._create_note_node(note)

        print("🔗 Creating relationships...")
        for rel in relationships:
            self._create_relationship(rel)

        print("✅ Seeding complete!")

    def _create_note_node(self, note: Dict):
        """Create a note node in Neo4j"""
        query = """
        CREATE (n:Note {
            id: $id,
            title: $title,
            type: $type,
            project: $project,
            domain: $domain,
            confidence: $confidence,
            created: $created,
            updated: $updated,
            path: $path
        })
        WITH n
        UNWIND $tags AS tag
        SET n += { tags: tag }
        """

        with self.driver.session() as session:
            session.run(
                query,
                {
                    "id": note["id"],
                    "title": note["title"],
                    "type": note["type"],
                    "project": note["project"],
                    "domain": note["domain"],
                    "confidence": note["confidence"],
                    "created": note["created"],
                    "updated": note["updated"],
                    "path": note["path"],
                    "tags": note.get("tags", []),
                },
            )

    def _create_relationship(self, rel: Dict):
        """Create a relationship in Neo4j"""
        query = f"""
        MATCH (source:Note {{id: $source}})
        MATCH (target:Note {{id: $target}})
        CREATE (source)-[:{rel['type']}]->(target)
        """

        with self.driver.session() as session:
            try:
                session.run(query, {"source": rel["source"], "target": rel["target"]})
            except Exception as e:
                # Skip if source or target doesn't exist
                pass

    def verify_import(self) -> Dict:
        """Verify the import was successful"""
        with self.driver.session() as session:
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()
            rel_count = session.run(
                "MATCH ()-[r]->() RETURN count(r) as count"
            ).single()
            projects = session.run(
                "MATCH (n:Note) WHERE n.project IS NOT NULL "
                "RETURN count(distinct n.project) as count"
            ).single()

            return {
                "nodes": node_count["count"],
                "relationships": rel_count["count"],
                "projects": projects["count"],
            }

    def close(self):
        """Close database connection"""
        self.driver.close()


def main():
    """Main seeding workflow"""
    import os

    vault_path = Path.home() / "obsidian-vault"
    neo4j_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not neo4j_password:
        neo4j_password = input("Enter Neo4j password: ")

    if not vault_path.exists():
        print(f"❌ Vault not found at {vault_path}")
        return

    # Parse vault
    parser = VaultParser(vault_path)
    notes, relationships = parser.parse_vault()

    # Seed Neo4j
    print(f"\n🚀 Seeding Neo4j at {neo4j_uri}...")
    seeder = Neo4jSeeder(neo4j_uri, neo4j_user, neo4j_password)

    try:
        seeder.seed_graph(notes, relationships)

        # Verify import
        stats = seeder.verify_import()
        print(f"\n📊 Import Statistics:")
        print(f"  - Nodes: {stats['nodes']}")
        print(f"  - Relationships: {stats['relationships']}")
        print(f"  - Projects: {stats['projects']}")

    finally:
        seeder.close()


if __name__ == "__main__":
    main()
```

## Running the Seeding Script

### Step 1: Prepare Neo4j

```bash
# Start Neo4j
neo4j start

# Verify it's running
curl http://localhost:7474/db/neo4j/open

# Clear existing data (optional - WARNING: destructive!)
# cypher-shell -u neo4j -p <password>
# > MATCH (n) DETACH DELETE n;
# > :exit
```

### Step 2: Set Environment Variables

```bash
export NEO4J_URI="neo4j://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password"
```

### Step 3: Run the Seeding Script

```bash
cd dashboards/scripts
python seed_neo4j.py
```

### Step 4: Verify in Neo4j Browser

```bash
# Open browser interface
open http://localhost:7474/browser/

# Run verification query
MATCH (n) RETURN count(n) as total_nodes;
MATCH ()-[r]->() RETURN count(r) as total_relationships;
MATCH (n:Note {type: "Project"}) RETURN n.project, count(*) as count GROUP BY n.project;
```

## Expected Output

```
📚 Parsing vault at /Users/you/obsidian-vault...
✅ Parsed 147 notes, 312 relationships

🚀 Seeding Neo4j at neo4j://localhost:7687...
📝 Creating nodes...
🔗 Creating relationships...
✅ Seeding complete!

📊 Import Statistics:
  - Nodes: 147
  - Relationships: 312
  - Projects: 3
```

## Data Mapping

### Note Metadata → Neo4j Properties

| Obsidian | Neo4j Property | Type | Example |
|----------|----------------|------|---------|
| title | title | string | "AI Safety Concepts" |
| type (frontmatter) | type | string | "Concept" or "Project" |
| domain (frontmatter) | domain | string | "AI-Safety" |
| tags (frontmatter) | tags | array | ["research", "urgent"] |
| confidence (frontmatter) | confidence | float | 0.85 |
| created (frontmatter) | created | ISO date | "2026-04-25T10:30:00Z" |

### Relationship Types

| Type | Meaning | Created From |
|------|---------|--------------|
| REFERENCES | One note links to another | `[[link]]` in content |
| RELATED_TO | Conceptually related | (Manual, added via update) |
| CONTRADICTS | Conflicting information | (Manual, added via update) |
| DEPENDS_ON | Prerequisite knowledge | (Manual, added via update) |

## Incremental Updates

For ongoing updates without full re-seeding:

```python
# Add a new note
query = """
CREATE (n:Note {
    id: $id,
    title: $title,
    type: $type,
    domain: $domain,
    confidence: $confidence
})
"""
session.run(query, {...})

# Update an existing note
query = """
MATCH (n:Note {id: $id})
SET n.title = $title,
    n.updated = $updated
"""
session.run(query, {...})

# Add a manual relationship
query = """
MATCH (a:Note {id: $source})
MATCH (b:Note {id: $target})
CREATE (a)-[:CONTRADICTS {confidence: $confidence}]->(b)
"""
session.run(query, {...})
```

## Troubleshooting

### Connection Refused
```
⚠️ Error: Connection refused at neo4j://localhost:7687

Fix:
1. Ensure Neo4j is running: neo4j status
2. Start it: neo4j start
3. Check port: netstat -an | grep 7687
```

### Authentication Failed
```
⚠️ Error: Invalid credentials

Fix:
1. Reset Neo4j password: neo4j-admin set-password
2. Verify in browser: http://localhost:7474/
3. Update environment variable: export NEO4J_PASSWORD="correct-password"
```

### Memory Issues
```
⚠️ Error: OutOfMemory

Fix (for large vaults):
1. Increase Neo4j heap: edit neo4j.conf
2. Set: dbms.memory.heap.initial_size=2G
3. Set: dbms.memory.heap.max_size=4G
4. Restart: neo4j restart
```

### Slow Import
```
Optimize with batch processing:

# Import in batches of 100
for i in range(0, len(notes), 100):
    batch = list(notes.items())[i:i+100]
    seeder._create_batch(batch)
```

## Next Steps

1. **Verify Dashboard Connection**: Run `/graph` in Chainlit dashboard
2. **Add Manual Relationships**: Update Neo4j with contradictions and dependencies
3. **Set Up Auto-Sync**: Configure n8n workflow to auto-update Neo4j on capture
4. **Enable Feedback Loop**: Track which recommendations were helpful

---

**Status**: Ready for use
**Last Updated**: 2026-04-25
**Related**: ../README.md, ../../agents/validation-worker.md
