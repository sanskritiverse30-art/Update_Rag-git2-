from rag_engine import RAGAssistant


def main() -> None:
    assistant = RAGAssistant()
    assistant.build_index()


if __name__ == "__main__":
    main()