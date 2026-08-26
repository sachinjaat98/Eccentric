from eccentric.config import Settings
from eccentric.web import create_app


def app(tmp_path):
    instance = create_app(Settings(upload_dir=tmp_path / "uploads", audio_dir=tmp_path / "audio"))
    instance.config["TESTING"] = True
    return instance


def test_health_endpoint(tmp_path):
    response = app(tmp_path).test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_home_page(tmp_path):
    response = app(tmp_path).test_client().get("/")
    assert response.status_code == 200
    assert b"Eccentric" in response.data


def test_translate_requires_text(tmp_path):
    response = app(tmp_path).test_client().post("/api/v1/translate", json={})
    assert response.status_code == 400


def test_ocr_requires_upload(tmp_path):
    response = app(tmp_path).test_client().post("/api/v1/ocr")
    assert response.status_code == 400


def test_audio_file_is_served_from_configured_directory(tmp_path):
    instance = app(tmp_path)
    audio_file = tmp_path / "audio" / "sample.mp3"
    audio_file.write_bytes(b"ID3")
    response = instance.test_client().get("/api/v1/audio/sample.mp3")
    assert response.status_code == 200
    assert response.mimetype == "audio/mpeg"
