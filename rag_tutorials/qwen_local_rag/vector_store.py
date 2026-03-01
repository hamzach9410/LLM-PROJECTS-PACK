from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from agno.knowledge.embedder.ollama import OllamaEmbedder
from langchain_core.embeddings import Embeddings
from typing import List

class OllamaEmbedderr(Embeddings):
    def __init__(self, model_id="snowflake-arctic-embed"):
        self.embedder = OllamaEmbedder(id=model_id, dimensions=1024)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embedder.get_embedding(text)

class QwenVectorManager:
    def __init__(self, url="http://localhost:6333", collection="qwen-research-index"):
        self.client = QdrantClient(url=url)
        self.collection = collection

    def ensure_collection(self):
        try:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
        except Exception as e:
            if "already exists" not in str(e).lower(): raise e

    def get_vector_store(self):
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection,
            embedding=OllamaEmbedderr()
        )
