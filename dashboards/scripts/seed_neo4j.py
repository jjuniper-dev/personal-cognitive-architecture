#!/usr/bin/env python3
"""Seed Neo4j knowledge graph from Obsidian vault"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import re
import os

try:
    import frontmatter
except ImportError:
    print("❌ Missing dependency: python-frontmatter")
    print("Install with: pip install python-frontmatter")
    sys.exit(1)

try:
    from neo4j import GraphDatabase
except ImportError:
    print("❌ Missing dependency: neo4j")
    print("Install with: pip install neo4j")
    sys.exit(1)


class VaultParser:
    """Extract notes, concepts, and relationships from Obsidian vault"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.notes: Dict = {}
        self.relationships: List[Dict] = []
        self.projects: Set[str] = set()
        self.domains: Set[str] = set()

    def parse_vault(self) -> Tuple[Dict, List]:
        """Parse all markdown files in vault"""
        print(f"📚 Parsing vault at {self.vault_path}...")

        md_files = list(self.vault_path.rglob("*.md"))
        print(f"   Found {len(md_files)} markdown files")

        for md_file in md_files:
            if ".obsidian" in str(md_file) or "node_modules" in str(md_file):
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

            note_id = file_path.stem
            relative_path = file_path.relative_to(self.vault_path)
            path_parts = relative_path.parts

            note_type = self._get_note_type(path_parts, metadata)
            project = self._get_project(path_parts)
            domain = metadata.get("domain", "")

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

            for link_target in links:
                self.relationships.append(
                    {
                        "source": note_id,
                        "target": link_target,
                        "type": "REFERENCES",
                    }
                )

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
        if len(path_parts) > 1 and path_parts[0].startswith("10-"):
            return path_parts[1]
        return ""

    def _extract_links(self, content: str) -> List[str]:
        """Extract wiki links from markdown content"""
        links = []
        pattern = r"\[\[([^\[\]]+)\]\]"
        for match in re.finditer(pattern, content):
            link = match.group(1)
            target = link.split("|")[0].strip()
            links.append(target)
        return links


class Neo4jSeeder:
    """Seed Neo4j with knowledge graph data"""

    def __init__(self, uri: str, user: str, password: str):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            raise

    def seed_graph(self, notes: Dict, relationships: List):
        """Create nodes and relationships in Neo4j"""
        if not notes:
            print("⚠️ No notes to seed")
            return

        print(f"📝 Creating {len(notes)} nodes...")
        for i, (note_id, note) in enumerate(notes.items()):
            self._create_note_node(note)
            if (i + 1) % 25 == 0:
                print(f"   Created {i + 1} nodes...")

        print(f"🔗 Creating {len(relationships)} relationships...")
        valid_relationships = 0
        for i, rel in enumerate(relationships):
            if self._create_relationship(rel):
                valid_relationships += 1
            if (i + 1) % 50 == 0:
                print(f"   Created {valid_relationships} valid relationships...")

        print(f"✅ Seeding complete! ({valid_relationships} valid relationships)")

    def _create_note_node(self, note: Dict):
        """Create a note node in Neo4j"""
        query = """
        MERGE (n:Note {id: $id})
        SET n.title = $title,
            n.type = $type,
            n.project = $project,
            n.domain = $domain,
            n.confidence = $confidence,
            n.created = $created,
            n.updated = $updated,
            n.path = $path
        """

        with self.driver.session() as session:
            try:
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
                    },
                )
            except Exception as e:
                print(f"   ⚠️ Error creating node {note['id']}: {e}")

    def _create_relationship(self, rel: Dict) -> bool:
        """Create a relationship in Neo4j, return True if successful"""
        query = f"""
        MATCH (source:Note {{id: $source}})
        MATCH (target:Note {{id: $target}})
        MERGE (source)-[:{rel['type']}]->(target)
        """

        with self.driver.session() as session:
            try:
                result = session.run(
                    query, {"source": rel["source"], "target": rel["target"]}
                )
                return result.consume().counters.relationships_created > 0
            except Exception:
                return False

    def verify_import(self) -> Dict:
        """Verify the import was successful"""
        with self.driver.session() as session:
            node_result = session.run("MATCH (n) RETURN count(n) as count")
            rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            project_result = session.run(
                "MATCH (n:Note) WHERE n.project IS NOT NULL "
                "RETURN count(distinct n.project) as count"
            )

            node_count = node_result.single()[0] if node_result.single() else 0
            rel_count = rel_result.single()[0] if rel_result.single() else 0
            project_count = (
                project_result.single()[0] if project_result.single() else 0
            )

            return {
                "nodes": node_count,
                "relationships": rel_count,
                "projects": project_count,
            }

    def close(self):
        """Close database connection"""
        self.driver.close()


def main():
    """Main seeding workflow"""
    vault_path = Path.home() / "obsidian-vault"
    neo4j_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not neo4j_password:
        try:
            neo4j_password = input("Enter Neo4j password: ")
        except KeyboardInterrupt:
            print("\n❌ Cancelled")
            return

    if not vault_path.exists():
        print(f"❌ Vault not found at {vault_path}")
        return

    parser = VaultParser(vault_path)
    notes, relationships = parser.parse_vault()

    print(f"\n🚀 Seeding Neo4j at {neo4j_uri}...")
    seeder = Neo4jSeeder(neo4j_uri, neo4j_user, neo4j_password)

    try:
        seeder.seed_graph(notes, relationships)

        stats = seeder.verify_import()
        print(f"\n📊 Import Statistics:")
        print(f"  - Nodes: {stats['nodes']}")
        print(f"  - Relationships: {stats['relationships']}")
        print(f"  - Projects: {stats['projects']}")
        print(f"\n✨ Knowledge graph is ready!")
        print(f"   View in Chainlit: `/graph`")
        print(f"   View in browser: http://localhost:7474/")

    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
    finally:
        seeder.close()


if __name__ == "__main__":
    main()
