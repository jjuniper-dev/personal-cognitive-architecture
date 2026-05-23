# UC-02 · Voice-to-Knowledge
**Cluster:** Personal Knowledge  
**Status:** 🔴 Not Started — blocked on iOS capture pipeline  
**Layer:** L1 Knowledge & Control / L3 Workflow & Integration

---

## Purpose
Capture voice input from iPhone (memos, dictations, ambient notes), transcribe via Whisper, extract structured knowledge, and route to Neo4j (UC-1) and Obsidian vault. Closes the capture loop for spoken thought.

---

## Trigger
| Type | Source |
|------|--------|
| iOS Shortcut | Voice memo recorded → file posted to n8n webhook |
| File drop | Audio file placed in watched folder (Mac / Tailscale path) |
| Manual | n8n manual trigger for batch reprocessing |

---

## Agent Flow

```
[Voice Input — iPhone / Mac]
    │
    ▼
[n8n Webhook / File Watcher]
  • Receive audio file (m4a / mp3 / wav)
  • Extract metadata (timestamp, source device, duration)
    │
    ▼
[Whisper Transcription]
  • Local Whisper (RTX 3090 — planned)
  • Interim: OpenAI Whisper API
  • Output: raw transcript + confidence
    │
    ▼
[Cleanup Agent — Haiku T=0.5]
  • Remove filler words, fix punctuation
  • Detect language (EN / FR)
  • Segment by topic if multi-topic memo
    │
    ▼
[Extraction Agent — Sonnet T=0.3]
  • Extract entities, actions, references
  • Generate Obsidian-formatted note (frontmatter + body)
  • Propose Neo4j nodes and relationships
    │
    ├──▶ [Obsidian Write — via URI / webhook]
    │      • /inbox/voice/ with auto-title
    │
    └──▶ [UC-01 Knowledge Graph ingest webhook]
           • Pass extracted entities + relationships
```

---

## MCP Tools

| Tool | Role |
|------|------|
| `n8n-mcp` · `create_workflow` | Author transcription + routing workflow |
| `n8n-mcp` · `search_nodes` | Find audio/file handling, HTTP nodes |
| OpenAI Whisper API (HTTP node) | Interim transcription |
| Local Whisper (HTTP node → FastAPI) | Target transcription (RTX 3090) |
| Obsidian URI / webhook | Vault write |
| UC-01 webhook | Knowledge graph ingest |

---

## n8n Skills Required

| Skill | Usage |
|-------|-------|
| Webhook trigger | Receive audio from iOS |
| Read/Write Binary Files node | Handle audio file bytes |
| HTTP Request node | Whisper API call, Obsidian write |
| Code node (JS) | Transcript cleanup, frontmatter generation |
| AI Agent node (Haiku) | Text cleanup + segmentation |
| AI Agent node (Sonnet) | Entity extraction |
| Switch node | Route by language / topic count |
| Move Binary Data node | Prep file for API upload |

---

## Claude Skills (n8n-skills)

- **Patterns** — sequential pipeline (no orchestrator needed, linear flow)
- **Expression Syntax** — binary data handling (`$binary`, `$json`)
- **Validation Expert** — audio node config, multipart form upload

---

## Dependencies

| Dependency | Status |
|------------|--------|
| iOS Shortcut → n8n webhook | 🔴 Gating — not yet built |
| n8n (local Docker) | ✅ Live |
| Whisper API (OpenAI) | ✅ Available (interim) |
| Local Whisper / RTX 3090 | 🔴 Hardware not yet acquired (~$800 CAD) |
| Obsidian vault + write pipeline | 🟡 URI scheme live, webhook planned |
| UC-01 ingest webhook | 🟡 Planned |
| Tailscale mesh (file path access) | ✅ Live |

---

## Known Issues / Watch Items
- Binary file handling in n8n can be finicky — validate multipart upload node config before deploying
- Local Whisper (RTX 3090) is the target to avoid OpenAI data residency; keep interim API usage for non-sensitive content only
- Multi-topic segmentation heuristic needs prompt tuning — Haiku at T=0.5 may need T=0.3 for consistency

---

## Related UCs
- UC-01 Knowledge Graph (primary downstream consumer)
- UC-03 Life Memory Archive (voice notes as memory input)
- UC-06 Ayla Assistant (may trigger voice capture via conversational command)
