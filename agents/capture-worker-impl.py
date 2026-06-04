#!/usr/bin/env python3
"""
Capture Worker Agent - Ingestion Pipeline

Handles:
- Voice/audio capture and transcription
- Article/URL extraction
- Signal/RSS feeds
- Metadata extraction
- Quality validation
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from pathlib import Path
import logging
import mimetypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PCA Capture Worker", version="1.0.0")

# Configuration
TRANSCRIPTION_PROVIDER = os.getenv("TRANSCRIPTION_PROVIDER", "local")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class CaptureInput(BaseModel):
    """Raw capture from source"""
    source_type: str  # voice, article, signal, text
    content: str  # text content or URL for articles
    metadata: Optional[Dict] = None
    domain: Optional[str] = None
    tags: List[str] = []


class ProcessedCapture(BaseModel):
    """Processed and validated capture"""
    id: str
    source_type: str
    content: str
    metadata: Dict
    quality_score: float  # 0-1
    validation_errors: List[str]
    ready_for_validation: bool


class CaptureWorker:
    """
    Ingestion worker for the PCA system.

    Responsibilities:
    - Accept captures from various sources
    - Transcribe voice/audio
    - Extract article content
    - Parse RSS feeds
    - Validate quality
    - Send to orchestrator
    """

    def __init__(self):
        self.transcription_client = self._init_transcription()
        self.article_extractor = self._init_article_extractor()

    def _init_transcription(self):
        """Initialize transcription service"""
        if TRANSCRIPTION_PROVIDER == "deepgram" and DEEPGRAM_API_KEY:
            try:
                from deepgram import Deepgram
                return Deepgram(DEEPGRAM_API_KEY)
            except:
                logger.warning("Deepgram not available")

        if TRANSCRIPTION_PROVIDER == "openai" and OPENAI_API_KEY:
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                return openai
            except:
                logger.warning("OpenAI not available")

        # Fallback: local whisper
        try:
            import whisper
            return whisper.load_model("base")
        except:
            logger.warning("No transcription service available")
            return None

    def _init_article_extractor(self):
        """Initialize article extraction service"""
        try:
            # Could use trafilatura or Mercury parser
            # For now: simple requests-based approach
            import requests
            return requests
        except:
            return None

    async def process_voice(self, audio_file: UploadFile) -> Dict:
        """
        Process voice capture.

        1. Validate audio format
        2. Transcribe
        3. Validate transcription
        """
        logger.info(f"Processing voice: {audio_file.filename}")

        try:
            # Read file
            audio_content = await audio_file.read()

            # Validate size (max 25MB)
            if len(audio_content) > 25 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="Audio file too large")

            # Transcribe based on provider
            if TRANSCRIPTION_PROVIDER == "deepgram" and self.transcription_client:
                transcript = await self._transcribe_deepgram(audio_content)
            elif TRANSCRIPTION_PROVIDER == "openai" and self.transcription_client:
                transcript = await self._transcribe_openai(audio_content, audio_file.filename)
            else:
                transcript = await self._transcribe_local(audio_content)

            if not transcript or transcript.get("success") is False:
                raise HTTPException(status_code=500, detail="Transcription failed")

            return {
                "source_type": "voice",
                "content": transcript["text"],
                "metadata": {
                    "original_filename": audio_file.filename,
                    "duration_seconds": transcript.get("duration", 0),
                    "confidence": transcript.get("confidence", 0.85),
                    "language": transcript.get("language", "en")
                }
            }

        except Exception as e:
            logger.error(f"Voice processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")

    async def _transcribe_deepgram(self, audio_content: bytes) -> Dict:
        """Transcribe using Deepgram API"""
        import asyncio

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.transcription_client.transcription.prerecorded(
                    audio_content,
                    {"model": "nova-2", "language": "en"}
                )
            )

            result = response["results"]["channels"][0]["alternatives"][0]
            return {
                "success": True,
                "text": result["transcript"],
                "confidence": result.get("confidence", 0.9),
                "duration": response["metadata"].get("duration", 0)
            }
        except Exception as e:
            logger.error(f"Deepgram error: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _transcribe_openai(self, audio_content: bytes, filename: str) -> Dict:
        """Transcribe using OpenAI Whisper API (v1)"""
        try:
            import io
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)
            audio_file = io.BytesIO(audio_content)
            audio_file.name = filename

            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

            return {
                "success": True,
                "text": response.text,
                "confidence": 0.95
            }
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _transcribe_local(self, audio_content: bytes) -> Dict:
        """Transcribe using local Whisper model"""
        try:
            import tempfile
            import os

            # Write to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_content)
                tmp_path = tmp.name

            try:
                # Transcribe
                result = self.transcription_client.transcribe(tmp_path, language="en")

                return {
                    "success": True,
                    "text": result["text"],
                    "confidence": 0.85
                }
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Local transcription error: {str(e)}")
            return {"success": False, "error": str(e)}

    async def process_article(self, url: str) -> Dict:
        """
        Process article/URL capture.

        1. Fetch URL
        2. Extract content (title, body, metadata)
        3. Validate quality
        """
        logger.info(f"Processing article: {url}")

        try:
            # Validate URL
            if not url.startswith(("http://", "https://")):
                raise HTTPException(status_code=400, detail="Invalid URL")

            # Fetch and extract
            import requests
            from html.parser import HTMLParser

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Simple content extraction (in production: use trafilatura)
            title = self._extract_title(response.text)
            content = self._extract_content(response.text)

            if not content or len(content) < 50:
                raise HTTPException(status_code=400, detail="No substantial content found")

            return {
                "source_type": "article",
                "content": content,
                "metadata": {
                    "url": url,
                    "title": title,
                    "word_count": len(content.split()),
                    "fetched_at": datetime.now().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Article processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Article processing failed: {str(e)}")

    def _extract_title(self, html: str) -> str:
        """Extract title from HTML"""
        import re

        match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        match = re.search(r"<h1[^>]*>([^<]+)</h1>", html, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return "Untitled"

    def _extract_content(self, html: str) -> str:
        """Extract main content from HTML (simplified)"""
        import re

        # Remove scripts and styles
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.IGNORECASE | re.DOTALL)

        # Extract from common content containers
        for selector in ["<article[^>]*>", "<main[^>]*>", "<div class=\"content\""]:
            match = re.search(selector + r"(.*?)</(?:article|main|div)>", html, re.IGNORECASE | re.DOTALL)
            if match:
                html = match.group(1)
                break

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    async def process_signal(self, feed_url: str) -> Dict:
        """Process signal/RSS feed entry"""
        logger.info(f"Processing signal: {feed_url}")

        try:
            import feedparser

            feed = feedparser.parse(feed_url)

            if not feed.entries:
                raise HTTPException(status_code=400, detail="No entries in feed")

            # Get latest entry
            entry = feed.entries[0]

            return {
                "source_type": "signal",
                "content": entry.get("summary", entry.get("description", "")),
                "metadata": {
                    "url": feed_url,
                    "feed_title": feed.feed.get("title", ""),
                    "entry_title": entry.get("title", ""),
                    "published": entry.get("published", datetime.now().isoformat()),
                    "is_signal": True
                }
            }

        except Exception as e:
            logger.error(f"Signal processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Signal processing failed: {str(e)}")

    def validate_capture(self, processed: Dict) -> ProcessedCapture:
        """Validate processed capture quality"""
        errors = []
        quality_score = 1.0

        # Content length check
        content_length = len(processed.get("content", ""))
        if content_length < 20:
            errors.append("Content too short (minimum 20 characters)")
            quality_score -= 0.3
        elif content_length > 100000:
            errors.append("Content too long (maximum 100000 characters)")
            quality_score -= 0.2

        # Metadata validation
        metadata = processed.get("metadata", {})
        has_timestamp = any(k in metadata for k in ["fetched_at", "original_filename", "captured_at", "published"])
        if not has_timestamp:
            errors.append("Missing timestamp")
            quality_score -= 0.1

        # Language/encoding check (simplified)
        try:
            processed.get("content", "").encode("utf-8")
        except:
            errors.append("Invalid encoding")
            quality_score -= 0.5

        return ProcessedCapture(
            id=f"capture-{datetime.now().timestamp()}",
            source_type=processed.get("source_type", "text"),
            content=processed.get("content", ""),
            metadata=metadata,
            quality_score=max(0.0, min(1.0, quality_score)),
            validation_errors=errors,
            ready_for_validation=len(errors) == 0 and quality_score >= 0.7
        )


# Initialize worker
worker = CaptureWorker()


@app.post("/capture/voice")
async def capture_voice(file: UploadFile = File(...)) -> Dict:
    """Capture and transcribe voice"""
    processed = await worker.process_voice(file)
    validated = worker.validate_capture(processed)
    return validated.dict()


@app.post("/capture/article")
async def capture_article(url: str) -> Dict:
    """Capture article from URL"""
    processed = await worker.process_article(url)
    validated = worker.validate_capture(processed)
    return validated.dict()


@app.post("/capture/signal")
async def capture_signal(feed_url: str) -> Dict:
    """Capture from signal/RSS feed"""
    processed = await worker.process_signal(feed_url)
    validated = worker.validate_capture(processed)
    return validated.dict()


@app.post("/capture/text")
async def capture_text(request: CaptureInput) -> Dict:
    """Capture text directly"""
    processed = {
        "source_type": "text",
        "content": request.content,
        "metadata": {
            "domain": request.domain,
            "tags": request.tags,
            "captured_at": datetime.now().isoformat()
        }
    }
    validated = worker.validate_capture(processed)
    return validated.dict()


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "role": "capture-worker",
        "transcription_provider": TRANSCRIPTION_PROVIDER,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("CAPTURE_WORKER_PORT", 8002))
    host = os.getenv("CAPTURE_WORKER_HOST", "127.0.0.1")

    logger.info(f"Starting PCA Capture Worker on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
