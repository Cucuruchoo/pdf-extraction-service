from abc import ABC, abstractmethod


class TextExtractor(ABC):
    @abstractmethod
    def extract(self, content: bytes) -> str:
        """Extract text from PDF content."""
        raise NotImplementedError
