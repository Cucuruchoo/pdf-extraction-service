import os

from app.application.extraction_service import ExtractionService
from app.domain.text_extractor import TextExtractor
from app.infrastructure.pypdf_text_extractor import PyPdfTextExtractor


def get_text_extractor() -> TextExtractor:
    provider = os.getenv("EXTRACTION_PROVIDER", "pypdf").lower()

    if provider == "pypdf":
        return PyPdfTextExtractor()

    raise RuntimeError(f"Unsupported extraction provider: {provider}")


def get_extraction_service() -> ExtractionService:
    return ExtractionService(
        extractor=get_text_extractor(),
    )
