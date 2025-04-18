# answer_engine.py

from vector_store import VectorStore

class AnswerEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def answer(self, question: str, top_k: int = 1) -> str:
        # Search vector store
        results = self.vector_store.search(question, top_k=top_k)
        
        if not results:
            return "Sorry, I couldn't find an answer."

        # For now, just return the top document's snippet
        top_result = results[0]
        snippet = top_result['content'][:500]  # Limit to 500 chars

        return f"🔎 Based on this page: {top_result['url']}\n\n{snippet}"
