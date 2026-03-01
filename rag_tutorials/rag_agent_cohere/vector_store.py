from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

class QdrantManager:
    def __init__(self, url, api_key, collection="cohere_research_index"):
        self.client = QdrantClient(url=url, api_key=api_key, timeout=60)
        self.collection = collection

    def ensure_collection(self, size=1024):
        try:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE)
            )
        except Exception as e:
            if "already exists" not in str(e).lower(): raise e

    def get_vector_store(self, embedding_model):
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection,
            embedding=embedding_model
        )
