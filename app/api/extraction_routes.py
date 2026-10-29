
import logging
import os
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
    status,
)

from app.api.dependencies import get_extraction_service
from app.application.extraction_service import ExtractionService
from app.schemas.extraction_schema import ExtractionResponse

router = APIRouter(prefix="/internal/v1", tags=["extraction"])

logger = logging.getLogger(__name__)

MAX_PDF_SIZE_BYTES = int(
    os.getenv("MAX_PDF_SIZE_BYTES", str(10 * 1024 * 1024))
)


@router.post(
    "/extract",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/pdf": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            },
        }
    },
)
async def extract_pdf_text(
    request: Request,
    filename: Annotated[str, Header(alias="X-Filename")],
    service: Annotated[
        ExtractionService, Depends(get_extraction_service)
    ],
) -> ExtractionResponse:
    content_type = (
        request.headers.get("content-type", "")
        .split(";", 1)[0]
        .strip()
        .lower()
    )

    if content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Content-Type must be application/pdf.",
        )

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Filename must end in .pdf.",
        )

    content = bytearray()

    async for chunk in request.stream():
        if len(content) + len(chunk) > MAX_PDF_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="PDF exceeds maximum allowed size.",
            )

        content.extend(chunk)

    pdf_bytes = bytes(content)

    logger.info(
        "Extracting PDF: filename=%s size_bytes=%s",
        filename,
        len(pdf_bytes),
    )

    try:
        extracted_text = service.extract_text(pdf_bytes)
    except ValueError as error:
        logger.warning("PDF extraction failed: %s", error)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return ExtractionResponse(
        filename=filename,
        content_text=extracted_text,
        character_count=len(extracted_text),
        size_bytes=len(pdf_bytes),
    )
