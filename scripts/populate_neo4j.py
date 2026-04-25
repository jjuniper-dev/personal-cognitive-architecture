#!/usr/bin/env python3
import json
import os
from neo4j import GraphDatabase
from datetime import datetime

class PersonalGraphDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters or {}).consume()

    def create_self_node(self):
        query = """
        MERGE (self:Self {name: 'Self'})
        SET self.role = 'Learner, Builder, Mentor, Strategic Thinker',
            self.created_date = datetime(),
            self.core_values = ['Contribution', 'Growth', 'Autonomy', 'Authenticity'],
            self.mindset = ['Systems thinking', 'Self-aware', 'Growth-oriented', 'Intentional']
        RETURN self
        """
        return self.execute_query(query)

    def create_values(self):
        values = [
            {"name": "Contribution", "description": "Making a real difference in work and life"},
            {"name": "Growth", "description": "Personal and others' continuous development"},
            {"name": "Autonomy", "description": "Freedom to make own choices and decisions"},
            {"name": "Authenticity", "description": "Being genuine, no masks or performance"}
        ]

        for value in values:
            query = """
            MERGE (v:Value {name: $name})
            SET v.description = $description
            RETURN v
            """
            self.execute_query(query, value)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (v:Value {name: $name})
            MERGE (self)-[:VALUES]->(v)
            """
            self.execute_query(link_query, {"name": value["name"]})

    def create_learning_styles(self):
        modalities = [
            {"modality": "Visual", "description": "Diagrams, charts, videos"},
            {"modality": "Auditory", "description": "Discussion, podcasts, talking it out"}
        ]

        approaches = [
            {"modality": "Trial and Error", "description": "Hands-on experimentation and learning"},
            {"modality": "Teaching Others", "description": "Learning by explaining and mentoring"}
        ]

        all_styles = modalities + approaches

        for style in all_styles:
            query = """
            MERGE (ls:LearningStyle {modality: $modality})
            SET ls.description = $description
            RETURN ls
            """
            self.execute_query(query, style)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (ls:LearningStyle {modality: $modality})
            MERGE (self)-[:HAS_LEARNING_STYLE]->(ls)
            """
            self.execute_query(link_query, {"modality": style["modality"]})

    def create_work_context(self):
        contexts = [
            {"aspect": "Environment: Flex Remote", "description": "Mix of remote and office work"},
            {"aspect": "Environment: Solo Deep Work", "description": "Dedicated space for focused work"},
            {"aspect": "Pace: Deep Focus", "description": "Long stretches on meaningful work"},
            {"aspect": "Pace: Balanced Collaboration", "description": "Collaboration balanced with focus"},
            {"aspect": "Value: Learning", "description": "Constantly growing and new challenges"},
            {"aspect": "Value: Impact", "description": "Seeing work make real difference"},
            {"aspect": "Value: Mastery", "description": "Getting excellent at what matters"},
            {"aspect": "Value: Autonomy", "description": "Owning work and decisions"},
            {"aspect": "Time: Deep Work Priority", "description": "Most time on core work, minimal meetings"},
            {"aspect": "Time: Reflection", "description": "Intentional thinking and planning time"}
        ]

        for context in contexts:
            query = """
            MERGE (wc:WorkContext {aspect: $aspect})
            SET wc.description = $description
            RETURN wc
            """
            self.execute_query(query, context)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (wc:WorkContext {aspect: $aspect})
            MERGE (self)-[:WORKS_IN]->(wc)
            """
            self.execute_query(link_query, {"aspect": context["aspect"]})

    def create_relationships(self):
        rel_types = [
            {"type": "Deep 1-on-1", "preference": "Preferred"},
            {"type": "Small Groups (3-5)", "preference": "Preferred"},
            {"type": "Async Communication", "preference": "Preferred"},
            {"type": "Mentoring", "preference": "Energizing"},
            {"type": "Peer Collaboration", "preference": "Energizing"},
            {"type": "Surface Talk", "preference": "Draining"},
            {"type": "Competitive Dynamics", "preference": "Draining"}
        ]

        for rel in rel_types:
            query = """
            MERGE (r:Relationship {type: $type})
            SET r.preference = $preference
            RETURN r
            """
            self.execute_query(query, rel)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (r:Relationship {type: $type})
            MERGE (self)-[:HAS_RELATIONSHIP_STYLE]->(r)
            """
            self.execute_query(link_query, {"type": rel["type"]})

            # Link energizing relationships to values
            if rel["preference"] == "Energizing":
                values_query = """
                MATCH (r:Relationship {type: $type}), (v:Value)
                WHERE v.name IN ['Contribution', 'Growth']
                MERGE (r)-[:ROOTED_IN]->(v)
                """
                self.execute_query(values_query, {"type": rel["type"]})

    def create_energy(self):
        energy_aspects = [
            {"aspect": "Chronotype: Early Morning", "description": "Peak thinking time before others awake"},
            {"aspect": "Recharge Need: Solo Time", "description": "Essential for recharging as introvert"},
            {"aspect": "Creative Necessity: Deep Work", "description": "Best thinking happens in solitude"},
            {"aspect": "Rhythm: Protected Focus Blocks", "description": "Deep work time blocked off"}
        ]

        for energy in energy_aspects:
            query = """
            MERGE (e:Energy {aspect: $aspect})
            SET e.description = $description
            RETURN e
            """
            self.execute_query(query, energy)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (e:Energy {aspect: $aspect})
            MERGE (self)-[:OPERATES_WITH_ENERGY]->(e)
            """
            self.execute_query(link_query, {"aspect": energy["aspect"]})

    def create_challenges(self):
        challenges = [
            {"name": "Networking & Visibility", "impact": "Ideas need visibility to have impact"},
            {"name": "Turning Ideas into Action", "impact": "Execution gap between thinking and doing"}
        ]

        for challenge in challenges:
            query = """
            MERGE (c:Challenge {name: $name})
            SET c.impact = $impact
            RETURN c
            """
            self.execute_query(query, challenge)

            # Link to Self
            link_query = """
            MATCH (self:Self {name: 'Self'}), (c:Challenge {name: $name})
            MERGE (self)-[:FACES_CHALLENGE]->(c)
            """
            self.execute_query(link_query, {"name": challenge["name"]})

    def create_cross_relationships(self):
        # LearningStyle SHAPES WorkContext
        query = """
        MATCH (ls:LearningStyle {modality: 'Visual'}), (wc:WorkContext {aspect: 'Environment: Solo Deep Work'})
        MERGE (ls)-[:SHAPES]->(wc)
        """
        self.execute_query(query)

        # Mentoring ENERGIZED_BY Learning approaches
        query = """
        MATCH (ls:LearningStyle {modality: 'Teaching Others'}), (r:Relationship {type: 'Mentoring'})
        MERGE (ls)-[:ENERGIZED_BY]->(r)
        """
        self.execute_query(query)

    def populate_database(self):
        print("🚀 Creating Self node...")
        self.create_self_node()

        print("📌 Creating Values...")
        self.create_values()

        print("🧠 Creating Learning Styles...")
        self.create_learning_styles()

        print("💼 Creating Work Context...")
        self.create_work_context()

        print("👥 Creating Relationships...")
        self.create_relationships()

        print("⚡ Creating Energy patterns...")
        self.create_energy()

        print("⚠️  Creating Challenges...")
        self.create_challenges()

        print("🔗 Creating cross-relationships...")
        self.create_cross_relationships()

        print("✅ Database population complete!")

def main():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    db = PersonalGraphDatabase(uri, user, password)
    try:
        db.populate_database()
    finally:
        db.close()

if __name__ == "__main__":
    main()
