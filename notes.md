# Refactoring Notes - RAG Application

### Design Decisions
The primary focus of this refactor was to transform a monolithic script into a modular, production-ready architecture. I implemented a **Layered Architecture** by separating concerns into four distinct layers: Web API (FastAPI), Business Logic (LangGraph), Data Access (Qdrant/In-memory), and Schemas (Pydantic). 

To ensure the code is testable and maintainable, I utilized **Dependency Injection** via FastAPI's `Depends` system. By injecting `DocumentStore` and `EmbeddingService` into the `RagWorkflow`, the orchestration logic remains decoupled from the underlying storage technology. This allows for seamless switching between different database providers without modifying the core workflow.

### Trade-offs
One significant trade-off was the decision to maintain the **deterministic fallback logic** in the search functionality (returning the first document if no match is found). While this might not be ideal for a real-world production RAG system, I chose to preserve this behavior to strictly adhere to the requirement of "maintaining original behavior" while focusing the effort on structural improvements and OOP principles.

### Maintainability
The new structure significantly improves maintainability through **Encapsulation**. Each service has a single responsibility; for instance, any changes to the embedding generation logic only require modifications within the `EmbeddingService` class. Furthermore, the use of **Abstract Base Classes (ABC)** for the storage layer ensures that any future storage implementations (e.g., moving from Qdrant to Pinecone or PGVector) will follow a consistent interface, reducing the risk of regression in the API layer.