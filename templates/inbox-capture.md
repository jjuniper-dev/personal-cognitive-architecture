---
type: capture
source_type: {{SOURCE_TYPE}}
captured_at: {{TIMESTAMP}}
capture_id: {{CAPTURE_ID}}
status: raw
confidence: {{CONFIDENCE_INITIAL}}
domain: {{DOMAIN}}
sensitivity: {{SENSITIVITY}}
processing_state: inbox
validation_id: ~
routing_action: ~
tags: []
---

# {{TITLE}}

## Raw Capture

{{CONTENT}}

## Source Metadata

- **Source Type**: {{SOURCE_TYPE}}
- **Captured**: {{TIMESTAMP}}
- **Device/Location**: {{DEVICE_LOCATION}}
{{#if SOURCE_URL}}- **URL**: {{SOURCE_URL}}{{/if}}
{{#if AUTHOR}}- **Author**: {{AUTHOR}}{{/if}}
{{#if PUBLICATION_DATE}}- **Published**: {{PUBLICATION_DATE}}{{/if}}

## Initial Classification

### Possible Note Type
- [ ] Task (action required)
- [ ] Meeting (discussion/input)
- [ ] Idea (concept/insight)
- [ ] Reference (information to keep)
- [ ] Decision (choice/consequence)
- [ ] Question (research/clarification needed)
- [ ] Observation (personal note)

### Possible Domain
- [ ] Strategic Planning
- [ ] Product Delivery
- [ ] Research
- [ ] Operations
- [ ] Governance
- [ ] External Engagement
- [ ] Personal

### Possible Project
{{#if INFERRED_PROJECT}}- Inferred: **{{INFERRED_PROJECT}}**{{/if}}
- _Specify if different_: 

### Urgency / Priority
- [ ] Low (can wait)
- [ ] Medium (normal priority)
- [ ] High (soon)
- [ ] Urgent (immediate)

## Processing Notes

### Needs Review?
- [ ] No (appears clear)
- [ ] Yes (ambiguous or requires verification)
  - Reason: _specify_

### Next Steps
- [ ] Promote to knowledge base (decision made above)
- [ ] Link to related note (specify: _______)
- [ ] Archive (not actionable)
- [ ] Hold in inbox (awaiting context)

---

**Status**: Awaiting triage
**Last Modified**: {{TIMESTAMP}}
