# Eddie AI – Retrieval Augmented Generation (RAG) Assistant

## 

**Name:** Thota Sanskriti Naidu

**Course:** Software Engineering (CS 325)

**Project:** Project 1C – Software Refactoring and Testing
---

# Project Overview

Eddie AI is a Retrieval Augmented Generation (RAG) assistant that answers user questions using only the information contained in local documents.

The application indexes documents, stores their embeddings in ChromaDB, retrieves relevant information, and generates answers using a local Large Language Model (LLM) through Ollama.

The codebase was refactored for Project 1C using SOLID design principles to improve maintainability, modularity, and testability.

---

# Features

- Document indexing
- Automatic text chunking
- Semantic search using ChromaDB
- SentenceTransformer embeddings
- Local LLM integration with Ollama
- Streamlit chat interface
- Modular architecture
- Unit testing using Pytest
- Mock LLM service for testing
- Docker support
- GitHub Actions CI workflow

---

# Technologies Used

- Python
- Streamlit
- ChromaDB
- SentenceTransformers
- Ollama
- Pytest
- Docker
- GitHub Actions

---

# Project Structure

```text
app/
    interfaces.py
    text_chunker.py
    document_indexer.py
    vector_store.py
    llm_service.py
    rag_pipeline.py

data/
    *.txt

app/tests/
    test_text_chunker.py
    test_mock_llm.py
    test_rag_pipeline.py

app/diagrams/
    class_diagram.png
    sequence_diagram.png

README.md
REFACTORING.md
Dockerfile
requirements.txt
app.py
```

---

# Software Design Improvements

The project was refactored using the following SOLID principles:

- Single Responsibility Principle (SRP)
- Dependency Inversion Principle (DIP)

More details are provided in **REFACTORING.md**.

---

# Prerequisites

Install:

- Python 3.10 or Python 3.11
- Git
- Ollama
- Docker Desktop (optional)

---

# Installation

## Clone the Repository

```bash
git clone git clone <https://github.com/sanskritiverse30-art/Update_Rag-git2-> 
cd rag-knowledge-assistant-project1c
```


Create a virtual environment:

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

Create a virtual environment (recommended)

python -m venv venv

Activate it:

macOS / Linux

source venv/bin/activate

Windows
venv\Scripts\activate

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start Ollama:

```bash
ollama serve
```

Download the required model (first time only):

```bash
ollama pull llama3.2:latest
```

Start the Streamlit application:

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

# Running Unit Tests

Run:

```bash
pytest
```

Expected output:

```text
=========================
4 passed
=========================
```

The test suite verifies:

- Text chunking
- Mock LLM behavior
- RAG pipeline
- Dependency injection

---

# Docker
(Before running the commands, make sure Docker is running in Background)
Build the Docker image:

```bash
docker build -t eddie-ai .
```

Run:

```bash
docker run -p 8501:8501 eddie-ai
```

---

# GitHub Actions

The project contains a GitHub Actions workflow that automatically executes the test suite whenever code is pushed to the repository.

Workflow location:

```
.github/workflows/tests.yml
```

---

# UML Diagrams

The repository includes:

- Class Diagram
- Sequence Diagram

These diagrams illustrate the refactored architecture and the interaction between system components.

---

# Refactoring Summary

The original implementation placed multiple responsibilities inside a single `RAGAssistant` class.

The refactored implementation separates responsibilities into dedicated classes, making the project:

- Easier to maintain
- Easier to extend
- Easier to test
- More modular
- Better aligned with SOLID principles

A detailed explanation is available in **REFACTORING.md**.