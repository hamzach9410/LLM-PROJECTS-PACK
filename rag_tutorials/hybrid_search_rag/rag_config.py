import os
from raglite import RAGLiteConfig
from rerankers import Reranker

class HybridRAGConfig:
    def __init__(self, openai_key, anthropic_key, cohere_key, db_url):
        self.openai_key = openai_key
        self.anthropic_key = anthropic_key
        self.cohere_key = cohere_key
        self.db_url = db_url
        self._set_env()

    def _set_env(self):
        os.environ["OPENAI_API_KEY"] = self.openai_key
        os.environ["ANTHROPIC_API_KEY"] = self.anthropic_key
        os.environ["COHERE_API_KEY"] = self.cohere_key

    def get_raglite_config(self):
        """Build and return the raglite configuration object."""
        return RAGLiteConfig(
            db_url=self.db_url,
            llm="claude-3-5-sonnet-20240620",
            embedder="text-embedding-3-large",
            embedder_normalize=True,
            chunk_max_size=2000,
            reranker=Reranker("cohere", api_key=self.cohere_key, lang="en")
        )
