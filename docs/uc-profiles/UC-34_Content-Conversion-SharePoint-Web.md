# UC-34 · Content Conversion for SharePoint / Web
**Cluster:** Knowledge Publishing  
**Status:** 🔴 Not Started  
**Layer:** L3 Workflow & Integration

---

## Purpose
Convert content between formats for publication — Obsidian Markdown → SharePoint-compatible HTML, Word docs → structured web content, raw notes → polished briefs. Serves the HC/PHAC knowledge-sharing workflow and reduces friction in publishing EA deliverables to internal platforms.

---

## Trigger
| Type | Source |
|------|--------|
| Manual | User submits Obsidian note or file path to Ayla |
| Webhook | n8n receives file + target format + destination |
| Schedule | Batch conversion of flagged notes (tagged `#publish`) |

---

## Agent Flow

```
[Input — file / note / content]
    │
    ▼
[Format Detector — Code node]
  • Identify source: Markdown / DOCX / PPTX / plain text
  • Identify target: SharePoint HTML / web HTML / Word / PDF / clean Markdown
    │
    ▼
[Content Cleaner — Haiku T=0.3]
  • Strip Obsidian-specific syntax (wikilinks, callouts, frontmatter)
  • Normalise headings, lists, tables
  • Flag embedded images for separate handling
    │
    ▼
[Conversion Engine — n8n]
  ├──▶ Markdown → HTML (marked.js / pandoc via Execute Command)
  ├──▶ DOCX → HTML (mammoth.js via Execute Command)
  ├──▶ Markdown → DOCX (pandoc)
  └──▶ Any → PDF (pandoc + wkhtmltopdf or WeasyPrint)
    │
    ▼
[Polish Agent — Sonnet T=0.3]
  • Apply target platform style rules
    - SharePoint: remove unsupported HTML tags, inline styles only
    - Web: semantic HTML5, accessible markup
    - Word: apply HC/PHAC template styles
  • Rewrite any Obsidian-native constructs for target audience
    │
    ▼
[Output Router]
  ├──▶ File write (converted output)
  ├──▶ SharePoint upload (HTTP node → Graph API — future)
  ├──▶ Obsidian: write converted version alongside source
  └──▶ GitHub Pages (for public-facing EA content)
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author conversion pipeline |
| `n8n-mcp` · `search_nodes` | Execute Command, file, HTTP nodes |
| Execute Command node | pandoc, mammoth.js, wkhtmltopdf |
| Microsoft Graph API (HTTP node) | SharePoint upload (future) |
| GitHub API (HTTP + PAT) | Publish to GitHub Pages |
| Obsidian URI / webhook | Write converted output back to vault |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive conversion requests |
| Manual trigger | One-off conversions |
| Schedule trigger | Batch #publish tag processing |
| Code node (JS) | Format detection, HTML sanitisation |
| Execute Command node | pandoc, mammoth, wkhtmltopdf |
| AI Agent node (Haiku) | Content cleaning |
| AI Agent node (Sonnet) | Platform-specific polish |
| Switch node | Source/target format routing |
| Read/Write Binary Files node | File I/O |
| HTTP Request node | SharePoint Graph API, GitHub |

---

## Claude Skills (n8n-skills)

- **Patterns** — detect → transform → polish → route (sequential with type-based branching)
- **Tools Expert** — Execute Command node for pandoc/mammoth
- **Expression Syntax** — binary file handling, MIME type detection
- **Validation Expert** — HTML output validation (SharePoint compatibility)

---

## Dependencies

| Dependency | Status |
|------------|--------|
| n8n (local Docker) | ✅ Live |
| pandoc (installed on n8n host) | 🔴 Needs install |
| mammoth.js (Node — Execute Command) | 🔴 Needs install |
| wkhtmltopdf or WeasyPrint | 🔴 Needs install |
| Microsoft Graph API access (SharePoint) | 🔴 Future — GC tenant access required |
| GitHub Pages site (`jjuniper-dev/status-site`) | ✅ Live |
| Obsidian vault write pipeline | 🟡 URI live |
| HC/PHAC Word template | 🟡 Exists — needs digitisation as python-pptx/pandoc template |

---

## Known Issues / Watch Items
- SharePoint HTML compatibility is notoriously restrictive — inline styles only, many tags stripped; the Polish Agent prompt needs to be tuned specifically for SharePoint's rendering engine
- pandoc is the right Swiss Army knife here — install on n8n Docker host early as it unblocks UC-33 and UC-34 simultaneously
- GC SharePoint (M365) upload via Graph API requires OAuth with GC tenant credentials — not feasible for personal/local setup; target is manual upload of converted file for now
- Obsidian wikilinks (`[[note-name]]`) have no universal HTML equivalent — define a conversion strategy (strip, convert to relative URL, or flag for manual review)

---

## Related UCs
- UC-32 Automated Briefing Generation (briefs as conversion source)
- UC-33 Presentation & Diagram Generation (PPTX as conversion source)
- UC-21 Agent Ecosystem Framework (framework docs as conversion source for web publish)
- UC-24 Strategic Screening (EA deliverables as conversion source)
