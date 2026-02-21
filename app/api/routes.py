import time
from fastapi import APIRouter, Depends
from app.schemas import (
    DocumentRequest, DocumentResponse, 
    QuestionRequest, QuestionResponse, 
    StatusResponse
)
from app.dependencies import get_workflow, get_store, get_embedder

router = APIRouter()

@router.post("/add", response_model=DocumentResponse)
async def add_document(
    req: DocumentRequest, 
    store=Depends(get_store), 
    embedder=Depends(get_embedder)
):
    """Adds a document to the store after generating its embedding."""
    vector = embedder.get_embedding(req.text)
    doc_id = store.add(text=req.text, vector=vector)
    
    return DocumentResponse(id=doc_id, status="success")

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    req: QuestionRequest, 
    workflow=Depends(get_workflow)
):
    """Processes a query through the RAG workflow and returns a response."""
    start_time = time.perf_counter()
    result = workflow.run(req.question)
    latency = time.perf_counter() - start_time
    
    return QuestionResponse(
        question=req.question,
        answer=result["answer"],
        context_used=[result["context"]],
        latency_sec=round(latency, 4)
    )

@router.get("/status", response_model=StatusResponse)
async def get_system_status(store=Depends(get_store)):
    """Returns the current readiness and document count of the storage."""
    status = store.get_status()
    return StatusResponse(
        qdrant_ready=status["qdrant_ready"],
        in_memory_docs_count=status["in_memory_docs_count"],
        graph_ready=True
    )