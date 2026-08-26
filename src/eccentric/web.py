"""Flask application factory and HTTP endpoints."""
from __future__ import annotations

from pathlib import Path
from time import perf_counter
from uuid import uuid4

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from . import __version__
from .config import Settings
from .services import ServiceError, clean_language, extract_text, synthesize_speech, translate_text


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings()
    settings.prepare_directories()
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = settings.max_upload_bytes

    @app.get("/")
    def index():
        return render_template("index.html", version=__version__)

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="eccentric", version=__version__)

    @app.post("/api/v1/ocr")
    def ocr():
        image = request.files.get("image")
        if image is None or not image.filename:
            return _error("An image file is required in the 'image' field.", 400)
        suffix = Path(secure_filename(image.filename)).suffix.lower().lstrip(".")
        if suffix not in settings.allowed_extensions:
            return _error("Unsupported image format.", 415)
        language = request.form.get("language", "eng")
        path = settings.upload_dir / f"{uuid4().hex}.{suffix}"
        image.save(path)
        start = perf_counter()
        try:
            text = extract_text(path, language)
        except ServiceError as exc:
            return _error(str(exc), 503)
        finally:
            path.unlink(missing_ok=True)
        return jsonify(text=text, language=language, processing_ms=round((perf_counter() - start) * 1000, 2))

    @app.post("/api/v1/translate")
    def translate():
        payload = request.get_json(silent=True) or {}
        text = str(payload.get("text", "")).strip()
        if not text:
            return _error("'text' is required.", 400)
        try:
            source = clean_language(payload.get("source_language", "auto"), "auto")
            target = clean_language(payload.get("target_language", "en"), "en")
            translated = translate_text(text, source, target)
        except ValueError as exc:
            return _error(str(exc), 400)
        except ServiceError as exc:
            return _error(str(exc), 503)
        return jsonify(original_text=text, translated_text=translated, source_language=source, target_language=target)

    @app.post("/api/v1/speech")
    def speech():
        payload = request.get_json(silent=True) or {}
        text = str(payload.get("text", "")).strip()
        if not text:
            return _error("'text' is required.", 400)
        try:
            language = clean_language(payload.get("language", "en"), "en")
            filename = f"{uuid4().hex}.mp3"
            synthesize_speech(text, language, settings.audio_dir / filename)
        except (ValueError, ServiceError) as exc:
            return _error(str(exc), 400 if isinstance(exc, ValueError) else 503)
        return jsonify(audio_url=f"/api/v1/audio/{filename}", language=language), 201

    @app.get("/api/v1/audio/<path:filename>")
    def audio(filename: str):
        return send_from_directory(settings.audio_dir, filename, mimetype="audio/mpeg")

    @app.errorhandler(413)
    def too_large(_error_value):
        return _error("Uploaded file exceeds the size limit.", 413)

    @app.errorhandler(Exception)
    def unexpected(error: Exception):
        if isinstance(error, HTTPException):
            return error
        app.logger.exception("Unhandled request error", exc_info=error)
        return _error("Internal server error.", 500)

    return app


def _error(message: str, status: int):
    return jsonify(error={"message": message, "status": status}), status
