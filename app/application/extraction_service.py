from app.domain.text_extractor import TextExtractor


class ExtractionService:
    def __init__(self, extractor: TextExtractor):
        self.extractor = extractor

    def extract_text(self, content: bytes) -> str:
        if not content:
            raise ValueError("The uploaded file is empty.")

        return self.extractor.extract(content)
