# Eddie — AI RAG Knowledge Assistant

Eddie is a **Retrieval-Augmented Generation (RAG) AI assistant** built with Streamlit that answers questions strictly from your local documents. It uses embeddings + vector search + LLM generation to provide grounded, document-based answers.

---

## What this project does

Eddie allows you to:
- Ask questions in natural language
- Retrieve relevant context from your `.txt` documents
- Generate AI answers based ONLY on retrieved content
- View sources used for every answer
- Give feedback (👍 / 👎) on responses
- Track usage statistics
- Export chat history as a PDF

---

## Core Features

### 📄 Document-based Q&A (RAG System)
- Loads `.txt` files from `data/`
- Splits documents into chunks
- Stores embeddings in **ChromaDB**
- Retrieves most relevant chunks for each query
- Uses LLM to generate grounded answers

---

###  AI Assistant (Eddie)
- Answers only using your uploaded documents
- Refuses to hallucinate outside context
- Shows source documents used in response

---

### Feedback & Analytics
- 👍 / 👎 feedback system after each answer
- Tracks:
  - Total queries
  - Helpfulness rate
- Stores feedback in CSV (`report.csv`)

---

###  Export Feature
- Export chat history as PDF
- Useful for:
  - demos
  - grading
  - project submission

---

###  Streamlit Chat UI
- ChatGPT-style interface
- Real-time responses
- Session-based chat history (single-session mode for simplicity)

---

## 🏗️ Project Structure
rag-knowledge-assistant/
│
├── dashboard.py # Streamlit UI (main app)
├── rag_engine.py # RAG pipeline (retrieval + generation)
├── feedback_store.py # Feedback tracking + stats
├── chat_storage.py # (optional / removed in latest version)
├── config.py # Configuration settings
│
├── data/ # Your documents (.txt files)
├── chroma_db/ # Vector database storage
├── report.csv # Feedback + usage logs
└── README.md

---

## Installation

### 1. Clone the project
```bash
git clone <Updated_Rag-git2->
cd rag-knowledge-assistant

2. Create environment (recommended)
conda create -n rag python=3.10
conda activate rag
3. Install dependencies
pip install -r requirements.txt
4. Run Streamlit app
streamlit run dashboard.py

# How RAG Works
User asks a question
Question is converted into embeddings
ChromaDB retrieves top matching document chunks
Retrieved context is passed to LLM
LLM generates answer using ONLY that context
Sources are displayed
Feedback is stored


## Example Output

Question:

What is the remote work policy?

Answer:

Remote work is allowed after 90 days of employment...

Sources:

employee_handbook.txt
remote_work_policy.txt

# Stats Tracked
Total queries
Helpful responses
Success rate (%)

Displayed in sidebar inside the app.

# Tech Stack
Python
Streamlit
LangChain-style RAG pipeline
ChromaDB (vector database)
SentenceTransformers (embeddings)
ReportLab (PDF export)

# Key Design Decisions
Strict document-only answering (no hallucinations)
Lightweight local vector DB (Chroma)
Streamlit for fast UI development
Simple feedback loop for evaluation
Single-session mode for simplicity and stability


# Future Improvements
Add a feature, that stores old chats, and a user can rename or delete chats (old chats) but it makes the interface complex to use. 
Like it's not smooth, adding that feature makes it complex. 


# Notes
Ensure data/ folder contains .txt files before running
ChromaDB index is auto-created on first run
Feedback is stored in report.csv