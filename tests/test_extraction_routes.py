
import pytest
from fastapi.testclient import TestClient

from app.api import extraction_routes
from app.api.dependencies import get_extraction_service
from app.main import app


PDF_CONTENT = b"%PDF-example-content"


class SuccessfulExtractionService:
    def extract_text(self, content: bytes) -> str:
        return "Example extracted text"


class FailingExtractionService:
    def extract_text(self, content: bytes) -> str:
        raise ValueError("Invalid PDF file.")


@pytest.fixture
def client():
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_extract_endpoint_returns_extracted_text(client):
    app.dependency_overrides[get_extraction_service] = (
        lambda: SuccessfulExtractionService()
    )

    response = client.post(
        "/internal/v1/extract",
        content=PDF_CONTENT,
        headers={
            "Content-Type": "application/pdf",
            "X-Filename": "document.pdf",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "document.pdf",
        "content_text": "Example extracted text",
        "character_count": 22,
        "size_bytes": len(PDF_CONTENT),
    }


def test_extract_endpoint_returns_400_when_extraction_fails(client):
    app.dependency_overrides[get_extraction_service] = (
        lambda: FailingExtractionService()
    )

    response = client.post(
        "/internal/v1/extract",
        content=b"invalid-content",
        headers={
            "Content-Type": "application/pdf",
            "X-Filename": "invalid.pdf",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid PDF file.",
    }


def test_extract_endpoint_rejects_invalid_content_type(client):
    response = client.post(
        "/internal/v1/extract",
        content=PDF_CONTENT,
        headers={
            "Content-Type": "text/plain",
            "X-Filename": "document.pdf",
        },
    )

    assert response.status_code == 415
    assert response.json() == {
        "detail": "Content-Type must be application/pdf.",
    }


def test_extract_endpoint_rejects_invalid_filename(client):
    response = client.post(
        "/internal/v1/extract",
        content=PDF_CONTENT,
        headers={
            "Content-Type": "application/pdf",
            "X-Filename": "document.txt",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Filename must end in .pdf.",
    }


def test_extract_endpoint_rejects_oversized_pdf(client, monkeypatch):
    monkeypatch.setattr(
        extraction_routes,
        "MAX_PDF_SIZE_BYTES",
        10,
    )

    response = client.post(
        "/internal/v1/extract",
        content=PDF_CONTENT,
        headers={
            "Content-Type": "application/pdf",
            "X-Filename": "document.pdf",
        },
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "PDF exceeds maximum allowed size.",
    }
