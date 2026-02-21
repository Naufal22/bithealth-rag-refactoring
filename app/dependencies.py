from qdrant_client import QdrantClient
from app.services.embedding import EmbeddingService
from app.services.storage import QdrantStore, InMemoryStore
from app.services.workflow import RagWorkflow

# Initialize core services
embedding_service = EmbeddingService()

try:
    # Attempt to initialize production-grade storage
    client = QdrantClient(":memory:") 
    document_store = QdrantStore(client)
except Exception:
    # Fallback to local memory storage on failure
    document_store = InMemoryStore()

# Main workflow orchestration
rag_workflow = RagWorkflow(document_store, embedding_service)

def get_store():
    """Dependency provider for document storage."""
    return document_store

def get_embedder():
    """Dependency provider for embedding service."""
    return embedding_service

def get_workflow():
    """Dependency provider for RAG workflow."""
    return rag_workflow