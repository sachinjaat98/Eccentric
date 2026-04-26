# Architecture

System design and architecture overview for Eccentric.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Module Structure](#module-structure)
4. [Data Flow](#data-flow)
5. [Components](#components)
6. [Design Patterns](#design-patterns)
7. [Performance Considerations](#performance-considerations)

---

## System Overview

Eccentric is a modular text recognition and translation system with three main components:

1. **OCR Module** - Detects and extracts text from images
2. **Translation Module** - Translates text to multiple languages
3. **TTS Module** - Converts text to speech

Each module is independent and can be used separately or combined in a pipeline.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
│              (Flask REST API - routes.py)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   OCR Flow   │  │ Translation  │  │    TTS Flow   │      │
│  │              │  │    Flow      │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
├─────────┼─────────────────┼─────────────────┼──────────────┤
│         │                 │                 │              │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌──────▼────────┐     │
│  │ OCR Engine  │  │Translation   │  │  TTS Engine   │     │
│  │             │  │  Engine      │  │               │     │
│  │ - EAST      │  │              │  │ - gTTS        │     │
│  │ - Tesseract │  │ - googletrans│  │ - Language    │     │
│  │             │  │ - Cache      │  │   Support     │     │
│  └──────┬──────┘  └──────┬───────┘  └──────┬────────┘     │
│         │                 │                 │              │
├─────────┼─────────────────┼─────────────────┼──────────────┤
│         │                 │                 │              │
│  ┌──────▼──────────────────▼──────────────────▼────────┐  │
│  │           Utilities Layer                          │  │
│  │  ImageUtils │ TextUtils │ FileUtils │ LogUtils   │  │
│  └───────────────────────────────────────────────────┘  │
│         │                 │                              │
├─────────┼─────────────────┼──────────────────────────────┤
│         │                 │                              │
│  ┌──────▼──────────────────▼───────────────────────────┐ │
│  │        External Services & APIs                     │ │
│  │                                                     │ │
│  │  AWS S3 │ Google APIs │ Local Storage │ Database   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Structure

### Directory Organization

```
src/
├── __init__.py
├── app.py                      # Application initialization
│
├── api/                        # API Layer
│   ├── __init__.py
│   ├── routes.py              # Flask routes & endpoints
│   ├── middleware.py          # Request/response processing
│   ├── errors.py              # Error handling & responses
│   └── validators.py          # Input validation
│
├── ocr/                        # OCR Module
│   ├── __init__.py
│   ├── ocr_engine.py          # Main OCR engine
│   ├── text_detector.py       # EAST text detection
│   ├── text_recognizer.py     # Tesseract OCR
│   └── utils.py               # Image processing utilities
│
├── translation/               # Translation Module
│   ├── __init__.py
│   ├── translator.py          # Main translator engine
│   ├── language_support.py    # Language configuration
│   ├── cache.py               # Translation cache
│   └── utils.py               # Translation utilities
│
├── tts/                        # Text-to-Speech Module
│   ├── __init__.py
│   ├── tts_engine.py          # Main TTS engine
│   ├── voice_provider.py      # Voice provider interface
│   └── utils.py               # Audio utilities
│
└── utils/                      # Shared Utilities
    ├── __init__.py
    ├── image_utils.py         # Image operations
    ├── text_utils.py          # Text operations
    ├── file_utils.py          # File operations
    └── validators.py          # Input validation
```

---

## Data Flow

### Complete Pipeline Flow

```
User Input (Image)
       │
       ▼
┌─────────────────────────────────┐
│  1. Image Validation            │
│  - Check file format            │
│  - Verify size limits           │
│  - Check image dimensions       │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  2. Image Preprocessing         │
│  - Resize/normalize             │
│  - Rotation correction          │
│  - Contrast enhancement         │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  3. Text Detection (EAST)       │
│  - Detect text regions          │
│  - Extract bounding boxes       │
│  - Score confidence             │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  4. Text Extraction (Tesseract) │
│  - OCR on detected regions      │
│  - Extract text content         │
│  - Get confidence scores        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  5. Translation (Optional)      │
│  - Check cache first            │
│  - Translate using API          │
│  - Cache result                 │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  6. Text-to-Speech (Optional)   │
│  - Generate audio               │
│  - Add prosody/accent           │
│  - Save/stream output           │
└──────────────┬──────────────────┘
               │
               ▼
           Output
      (Text + Audio)
```

### Modular Component Interactions

```
Input Image
    │
    ├─────────────────────────────────┐
    │                                 │
    ▼                                 ▼
┌──────────────┐             ┌──────────────────┐
│  OCR Module  │────────────▶│ Raw Extracted    │
│              │             │ Text             │
└──────────────┘             └─────────┬────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │ Translation      │─────▶ Translated
                            │ Module (Optional)│      Text
                            └──────────┬───────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │ TTS Module       │─────▶ Audio
                            │ (Optional)       │      Output
                            └──────────────────┘
```

---

## Components

### OCR Engine

**Responsibility:** Extract text from images

**Input:** Image file path
**Output:** Extracted text with metadata

```python
{
    "text": "Extracted text...",
    "confidence": 0.95,
    "bounding_boxes": [...],
    "language": "en",
    "processing_time": 2.5
}
```

**Key Functions:**
- `extract_text(image_path)` - Main extraction
- `detect_text_regions(image)` - EAST detection
- `recognize_text(regions)` - Tesseract OCR
- `get_confidence_scores(results)` - Confidence calculation

### Translation Engine

**Responsibility:** Translate text to target languages

**Input:** Text, target language
**Output:** Translated text

```python
{
    "original": "Hello",
    "translated": "Namaste",
    "source_lang": "en",
    "target_lang": "hi",
    "provider": "google",
    "cached": False
}
```

**Key Functions:**
- `translate(text, target_lang)` - Main translation
- `get_supported_languages()` - List languages
- `cache_translation(key, value)` - Cache management
- `validate_language_code(code)` - Language validation

### TTS Engine

**Responsibility:** Convert text to speech

**Input:** Text, language, voice settings
**Output:** Audio file/stream

```python
{
    "audio_file": "path/to/audio.mp3",
    "language": "hi",
    "duration": 5.2,
    "format": "mp3",
    "sample_rate": 22050
}
```

**Key Functions:**
- `synthesize(text, language)` - Text to speech
- `set_voice_properties(speed, pitch)` - Voice settings
- `save_audio(output_path)` - Save output
- `stream_audio()` - Real-time streaming

---

## Design Patterns

### 1. Module Pattern

Each module (OCR, Translation, TTS) is independent:

```python
# OCR Module
from src.ocr.ocr_engine import OCREngine
ocr = OCREngine()
text = ocr.extract_text(image_path)

# Translation Module
from src.translation.translator import TranslationEngine
translator = TranslationEngine()
translated = translator.translate(text, 'es')

# TTS Module
from src.tts.tts_engine import TextToSpeechEngine
tts = TextToSpeechEngine()
audio = tts.synthesize(translated, 'es')
```

### 2. Pipeline Pattern

Compose modules into a complete pipeline:

```python
class Pipeline:
    def __init__(self, ocr, translator, tts):
        self.ocr = ocr
        self.translator = translator
        self.tts = tts
    
    def process(self, image_path, target_lang):
        # Extract text
        text = self.ocr.extract_text(image_path)
        
        # Translate
        translated = self.translator.translate(text, target_lang)
        
        # Synthesize speech
        audio = self.tts.synthesize(translated, target_lang)
        
        return {
            'original_text': text,
            'translated_text': translated,
            'audio_file': audio
        }
```

### 3. Dependency Injection

Inject dependencies into components:

```python
class OCREngine:
    def __init__(self, image_processor, detector, recognizer):
        self.image_processor = image_processor
        self.detector = detector
        self.recognizer = recognizer
```

### 4. Caching Pattern

Cache expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def translate_cached(text, target_lang):
    return translate_api(text, target_lang)
```

---

## Performance Considerations

### Image Processing

```
┌─────────────────────────────────────────┐
│  Image Size                             │
├─────────────────────────────────────────┤
│  Small (< 512x512)      → Fast (< 1s)  │
│  Medium (512x1024)      → Good (1-3s)  │
│  Large (> 1024x1024)    → Slow (3-5s)  │
│  Very Large (> 4096px)  → Resize first │
└─────────────────────────────────────────┘
```

### Optimization Strategies

1. **Image Resizing**
   - Resize large images before processing
   - Target: 320x320 for speed, 640x640 for accuracy

2. **Batch Processing**
   - Process multiple images in parallel
   - Use multi-threading for I/O-bound operations
   - Use multi-processing for CPU-bound operations

3. **Caching**
   - Cache translations (100+ language pairs)
   - Cache model weights in memory
   - Use Redis for distributed caching

4. **GPU Acceleration**
   - Use GPU for image processing if available
   - CUDA support for NVIDIA GPUs
   - OpenCL support for AMD GPUs

### Memory Management

```python
# Monitor memory usage
import psutil
process = psutil.Process()
memory_info = process.memory_info()
print(f"Memory: {memory_info.rss / 1024 / 1024:.2f} MB")

# Clear cache when needed
import gc
gc.collect()
```

### Concurrency

```
┌──────────────────────────────────┐
│  Request Handling                │
├──────────────────────────────────┤
│  Flask (threaded)  → Good        │
│  Gunicorn (4 workers) → Better   │
│  Nginx + Gunicorn  → Best        │
│  Docker (scaled)   → Production  │
└──────────────────────────────────┘
```

---

## Error Handling & Recovery

### Error Categories

```
OCR Errors
├── Invalid image format
├── Corrupted image data
├── Text not detected
└── Tesseract failure

Translation Errors
├── Unsupported language
├── API rate limit exceeded
├── Network timeout
└── Invalid text input

TTS Errors
├── Unsupported language
├── Audio generation failure
├── Invalid audio format
└── Storage issues
```

### Recovery Strategy

```python
try:
    result = process_image(image)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    return {"error": "Invalid input", "details": str(e)}
except TimeoutError as e:
    logger.warning(f"Timeout: {e}, retrying...")
    return retry_with_exponential_backoff()
except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    return {"error": "Internal server error"}
```

---

## Scaling Considerations

### Vertical Scaling (Single Machine)

- Increase CPU cores for parallel processing
- Increase RAM for model caching
- Use SSD for faster I/O

### Horizontal Scaling (Multiple Machines)

- Load balancer (nginx)
- API server replicas
- Shared cache (Redis)
- Database for persistence

### Cloud Deployment

- AWS EC2 / ECS / Lambda
- Google Cloud Run / Compute Engine
- Azure App Service / Functions
- Kubernetes for orchestration

---

**Last Updated:** 2026-04-26
