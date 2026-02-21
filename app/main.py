from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAG Service Refactored",
    description="Modular RAG application with LangGraph and Qdrant storage.",
    version="1.0.0"
)

# Attach API routes to the main application
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Entry point for local development
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)