"""
OCR Module Tests
"""
import pytest
import os
from src.ocr.ocr_engine import OCREngine


class TestOCREngine:
    """Test cases for OCR Engine"""

    @pytest.fixture
    def ocr(self):
        """Initialize OCR engine"""
        return OCREngine()

    def test_ocr_initialization(self, ocr):
        """Test OCR engine initialization"""
        assert ocr is not None

    def test_extract_text_with_valid_image(self, ocr):
        """Test text extraction with valid image"""
        # Create a dummy test image path
        test_image = "data/examples/sample.jpg"
        if os.path.exists(test_image):
            result = ocr.extract_text(test_image)
            assert isinstance(result, str)
            assert len(result) >= 0

    def test_extract_text_with_invalid_image(self, ocr):
        """Test text extraction with invalid image path"""
        with pytest.raises(ValueError):
            ocr.extract_text("nonexistent_image.jpg")

    def test_extract_text_with_confidence(self, ocr):
        """Test text extraction with confidence scores"""
        test_image = "data/examples/sample.jpg"
        if os.path.exists(test_image):
            result = ocr.extract_text_with_confidence(test_image)
            assert isinstance(result, list)
            if len(result) > 0:
                assert "text" in result[0]
                assert "confidence" in result[0]
                assert "bbox" in result[0]
