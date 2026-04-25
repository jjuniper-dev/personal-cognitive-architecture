"""
Neo4j Client for PCA Knowledge Graph

Manages connection to Neo4j and provides query templates
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import os


@dataclass
class GraphNode:
    """Represents a node in the knowledge graph"""

    node_id: str
    title: str
    node_type: str  # Note, Project, Concept, Person
    project: Optional[str] = None
    domain: Optional[str] = None
    confidence: Optional[float] = None
    properties: Dict = None


@dataclass
class GraphRelationship:
    """Represents a relationship in the knowledge graph"""

    source_id: str
    target_id: str
    relationship_type: str  # related-to, depends-on, contradicts, extends
    confidence: Optional[float] = None
    properties: Dict = None


class Neo4jClient:
    """Client for Neo4j knowledge graph operations"""

    def __init__(
        self,
        uri: str = "neo4j://localhost:7687",
        username: str = "neo4j",
        password: str = None,
    ):
        """Initialize Neo4j client"""
        self.uri = uri
        self.username = username
        self.password = password or os.getenv("NEO4J_PASSWORD", "")
        self.driver = None
        self.connected = False

    def connect(self) -> bool:
        """Establish connection to Neo4j"""
        try:
            from neo4j import GraphDatabase

            self.driver = GraphDatabase.driver(
                self.uri, auth=(self.username, self.password)
            )
            self.driver.verify_connectivity()
            self.connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")
            self.connected = False
            return False

    def disconnect(self):
        """Close connection"""
        if self.driver:
            self.driver.close()
            self.connected = False

    def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute a Cypher query and return results"""
        if not self.connected:
            return []

        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Query execution error: {str(e)}")
            return []

    def get_knowledge_graph(self, limit: int = 100) -> Tuple[List[Dict], List[Dict]]:
        """
        Get all nodes and relationships from knowledge graph

        Returns: (nodes, relationships)
        """
        # Get all nodes
        nodes_query = """
        MATCH (n)
        RETURN
            id(n) as id,
            n.title as title,
            labels(n)[0] as type,
            n.project as project,
            n.domain as domain,
            n.confidence as confidence
        LIMIT $limit
        """

        nodes_raw = self.execute_query(nodes_query, {"limit": limit})
        nodes = []
        for node in nodes_raw:
            nodes.append(
                {
                    "id": str(node.get("id")),
                    "label": node.get("title", "Unknown"),
                    "type": node.get("type", "Note"),
                    "project": node.get("project"),
                    "domain": node.get("domain"),
                    "confidence": node.get("confidence"),
                }
            )

        # Get all relationships
        relationships_query = """
        MATCH (n)-[r]->(m)
        RETURN
            id(n) as source_id,
            id(m) as target_id,
            type(r) as type,
            r.confidence as confidence
        LIMIT $limit
        """

        relationships_raw = self.execute_query(relationships_query, {"limit": limit})
        relationships = []
        for rel in relationships_raw:
            relationships.append(
                {
                    "source": str(rel.get("source_id")),
                    "target": str(rel.get("target_id")),
                    "type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence"),
                }
            )

        return nodes, relationships

    def get_project_graph(self, project: str) -> Tuple[List[Dict], List[Dict]]:
        """Get subgraph for a specific project"""
        nodes_query = """
        MATCH (n {project: $project})
        RETURN
            id(n) as id,
            n.title as title,
            labels(n)[0] as type,
            n.project as project,
            n.domain as domain
        """

        nodes_raw = self.execute_query(nodes_query, {"project": project})
        nodes = [
            {
                "id": str(n.get("id")),
                "label": n.get("title", "Unknown"),
                "type": n.get("type", "Note"),
                "project": project,
                "domain": n.get("domain"),
            }
            for n in nodes_raw
        ]

        # Get relationships within project
        rels_query = """
        MATCH (n {project: $project})-[r]->(m {project: $project})
        RETURN
            id(n) as source_id,
            id(m) as target_id,
            type(r) as type
        """

        rels_raw = self.execute_query(rels_query, {"project": project})
        relationships = [
            {
                "source": str(r.get("source_id")),
                "target": str(r.get("target_id")),
                "type": r.get("type", "RELATED_TO"),
            }
            for r in rels_raw
        ]

        return nodes, relationships

    def get_contradictions(self) -> List[Dict]:
        """Find all contradictory relationships"""
        query = """
        MATCH (n)-[r:CONTRADICTS]->(m)
        RETURN
            id(n) as source_id,
            n.title as source_title,
            id(m) as target_id,
            m.title as target_title,
            r.confidence as confidence
        """

        results = self.execute_query(query)
        return results

    def get_related_notes(self, note_id: str, depth: int = 2) -> Tuple[List[Dict], List[Dict]]:
        """Get notes related to a specific note"""
        query = f"""
        MATCH (start)-[*1..{depth}]-(related)
        WHERE id(start) = $note_id
        RETURN
            id(related) as id,
            related.title as title,
            labels(related)[0] as type,
            related.project as project
        """

        nodes_raw = self.execute_query(query, {"note_id": int(note_id)})
        nodes = [
            {
                "id": str(n.get("id")),
                "label": n.get("title", "Unknown"),
                "type": n.get("type", "Note"),
                "project": n.get("project"),
            }
            for n in nodes_raw
        ]

        # Get paths
        paths_query = f"""
        MATCH (start)-[r*1..{depth}]-(related)
        WHERE id(start) = $note_id
        RETURN
            [x IN range(0, length(r)-1) | {{
                source: id(nodes(r)[x]),
                target: id(nodes(r)[x+1]),
                type: type(relationships(r)[x])
            }}] as edges
        """

        paths_raw = self.execute_query(paths_query, {"note_id": int(note_id)})
        relationships = []
        for path in paths_raw:
            if path.get("edges"):
                for edge in path["edges"]:
                    relationships.append(
                        {
                            "source": str(edge["source"]),
                            "target": str(edge["target"]),
                            "type": edge["type"],
                        }
                    )

        return nodes, relationships

    def get_domain_graph(self, domain: str) -> Tuple[List[Dict], List[Dict]]:
        """Get subgraph for a specific domain"""
        nodes_query = """
        MATCH (n {domain: $domain})
        RETURN
            id(n) as id,
            n.title as title,
            labels(n)[0] as type,
            n.domain as domain,
            n.project as project
        """

        nodes_raw = self.execute_query(nodes_query, {"domain": domain})
        nodes = [
            {
                "id": str(n.get("id")),
                "label": n.get("title", "Unknown"),
                "type": n.get("type", "Note"),
                "domain": domain,
                "project": n.get("project"),
            }
            for n in nodes_raw
        ]

        # Get relationships
        rels_query = """
        MATCH (n {domain: $domain})-[r]->(m {domain: $domain})
        RETURN
            id(n) as source_id,
            id(m) as target_id,
            type(r) as type
        """

        rels_raw = self.execute_query(rels_query, {"domain": domain})
        relationships = [
            {
                "source": str(r.get("source_id")),
                "target": str(r.get("target_id")),
                "type": r.get("type", "RELATED_TO"),
            }
            for r in rels_raw
        ]

        return nodes, relationships

    def get_stats(self) -> Dict:
        """Get graph statistics"""
        stats_query = """
        RETURN
            count(*) as total_nodes,
            count(distinct labels(*)[0]) as node_types
        """

        # Node count
        node_count_query = "MATCH (n) RETURN count(n) as count"
        node_count = self.execute_query(node_count_query)

        # Relationship count
        rel_count_query = "MATCH ()-[r]->() RETURN count(r) as count"
        rel_count = self.execute_query(rel_count_query)

        # Project count
        project_count_query = "MATCH (n) WHERE n.project IS NOT NULL RETURN count(distinct n.project) as count"
        project_count = self.execute_query(project_count_query)

        return {
            "total_nodes": node_count[0]["count"] if node_count else 0,
            "total_relationships": rel_count[0]["count"] if rel_count else 0,
            "total_projects": project_count[0]["count"] if project_count else 0,
        }


class CypherQueries:
    """Common Cypher query templates"""

    @staticmethod
    def get_all_nodes_and_edges(limit: int = 100) -> Tuple[str, str]:
        """Get all nodes and edges for visualization"""
        nodes_query = f"""
        MATCH (n)
        RETURN {{
            id: id(n),
            label: n.title,
            type: labels(n)[0],
            project: n.project,
            domain: n.domain,
            confidence: n.confidence
        }} as node
        LIMIT {limit}
        """

        edges_query = f"""
        MATCH (n)-[r]->(m)
        RETURN {{
            source: id(n),
            target: id(m),
            type: type(r),
            confidence: r.confidence
        }} as edge
        LIMIT {limit}
        """

        return nodes_query, edges_query

    @staticmethod
    def get_contradictions() -> str:
        """Find contradictions in knowledge graph"""
        return """
        MATCH (a)-[r:CONTRADICTS]->(b)
        RETURN a.title as source, b.title as target, r.confidence as confidence
        ORDER BY r.confidence DESC
        """

    @staticmethod
    def get_by_project(project: str) -> Tuple[str, str]:
        """Get nodes and edges for a project"""
        nodes_query = f"""
        MATCH (n {{project: '{project}'}})
        RETURN {{
            id: id(n),
            label: n.title,
            type: labels(n)[0]
        }} as node
        """

        edges_query = f"""
        MATCH (n {{project: '{project}'}})-[r]->(m {{project: '{project}'}})
        RETURN {{
            source: id(n),
            target: id(m),
            type: type(r)
        }} as edge
        """

        return nodes_query, edges_query

    @staticmethod
    def get_impact_analysis(note_id: str) -> str:
        """Find all notes affected by a note"""
        return f"""
        MATCH (n)-[*..3]->(affected)
        WHERE id(n) = {note_id}
        RETURN DISTINCT affected.title, count(*) as impact_count
        ORDER BY impact_count DESC
        """
