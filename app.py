from rag_engine import RAGAssistant
from feedback_store import FeedbackStore


def main():
    assistant = RAGAssistant()
    store = FeedbackStore()

    print("\n🧠 Custom AI Knowledge Assistant (PRO MODE + RERANKING)")
    print("Type 'exit' | 'stats' | 'export'\n")

    print("Indexing documents...")
    assistant.build_index()
    print("Index ready!\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        # STATS
        if query.lower() == "stats":
            stats = store.get_stats()
            print("\n📊 REPORT")
            print(stats)
            continue

        # EXPORT
        if query.lower() == "export":
            file_path = store.export_csv()
            print(f"\n📄 Exported: {file_path}\n")
            continue

        try:
            print("\nThinking...\n")

            answer, sources = assistant.generate_answer(query)

            print("\nAnswer:")
            print(answer)

            print("\nSources:")
            for s in sources:
                print("-", s)

            fb = input("\nWas this helpful? (y/n): ").strip().lower()

            store.log(query, answer, sources, fb)

            print("\n" + "-" * 50 + "\n")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()