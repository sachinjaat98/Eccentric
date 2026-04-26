# Text Recognition System with Multilingual Voice Conversion

A comprehensive text recognition and translation system that breaks down language barriers through optical character recognition (OCR), text translation, and speech synthesis.

**Status:** Final Year Project  
**Last Updated:** 2026-04-26

---

## 🎯 Project Overview

This application automates language translation and voice conversion to overcome language barriers between countries and regions. It enables users to:

- **Extract text** from images (camera or uploaded files)
- **Recognize and digitize** text using OCR technology
- **Translate** text between multiple languages (English to international and Indian languages)
- **Convert** translated text to speech with natural voice synthesis

### Key Features

✅ Real-time text extraction from images  
✅ Multi-language translation support  
✅ Text-to-speech conversion  
✅ Speech recognition capabilities  
✅ User-friendly web interface  
✅ Camera integration for instant document scanning  

---

## 👥 Team Members

| Name | Role |
|------|------|
| Sachin Kumar | - |
| Shivani Sachan | - |
| Ritika | - |
| Prem Kumar Sharma | - |
| Anmol Guleri | - |

---

## 🛠️ Technology Stack

### Hardware

- **Raspberry Pi 3**
  - Broadcom BCM2837 SoC Multimedia processor
  - 4x ARM Cortex-A53 @ 1.2GHz
  - 1GB LPDDR2 RAM (900MHz) — expandable via microSD card (up to 64GB)
  - Wi-Fi 802.11n & Bluetooth 4.1 Classic
  - 40 GPIO pins
  - 3.5mm audio jack for speaker/headphones

- **Raspberry Pi Camera Module**
  - 5MP sensor
  - 2592×1944 resolution
  - 25mm × 25mm form factor
  - Flat flex cable connection (1mm pitch, 15-conductor Type B)

### Software & Libraries

| Component | Purpose |
|-----------|---------|
| **Raspbian** | Operating System |
| **AWS** | Cloud services & storage |
| **Tesseract** | OCR engine for text recognition |
| **EAST** | Efficient Accurate Scene Text Detector |
| **gTTS** | Google Text-to-Speech API |
| **Googletrans** | Google Translate API wrapper (open-source Python library) |
| **Python** | Primary programming language |

---

## 📋 System Architecture

### Text Extraction & Recognition
1. Capture image via camera or upload from system
2. Detect text regions using EAST (Efficient Accurate Scene Text Detector)
3. Extract text using Tesseract OCR engine
4. Digitize and prepare text for translation

### Text Translation
- **Input:** English text (primary language)
- **Process:** 
  - Split text into words
  - Query translation dictionary
  - Leverage Google Translate API for complex phrases
  - Support for 100+ languages (international and Indian languages)
- **Output:** Translated text in target language

### Voice Conversion
- Convert translated text to speech using Google Text-to-Speech (gTTS)
- Natural-sounding multilingual audio output
- Real-time playback capability

---

## 💡 Use Cases & Applications

### Language Accessibility
- Enables travelers to instantly translate signage, menus, and documents in foreign countries
- Bridges communication gaps between multilingual communities

### Assistive Technology
- **For Visually Impaired:** Audio output helps blind and low-vision users access text from their environment
- **For Deaf Community:** Visual translation and text recognition support

### Travel & Tourism
- Real-time translation of restaurant menus, street signs, and travel documents
- Eliminates reliance on human translators

### Education & Accessibility
- Language learning support for international students
- Document translation for academic materials

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Translation Speed** | Seconds (vs. hours for human translation) |
| **Translation Capacity** | 10,000+ words processed in seconds |
| **Accuracy** | High accuracy with Tesseract OCR + EAST detection |
| **Language Support** | 100+ languages (international & Indian) |
| **Platform** | Raspberry Pi 3 compatible |

---

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi 3 with Raspbian OS
- Python 3.x
- Camera module or USB camera
- Internet connection (for AWS & Google APIs)

### Installation
```bash
# Clone the repository
git clone https://github.com/sachinjaat98/Eccentric.git
cd Eccentric

# Install dependencies
pip install -r requirements.txt

# Install system packages
sudo apt-get install tesseract-ocr
sudo apt-get install python3-opencv
```

### Running the Application
```bash
python3 main.py
```

---

## 📸 System Demonstration

![System Architecture](https://github.com/sachinjaat98/Eccentric/assets/56782045/b21e1195-47a8-4e7d-a3c0-7d7938c6cea1)

![Text Recognition Demo](https://github.com/sachinjaat98/Eccentric/assets/56782045/96c2367f-1a7d-4817-93ef-41051b656997)

![Recognized Text Example](https://github.com/sachinjaat98/Eccentric/assets/56782045/c57e8078-fa22-4087-9374-f95cb4806fe9)

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
GOOGLE_TRANSLATE_API_KEY=your_api_key
```

---

## 📄 License

[Add your license here - e.g., MIT, GPL-3.0, etc.]

---

## 📧 Contact & Support

For questions, suggestions, or contributions, please reach out to the project team or create an issue on GitHub.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

**Last Updated:** 2026-04-26
