from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from agno.embedder.ollama import OllamaEmbedder
from langchain_core.embeddings import Embeddings
from typing import List

class LocalEmbedder(Embeddings):
    """Wrapper for OllamaEmbedder to be compatible with LangChain components."""
    def __init__(self, model_name="snowflake-arctic-embed"):
        self.embedder = OllamaEmbedder(id=model_name, dimensions=1024)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embedder.get_embedding(text)

class VectorManager:
    def __init__(self, url, api_key):
        self.client = QdrantClient(url=url, api_key=api_key, timeout=60)
        self.collection_name = "deepseek-local-rag"

    def setup_collection(self, vector_size=1024):
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
            embedding=LocalEmbedder()
        )
