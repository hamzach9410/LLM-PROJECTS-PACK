from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

class PharmaConfig:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.embed_model = "models/embedding-001"
        self.chat_model = "gemini-1.5-pro"

    def get_embeddings(self):
        return GoogleGenerativeAIEmbeddings(model=self.embed_model, google_api_key=self.api_key)

    def get_vector_db(self, persist_dir='./pharma_db'):
        return Chroma(
            collection_name="pharma_research_vault",
            embedding_function=self.get_embeddings(),
            persist_directory=persist_dir
        )

    def get_chat_model(self):
        return ChatGoogleGenerativeAI(
            model=self.chat_model,
            google_api_key=self.api_key,
            temperature=0.7
        )
