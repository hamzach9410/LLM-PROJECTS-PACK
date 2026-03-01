from raglite import RAGLiteConfig
from rerankers import Reranker

class LocalHybridConfig:
    def __init__(self, db_url, llm_path, embedder_path):
        self.db_url = db_url
        self.llm_path = llm_path
        self.embedder_path = embedder_path

    def get_raglite_config(self):
        """Construct the raglite config for local GGUF execution."""
        return RAGLiteConfig(
            db_url=self.db_url,
            llm=f"llama-cpp-python/{self.llm_path}",
            embedder=f"llama-cpp-python/{self.embedder_path}",
            embedder_normalize=True,
            chunk_max_size=512,
            reranker=Reranker("ms-marco-MiniLM-L-12-v2", model_type="flashrank")
        )
