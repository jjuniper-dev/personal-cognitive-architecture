---
type: agent-specification
role: worker
created: 2026-04-25
status: active
---

# Capture Worker Specification

## Identity

**Name**: Capture Worker  
**Role**: Ingestion and extraction  
**Responsibilities**: Receive captures, normalize content, extract metadata, produce validated candidates  
**Authority**: Low (executes only, no routing decisions)  
**Scope**: Stage 1-2 of pipeline (Capture → Normalize)  

## Purpose

The Capture Worker handles the **intake and preparation** of raw captures. It:

1. **Receives** — accepts multimodal inputs (voice, text, articles, PDFs)
2. **Transcribes** — speech-to-text if needed
3. **Extracts** — text from PDFs, metadata from sources
4. **Normalizes** — standardizes formats, cleans content
5. **Chunks** — breaks content into processable units
6. **Enriches** — adds derived metadata (word count, language, entities)
7. **Validates** — quality checks before handoff

The Capture Worker **does not make decisions**. It prepares data and hands it off to the Validation Worker.

## Input Contract

Receives webhook from external source:

```json
{
  "source_type": "voice|article|pdf|web|email|rss|api",
  "content": "raw content",
  "metadata": {...},
  "timestamp": "ISO-8601"
}
```

See: `schemas/ingest-capture.schema.json`

## Output Contract

Produces normalized candidate:

```json
{
  "capture_id": "uuid",
  "source_type": "...",
  "normalized_text": "cleaned text",
  "metadata": {...},
  "quality_metrics": {
    "transcription_confidence": 0.94,
    "extraction_completeness": 0.95
  }
}
```

## Responsibilities

### Transcription (Voice)
- Call Whisper API or local model
- Set fallback: if API fails, use local
- Record confidence score
- Handle failure: log and continue with low confidence

### Text Extraction (PDF)
- Use PDF extraction library
- Fall back to OCR if needed
- Record extraction confidence
- Handle scanned documents

### Metadata Extraction
- Title, author, publication date, URL
- Domain authority
- Language detection
- Named entity recognition (people, organizations, topics)

### Content Normalization
- Remove duplicates formatting
- Standardize whitespace
- Handle encoding
- Clean HTML if needed

### Chunking
- Break into propositions or paragraphs (not pages)
- Preserve context (previous/next chunk references)
- Assign chunk IDs
- Maintain source location (byte ranges)

### Quality Validation
- Transcription confidence > 0.70?
- Extraction completeness > 0.60?
- Text coherence check
- Language detection successful?
- Content not empty?

## Processing Pipeline

```
Input
  ↓
[By Source Type]
  ├─ Voice → Transcribe
  ├─ PDF → Extract
  ├─ Web → Download + Extract
  └─ Article → Parse metadata
  ↓
Normalize (format standardization)
  ↓
Quality Check
  ├─ Pass → Chunk & Enrich
  └─ Fail → Flag low confidence
  ↓
Output (to Validation Worker)
```

## Error Handling

### Transcription Fails
```
→ Try fallback model
→ If both fail: Set confidence = 0.0
→ Continue to next stage (validation will handle low confidence)
```

### PDF Extraction Fails
```
→ Try OCR
→ If OCR fails: Flag as "requires-manual-review"
→ Log error, continue
```

### Language Detection Fails
```
→ Assume English
→ Flag for validation review
```

### Quality Check Fails
```
→ Flag quality metrics as problematic
→ Set low confidence scores
→ Continue (validation makes routing decision)
```

## Latency Targets

| Source Type | Target | Notes |
|-------------|--------|-------|
| Voice (10s audio) | 3-5s | Local transcription, fast |
| Article (2KB) | 1-2s | Text extraction only |
| PDF (10 pages) | 5-10s | OCR if needed |
| Web (download + parse) | 3-5s | Network dependent |

## Cost Model

| Operation | Cost | Notes |
|-----------|------|-------|
| Whisper Local | $0.00 | Phase 1/2, on-device |
| Whisper API | $0.01/min | Phase 1 fallback |
| PDF Extraction | $0.00 | Library-based |
| Named Entity Recognition | $0.00-0.05 | Depends on method |

## Monitoring

### Metrics
- Transcription success rate (should be >95%)
- Extraction completeness (average)
- Quality check pass rate (should be >85%)
- Latency p95 (target: <10s)
- Cost per 100 captures

### Alerts
- Transcription failing on 5+ consecutive attempts
- Extraction latency exceeds 15s
- Quality check fail rate > 20%
- Cascade failures (extraction → quality check → fail)

## Non-Negotiable Principles

1. **No data loss** — preserve all input even if quality is low
2. **Quality is explicit** — confidence scores record uncertainty
3. **Errors are logged** — no silent failures
4. **Normalization is reversible** — can reconstruct original
5. **Metadata is preserved** — keep all source context

---

**Status**: Active specification (v1.0)
**Last Updated**: 2026-04-25
**Related**: pca-orchestrator.md, validation-worker.md
