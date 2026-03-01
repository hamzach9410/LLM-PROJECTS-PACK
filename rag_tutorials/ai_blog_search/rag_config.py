from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

class BlogSearchConfig:
    def __init__(self, gemini_key, qdrant_host, qdrant_key):
        self.gemini_key = gemini_key
        self.qdrant_host = qdrant_host
        self.qdrant_key = qdrant_key

    def get_embeddings(self):
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.gemini_key)

    def get_qdrant_client(self):
        return QdrantClient(url=self.qdrant_host, api_key=self.qdrant_key)

    def get_vector_store(self, collection="ai_blog_vault"):
        return QdrantVectorStore(
            client=self.get_qdrant_client(),
            collection_name=collection,
            embedding=self.get_embeddings()
        )

    def get_llm(self, temperature=0, model="gemini-2.0-flash"):
        return ChatGoogleGenerativeAI(api_key=self.gemini_key, temperature=temperature, model=model, streaming=True)
