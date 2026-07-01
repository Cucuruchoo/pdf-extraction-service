import pytest

from app.application.extraction_service import ExtractionService
from app.domain.text_extractor import TextExtractor


class FakeTextExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        return "Extracted text"


def test_extract_text_returns_extracted_content():
    service = ExtractionService(FakeTextExtractor())

    result = service.extract_text(b"pdf-content")

    assert result == "Extracted text"


def test_extract_text_rejects_empty_content():
    service = ExtractionService(FakeTextExtractor())

    with pytest.raises(ValueError, match="uploaded file is empty"):
        service.extract_text(b"")
