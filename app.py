import streamlit as st

from app.text_chunker import TextChunker
from app.vector_store import SentenceTransformerEmbeddingService, ChromaVectorStore
from app.llm_service import OllamaLLMService
from app.document_indexer import DocumentIndexer
from app.rag_pipeline import RAGPipeline


st.set_page_config(page_title="Eddie AI", layout="wide")


@st.cache_resource
def initialize_pipeline():
    embedding_service = SentenceTransformerEmbeddingService()
    vector_store = ChromaVectorStore()
    llm_service = OllamaLLMService()
    chunker = TextChunker()

    indexer = DocumentIndexer(
        embedding_service=embedding_service,
        vector_store=vector_store,
        chunker=chunker
    )

    indexer.build_index()

    return RAGPipeline(
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm_service=llm_service
    )


pipeline = initialize_pipeline()

if "chat" not in st.session_state:
    st.session_state.chat = []

st.title("Eddie AI Assistant")
st.caption("Answers ONLY from your documents")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    answer, sources = pipeline.generate_answer(user_input)

    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            st.caption("Sources: " + ", ".join(sources))

    st.session_state.chat.append({"role": "assistant", "content": answer})