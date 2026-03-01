import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from agno.models.openai import OpenAIChat

class RoutingConfig:
    def __init__(self, openai_key, qdrant_url, qdrant_key):
        self.openai_key = openai_key
        self.qdrant_url = qdrant_url
        self.qdrant_key = qdrant_key
        os.environ["OPENAI_API_KEY"] = openai_key

    def get_embeddings(self):
        return OpenAIEmbeddings(model="text-embedding-3-small")

    def get_llm(self, temperature=0):
        return ChatOpenAI(temperature=temperature, model="gpt-4o")

    def get_agno_model(self):
        return OpenAIChat(id="gpt-4o", api_key=self.openai_key)

    def get_qdrant_client(self):
        return QdrantClient(url=self.qdrant_url, api_key=self.qdrant_key)

    def get_vector_store(self, collection_name):
        return QdrantVectorStore(
            client=self.get_qdrant_client(),
            collection_name=collection_name,
            embedding=self.get_embeddings()
        )
