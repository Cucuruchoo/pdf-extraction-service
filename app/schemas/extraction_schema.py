from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    filename: str
    content_text: str
    character_count: int
    size_bytes: int
