from abc import ABC, abstractmethod


class EmbeddingServiceInterface(ABC):
    @abstractmethod
    def embed(self, text: str) -> list:
        pass


class VectorStoreInterface(ABC):
    @abstractmethod
    def add_document(self, doc_id: str, embedding: list, document: str, source: str) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: list, k: int = 5) -> dict:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class LLMServiceInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass