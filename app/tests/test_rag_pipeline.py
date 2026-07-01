from app.rag_pipeline import RAGPipeline
from app.llm_service import MockLLMService


class FakeEmbeddingService:
    def embed(self, text: str) -> list:
        return [0.1, 0.2, 0.3]


class FakeVectorStore:
    def search(self, query_embedding: list, k: int = 5) -> dict:
        return {
            "documents": [[
                "This is a valid document chunk about artificial intelligence and retrieval augmented generation."
            ]],
            "metadatas": [[
                {"source": "test_document.txt"}
            ]]
        }


def test_rag_pipeline_returns_answer_and_sources():
    pipeline = RAGPipeline(
        embedding_service=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
        llm_service=MockLLMService()
    )

    answer, sources = pipeline.generate_answer("What is RAG?")

    assert answer == "Mock answer generated for testing."
    assert sources == ["test_document.txt"]