# RAG Knowledge Assistant (with Feedback + Reporting)

A simple **Retrieval-Augmented Generation (RAG)** 
chatbot that answers questions based only on local documents. It also includes 
**feedback tracking, CSV export, and basic analytics**.

---

## What this project does

This chatbot:
- Reads `.txt` documents from a local `data/` folder
- Splits them into chunks (better retrieval)
- Stores embeddings in a vector database (ChromaDB)
- Retrieves relevant chunks based on user questions
- Uses an LLM (Ollama / local model or HF pipeline) to generate answers
- Restricts answers strictly to document context only

It also:
- Collects user feedback (Helpful / Not Helpful)
- Tracks usage statistics
- Allows exporting a full report as CSV
- Supports reranking + improved retrieval (latest version)

---

##  Key Features

###  Document-based QA
Answers ONLY from uploaded documents. If info is missing, it says so.

###  RAG Pipeline
- Chunking documents
- Embedding (SentenceTransformers)
- Vector search (ChromaDB)
- Optional reranking for better accuracy

###  Analytics System
- Total questions asked
- Helpful vs not helpful responses
- Success rate tracking
- `/stats` command inside CLI

###  Feedback System
After every answer:
- User can rate response (y/n)
- Feedback is stored for analysis

###  Export System
- Export all interactions into a `report.csv`
- Useful for professors / evaluation / demo

---

## Project Structure
rag-knowledge-assistant/
│
├── app.py # Main CLI chatbot loop
├── rag_engine.py # RAG pipeline (retrieval + generation)
├── feedback_store.py # Stores logs + stats + CSV export
├── config.py # Central configuration (models, paths, params)
│
├── data/ # Your documents (.txt files)
├── chroma_db/ # Vector database storage
└── report.csv # Generated usage report

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Start Ollama (if using local model)
ollama serve
3. Pull model (first time only)
ollama pull llama3.2
4. Run app
python app.py
 Commands in Chat

#Inside the chatbot:

Ask any question → gets answer from documents
stats → view usage report
export → download CSV report
exit → quit app
 Example Output
Answer:
Remote work is allowed after 90 days of employment...

Sources:
- remote_work_policy.txt
- employee_handbook.txt

# Was this helpful? (y/n):
 How RAG Works Here
User asks a question
Question is embedded into vector space
Top matching document chunks are retrieved
(Optional) reranker improves relevance
LLM generates final answer using ONLY context
System logs feedback + sources


 # Improvements Added
Better chunking strategy
Strict document-only answering
Reranking support (improved accuracy)
Feedback tracking system
CSV export for evaluation