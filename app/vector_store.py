import chromadb
from sentence_transformers import SentenceTransformer

from app.interfaces import EmbeddingServiceInterface, VectorStoreInterface


class SentenceTransformerEmbeddingService(EmbeddingServiceInterface):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list:
        return self.model.encode(text).tolist()


class ChromaVectorStore(VectorStoreInterface):
    def __init__(self, db_path: str = "chroma_db", collection_name: str = "docs"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_document(self, doc_id: str, embedding: list, document: str, source: str) -> None:
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[{"source": source}]
        )

    def search(self, query_embedding: list, k: int = 5) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

    def count(self) -> int:
        return self.collection.count()