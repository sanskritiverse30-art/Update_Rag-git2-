# Refactoring Report

## Overview

The original Project 1B implementation worked correctly but placed many responsibilities inside a single `RAGAssistant` class. This made the code difficult to maintain, extend, and test. For Project 1C, the codebase was refactored using SOLID design principles to improve modularity, readability, and testability while preserving the application's original functionality.

---

# SOLID Principle 1: Single Responsibility Principle (SRP)

### Before Refactoring

The `RAGAssistant` class was responsible for:

- Creating embeddings
- Connecting to ChromaDB
- Building the document index
- Chunking text
- Retrieving relevant context
- Generating prompts
- Communicating with the language model

Having all of these responsibilities in one class violated the Single Responsibility Principle because one class had multiple reasons to change.

### After Refactoring

Responsibilities were separated into dedicated classes:

- `TextChunker` – splits documents into chunks
- `DocumentIndexer` – loads documents and builds the vector database
- `SentenceTransformerEmbeddingService` – generates embeddings
- `ChromaVectorStore` – manages vector storage and retrieval
- `OllamaLLMService` – communicates with the language model
- `RAGPipeline` – coordinates retrieval and answer generation

### Benefits

- Improved readability
- Easier debugging
- Easier maintenance
- Individual components can be tested independently

---

# SOLID Principle 2: Dependency Inversion Principle (DIP)

### Before Refactoring

The application directly created and used concrete implementations such as:

- SentenceTransformer
- ChromaDB
- Ollama

This tightly coupled the RAG system to specific implementations.

### After Refactoring

Interfaces were introduced:

- `EmbeddingServiceInterface`
- `VectorStoreInterface`
- `LLMServiceInterface`

The `RAGPipeline` depends only on these abstractions rather than concrete classes.

Concrete implementations include:

- `SentenceTransformerEmbeddingService`
- `ChromaVectorStore`
- `OllamaLLMService`
- `MockLLMService`

### Benefits

- Easier unit testing
- Mock objects can replace external services
- Easier to extend the project with different vector databases or language models
- Reduced coupling between components

---

# Testing Improvements

Refactoring made it possible to test individual components independently.

Implemented tests include:

- TextChunker
- MockLLMService
- RAGPipeline using mocked dependencies

All tests pass successfully.

---

# Conclusion

The refactored architecture follows better software engineering practices by separating responsibilities and reducing dependencies between components. The application retains the same functionality while becoming easier to maintain, test, and extend.