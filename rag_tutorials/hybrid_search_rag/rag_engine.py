from pathlib import Path
from raglite import insert_document, hybrid_search, retrieve_chunks, rerank_chunks, rag

class HybridRAGEngine:
    def __init__(self, config):
        self.config = config

    def ingest_document(self, file_path):
        """Insert a document into the RAG system."""
        try:
            insert_document(Path(file_path), config=self.config)
            return True, f"Successfully indexed: {Path(file_path).name}"
        except Exception as e:
            return False, f"Ingestion failed: {str(e)}"

    def search_and_rank(self, query, num_results=10):
        """Perform hybrid search and reranking."""
        try:
            chunk_ids, _ = hybrid_search(query, num_results=num_results, config=self.config)
            if not chunk_ids:
                return []
            chunks = retrieve_chunks(chunk_ids, config=self.config)
            return rerank_chunks(query, chunks, config=self.config)
        except Exception:
            return []

    def stream_rag_response(self, query, chat_history):
        """Stream RAG response with full context synthesis."""
        system_prompt = "You are a knowledgeable assistant. Answer based ONLY on provided context."
        return rag(
            prompt=query,
            system_prompt=system_prompt,
            search=hybrid_search,
            messages=chat_history,
            max_contexts=5,
            config=self.config
        )
