---
type: specification
created: 2026-04-24
updated: 2026-04-24
tags: [pca, reconciliation, core-engine]
status: active
---

# PCA Cognitive Reconciliation Engine

## Overview

The Cognitive Reconciliation Engine (CRE) is the core differentiator of the PCA architecture.

It is the mechanism by which the system actively evaluates new information against existing knowledge, identifies relationships and contradictions, updates confidence levels, and evolves its internal model over time.

The CRE transforms the PCA from a passive knowledge repository into an active, learning cognitive system.

## Purpose

The CRE serves three critical functions:

1. **Comparative Analysis** — Compare new input against existing knowledge graph
2. **Relationship Detection** — Identify reinforcement, contradictions, gaps, and novel contributions
3. **Model Evolution** — Update confidence levels, restructure beliefs, and trigger deeper analysis when needed

## Core Responsibilities

The CRE is responsible for:

- Accepting validated inputs from the Validation & Scoring layer
- Querying the Knowledge Graph for related information
- Detecting semantic and logical relationships
- Identifying conflicts, reinforcements, and gaps
- Updating confidence scores for affected knowledge
- Flagging contradictions for human review
- Triggering escalation or deeper reconciliation when needed
- Returning action items and integration recommendations

## Reconciliation Modes

### Mode 0: Off (Capture Only)

Inputs flow directly to storage without reconciliation.

**Use case**: High-volume, low-impact intake when reconciliation overhead is unjustified.

**Behavior**:
- Capture and tag only
- No knowledge graph querying
- No confidence updates
- Direct storage in Inbox

### Mode 1: Local (Bounded Reconciliation)

Reconciliation using available local context with constrained scope.

**Use case**: Standard ingestion with lightweight comparison.

**Behavior**:
- Query knowledge graph for related nodes (3-hop neighborhood)
- Surface direct relationships and immediate contradictions
- Update confidence for affected nodes
- Route results based on findings

**Cost**: Minimal (semantic search + relationship analysis)

### Mode 2: Deep (Comprehensive Synthesis)

Broader synthesis using expanded retrieval and extended review controls.

**Use case**: High-impact information, significant contradictions, or strategic decisions.

**Behavior**:
- Expanded knowledge graph traversal (full domain context)
- Retrieve supporting and contradicting evidence
- Surface chains of reasoning affected by new information
- Generate reconciliation report with implications
- Escalate to human review automatically

**Cost**: High (full reasoning chain analysis + report generation)

**Human oversight**: Required

## Reconciliation Workflow

### Input

Input contract (confidence_score: 0.0–1.0):

```json
{
  "input_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "New finding on topic X contradicts previous understanding",
  "source": "research-database-001",
  "confidence_score": 0.75,
  "domain": "health-policy",
  "metadata": {
    "timestamp": "2026-04-24T22:00:00Z",
    "priority": "high"
  }
}
```

### Processing Pipeline

1. **Graph Querying Phase**
   - Search for semantically related nodes in knowledge graph
   - Identify direct connections (1-2 hops)
   - Surface domain-level context
   - Retrieve supporting and contradicting material

2. **Relationship Detection Phase**
   - Compare input against retrieved nodes
   - Classify relationship type:
     - **Reinforcement** — Confirms existing knowledge
     - **Challenge** — Contradicts existing knowledge
     - **Expansion** — Extends existing knowledge
     - **Novel** — Introduces new domain or concept
     - **Null** — No meaningful relationship

3. **Confidence Analysis Phase**
   - Calculate impact on related nodes
   - Determine if existing confidence scores should shift
   - Flag if contradiction is material (high confidence mismatch)
   - Identify chains of dependent reasoning affected

4. **Escalation Determination Phase**
   - Assess contradiction severity
   - Evaluate impact scope
   - Determine human review requirement
   - Route to appropriate handler

5. **Integration Decision Phase**
   - Generate recommendations for integration
   - Suggest any restructuring needed
   - Flag follow-up analysis or research threads
   - Create action items

### Output

Output contract (confidence_delta: -0.3 to +0.3, confidence ranges: 0.0–1.0, all enum types shown):

```json
{
  "reconciliation_id": "660f9511-f30c-52e5-b827-557766551111",
  "input_id": "550e8400-e29b-41d4-a716-446655440000",
  "mode": "local",
  "relationships": [
    {
      "related_node_id": "770g9622-g41d-63f6-c838-668877662222",
      "relationship_type": "challenge",
      "confidence_delta": -0.15,
      "evidence_summary": "New finding contradicts prior assumption on mechanism",
      "requires_update": true
    },
    {
      "related_node_id": "880h0733-h52e-74g7-d949-779988773333",
      "relationship_type": "expansion",
      "confidence_delta": 0.08,
      "evidence_summary": "New finding adds supporting evidence to adjacent domain",
      "requires_update": false
    }
  ],
  "contradictions": [
    {
      "conflicting_nodes": ["node-abc-123", "node-def-456"],
      "severity": "medium",
      "implication": "Confidence in downstream reasoning may be affected",
      "requires_human_review": true
    }
  ],
  "confidence_updates": [
    {
      "node_id": "node-abc-123",
      "current_confidence": 0.82,
      "recommended_confidence": 0.67,
      "justification": "Contradiction with medium severity reduces confidence"
    }
  ],
  "action_items": [
    {
      "type": "escalate",
      "priority": "high",
      "description": "High-severity contradiction requires human decision on belief update",
      "owner": "human",
      "target": "belief-cluster-health-policy"
    },
    {
      "type": "research",
      "priority": "medium",
      "description": "Source supporting evidence to resolve contradiction",
      "owner": "agent",
      "target": "node-abc-123"
    }
  ],
  "integration_recommendation": "review",
  "narrative_summary": "New input challenges existing understanding on mechanism (medium severity). One related node confidence reduced 0.82→0.67. Recommend human review before integration."
}
```

## Decision Logic

### When to Trigger Each Mode

| Condition | Mode | Rationale |
|-----------|------|-----------|
| Low-confidence, low-impact input | 0 (Off) | Reconciliation cost > benefit |
| Standard domain input, high confidence source | 1 (Local) | Efficient lightweight comparison |
| Cross-domain synthesis, new framework | 1 (Local) | Build relationships incrementally |
| Contradiction detected with trusted knowledge | 2 (Deep) | Material belief impact requires depth |
| Strategic or high-consequence input | 2 (Deep) | Enable comprehensive analysis |
| Domain shift or foundational challenge | 2 (Deep) | System model update may be needed |

### Contradiction Handling

When a contradiction is detected:

1. **Classify severity**:
   - **Low**: Different interpretation of same source, negligible impact
   - **Medium**: Factual disagreement on peripheral issue
   - **High**: Contradicts core belief or affects decision-making

2. **Determine scope**:
   - **Isolated**: Affects only one or two related nodes
   - **Local**: Affects cluster of related knowledge
   - **System-wide**: Cascading impact across domains

3. **Route appropriately**:
   - Low severity + isolated scope → Log and monitor
   - Medium severity → Flag for review, update confidence
   - High severity or system-wide → Escalate to human, halt dependent reasoning

4. **Update confidence**:
   - Reduce confidence in contradicted nodes
   - Add dispute tags to affected knowledge
   - Mark as requiring follow-up research

### Confidence Scoring Rules

- **Source credibility** (0.0-1.0): Established trustworthiness of source
- **Content quality** (0.0-1.0): Technical rigor, clarity, substantiation
- **Alignment** (0.0-1.0): Consistency with related knowledge
- **Reconciliation factor** (-0.3 to 0.3): Adjustment based on reconciliation findings

**Formula**:
```
final_confidence = 
  (source_credibility × 0.3) +
  (content_quality × 0.4) +
  (alignment × 0.3) +
  reconciliation_factor
```

Confidence bounds: [0.0, 1.0]

## Integration with Operating Model

### Orchestrator Integration

The Orchestrator receives reconciliation output and decides:

- **Accept**: Integrate directly, update knowledge graph
- **Review**: Flag for human validation before integration
- **Escalate**: Route to deeper analysis or human decision-making
- **Clarify**: Request additional information or context

### Human Review Triggers

Human review is required when:

- Contradiction detected with high-confidence existing knowledge
- Reconciliation identifies system-wide implications
- Input challenges a foundational belief or framework
- Confidence delta exceeds threshold (default: ±0.2)
- Output generation depends on reconciled knowledge
- Cross-domain synthesis produces novel but uncertain conclusions

### Worker Integration

Workers (summarizers, classifiers, etc.) may request reconciliation:

- Before processing multi-domain synthesis
- When detecting contradictions in source material
- Before generating high-stakes outputs
- When model confidence drops significantly

## Implementation Checklist

- [ ] Define semantic search implementation for graph querying
- [ ] Specify relationship classification algorithm
- [ ] Formalize confidence scoring model
- [ ] Define contradiction detection rules by domain
- [ ] Implement escalation logic in Orchestrator
- [ ] Create reconciliation templates for common patterns
- [ ] Build audit trail for belief changes
- [ ] Define performance SLAs (query time, reconciliation latency)
- [ ] Create monitoring for false positives/negatives
- [ ] Establish feedback loop for model improvement

## Success Criteria

The CRE succeeds when:

- New information is compared against relevant existing knowledge within 2 seconds (local mode)
- Contradictions are surfaced with high precision (low false positives)
- Confidence updates reflect genuine relationship changes
- Human review is triggered appropriately (not too much, not too little)
- System demonstrates learning over time (confidence profiles improve)
- Outputs can reference the reasoning chain (auditability)
