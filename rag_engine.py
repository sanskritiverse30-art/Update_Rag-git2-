from typing import List, Dict
import requests

import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

from config import *


class RAGAssistant:
    def __init__(self):
        # -----------------------
        # MODELS
        # -----------------------
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.reranker = CrossEncoder(RERANK_MODEL)

        # -----------------------
        # VECTOR DB
        # -----------------------
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(name="docs")

        self._index_built = False

    # -----------------------
    # OLLAMA CALL
    # -----------------------
    def _call_llm(self, prompt: str):
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    # -----------------------
    # CHUNKING
    # -----------------------
    def _chunk_text(self, text: str) -> List[str]:
        sentences = text.split(". ")
        chunks = []
        chunk = ""

        for s in sentences:
            s = s.strip()
            if not s:
                continue

            if len(chunk) + len(s) < CHUNK_SIZE:
                chunk += s + ". "
            else:
                chunks.append(chunk.strip())
                overlap = " ".join(chunk.split()[-CHUNK_OVERLAP:])
                chunk = overlap + " " + s + ". "

        if chunk:
            chunks.append(chunk.strip())

        return chunks

    # -----------------------
    # INDEX (FIXED FOR STREAMLIT)
    # -----------------------
    def build_index(self):
        # Prevent repeated indexing in Streamlit reruns
        if self._index_built:
            return

        # If DB already has data → skip rebuilding
        if self.collection.count() > 0:
            self._index_built = True
            print("Using existing ChromaDB index")
            return

        files = list(DATA_DIR.glob("*.txt"))

        if len(files) == 0:
            print("No documents found in data/ folder")
            return

        chunks = []
        metadatas = []
        ids = []

        for f in files:
            text = f.read_text(encoding="utf-8")
            file_chunks = self._chunk_text(text)

            for i, c in enumerate(file_chunks):
                chunks.append(c)
                metadatas.append({
                    "source": f.name
                })
                ids.append(f"{f.name}_{i}")

        embeddings = self.embedder.encode(chunks).tolist()

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        self._index_built = True
        print(f"Indexed {len(chunks)} chunks from {len(files)} files")

    # -----------------------
    # RETRIEVE
    # -----------------------
    def retrieve(self, query: str) -> List[Dict]:

        q_emb = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=q_emb,
            n_results=RETRIEVE_K
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        pairs = [(query, d) for d in docs]
        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(docs, metas, scores),
            key=lambda x: x[2],
            reverse=True
        )

        top = ranked[:MAX_CONTEXT_CHUNKS]

        return [
            {
                "text": d,
                "source": m["source"],
                "score": float(s)
            }
            for d, m, s in top
        ]

    # -----------------------
    # GENERATE
    # -----------------------
    def generate_answer(self, query: str):

        docs = self.retrieve(query)

        context = "\n\n".join(
            f"[{d['source']}]\n{d['text']}"
            for d in docs
        )

        prompt = f"""
You are AI Assistant Pro Mode.

Use ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
""".strip()

        answer = self._call_llm(prompt)

        sources = list({d["source"] for d in docs})

        return answer, sources