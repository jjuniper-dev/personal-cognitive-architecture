# PCA Capture API

Minimal FastAPI intake service for the iPhone capture path.

## What it does

- accepts a text-only iPhone capture webhook payload
- validates the payload
- stages the capture to disk in a structured, inspectable layout
- writes a JSONL audit/index trail
- exposes capture lookup endpoints for verification

## Run locally

```bash
cd src/capture-api
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

## Webhook endpoints

- `POST /webhook/pca-ingest`
- `POST /webhook/pca-capture`

Example payload:

```json
{
  "source": "iphone",
  "capture_type": "text",
  "timestamp": "2026-06-20T12:34:56Z",
  "text": "Need to send Chad the revised PATH/HAIL framing",
  "context_note": "PATH-HAIL project",
  "location": "office",
  "tags": ["work", "follow-up"]
}
```

## Storage layout

- `data/capture-staging/captures.jsonl`
- `data/capture-staging/audit.jsonl`
- `data/capture-staging/YYYY/MM/DD/<capture_id>/capture.json`
- `data/capture-staging/YYYY/MM/DD/<capture_id>/capture.md`

## Health

- `GET /health`

## Capture lookup

- `GET /captures/{capture_id}`
- `GET /captures/latest`
