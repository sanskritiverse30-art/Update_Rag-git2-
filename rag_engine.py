from pathlib import Path
from typing import List, Dict

import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

from config import *


class RAGAssistant:
    def __init__(self):
        # -----------------------
        # Models
        # -----------------------
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.reranker = CrossEncoder(RERANK_MODEL)

        # -----------------------
        # Vector DB
        # -----------------------
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(name="docs")

        self._index_built = False

    # ----------------------------
    # BETTER CHUNKING (sentence-aware + overlap)
    # ----------------------------
    def _chunk_text(self, text: str) -> List[str]:
        sentences = text.split(". ")
        chunks = []

        chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(chunk) + len(sentence) < CHUNK_SIZE:
                chunk += sentence + ". "
            else:
                chunks.append(chunk.strip())

                # overlap handling
                overlap_part = " ".join(chunk.split()[-CHUNK_OVERLAP:])
                chunk = overlap_part + " " + sentence + ". "

        if chunk:
            chunks.append(chunk.strip())

        return chunks

    # ----------------------------
    # INDEXING
    # ----------------------------
    def build_index(self):
        if self._index_built:
            return

        files = list(DATA_DIR.glob("*.txt"))

        chunks, metadatas, ids = [], [], []

        for file in files:
            text = file.read_text(encoding="utf-8")

            file_chunks = self._chunk_text(text)

            for i, chunk in enumerate(file_chunks):
                chunks.append(chunk)
                metadatas.append({"source": file.name})
                ids.append(f"{file.name}_{i}")

        embeddings = self.embedder.encode(chunks).tolist()

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        self._index_built = True
        print(f"Indexed {len(chunks)} chunks from {len(files)} files.\n")

    # ----------------------------
    # RETRIEVAL + RERANKING + FILTERING
    # ----------------------------
    def retrieve(self, query: str) -> List[Dict]:

        q_emb = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=q_emb,
            n_results=RETRIEVE_K
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        # -----------------------
        # RERANKING STEP
        # -----------------------
        pairs = [(query, doc) for doc in docs]
        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(docs, metas, scores),
            key=lambda x: x[2],
            reverse=True
        )

        # -----------------------
        # STRICT FILTERING
        # -----------------------
        filtered = []

        for doc, meta, score in ranked:
            if score >= RERANK_THRESHOLD:
                filtered.append({
                    "text": doc,
                    "source": meta["source"],
                    "score": float(score)
                })

            if len(filtered) >= MAX_CONTEXT_CHUNKS:
                break

        # fallback safety
        if len(filtered) < MIN_CONTEXT_CHUNKS:
            filtered = [
                {
                    "text": doc,
                    "source": meta["source"],
                    "score": float(score)
                }
                for doc, meta, score in ranked[:MIN_CONTEXT_CHUNKS]
            ]

        return filtered

    # ----------------------------
    # GENERATION
    # ----------------------------
    def generate_answer(self, query: str):

        retrieved_docs = self.retrieve(query)

        context = "\n\n".join(
            f"[{r['source']} | score={r['score']:.2f}]\n{r['text']}"
            for r in retrieved_docs
        )

        prompt = f"""
You are a helpful HR assistant.

Answer ONLY using the context below.
If the answer is not present, say:
"I could not find that information in the provided documents."

Be concise and accurate.

Context:
{context}

Question:
{query}

Answer:
""".strip()

        # HuggingFace pipeline is assumed already initialized in your app layer
        output = self.llm(
            prompt,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True
        )[0]["generated_text"]

        answer = output.split("Answer:")[-1].strip()

        sources = sorted(set(
            r["source"] for r in retrieved_docs
        ))

        return answer, sources