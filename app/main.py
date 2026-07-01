import logging
import os

from fastapi import FastAPI

from app.api.extraction_routes import router as extraction_router

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="PDF Extraction Service",
    version="0.1.0",
)

app.include_router(extraction_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "pdf-extraction-service",
    }
