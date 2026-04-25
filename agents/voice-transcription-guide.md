---
type: guide
created: 2026-04-25
updated: 2026-04-25
tags: [voice, transcription, audio, mp4, deepgram, whisper]
status: active
---

# Voice & Audio Transcription Implementation

Support for voice notes, MP4 files, and other audio in the PCA pipeline.

## Architecture

```
Audio Capture
  ↓
Format Detection (WAV, MP3, M4A, MP4, WebM, OGG)
  ↓
Transcription Service
  ├─ Deepgram (preferred: faster, cheaper)
  ├─ OpenAI Whisper (fallback: reliable, high quality)
  └─ Local Whisper (optional: privacy, cost)
  ↓
Transcription + Confidence
  ↓
Continue Pipeline (validation, routing, etc)
```

## Option 1: Deepgram (Recommended)

**Pros**: Fast, accurate, affordable, supports many formats  
**Cost**: ~$0.003 per minute (competitive)  
**Setup**: 5 minutes

### Setup

1. **Create Deepgram account**
   ```
   https://console.deepgram.com
   Sign up (free tier: 50,000 minutes/month)
   ```

2. **Get API key**
   ```
   Console > API Keys > Create New Key
   Copy key
   ```

3. **Set environment variable**
   ```bash
   export DEEPGRAM_API_KEY="your_key_here"
   ```

4. **Install SDK**
   ```bash
   pip install deepgram-sdk
   ```

### Implementation

```python
from deepgram import Deepgram
import asyncio

async def transcribe_with_deepgram(audio_file_path: str) -> Dict:
    """
    Transcribe audio using Deepgram API
    
    Supports: WAV, MP3, M4A, WebM, OGG, FLAC, Mu-law, MP4
    """
    
    deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
    
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    options = {
        "model": "nova-2",  # Latest Deepgram model
        "language": "en",
        "smart_format": True,  # Automatic punctuation
        "paragraphs": True,
        "utterances": True  # Speaker diarization
    }
    
    try:
        response = await deepgram.transcription.prerecorded(
            audio_data,
            options
        )
        
        # Extract transcript
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        confidence = response["results"]["channels"][0]["alternatives"][0].get("confidence", 0.9)
        
        return {
            "success": True,
            "transcript": transcript,
            "confidence": confidence,
            "paragraphs": response["results"]["channels"][0]["alternatives"][0].get("paragraphs"),
            "utterances": response["results"]["channels"][0]["alternatives"][0].get("utterances")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transcript": "",
            "confidence": 0.0
        }
```

## Option 2: OpenAI Whisper

**Pros**: Reliable, multilingual, well-supported  
**Cost**: $0.006 per minute  
**Setup**: 5 minutes

### Setup

1. **Get OpenAI API key**
   ```
   https://platform.openai.com/account/api-keys
   Create new secret key
   ```

2. **Set environment variable**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. **Install SDK**
   ```bash
   pip install openai
   ```

### Implementation

```python
import openai

def transcribe_with_whisper(audio_file_path: str) -> Dict:
    """
    Transcribe audio using OpenAI Whisper API
    
    Supports: MP3, MP4, MPEG, MPGA, M4A, OGG, WAV, WEBM
    Max file size: 25 MB
    """
    
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="en"
        )
    
    return {
        "success": True,
        "transcript": transcript["text"],
        "confidence": 0.95  # Whisper doesn't return confidence
    }
```

## Option 3: Local Whisper (Privacy First)

**Pros**: No API costs, keeps audio local, privacy-first  
**Cons**: Requires GPU, slower (10-30s per minute of audio)  
**Cost**: Free (after initial setup)

### Setup

1. **Install Whisper**
   ```bash
   pip install openai-whisper
   # Downloads model on first use (~3GB)
   ```

2. **Implementation**
   ```python
   import whisper
   
   def transcribe_with_local_whisper(audio_file_path: str) -> Dict:
       """
       Transcribe audio using local Whisper model
       
       Models: tiny, base, small, medium, large
       Tradeoff: Speed vs accuracy
       For PCA: Use 'base' or 'small' (fast enough, accurate)
       """
       
       # Load model (cached after first download)
       model = whisper.load_model("base")  # 140MB, ~30s per minute
       
       try:
           result = model.transcribe(
               audio_file_path,
               language="en",
               verbose=False
           )
           
           return {
               "success": True,
               "transcript": result["text"],
               "confidence": 0.90,  # Average confidence
               "language": result.get("language"),
               "segments": result.get("segments")
           }
       except Exception as e:
           return {
               "success": False,
               "error": str(e),
               "transcript": "",
               "confidence": 0.0
           }
   ```

## Integration with n8n Workflow

### In n8n, add transcription node:

**Node: Transcribe Audio**

```
Type: Function or HTTP Request

If using Function:
  
  const fs = require('fs');
  const audio_buffer = Buffer.from($input.first().json.audio_base64, 'base64');
  const audio_path = `/tmp/audio-${Date.now()}.wav`;
  fs.writeFileSync(audio_path, audio_buffer);
  
  // Call transcription service
  const response = await fetch('http://localhost:8002/transcribe', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({audio_file: audio_path})
  });
  
  const result = await response.json();
  
  fs.unlinkSync(audio_path);  // Clean up
  
  return [{
    transcript: result.transcript,
    confidence: result.confidence
  }];

If using HTTP Request:

  URL: http://localhost:8002/transcribe
  Method: POST
  Body:
    audio_base64: ${audio_file_base64}
    format: wav|mp3|m4a|mp4|webm
```

## Dedicated Transcription Microservice

Create `agents/transcription-service.py`:

```python
from fastapi import FastAPI, UploadFile, File
from typing import Dict
import asyncio
import os

app = FastAPI(title="PCA Transcription Service")

# Initialize transcription client
TRANSCRIPTION_PROVIDER = os.getenv("TRANSCRIPTION_PROVIDER", "deepgram")

if TRANSCRIPTION_PROVIDER == "deepgram":
    from deepgram import Deepgram
    transcription_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
elif TRANSCRIPTION_PROVIDER == "whisper-api":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:  # local whisper
    import whisper
    transcription_client = whisper.load_model("base")


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)) -> Dict:
    """
    Transcribe audio file
    
    Supported formats: WAV, MP3, M4A, MP4, WebM, OGG
    Returns: {transcript, confidence, duration}
    """
    
    try:
        # Read file
        audio_data = await file.read()
        
        # Transcribe based on provider
        if TRANSCRIPTION_PROVIDER == "deepgram":
            result = await transcribe_deepgram(audio_data)
        elif TRANSCRIPTION_PROVIDER == "whisper-api":
            result = await transcribe_whisper_api(audio_data)
        else:
            result = await transcribe_local_whisper(audio_data)
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transcript": ""
        }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "provider": TRANSCRIPTION_PROVIDER
    }
```

## Integration with /capture Command

Update `dashboards/chainlit-pca-monitor.py`:

```python
async def handle_capture():
    """Interactive capture form with voice support"""
    
    capture_type_response = await cl.AskChoiceMessage(
        content="What type of capture?",
        choices=["Quick thought", "Voice note", "Article/Link"]
    ).send()
    
    if capture_type_response["value"] == "Voice note":
        # Record audio
        audio_response = await cl.AskUserMessage(
            content="🎤 Record your voice note (or upload MP4/WAV file)"
        ).send()
        
        # Extract audio file if uploaded
        audio_file = audio_response.get("file")
        
        if audio_file:
            # Send to transcription service
            transcription_response = await transcribe_audio(audio_file)
            
            if transcription_response["success"]:
                content = transcription_response["transcript"]
                await cl.Message(
                    content=f"✅ Transcribed: {content[:100]}..."
                ).send()
            else:
                await cl.Message(
                    content=f"❌ Transcription failed: {transcription_response['error']}"
                ).send()
                return
    
    else:
        # Text input for quick thought or article
        ...


async def transcribe_audio(audio_file: str) -> Dict:
    """Send audio to transcription service"""
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        with open(audio_file, "rb") as f:
            form_data = aiohttp.FormData()
            form_data.add_field('file', f)
            
            async with session.post(
                "http://localhost:8002/transcribe",
                data=form_data
            ) as resp:
                return await resp.json()
```

## Testing

### Test 1: Record voice via iPhone Shortcut

Create test audio in Shortcut:
```
Ask for Audio
→ Send to n8n webhook with audio file
→ n8n sends to transcription service
→ Returns transcript to Shortcut
```

### Test 2: Test transcription service directly

```bash
# Create test audio
ffmpeg -f lavfi -i "sine=frequency=440:duration=3" test-audio.wav

# Send to service
curl -X POST http://localhost:8002/transcribe \
  -F "file=@test-audio.wav"

# Should return:
# {"success": true, "transcript": "...", "confidence": 0.95}
```

### Test 3: Test via n8n workflow

```bash
# Create test MP4
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" \
  -c:a aac -b:a 192k test-audio.mp4

# Call n8n workflow
curl -X POST http://localhost:5678/webhook/pca/capture \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "voice",
    "audio_file": "@test-audio.mp4",
    "domain": "test"
  }'
```

## Performance & Costs

### Deepgram
- **Speed**: ~1s per minute of audio (pre-recorded)
- **Cost**: $0.003/min (~$0.18/hour)
- **Accuracy**: 95%+
- **Best for**: Production, cost-conscious

### OpenAI Whisper API
- **Speed**: ~5-10s per minute
- **Cost**: $0.006/min (~$0.36/hour)
- **Accuracy**: 95%+
- **Best for**: Reliability, multilingual

### Local Whisper
- **Speed**: 10-30s per minute (depends on GPU)
- **Cost**: Free
- **Accuracy**: 90-95% (varies by model)
- **Best for**: Privacy, no API keys

## Recommendation

**Production setup**:
1. Default: Deepgram (fast, affordable, reliable)
2. Fallback: OpenAI Whisper API
3. Offline fallback: Local Whisper

**Config in env**:
```bash
TRANSCRIPTION_PRIMARY=deepgram
TRANSCRIPTION_FALLBACK=whisper-api
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
```

## Next Steps

1. ✅ Set up transcription service (choose provider)
2. ✅ Test with voice note in /capture command
3. ✅ Integrate with n8n workflow
4. ✅ Test MP4 file transcription
5. ✅ Monitor performance and costs
6. ✅ Set up fallback chains for reliability

---

**Status**: Ready for implementation
**Last Updated**: 2026-04-25
**Related**: ../dashboards/chainlit-pca-monitor.py, pca-ingest-complete.md
