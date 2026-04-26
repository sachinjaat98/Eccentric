# Setup Guide

Complete step-by-step setup instructions for running Eccentric.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **OS:** Ubuntu 18.04 LTS, Debian 10, or macOS 10.14+
- **CPU:** 2 GHz or faster (1.2 GHz ARM for Raspberry Pi)
- **RAM:** 2 GB (1 GB for Raspberry Pi)
- **Disk:** 2 GB free space
- **Python:** 3.7 or higher

### Recommended Requirements

- **CPU:** Quad-core processor or higher
- **RAM:** 4 GB or more
- **Disk:** 4 GB or more
- **GPU:** Optional (for faster processing)

---

## Prerequisites

### 1. Install Python 3.7+

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

### 2. Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)

### 3. Install OpenCV Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-opencv
sudo apt-get install libatlas-base-dev libjasper-dev
sudo apt-get install libtiff5 libjasper1 libqtgui4 python3-pyqt5
```

### 4. Git Installation

**Ubuntu/Debian:**
```bash
sudo apt-get install git
```

**macOS:**
```bash
brew install git
```

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sachinjaat98/Eccentric.git
cd Eccentric
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r config/requirements.txt
```

### Step 4: Download Pre-trained Models

The repository should include model files. If not, download them:

```bash
# Create models directory if it doesn't exist
mkdir -p models/dnn

# Download EAST text detection model
wget https://drive.google.com/uc?id=MODEL_ID -O models/dnn/frozen_east_text_detection.pb
```

### Step 5: Verify Installation

```bash
# Test imports
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import pytesseract; print('Tesseract:', pytesseract.get_tesseract_version())"
python3 -c "import googletrans; print('googletrans imported successfully')"
python3 -c "import gtts; print('gTTS imported successfully')"
```

---

## Configuration

### Step 1: Create Environment File

```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

### Step 2: Configure API Keys

Edit `.env` file with your credentials:

```env
# AWS Configuration (if using AWS storage)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Google APIs (optional - uses free tier by default)
GOOGLE_TRANSLATE_API_KEY=your_api_key
GOOGLE_TTS_API_KEY=your_api_key

# Application Settings
LOG_LEVEL=INFO
DEBUG=False
DEFAULT_LANGUAGE=en
TARGET_LANGUAGES=es,fr,hi,ta,te

# Raspberry Pi Configuration
CAMERA_MODULE=True
AUDIO_OUTPUT_DEVICE=speaker
```

### Step 3: Verify Configuration

```bash
# Test configuration loading
python3 -c "from config.settings import *; print('Configuration loaded successfully')"
```

---

## Running the Application

### Option 1: Run Flask API Server

```bash
# Start the API server
python main.py

# Server will start on http://localhost:5000
```

### Option 2: Run with Gunicorn (Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.api.routes:app
```

### Option 3: Run with Docker

```bash
# Build Docker image
docker build -t eccentric .

# Run container
docker run -p 5000:5000 -v $(pwd):/app eccentric
```

---

## Testing

### Run Test Suite

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_ocr.py

# Run with coverage
pytest --cov=src tests/
```

### Manual Testing

```bash
# Test API endpoints
curl http://localhost:5000/api/health

# Process image
curl -X POST http://localhost:5000/api/process-image \
  -F "image=@data/examples/sample.jpg" \
  -F "language=es"
```

---

## Directory Structure After Setup

```
Eccentric/
├── venv/                          # Virtual environment
├── logs/                          # Log files (created at runtime)
├── config/
│   ├── settings.py
│   ├── logger.py
│   └── requirements.txt
├── src/
│   ├── app.py
│   ├── api/
│   ├── ocr/
│   ├── translation/
│   ├── tts/
│   └── utils/
├── models/
│   └── dnn/                       # Pre-trained models
├── data/
│   ├── examples/                  # Sample images
│   └── coco.names
├── docs/
├── tests/
├── .env                           # Your configuration
├── main.py
└── README.md
```

---

## Raspberry Pi Specific Setup

### 1. Update System

```bash
sudo apt-get update
sudo apt-get upgrade
```

### 2. Install Camera Support

```bash
sudo apt-get install python3-picamera
```

### 3. Enable Camera Module

```bash
sudo raspi-config
# Select Interfacing Options → Camera → Enable
# Reboot required
```

### 4. Run Lightweight Version

```bash
# Reduce log level for performance
LOG_LEVEL=WARNING python main.py
```

---

## Troubleshooting

### Issue: Tesseract Not Found

**Error:** `TesseractNotFoundError`

**Solution:**
```bash
# Reinstall tesseract
sudo apt-get install --reinstall tesseract-ocr

# Update pytesseract configuration
# In Python, set tesseract path explicitly:
pytesseract.pytesseract.pytesseract_cmd = r'/usr/bin/tesseract'
```

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'cv2'`

**Solution:**
```bash
# Reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python

# Or use system package
sudo apt-get install python3-opencv
```

### Issue: Google API Errors

**Error:** `ConnectionError` or `HTTPError`

**Solution:**
- Check internet connection
- Verify API keys in `.env` file
- Check API rate limits
- Use offline mode if applicable

### Issue: Memory Errors on Raspberry Pi

**Error:** `MemoryError` during processing

**Solution:**
```bash
# Resize images before processing
# Reduce DETECTION_WIDTH and HEIGHT in settings.py
TEXT_DETECTION_WIDTH = 160
TEXT_DETECTION_HEIGHT = 160

# Enable memory optimization
DEBUG = False
LOG_LEVEL = ERROR
```

### Issue: Permissions Denied

**Error:** `Permission denied` when creating directories

**Solution:**
```bash
# Fix permissions
chmod -R 755 Eccentric/

# Or run with appropriate user
sudo chown -R $USER:$USER Eccentric/
```

### Issue: Port Already in Use

**Error:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Use different port
python main.py --port 5001

# Or find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

---

## Performance Optimization

### 1. Image Processing

```python
# Reduce image size before processing
TEXT_DETECTION_WIDTH = 320  # Default
TEXT_DETECTION_HEIGHT = 320

# Or use:
TEXT_DETECTION_WIDTH = 160  # For Raspberry Pi
TEXT_DETECTION_HEIGHT = 160
```

### 2. Caching

```python
# Cache translations to avoid duplicate API calls
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_translate(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)
```

### 3. Concurrent Processing

```bash
# Run multiple gunicorn workers
gunicorn -w 8 -b 0.0.0.0:5000 src.api.routes:app
```

---

## Updating

### Update Repository

```bash
git pull origin main
pip install -r config/requirements.txt --upgrade
```

### Update Models

```bash
# Download latest models if available
cd models/dnn
wget <latest_model_url>
```

---

## Support & Help

For issues and help:
1. Check [Troubleshooting](#troubleshooting) section
2. Review log files in `logs/` directory
3. Open GitHub issue: https://github.com/sachinjaat98/Eccentric/issues
4. Contact team: [contact@example.com]

---

**Last Updated:** 2026-04-26
