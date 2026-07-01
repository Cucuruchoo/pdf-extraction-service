from io import BytesIO

from pypdf import PdfReader

from app.domain.text_extractor import TextExtractor


class PyPdfTextExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        if not content:
            raise ValueError("PDF content is empty.")

        try:
            reader = PdfReader(BytesIO(content))
        except Exception as error:
            raise ValueError("Invalid PDF file.") from error

        text_parts: list[str] = []

        try:
            for page in reader.pages:
                page_text = page.extract_text() or ""

                if page_text.strip():
                    text_parts.append(page_text.strip())
        except Exception as error:
            raise ValueError("PDF text extraction failed.") from error

        extracted_text = "\n\n".join(text_parts).strip()

        if not extracted_text:
            raise ValueError("No text could be extracted from the PDF.")

        return extracted_text
