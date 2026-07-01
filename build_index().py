def build_index(self, docs_path="data/"):

    try:
        self.client.delete_collection("docs")
    except:
        pass

    self.collection = self.client.get_or_create_collection("docs")

    print("🚀 Building index...")

    doc_id = 0

    for file in os.listdir(docs_path):

        if not file.endswith(".txt"):
            continue

        print(f"Loading: {file}")

        with open(os.path.join(docs_path, file), "r", encoding="utf-8") as f:
            text = f.read()

        chunks = self.chunk_text(text)

        print(f"Chunks: {len(chunks)}")

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

    print(f"✅ Index built! Total chunks = {self.collection.count()}")