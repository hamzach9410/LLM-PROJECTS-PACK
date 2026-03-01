from ragie_client import RagieClient
from anthropic_client import AnthropicClient

class RAGServiceEngine:
    def __init__(self, ragie_key, anthropic_key):
        self.ragie = RagieClient(ragie_key)
        self.anthropic = AnthropicClient(anthropic_key)

    def ingest_new_source(self, url, name=None, mode="fast"):
        """Pipeline to ingest new documentation."""
        return self.ragie.upload_url(url, name, mode)

    def run_strategic_query(self, query, scope="tutorial"):
        """Full retrieval-synthesis pipeline execution."""
        chunks = self.ragie.retrieve_scored_chunks(query, scope)
        if not chunks:
            return "No relevant intelligence found in the indexed repository."
        return self.anthropic.generate_rag_response(query, chunks)
