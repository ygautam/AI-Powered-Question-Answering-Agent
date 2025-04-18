from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embeddings = []
        self.texts = []
        self.urls = []
        self.index = None

    def add_documents(self, docs):
        """
        docs: List of dicts with 'url' and 'content'
        """
        self.texts = [doc['content'] for doc in docs]
        self.urls = [doc['url'] for doc in docs]
        self.embeddings = self.model.encode(self.texts, show_progress_bar=True)
        if not self.embeddings:
            raise ValueError("No embeddings found. Cannot build index.")
        self._build_index()

    def _build_index(self):
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def search(self, query, top_k=3):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        results = []
        for i in indices[0]:
            results.append({
                "url": self.urls[i],
                "content": self.texts[i]
            })
        return results
