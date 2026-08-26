"""Application configuration."""
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
    upload_dir: Path = field(default_factory=lambda: Path(os.getenv("UPLOAD_DIR", "data/uploads")).resolve())
    audio_dir: Path = field(default_factory=lambda: Path(os.getenv("AUDIO_DIR", "output/audio")).resolve())
    allowed_extensions: frozenset[str] = frozenset({"png", "jpg", "jpeg", "webp", "bmp", "tiff"})

    def prepare_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
