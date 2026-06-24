import streamlit as st
from rag_engine import RAGAssistant

st.set_page_config(page_title="Eddie AI", layout="wide")

assistant = RAGAssistant()
assistant.build_index()

# chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

st.title("Eddie AI Assistant")
st.caption("Answers ONLY from your documents")

# display chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input box
user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    answer, sources = assistant.generate_answer(user_input)

    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            st.caption("Sources: " + ", ".join(sources))

    st.session_state.chat.append({"role": "assistant", "content": answer})