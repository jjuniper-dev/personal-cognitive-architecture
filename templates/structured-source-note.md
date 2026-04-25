---
type: source
source_type: article
capture_id: {{CAPTURE_ID}}
validation_id: {{VALIDATION_ID}}
captured_at: {{TIMESTAMP}}
title: {{TITLE}}
author: {{AUTHOR}}
publication_date: {{PUBLICATION_DATE}}
domain: {{DOMAIN}}
url: {{URL}}
status: {{STATUS}}
confidence_score: {{CONFIDENCE_SCORE}}
routing_action: {{ROUTING_ACTION}}
destination_folder: {{DESTINATION}}
tags:
  - {{DOMAIN}}
  - {{PROJECT}}
  - reference
projects:
  - {{PROJECT}}
processing_state: integrated
---

# {{TITLE}}

**Author**: {{AUTHOR}}
**Published**: {{PUBLICATION_DATE}}
**Source**: [{{DOMAIN}}]({{URL}})
**Captured**: {{TIMESTAMP}}

---

## Summary

{{AI_SUMMARY}}

---

## Key Points

- {{KEY_POINT_1}}
- {{KEY_POINT_2}}
- {{KEY_POINT_3}}

---

## Full Content

### Introduction

{{INTRODUCTION_SECTION}}

### Body

{{BODY_SECTION}}

### Conclusion

{{CONCLUSION_SECTION}}

---

## Key Concepts

{{#CONCEPTS}}
- **{{CONCEPT_NAME}}**: {{CONCEPT_DEFINITION}}
{{/CONCEPTS}}

---

## Named Entities

### People
{{#PEOPLE}}
- {{PERSON_NAME}}
{{/PEOPLE}}

### Organizations
{{#ORGANIZATIONS}}
- {{ORG_NAME}}
{{/ORGANIZATIONS}}

### Topics / Themes
{{#TOPICS}}
- {{TOPIC}}
{{/TOPICS}}

---

## Relationships

### Related Notes
{{#RELATED_NOTES}}
- [[{{RELATED_NOTE_TITLE}}]] ({{RELATIONSHIP_TYPE}})
{{/RELATED_NOTES}}

### Projects
{{#PROJECT_LINKS}}
- [[{{PROJECT_NAME}}]]
{{/PROJECT_LINKS}}

---

## Source Credibility Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Publication Tier | {{CREDIBILITY_TIER}} | {{CREDIBILITY_NOTES}} |
| Author Expertise | {{AUTHOR_EXPERTISE}} | {{AUTHOR_NOTES}} |
| Domain Authority | {{DOMAIN_AUTHORITY}} | {{DOMAIN_NOTES}} |
| Recency | {{RECENCY}} | Published {{DAYS_AGO}} days ago |

**Overall Credibility**: {{CREDIBILITY_SCORE}}/1.0

---

## Personal Notes

### Why I Captured This
{{WHY_CAPTURED}}

### How This Applies
{{APPLICATION}}

### Action Items (if any)
- [ ] {{ACTION_1}}
- [ ] {{ACTION_2}}

---

## Processing Metadata

| Field | Value |
|-------|-------|
| Confidence Score | {{CONFIDENCE_SCORE}} |
| Routing Action | {{ROUTING_ACTION}} |
| State | {{STATUS}} |
| Requires Review | {{REQUIRES_REVIEW}} |
| Models Used | {{MODELS_USED}} |
| Processing Time | {{PROCESSING_TIME}} |

---

**Status**: {{STATUS}}
**Last Review**: {{LAST_REVIEW_DATE}}
**Next Action**: {{NEXT_ACTION}}
