from io import BytesIO

import pytest
from pypdf import PdfWriter

from app.infrastructure.pypdf_text_extractor import PyPdfTextExtractor


def test_rejects_empty_content():
    extractor = PyPdfTextExtractor()

    with pytest.raises(ValueError, match="PDF content is empty"):
        extractor.extract(b"")


def test_rejects_invalid_pdf():
    extractor = PyPdfTextExtractor()

    with pytest.raises(ValueError, match="Invalid PDF file"):
        extractor.extract(b"this-is-not-a-pdf")


def test_rejects_pdf_without_text():
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)

    buffer = BytesIO()
    writer.write(buffer)

    extractor = PyPdfTextExtractor()

    with pytest.raises(ValueError, match="No text could be extracted"):
        extractor.extract(buffer.getvalue())
