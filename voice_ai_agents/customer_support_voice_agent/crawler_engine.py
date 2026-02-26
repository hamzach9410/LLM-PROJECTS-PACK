import os
import uuid
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from firecrawl import FirecrawlApp
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from fastembed import TextEmbedding
from utils import setup_logger

# Initialize logger
logger = setup_logger(__name__)

class CrawlerException(Exception):
    """Base exception for crawler and RAG operations."""
    pass

class CrawlError(CrawlerException):
    """Raised when crawling fails."""
    pass

class VectorDBError(CrawlerException):
    """Raised when Qdrant operations fail."""
    pass

# Constants
DEFAULT_COLLECTION = "docs_embeddings"
    """
    Engine to handle documentation crawling via Firecrawl and 
    Vector Database operations using Qdrant.
    """
    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str = "docs_embeddings"):
        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.embedding_model = TextEmbedding()
        self.collection_name = collection_name
        self._init_collection()

    def _init_collection(self) -> None:
        """Initialize the Qdrant collection if it doesn't exist."""
        test_embedding = list(self.embedding_model.embed(["test"]))[0]
        embedding_dim = len(test_embedding)
        
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
            )
            logger.info(f"Collection {self.collection_name} initialized.")
        except Exception as e:
            if "already exists" not in str(e):
                logger.error(f"Error creating collection: {e}")
                raise e

    def crawl_docs(self, firecrawl_api_key: str, url: str, limit: int = 5) -> List[Dict]:
        """
        Crawl documentation using Firecrawl.
        
        Args:
            firecrawl_api_key (str): Firecrawl API key.
            url (str): Target documentation URL.
            limit (int): Max pages to crawl.
            
        Returns:
            List[Dict]: List of pages with content and metadata.
        """
        logger.info(f"Starting crawl for URL: {url} with limit: {limit}")
        firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        pages = []
        
        response = firecrawl.crawl_url(
            url,
            params={
                'limit': limit,
                'scrapeOptions': {'formats': ['markdown', 'html']}
            }
        )
        
        while True:
            for page in response.get('data', []):
                content = page.get('markdown') or page.get('html', '')
                metadata = page.get('metadata', {})
                source_url = metadata.get('sourceURL', '')
                
                pages.append({
                    "content": content,
                    "url": source_url,
                    "metadata": {
                        "title": metadata.get('title', ''),
                        "description": metadata.get('description', ''),
                        "language": metadata.get('language', 'en'),
                        "crawl_date": datetime.now().isoformat()
                    }
                })
            
            next_url = response.get('next')
            if not next_url:
                break
                
            response = firecrawl.get(next_url)
            time.sleep(1)
        
        logger.info(f"Crawl complete. Retrieved {len(pages)} pages.")
        return pages

    def store_embeddings(self, pages: List[Dict]) -> None:
        """Store crawled pages as embeddings in Qdrant."""
        logger.info(f"Storing embeddings for {len(pages)} pages.")
        for page in pages:
            if not page["content"]:
                continue
            embedding = list(self.embedding_model.embed([page["content"]]))[0]
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding.tolist(),
                        payload={
                            "content": page["content"],
                            "url": page["url"],
                            **page["metadata"]
                        }
                    )
                ]
            )

    def search(self, query: str, limit: int = 3) -> List[Any]:
        """Search for relevant content in the vector database."""
        query_embedding = list(self.embedding_model.embed([query]))[0]
        search_response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=limit,
            with_payload=True
        )
        return search_response.points if hasattr(search_response, 'points') else []

    def reset(self) -> None:
        """Clear all data by deleting and recreating the collection."""
        self.client.delete_collection(collection_name=self.collection_name)
        self._init_collection()
        logger.info("Engine reset complete.")
