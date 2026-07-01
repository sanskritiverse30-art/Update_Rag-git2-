from app.interfaces import EmbeddingServiceInterface, VectorStoreInterface, LLMServiceInterface


class RAGPipeline:
    def __init__(
        self,
        embedding_service: EmbeddingServiceInterface,
        vector_store: VectorStoreInterface,
        llm_service: LLMServiceInterface
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_service = llm_service

    def retrieve_context(self, query: str, k: int = 5) -> str:
        query_embedding = self.embedding_service.embed(query.lower().strip())
        results = self.vector_store.search(query_embedding, k)

        docs = results.get("documents", [[]])[0]

        cleaned_docs = []
        for doc in docs:
            if doc and 30 < len(doc.strip()) < 800:
                cleaned_docs.append(doc.strip())

        return "\n\n".join(cleaned_docs)

    def get_sources(self, query: str, k: int = 5) -> list[str]:
        query_embedding = self.embedding_service.embed(query.lower().strip())
        results = self.vector_store.search(query_embedding, k)

        metadatas = results.get("metadatas", [[]])[0]

        return list({
            metadata.get("source", "unknown")
            for metadata in metadatas
            if metadata
        })

    def build_prompt(self, query: str, context: str) -> str:
        return f"""
You are Eddie, a strict document-only assistant.

RULES:
- Answer ONLY using the context
- Do NOT copy full documents
- Give short precise answers
- If not found say: Not found in documents

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    def generate_answer(self, query: str) -> tuple[str, list[str]]:
        context = self.retrieve_context(query)

        if not context:
            return "Not found in documents.", self.get_sources(query)

        prompt = self.build_prompt(query, context)
        answer = self.llm_service.generate(prompt)

        return answer, self.get_sources(query)