# UC-33 · Presentation & Diagram Generation
**Cluster:** Knowledge Publishing  
**Status:** 🔴 Not Started  
**Layer:** L2 Agent Runtime / L3 Workflow & Integration

---

## Purpose
Generate professional presentations (PPTX) and architecture diagrams (Mermaid, draw.io, PlantUML) from structured inputs — briefs, Obsidian notes, or natural language prompts. Serves both the HC/PHAC EA practice (ARB decks, capability maps) and the personal Ayla ecosystem (architecture documentation, UC-21 framework visuals).

---

## Trigger
| Type | Source |
|------|--------|
| Manual | User submits brief or Obsidian note to Ayla |
| Webhook | n8n receives structured payload (title, sections, diagram spec) |
| Template-driven | User selects a presentation template + content source |

---

## Agent Flow

```
[Input — brief / note / prompt]
    │
    ▼
[Content Structurer — Sonnet T=0.3]
  • Parse input into slide structure or diagram spec
  • Identify output type: PPTX / Mermaid / draw.io / PlantUML
  • Apply design system rules:
    - HC/PHAC: Arial, teal/green palette, 16:9, cross-cutting governance bands
    - Personal: IBM Plex, dark teal (status-site design system)
    │
    ▼
[Content Router — Switch]
    │
    ├──▶ [PPTX Generation]
    │      • python-pptx (new decks only — not editing existing)
    │      • claude.ai/design for modifying existing decks
    │      • Apply HC/PHAC PowerPoint Design System
    │      • Output: .pptx file
    │
    ├──▶ [Mermaid Diagram]
    │      • Generate Mermaid DSL from spec
    │      • Validate syntax
    │      • Output: .mermaid + rendered PNG via Mermaid CLI
    │
    └──▶ [Architecture Diagram — draw.io / PlantUML]
           • Generate XML (draw.io) or PlantUML DSL
           • Output: source file + export
    │
    ▼
[Review Agent — Haiku T=0.8]
  • Check slide count vs. content density
  • Validate diagram correctness (node/edge consistency)
  • Flag design system violations
    │
    ▼
[Output]
  ├──▶ File write to outputs dir
  ├──▶ Obsidian attachment (for personal use)
  └──▶ SharePoint / OneDrive upload (for HC/PHAC use — future)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author generation pipeline |
| `n8n-mcp` · `search_nodes` | Execute Command, HTTP, file nodes |
| Execute Command node (n8n) | Run python-pptx scripts, Mermaid CLI |
| HTTP Request node | claude.ai/design API (if available) |
| Obsidian URI / webhook | Attach output to vault note |
| GitHub API (HTTP + PAT) | Publish diagrams to repo docs |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive generation requests |
| AI Agent node (Sonnet) | Content structuring |
| AI Agent node (Haiku) | Review and validation |
| Execute Command node | python-pptx, Mermaid CLI |
| Switch node | Output type routing |
| Read/Write Binary Files node | Handle .pptx, .png output files |
| HTTP Request node | External APIs, file delivery |
| Code node (JS) | Slide spec assembly, diagram DSL construction |

---

## Claude Skills (n8n-skills)

- **Patterns** — transform-and-route (content in → structured output by type)
- **Tools Expert** — Execute Command node for CLI tools
- **Validation Expert** — Mermaid syntax validation, PPTX structure check
- **Expression Syntax** — binary file handling for PPTX output

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| python-pptx (installed on n8n host) | 🔴 Needs install + test |
| Mermaid CLI (mmdc) | 🔴 Needs install on n8n host |
| HC/PHAC PowerPoint Design System | ✅ Defined (Arial, teal/green, 16:9) |
| Personal design system (IBM Plex / dark teal) | ✅ Defined |
| Obsidian vault write pipeline | 🟡 URI live |
| SharePoint / OneDrive integration | 🔴 Future — not planned yet |

---

## Known Issues / Watch Items
- python-pptx cannot reliably edit existing PPTX files — confirmed architectural constraint; new decks only via code; existing deck modification routes to claude.ai/design
- Mermaid CLI in Execute Command node: path/permissions in Docker same gotcha as yt-dlp (UC-05) — test early
- HC/PHAC deck generation must not use OpenAI or any non-GC-approved AI endpoint for content involving Protected B data
- Design system enforcement: build a validation step that checks font, colour, and layout compliance before output is delivered

---

## Related UCs
- UC-21 Agent Ecosystem Framework (architecture diagrams for PCA docs)
- UC-24 Strategic Screening (EA diagrams)
- UC-25 AI Capability Framework (capability map visuals)
- UC-32 Automated Briefing Generation (briefings may include generated slides)
- UC-34 Content Conversion (downstream consumer of generated content)
