from abc import ABC, abstractmethod
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore(ABC):
    """Abstract interface for document storage."""
    
    @abstractmethod
    def add(self, text: str, vector: List[float]) -> int:
        pass

    @abstractmethod
    def search(self, query: str, vector: List[float]) -> List[str]:
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass

class InMemoryStore(DocumentStore):
    """Fallback storage using local memory."""
    
    def __init__(self):
        self.docs_memory = []

    def add(self, text: str, vector: List[float]) -> int:
        doc_id = len(self.docs_memory)
        self.docs_memory.append(text)
        return doc_id

    def search(self, query: str, vector: List[float]) -> List[str]:
        results = []
        for doc in self.docs_memory:
            if query.lower() in doc.lower():
                results.append(doc)
        
        # fallback to the first document if no match found
        if not results and self.docs_memory:
            results = [self.docs_memory[0]]
        return results

    def get_status(self) -> Dict[str, Any]:
        return {"qdrant_ready": False, "in_memory_docs_count": len(self.docs_memory)}

class QdrantStore(DocumentStore):
    """Production-grade storage using Qdrant."""
    
    def __init__(self, client: QdrantClient, collection_name: str = "demo_collection"):
        self.client = client
        self.collection_name = collection_name
        self._setup_collection()

    def _setup_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=128, distance=Distance.COSINE)
        )

    def add(self, text: str, vector: List[float]) -> int:
        doc_id = int(self.client.get_collection(self.collection_name).points_count)
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=doc_id, vector=vector, payload={"text": text})]
        )
        return doc_id

    def search(self, query: str, vector: List[float]) -> List[str]:
        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=2
        ).points

        return [hit.payload["text"] for hit in hits]

    def get_status(self) -> Dict[str, Any]:
        count = self.client.get_collection(self.collection_name).points_count
        return {"qdrant_ready": True, "in_memory_docs_count": count}