from sentence_transformers import SentenceTransformer
import chromadb
import os
import re

# Optional LLM (Ollama)
try:
    from langchain_community.llms import Ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False


class RAGAssistant:

    def __init__(self):

        # -----------------------
        # EMBEDDINGS
        # -----------------------
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # -----------------------
        # CHROMA DB
        # -----------------------
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection("docs")

        # -----------------------
        # LLM (SAFE INIT)
        # -----------------------
        self.llm = None
        if OLLAMA_AVAILABLE:
            try:
                self.llm = Ollama(model="llama3.2:latest")
                print("✔ LLM CONNECTED")
            except:
                self.llm = None

    # -----------------------
    # BUILD INDEX (CLEAN + SAFE)
    # -----------------------
    def build_index(self, docs_path="data/"):

        if self.collection.count() > 0:
            print("✔ Index already exists")
            return

        if not os.path.exists(docs_path):
            print("❌ data/ folder missing")
            return

        doc_id = 0

        for file in os.listdir(docs_path):
            if not file.endswith(".txt"):
                continue

            path = os.path.join(docs_path, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = self.chunk_text(text)

            for chunk in chunks:
                chunk = chunk.strip()

                if len(chunk) < 30:
                    continue

                emb = self.embedder.encode(chunk).tolist()

                self.collection.add(
                    ids=[f"{file}_{doc_id}"],
                    embeddings=[emb],
                    documents=[chunk],
                    metadatas=[{"source": file}]
                )

                doc_id += 1

        print(f"✔ INDEX BUILT | chunks = {doc_id}")

    # -----------------------
    # CHUNKING (IMPORTANT FIX)
    # -----------------------
    def chunk_text(self, text, chunk_size=500, overlap=100):

        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current = ""

        for s in sentences:
            if len(current) + len(s) < chunk_size:
                current += " " + s
            else:
                chunks.append(current.strip())
                current = s

        if current:
            chunks.append(current.strip())

        return chunks

    # -----------------------
    # RETRIEVE (REAL FIX)
    # -----------------------
    def retrieve_context(self, query, k=5):

        query = query.lower().strip()

        q_emb = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=k
        )

        docs = results.get("documents", [[]])[0]

        # IMPORTANT: REMOVE FULL FILE BLEEDING
        cleaned = []
        for d in docs:
            if not d:
                continue
            d = d.strip()

            # only keep real chunks
            if 30 < len(d) < 800:
                cleaned.append(d)

        return "\n\n".join(cleaned)

    # -----------------------
    # SOURCES
    # -----------------------
    def get_sources(self, query, k=5):

        q_emb = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=k
        )

        metas = results.get("metadatas", [[]])[0]

        return list({m.get("source", "unknown") for m in metas})

    # -----------------------
    # GENERATE ANSWER (STRICT MODE FIX)
    # -----------------------
    def generate_answer(self, query):

        context = self.retrieve_context(query)

        if not context:
            return (
                "Not found in documents.",
                self.get_sources(query)
            )

        prompt = f"""
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

        if self.llm is None:
            return (
                "LLM not connected. Run: ollama serve",
                self.get_sources(query)
            )

        answer = self.llm.invoke(prompt)

        return answer, self.get_sources(query)