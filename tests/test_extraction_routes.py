from fastapi.testclient import TestClient

from app.api.dependencies import get_extraction_service
from app.main import app


class SuccessfulExtractionService:
    def extract_text(self, content: bytes) -> str:
        return "Example extracted text"


class FailingExtractionService:
    def extract_text(self, content: bytes) -> str:
        raise ValueError("Invalid PDF file.")


client = TestClient(app)


def test_extract_endpoint_returns_extracted_text():
    app.dependency_overrides[get_extraction_service] = (
        lambda: SuccessfulExtractionService()
    )

    response = client.post(
        "/internal/v1/extract",
        files={
            "file": (
                "document.pdf",
                b"%PDF-example-content",
                "application/pdf",
            ),
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "filename": "document.pdf",
        "content_text": "Example extracted text",
        "character_count": 22,
        "size_bytes": 20,
    }


def test_extract_endpoint_returns_400_when_extraction_fails():
    app.dependency_overrides[get_extraction_service] = (
        lambda: FailingExtractionService()
    )

    response = client.post(
        "/internal/v1/extract",
        files={
            "file": (
                "invalid.pdf",
                b"invalid-content",
                "application/pdf",
            ),
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid PDF file.",
    }
