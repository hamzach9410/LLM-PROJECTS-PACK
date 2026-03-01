from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant

class VectorStoreManager:
    def __init__(self, url, api_key, embeddings):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.embeddings = embeddings
        self.collection_name = "corrective-rag-collection"

    def setup_collection(self, vector_size=1536):
        """Create or reset the Qdrant collection."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def get_vectorstore(self):
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

    def add_documents(self, documents):
        vectorstore = self.get_vectorstore()
        vectorstore.add_documents(documents)
        return vectorstore.as_retriever()
