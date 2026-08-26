"""Provider adapters; third-party dependencies are imported only when used."""
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ServiceError(RuntimeError):
    """An external OCR, translation, or speech provider failed."""


def extract_text(image_path: Path, language: str = "eng") -> str:
    try:
        import pytesseract
        from PIL import Image
        with Image.open(image_path) as image:
            return pytesseract.image_to_string(image, lang=language).strip()
    except FileNotFoundError as exc:
        raise ServiceError("Tesseract is not installed or is unavailable on PATH.") from exc
    except Exception as exc:
        raise ServiceError(f"OCR failed: {exc}") from exc


def translate_text(text: str, source: str = "auto", target: str = "en") -> str:
    try:
        query = urlencode({"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text})
        request = Request(
            f"https://translate.googleapis.com/translate_a/single?{query}",
            headers={"User-Agent": "Eccentric/2.0"},
        )
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
        translated = "".join(part[0] for part in payload[0] if part[0])
        if not translated:
            raise ValueError("Translation provider returned no text.")
        return translated
    except Exception as exc:
        raise ServiceError(f"Translation failed: {exc}") from exc


def synthesize_speech(text: str, language: str, output_path: Path) -> Path:
    try:
        from gtts import gTTS
        gTTS(text=text, lang=language).save(str(output_path))
        return output_path
    except Exception as exc:
        raise ServiceError(f"Speech generation failed: {exc}") from exc


def clean_language(value: str, default: str) -> str:
    value = (value or default).strip().lower()
    if value == "auto":
        return value
    if not re.fullmatch(r"[a-z]{2,3}", value):
        raise ValueError("Language must be a 2 or 3 letter code.")
    return value
