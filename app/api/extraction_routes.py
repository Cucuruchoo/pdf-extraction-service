import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.dependencies import get_extraction_service
from app.application.extraction_service import ExtractionService
from app.schemas.extraction_schema import ExtractionResponse

router = APIRouter(
    prefix="/internal/v1",
    tags=["extraction"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/extract",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_pdf_text(
    file: UploadFile = File(...),
    service: ExtractionService = Depends(get_extraction_service),
) -> ExtractionResponse:
    filename = file.filename or "document.pdf"
    content = await file.read()

    logger.info(
        "Extracting PDF text: filename=%s size_bytes=%s",
        filename,
        len(content),
    )

    try:
        extracted_text = service.extract_text(content)
    except ValueError as error:
        logger.warning(
            "PDF extraction failed: filename=%s error=%s",
            filename,
            str(error),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return ExtractionResponse(
        filename=filename,
        content_text=extracted_text,
        character_count=len(extracted_text),
        size_bytes=len(content),
    )
