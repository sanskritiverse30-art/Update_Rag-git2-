Summer Software Engineering Project 2026 

# Eddie AI Assistant (RAG System)
(Eddie because, i couldn't find any other good name)

Eddie is a **document-based AI assistant** built using Retrieval-Augmented Generation (RAG).  
It answers questions **only from your uploaded documents**, ensuring grounded and reliable responses.

---

##  Features

-  Answers strictly from your documents (no hallucination)
- Semantic search using embeddings (Sentence Transformers)
-  Vector database powered by ChromaDB
-  Chat-style interface using Streamlit
-  Fast local LLM support via Ollama (Llama 3.2)
-  Supports multiple document sources (.txt files)

---

## Project Structure

```

rag-knowledge-assistant/
│
├── app.py                  # Streamlit UI (main entry point)
├── rag_engine.py           # Core RAG logic (retrieval + generation)
├── build_index.py          # Index builder for documents
├── config.py               # Configuration settings
├── chat_storage.py         # Chat history handling
│
├── data/                   # Knowledge base documents
│   ├── employee_handbook.txt
│   ├── remote_work_policy.txt
│   ├── security_policy.txt
│   ├── benefits_faq.txt
│
├── chroma_db/              # Vector database (auto-generated)
├── requirements.txt
└── README.md

````

---

## How It Works

1. Documents are loaded from the `data/` folder
2. Text is split into chunks
3. Each chunk is converted into embeddings (SentenceTransformers)
4. Stored in ChromaDB (vector database)
5. User question is embedded and matched with relevant chunks
6. LLM (Ollama - Llama 3.2) generates answer using retrieved context

---

## Example Questions
(Only works for the files stored in data/)
Try asking:

- What is the remote work policy?
- What are the security rules?
- What benefits do employees get?
- What is the code of conduct?
- What is the salary of Elon Musk? (should return "Not found in documents")

---

## Installation

### 1. Clone repo
```bash
git clone https://github.com/sanskritiverse30-art/Update_Rag-git2.git
cd rag-knowledge-assistant
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama (for LLM)

* Download: [https://ollama.com](https://ollama.com)
* Then run:

```bash
ollama serve
ollama run llama3.2
```

---

## Run the App

```bash
streamlit run app.py
```

---

## Requirements

* Python 3.10+
* Streamlit
* ChromaDB
* SentenceTransformers
* Ollama (optional but recommended)

---

## Notes

* The system only answers from `data/` folder documents
* If answer is not in documents → it will respond:

  > "Not found in documents"
* `chroma_db/` is auto-generated and should not be edited manually

---

## Working on Improvements like:
* Rename and Delete chats 
* the main owner getting a kind of feedback. 
(I Actually added feedback feature but it's brings an overall issue that it's complex, i am trying to find a way that how can i make the interface more smooth when it comes to user experience, so i am still working on that)

---
t
