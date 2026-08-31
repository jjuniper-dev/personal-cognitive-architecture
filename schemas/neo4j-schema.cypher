// Neo4j Schema Initialization for PCA Validation Layer
// Created: 2026-05-12
// Purpose: Define schema for VideoCapture validation results

// Constraints (ensure uniqueness)
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT assessment_id IF NOT EXISTS FOR (s:Assessment) REQUIRE s.assessment_id IS UNIQUE;

// Indices (improve query performance)
CREATE INDEX idx_validated IF NOT EXISTS FOR (v:VideoCapture) ON (v.validated);
CREATE INDEX idx_routing IF NOT EXISTS FOR (v:VideoCapture) ON (v.routing);
CREATE INDEX idx_created_at IF NOT EXISTS FOR (v:VideoCapture) ON (v.created_at);
CREATE INDEX idx_confidence IF NOT EXISTS FOR (s:Assessment) ON (s.confidence);

// Create Agent nodes (reference data)
CREATE (screening:Agent {
  name: "Screening Agent",
  model: "claude-3-5-sonnet",
  temperature: 0.3,
  purpose: "Conservative, consistent scoring across 4 dimensions",
  created_at: datetime()
})
RETURN screening;

CREATE (critical:Agent {
  name: "Critical Agent",
  model: "claude-3-5-haiku",
  temperature: 0.8,
  purpose: "Exploratory, independent assessment to detect blind spots",
  created_at: datetime()
})
RETURN critical;

// Example VideoCapture node (for testing)
// Uncomment to test after schema creation
/*
CREATE (video:VideoCapture {
  video_id: "test-video-001",
  title: "Test Video",
  url: "https://youtube.com/watch?v=test",
  transcript: "This is a test transcript...",
  source: "youtube",
  created_at: datetime(),
  validated: false,
  validation_started_at: null
})
RETURN video;
*/
