# Contributing to Eccentric

Thank you for your interest in contributing to Eccentric! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Commit Messages](#commit-messages)
7. [Pull Requests](#pull-requests)
8. [Issue Reporting](#issue-reporting)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct:

- **Be Respectful:** Treat all community members with respect and kindness
- **Be Inclusive:** Welcome people of all backgrounds and experience levels
- **Be Collaborative:** Work together constructively and share knowledge
- **Be Professional:** Maintain professionalism in all interactions
- **Zero Tolerance:** We do not tolerate harassment, discrimination, or abuse

### Reporting Violations

If you witness or experience violations, please report them to: [contact@example.com]

---

## Getting Started

### Prerequisites

- Python 3.7+
- Git
- Virtual environment manager (venv/conda)
- Text editor or IDE (VS Code, PyCharm, etc.)

### Fork & Clone

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Eccentric.git
cd Eccentric

# 3. Add upstream remote
git remote add upstream https://github.com/sachinjaat98/Eccentric.git

# 4. Verify remotes
git remote -v
```

---

## Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -r config/requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 3. Install Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

### 4. Create Feature Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

#### Imports

```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import cv2

# Local imports
from config.settings import DEBUG
from src.ocr.ocr_engine import OCREngine
```

#### Type Hints

```python
def extract_text(image_path: str, language: str = 'en') -> Dict[str, Any]:
    """Extract text from image.
    
    Args:
        image_path: Path to image file
        language: Language code (default: 'en')
    
    Returns:
        Dictionary with extracted text and metadata
    
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is not supported
    """
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
class OCREngine:
    """Optical Character Recognition Engine.
    
    This class provides text extraction from images using EAST
    text detection and Tesseract OCR.
    
    Attributes:
        model_path (str): Path to EAST model file
        confidence_threshold (float): Detection confidence threshold
    
    Example:
        >>> ocr = OCREngine()
        >>> result = ocr.extract_text('image.jpg')
        >>> print(result['text'])
    """
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        """Initialize OCR Engine.
        
        Args:
            model_path: Path to pre-trained EAST model
            confidence_threshold: Minimum confidence for detection
        
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        pass
```

#### Naming Conventions

```python
# Constants (UPPER_SNAKE_CASE)
MAX_IMAGE_SIZE = 4096
DEFAULT_LANGUAGE = 'en'

# Classes (PascalCase)
class OCREngine:
    pass

# Functions & methods (snake_case)
def extract_text():
    pass

# Private functions/methods (leading underscore)
def _internal_helper():
    pass

# Private constants (UPPER_SNAKE_CASE with leading underscore)
_INTERNAL_CONFIG = {}
```

#### Code Length & Complexity

```python
# Line length: 88 characters (black formatter standard)
# Max function length: 50 lines
# Max class length: 300 lines
# Max cyclomatic complexity: 10

# Use early returns to reduce nesting:
def process(value):
    if not value:
        return None
    
    if value < 0:
        return 0
    
    return process_valid(value)
```

### Formatting

```bash
# Format code with black
black src/

# Check style with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

---

## Testing

### Testing Requirements

- **Minimum Coverage:** 80%
- **Test Framework:** pytest
- **Test Format:** `test_*.py` files in `tests/` directory

### Writing Tests

```python
# tests/test_ocr.py
import pytest
from src.ocr.ocr_engine import OCREngine


class TestOCREngine:
    """Test cases for OCR Engine"""
    
    @pytest.fixture
    def ocr_engine(self):
        """Fixture: Initialize OCR engine"""
        return OCREngine()
    
    def test_initialization(self, ocr_engine):
        """Test OCR engine initialization"""
        assert ocr_engine is not None
    
    def test_extract_text_valid_image(self, ocr_engine):
        """Test text extraction with valid image"""
        result = ocr_engine.extract_text('tests/fixtures/sample.jpg')
        assert isinstance(result, dict)
        assert 'text' in result
    
    def test_extract_text_invalid_path(self, ocr_engine):
        """Test text extraction with invalid path"""
        with pytest.raises(FileNotFoundError):
            ocr_engine.extract_text('nonexistent.jpg')
    
    @pytest.mark.parametrize("language", ['en', 'es', 'hi'])
    def test_multiple_languages(self, ocr_engine, language):
        """Test OCR with multiple languages"""
        result = ocr_engine.extract_text('tests/fixtures/sample.jpg', language)
        assert result is not None
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ocr.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_ocr.py::TestOCREngine::test_initialization
```

---

## Commit Messages

### Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Build, dependencies, etc.

### Examples

```
feat: Add support for Hindi language translation

- Implement Hindi language support in translator
- Add Hindi language configuration in settings
- Update translation cache for Hindi translations

Closes #123
```

```
fix: Resolve memory leak in OCR processing

When processing large batch of images, memory was not being
properly freed after each OCR operation. This caused the
application to crash when processing 100+ images.

Fix: Explicitly call gc.collect() after each image processing
and release cv2 image resources.

Fixes #456
```

```
docs: Update setup guide for Raspberry Pi

- Add specific Raspberry Pi installation steps
- Document camera module configuration
- Add troubleshooting for Pi-specific issues
```

---

## Pull Requests

### Before Starting

1. Check [open issues](https://github.com/sachinjaat98/Eccentric/issues) and [pull requests](https://github.com/sachinjaat98/Eccentric/pulls)
2. Create an issue first for major changes
3. Discuss your approach in the issue

### PR Checklist

```markdown
- [ ] I have forked the repository
- [ ] I created a feature branch from main
- [ ] I have read the CONTRIBUTING guide
- [ ] My code follows PEP 8 style guidelines
- [ ] I have added tests for new functionality
- [ ] All tests pass locally
- [ ] I have updated documentation
- [ ] My commit messages follow the format
- [ ] I have reviewed my own code
```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
Describe tests performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

### After Submitting PR

1. GitHub Actions CI/CD will run tests
2. Maintainers will review your code
3. Address review comments
4. Once approved, maintainers will merge

---

## Issue Reporting

### Before Reporting

1. Search existing issues
2. Check documentation
3. Try the latest version
4. Check troubleshooting guide

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: (e.g., Ubuntu 20.04)
- Python: (e.g., 3.9)
- Eccentric: (e.g., v1.0.0)

## Error Message/Logs
Paste relevant error messages or logs

## Screenshots
Add screenshots if applicable

## Additional Context
Any other relevant information
```

---

## Development Tips

### Useful Commands

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Generate coverage report
pytest --cov=src --cov-report=html tests/
```

### Debugging

```python
# Add debug logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")

# Use pdb debugger
import pdb; pdb.set_trace()

# Print debugging
print(f"DEBUG: {variable}")
```

### Git Workflow

```bash
# Fetch latest changes
git fetch upstream

# Rebase on main
git rebase upstream/main

# Force push (be careful!)
git push --force-with-lease origin feature/branch

# Squash commits before PR
git rebase -i HEAD~3
```

---

## Getting Help

- 📖 Check documentation in `docs/`
- 🐛 Search existing issues
- 💬 Start a discussion
- 📧 Contact maintainers: [contact@example.com]

---

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors list
- Project documentation

---

Thank you for contributing to Eccentric! 🙏

**Last Updated:** 2026-04-26
