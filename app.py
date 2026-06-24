from rag_engine import RAGAssistant
from feedback_store import FeedbackStore


def main():
    assistant = RAGAssistant()
    store = FeedbackStore()

    print("\n AI Assistant Pro Mode")
    print("Type 'exit' | 'stats' | 'export'\n")

    print("Indexing documents...")
    assistant.build_index()
    print("Index ready!\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if query.lower() == "stats":
            print(store.get_stats())
            continue

        if query.lower() == "export":
            print(store.export_csv())
            continue

        try:
            print("\nThinking...\n")

            answer, sources = assistant.generate_answer(query)

            print("\nAnswer:\n", answer)

            print("\nSources:")
            for s in sources:
                print("-", s)

            fb = input("\nWas this helpful? (y/n): ")
            store.log(query, answer, sources, fb)

            print("\n" + "-" * 40 + "\n")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()