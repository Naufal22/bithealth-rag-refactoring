from typing import TypedDict, Any, Dict
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    """State definition for the LangGraph workflow."""
    question: str
    context: str
    answer: str

class RagWorkflow:
    """Orchestrates the RAG process using LangGraph."""

    def __init__(self, document_store: Any, embedding_service: Any):
        # Inject dependencies to avoid global state
        self.store = document_store
        self.embedder = embedding_service
        self.app = self._build_graph()

    def _retrieve_node(self, state: GraphState) -> Dict[str, Any]:
        """Fetch relevant documents based on the question."""
        vector = self.embedder.get_embedding(state["question"])
        docs = self.store.search(query=state["question"], vector=vector)
        
        # Original behavior: join docs or provide empty context
        context = "\n".join(docs) if docs else ""
        return {"context": context}

    def _generate_node(self, state: GraphState) -> Dict[str, Any]:
        """Generate a simulated answer using retrieved context."""
        # Maintaining original "dumb" behavior per instructions
        response = f"Simulated answer for '{state['question']}' using context: {state['context']}"
        return {"answer": response}

    def _build_graph(self):
        """Configure nodes and edges for the workflow."""
        workflow = StateGraph(GraphState)

        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate", self._generate_node)

        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def run(self, question: str) -> Dict[str, Any]:
        """Execution entry point for the workflow."""
        initial_state = {"question": question, "context": "", "answer": ""}
        return self.app.invoke(initial_state)