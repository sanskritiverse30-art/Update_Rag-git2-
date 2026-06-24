def build_index(self, docs_path="data/"):

    import os

    # 🔥 FORCE CLEAN DB EVERY RUN
    try:
        self.client.delete_collection("docs")
    except:
        pass

    self.collection = self.client.get_or_create_collection("docs")

    files = os.listdir(docs_path)
    print("FILES FOUND:", files)

    doc_id = 0
    total_chunks = 0

    for file in files:

        if not file.endswith(".txt"):
            continue

        path = os.path.join(docs_path, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"\nLOADING FILE: {file}")
        print("TEXT SAMPLE:", text[:100])

        chunks = self.chunk_text(text)

        print("CHUNKS CREATED:", len(chunks))

        for chunk in chunks:

            if len(chunk.strip()) < 20:
                continue

            embedding = self.embedder.encode(chunk).tolist()

            self.collection.add(
                ids=[f"doc_{doc_id}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": file}]
            )

            doc_id += 1
            total_chunks += 1

    print("\n TOTAL CHUNKS STORED:", total_chunks)
    print(" DB COUNT:", self.collection.count())