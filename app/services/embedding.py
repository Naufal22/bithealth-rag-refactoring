import random

class EmbeddingService:
    """Service to handle embedding generation."""
    
    def __init__(self, vector_size: int = 128):
        self.vector_size = vector_size

    def get_embedding(self, text: str) -> list[float]:
        # Seed ensures deterministic output for the same text
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)]