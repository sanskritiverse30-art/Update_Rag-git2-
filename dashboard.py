import streamlit as st
from rag_engine import RAGAssistant
from feedback_store import FeedbackStore
import uuid
from datetime import datetime

# -----------------------
# INIT
# -----------------------
st.set_page_config(page_title="RAG Assistant", layout="wide")

assistant = RAGAssistant()
assistant.build_index()

store = FeedbackStore()

# -----------------------
# SESSION STATE
# -----------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    st.session_state.current_session = str(uuid.uuid4())[:8]

if "sessions_data" not in st.session_state:
    st.session_state.sessions_data = {}

# create session if not exists
if st.session_state.current_session not in st.session_state.sessions_data:
    st.session_state.sessions_data[st.session_state.current_session] = []


# -----------------------
# SIDEBAR (CHAT HISTORY)
# -----------------------
st.sidebar.title(" Chat Sessions")

# new chat button
if st.sidebar.button("➕ New Chat"):
    new_id = str(uuid.uuid4())[:8]
    st.session_state.current_session = new_id
    st.session_state.sessions_data[new_id] = []
    st.rerun()

# show sessions
for sid in st.session_state.sessions_data.keys():
    if st.sidebar.button(f"Chat {sid}"):
        st.session_state.current_session = sid
        st.rerun()

st.sidebar.divider()

stats = store.get_stats()
st.sidebar.metric("Total Queries", stats["total_queries"])
st.sidebar.metric("Success Rate", f"{stats['helpfulness_rate']}%")


# -----------------------
# MAIN CHAT UI
# -----------------------
st.title(" RAG Knowledge Assistant")

session = st.session_state.current_session
chat_history = st.session_state.sessions_data[session]


# render chat history
for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -----------------------
# USER INPUT
# -----------------------
user_input = st.chat_input("Ask something from your documents...")

if user_input:

    # store user message
    chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            answer, sources = assistant.generate_answer(user_input)

            st.write(answer)

            st.caption("Sources:")
            st.write(", ".join(sources))

    # store assistant message
    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    # log feedback system (optional still CLI style)
    store.log(user_input, answer, sources, "y")