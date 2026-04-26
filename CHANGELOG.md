# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned Features
- Batch processing for multiple images
- Real-time video stream processing
- Offline mode with downloaded language packs
- Mobile app (iOS/Android)
- Web UI dashboard
- Multi-format output (PDF, Word, etc.)

---

## [1.0.0] - 2026-04-26

### Added

#### Core Features
- ✅ Text detection from images using EAST model
- ✅ Text recognition using Tesseract OCR
- ✅ Multi-language translation (100+ languages)
- ✅ Text-to-speech synthesis with natural voices
- ✅ Camera integration for Raspberry Pi
- ✅ REST API with Flask
- ✅ Support for multiple image formats (JPG, PNG, BMP, TIFF)

#### OCR Module (`src/ocr/`)
- EAST text detection with configurable confidence threshold
- Tesseract OCR engine integration
- Text region extraction with bounding boxes
- Confidence score calculation for accuracy assessment
- Image preprocessing (rotation, normalization, contrast enhancement)

#### Translation Module (`src/translation/`)
- Google Translate API integration
- Translation caching to reduce API calls
- Support for 100+ languages
- Language detection
- Batch translation support
- Rate limiting and error handling

#### TTS Module (`src/tts/`)
- Google Text-to-Speech (gTTS) integration
- Multi-language audio synthesis
- Configurable speech speed and pitch
- Audio format support (MP3, OGG, WAV)
- Real-time audio streaming

#### API Layer (`src/api/`)
- RESTful API endpoints
- Request validation and error handling
- CORS support for web applications
- API rate limiting
- Comprehensive logging

#### Configuration & Utilities
- Environment-based configuration management
- Structured logging system with file rotation
- Image processing utilities
- Text utilities (cleaning, validation)
- File handling utilities
- Input validation

#### Documentation
- Complete installation guide (SETUP.md)
- System architecture documentation (ARCHITECTURE.md)
- Developer contribution guidelines (CONTRIBUTING.md)
- API reference documentation (API.md)
- Comprehensive README.md
- Troubleshooting guide

#### Development Tools
- pytest framework with test templates
- Code style enforcement (PEP 8)
- Type hints throughout codebase
- Git hooks and pre-commit support
- CI/CD ready

#### Configuration Management
- `.env` file support with 80+ parameters
- Development, testing, and production modes
- Raspberry Pi specific configurations
- External service credentials management

### Changed
- Migrated from monolithic structure to modular architecture
- Reorganized codebase into logical modules
- Improved error handling and validation
- Enhanced logging with structured format

### Fixed
- Memory management in image processing
- Model loading performance
- API response times

### Dependencies
- Python 3.7+
- OpenCV (cv2) >= 4.5.0
- Tesseract-OCR >= 4.0
- googletrans >= 4.0.0
- gTTS >= 2.2.0
- Flask >= 2.0.0
- Numpy >= 1.19.0
- Pillow >= 8.0.0

---

## [0.9.0] - 2026-04-10

### Added
- Beta version release
- Core OCR functionality
- Basic translation support
- Raspberry Pi compatibility

### Known Issues
- Memory usage not optimized
- API response times slow with large images
- Limited error handling

---

## Migration Guide

### Upgrading from 0.9.0 to 1.0.0

#### Breaking Changes
None - This is the first stable release

#### New Structure
```
Old Structure          →  New Structure
────────────────────      ──────────────
EastOCR.py            →   src/ocr/
textDetectRecog.py    →   src/ocr/
(root scripts)        →   src/api/
(no config)           →   config/
(no docs)             →   docs/
```

#### Setup Changes

**Before:**
```bash
python3 EastOCR.py image.jpg
```

**After:**
```bash
# New way - via API
python main.py
# Then use API: POST /api/process-image

# Or direct Python import
from src.ocr.ocr_engine import OCREngine
ocr = OCREngine()
result = ocr.extract_text('image.jpg')
```

#### Configuration Changes

**Before:** Configuration in script files

**After:** Use `.env` file
```bash
cp .env.example .env
# Edit .env with your settings
python main.py
```

#### API Usage

**New API Endpoints:**
```
GET  /api/health                    # Health check
POST /api/process-image             # Full pipeline
POST /api/ocr                       # OCR only
POST /api/translate                 # Translation only
POST /api/tts                       # TTS only
GET  /api/languages                 # Supported languages
```

---

## Known Issues

### Current Release (1.0.0)

1. **Large Image Processing**
   - Images > 4MB may timeout
   - **Workaround:** Use image resizing before processing

2. **Rate Limiting**
   - Google Translate API has rate limits (500K chars/day free)
   - **Workaround:** Use translation caching, cache enabled by default

3. **Tesseract Memory**
   - High memory usage with PDF conversion
   - **Workaround:** Process images individually, not in batch

### Closed Issues

See [GitHub Issues](https://github.com/sachinjaat98/Eccentric/issues?state=closed) for resolved issues.

---

## Security

### Security Updates

- All dependencies are regularly updated
- Security vulnerabilities reported via GitHub Security Advisory
- See [SECURITY.md](./SECURITY.md) for security policy

### Reporting Security Issues

Please email security concerns to: [security@example.com]
Do not open public issues for security vulnerabilities.

---

## Version History Summary

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-04-26 | Stable | First stable release with full features |
| 0.9.0 | 2026-04-10 | Beta | Beta version with core functionality |
| 0.1.0 | 2022-08-25 | Initial | Project initiation |

---

## Future Roadmap

### v1.1.0 (Q3 2026)
- [ ] Batch image processing with queue system
- [ ] Real-time video stream support
- [ ] Improved accuracy with ensemble models
- [ ] WebSocket support for real-time updates
- [ ] Database integration (PostgreSQL)

### v1.2.0 (Q4 2026)
- [ ] Offline mode with downloaded language packs
- [ ] Mobile API optimization
- [ ] Advanced image preprocessing filters
- [ ] Custom model training support
- [ ] Performance analytics dashboard

### v2.0.0 (2027)
- [ ] Complete rewrite with async/await
- [ ] Microservices architecture
- [ ] Kubernetes deployment support
- [ ] Mobile applications (iOS/Android)
- [ ] Advanced ML features (entity recognition, sentiment analysis)
- [ ] Multi-modal processing (images + audio)

---

## Support

- **Documentation:** [docs/](./docs/)
- **Issues:** [GitHub Issues](https://github.com/sachinjaat98/Eccentric/issues)
- **Discussions:** [GitHub Discussions](https://github.com/sachinjaat98/Eccentric/discussions)
- **Email:** contact@example.com

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

## Acknowledgments

- Team Members: Sachin Kumar, Shivani Sachan, Ritika, Prem Kumar Sharma, Anmol Guleri
- Built with ❤️ for language accessibility
- Special thanks to the open-source community

---

**Last Updated:** 2026-04-26

For more details, visit: https://github.com/sachinjaat98/Eccentric
