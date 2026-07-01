import os

from app.text_chunker import TextChunker
from app.interfaces import EmbeddingServiceInterface, VectorStoreInterface


class DocumentIndexer:
    def __init__(
        self,
        embedding_service: EmbeddingServiceInterface,
        vector_store: VectorStoreInterface,
        chunker: TextChunker
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.chunker = chunker

    def build_index(self, docs_path: str = "data/") -> None:
        if self.vector_store.count() > 0:
            print("Index already exists")
            return

        if not os.path.exists(docs_path):
            print("data/ folder missing")
            return

        doc_id = 0

        for file_name in os.listdir(docs_path):
            if not file_name.endswith(".txt"):
                continue

            file_path = os.path.join(docs_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            chunks = self.chunker.chunk_text(text)

            for chunk in chunks:
                embedding = self.embedding_service.embed(chunk)

                self.vector_store.add_document(
                    doc_id=f"{file_name}_{doc_id}",
                    embedding=embedding,
                    document=chunk,
                    source=file_name
                )

                doc_id += 1

        print(f"Index built. Total chunks = {doc_id}")