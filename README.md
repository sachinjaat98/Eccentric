# Eccentric

Eccentric is a browser-based OCR, translation, and text-to-speech application. Upload an image, extract its text, translate it, and generate playable speech from one page.

## Features

- Drag-and-drop image upload with preview
- OCR with Tesseract
- Editable OCR results
- Translation, including Hindi, English, Spanish, French, German, Japanese, and Arabic
- MP3 speech generation and browser playback
- JSON API, health endpoint, input validation, upload size limits, and consistent error responses
- Docker deployment with Gunicorn and Tesseract

## Quick start

### Requirements

- Python 3.10 or newer
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and available on PATH
- Internet access for translation and speech generation

### Install and run

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python main.py --debug
~~~

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.

On Linux or macOS:

~~~bash
source .venv/bin/activate
~~~

### Install Tesseract

Ubuntu/Debian:

~~~bash
sudo apt-get install tesseract-ocr
~~~

On Windows, install Tesseract and add its installation folder (for example, C:\Program Files\Tesseract-OCR) to your system PATH.

## Using the dashboard

1. Add an image by clicking the upload area or dragging a file onto it.
2. Select **Extract text**.
3. Correct the recognized text if needed.
4. Choose a target language and select **Translate**.
5. Select **Generate speech** to create and play an MP3 file.

Supported upload formats: PNG, JPG/JPEG, WebP, BMP, and TIFF. The default upload limit is 10 MB.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | Browser dashboard |
| GET | /health | Service status and version |
| POST | /api/v1/ocr | Extract text from an uploaded image |
| POST | /api/v1/translate | Translate text |
| POST | /api/v1/speech | Generate speech audio |
| GET | /api/v1/audio/{filename} | Download or stream a generated MP3 |

### OCR

~~~bash
curl -X POST http://127.0.0.1:8000/api/v1/ocr \
  -F "image=@image0.jpg" \
  -F "language=eng"
~~~

### Translate

~~~bash
curl -X POST http://127.0.0.1:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Good morning", "source_language":"auto", "target_language":"hi"}'
~~~

### Generate speech

~~~bash
curl -X POST http://127.0.0.1:8000/api/v1/speech \
  -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते", "language":"hi"}'
~~~

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| MAX_UPLOAD_BYTES | 10485760 | Largest accepted image upload |
| UPLOAD_DIR | data/uploads | Temporary upload directory |
| AUDIO_DIR | output/audio | Generated MP3 directory |

## Production deployment

~~~bash
docker compose up --build
~~~

The service is exposed at port 8000. Generated audio and temporary data are kept in named Docker volumes.

## Development

~~~powershell
python -m pytest -q
python -m ruff check .
~~~

The automated tests cover the dashboard route, health endpoint, API validation, and audio delivery.

## Project layout

~~~text
src/eccentric/
├── web.py                 Flask routes and application factory
├── services.py            OCR, translation, and speech providers
├── config.py              Environment-backed configuration
└── templates/index.html   Browser dashboard
tests/                     API and dashboard tests
main.py                    Local development entry point
Dockerfile                 Production container image
compose.yaml               Docker Compose service
~~~

## Notes

The original college-project scripts (EastOCR.py, EastOCRvideo.py, and textDetectRecog.py) are retained as legacy reference material. New development should use the packaged application in src/eccentric/.
