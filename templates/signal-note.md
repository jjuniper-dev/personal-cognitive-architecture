---
type: signal
source_feed_id: {{SOURCE_FEED_ID}}
signal_id: {{SIGNAL_ID}}
title: {{TITLE}}
published_at: {{PUBLISHED_AT}}
ingested_at: {{TIMESTAMP}}
url: {{URL}}
status: {{STATUS}}
classification: {{CLASSIFICATION}}
overall_score: {{OVERALL_SCORE}}
tags:
  - signal
  - {{TOPIC_1}}
  - {{TOPIC_2}}
projects: []
---

# {{TITLE}}

**Source**: [{{SOURCE_FEED_NAME}}]({{SOURCE_FEED_URL}})
**Published**: {{PUBLISHED_AT}}
**Ingested**: {{TIMESTAMP}}

---

## Signal Classification

| Dimension | Score | Assessment |
|-----------|-------|-----------|
| **Relevance** | {{RELEVANCE}} | {{RELEVANCE_ASSESSMENT}} |
| **Urgency** | {{URGENCY}} | {{URGENCY_ASSESSMENT}} |
| **Novelty** | {{NOVELTY}} | {{NOVELTY_ASSESSMENT}} |
| **Credibility** | {{CREDIBILITY}} | {{CREDIBILITY_TIER}} |
| **Actionability** | {{ACTIONABILITY}} | {{ACTIONABILITY_ASSESSMENT}} |

**Overall Score**: {{OVERALL_SCORE}}/1.0 → **{{CLASSIFICATION}}**

---

## Summary

{{SUMMARY}}

---

## Details

### Key Points
- {{KEY_POINT_1}}
- {{KEY_POINT_2}}
- {{KEY_POINT_3}}

### Detected Topics
{{#DETECTED_TOPICS}}
- {{TOPIC}}
{{/DETECTED_TOPICS}}

### Named Entities
{{#DETECTED_ENTITIES}}
- **{{ENTITY_TYPE}}**: {{ENTITY_VALUE}} (confidence: {{CONFIDENCE}})
{{/DETECTED_ENTITIES}}

### Related Projects
{{#PROJECTS_MENTIONED}}
- [[{{PROJECT_NAME}}]]
{{/PROJECTS_MENTIONED}}

---

## Assessment

### Relevance Factors
{{#RELEVANCE_FACTORS}}
- {{FACTOR}}: {{WEIGHT}} → {{REASONING}}
{{/RELEVANCE_FACTORS}}

### Urgency Factors
{{#URGENCY_FACTORS}}
- {{FACTOR}}: {{WEIGHT}} → {{REASONING}}
{{/URGENCY_FACTORS}}

### Why This Classification?
{{CLASSIFICATION_REASONING}}

---

## What to Do Next

### If Keeping in Knowledge Base
- [ ] Link to related notes
- [ ] Verify project assignment
- [ ] Schedule for review

### If Escalating
- [ ] Who needs to know? {{STAKEHOLDER}}
- [ ] What action is needed? {{ACTION}}
- [ ] Timeline? {{TIMELINE}}

### If Archiving
- Reason: {{ARCHIVE_REASON}}

---

## Related Intelligence

### Similar Signals
{{#SIMILAR_SIGNALS}}
- [[{{SIGNAL_TITLE}}]] ({{RELATIONSHIP}})
{{/SIMILAR_SIGNALS}}

### Related Strategic Notes
{{#RELATED_NOTES}}
- [[{{NOTE_TITLE}}]]
{{/RELATED_NOTES}}

---

## Processing Metadata

| Field | Value |
|-------|-------|
| Signal ID | {{SIGNAL_ID}} |
| Feed ID | {{SOURCE_FEED_ID}} |
| Ingestion Time | {{TIMESTAMP}} |
| Processing Time | {{PROCESSING_TIME}}ms |
| Cost | ${{COST}} |
| Deduplication | {{DEDUP_STATUS}} |

---

**Status**: {{STATUS}}
**Classification**: {{CLASSIFICATION}}
**Last Review**: {{LAST_REVIEW_DATE}}
**Next Review**: {{NEXT_REVIEW_DATE}}
