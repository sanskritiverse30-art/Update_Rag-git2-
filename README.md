# Eddie AI – Retrieval Augmented Generation Assistant

## Overview

A document-based question answering system built using Retrieval Augmented Generation (RAG). Users can upload documents, build a searchable vector database, and ask questions that are answered using only the provided documents.

## Features

- Document indexing
- Semantic search using ChromaDB
- SentenceTransformer embeddings
- Ollama integration
- Streamlit user interface
- Modular architecture following SOLID principles
- Unit testing with pytest
- Mocked AI service for testing

## Technologies

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Ollama
- Pytest

## Installation

```bash
pip install -r requirements.txt

Running the application

streamlit run app.py

Running tests
pytest


Refactoring

This project was refactored using:

Single Responsibility Principle
Dependency Inversion Principle