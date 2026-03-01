import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_core.embeddings import Embeddings
from typing import List

class GeminiEmbedder(Embeddings):
    """Wrapper for Google Generative AI embeddings."""
    def __init__(self, api_key, model_name="models/text-embedding-004"):
        genai.configure(api_key=api_key)
        self.model = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        response = genai.embed_content(model=self.model, content=text, task_type="retrieval_document")
        return response['embedding']

class VectorManager:
    def __init__(self, url, api_key, google_key):
        self.client = QdrantClient(url=url, api_key=api_key, timeout=60)
        self.google_key = google_key
        self.collection_name = "gemini-agentic-rag"

    def setup_collection(self, vector_size=768):
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            return True, "Collection created."
        except Exception as e:
            if "already exists" in str(e).lower():
                return True, "Collection exists."
            return False, str(e)

    def get_vectorstore(self):
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=GeminiEmbedder(api_key=self.google_key)
        )
