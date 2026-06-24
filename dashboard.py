import streamlit as st
import datetime

from rag_engine import RAGAssistant
from feedback_store import FeedbackStore

from reportlab.pdfgen import canvas


# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="AI Assistant", layout="wide")

assistant = RAGAssistant()
assistant.build_index()

store = FeedbackStore()


# -----------------------
# SESSION STATE (SINGLE CHAT ONLY)
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None


# -----------------------
# SIDEBAR (STATS + EXPORT)
# -----------------------
st.sidebar.title("Eddie AI Assistant")

stats = store.get_stats()
st.sidebar.metric("Total Queries", stats["total_queries"])
st.sidebar.metric("Success Rate", f"{stats['helpfulness_rate']}%")


# EXPORT PDF
if st.sidebar.button("Export Chat PDF"):

    file_name = "chat_export.pdf"
    c = canvas.Canvas(file_name)
    y = 800

    c.drawString(50, y, "Eddie AI Chat Export")
    y -= 30

    for msg in st.session_state.messages:
        text = f"{msg['role']}: {msg['content'][:90]}"
        c.drawString(50, y, text)
        y -= 20

        if y < 50:
            c.showPage()
            y = 800

    c.save()

    st.sidebar.success(f"Saved {file_name}")


# -----------------------
# MAIN UI
# -----------------------
st.title("AI Assistant — Eddie")
st.caption("Document-based RAG assistant (answers only from your files).")


# SHOW CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------
# CHAT INPUT
# -----------------------
user_input = st.chat_input("Ask something from your documents...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            answer, sources = assistant.generate_answer(user_input)

            st.markdown(answer)
            st.caption("Sources: " + ", ".join(sources))

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Log usage
    store.log(user_input, answer, sources, "unknown")

    # Store for feedback
    st.session_state.last_question = user_input
    st.session_state.last_answer = answer


# -----------------------
# FEEDBACK SECTION
# -----------------------
if st.session_state.last_answer:

    st.markdown("### Was this helpful?")

    col1, col2 = st.columns(2)

    if col1.button("👍 Yes"):
        store.add_feedback(
            st.session_state.last_question,
            st.session_state.last_answer,
            True
        )
        st.success("Thanks for your feedback!")

    if col2.button("👎 No"):
        store.add_feedback(
            st.session_state.last_question,
            st.session_state.last_answer,
            False
        )
        st.success("Thanks for your feedback!")