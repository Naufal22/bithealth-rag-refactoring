from pydantic import BaseModel
from typing import List

# Data models for incoming requests
class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str

# Data models for API responses
class QuestionResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str]
    latency_sec: float

class DocumentResponse(BaseModel):
    id: int
    status: str

class StatusResponse(BaseModel):
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool