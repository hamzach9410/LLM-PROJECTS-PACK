import os
import uuid
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from fastembed import TextEmbedding

# Configure logger for this module
logger = logging.getLogger(__name__)

class RAGException(Exception):
    """Base exception for RAG operations."""
    pass

class CollectionError(RAGException):
    """Raised when collection operations fail."""
    pass

class StorageError(RAGException):
    """Raised when storing documents fails."""
    pass

# Constants
COLLECTION_NAME = "voice-rag-agent"

class RAGEngine:
    """
    Engine to handle Vector Database operations using Qdrant and FastEmbed.
    """
    def __init__(self, qdrant_url: str, qdrant_api_key: str):
        """
        Initialize the RAG engine with Qdrant credentials.
        
        Args:
            qdrant_url (str): The URL of the Qdrant instance.
            qdrant_api_key (str): The API key for authentication.
        """
        try:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            self.embedding_model = TextEmbedding()
            self._init_collection()
            logger.info("RAG Engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize QdrantClient: {e}")
            raise CollectionError(f"Initialization failed: {e}")

    def _init_collection(self) -> None:
        """
        Initialize the Qdrant collection if it doesn't exist.
        
        Raises:
            CollectionError: If collection creation fails.
        """
        try:
            test_embedding = list(self.embedding_model.embed(["test"]))[0]
            embedding_dim = len(test_embedding)
            
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=embedding_dim,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Collection {COLLECTION_NAME} created.")
        except Exception as e:
            if "already exists" not in str(e):
                logger.error(f"Error creating collection: {e}")
                raise CollectionError(f"Could not create collection: {e}")
            logger.debug(f"Collection {COLLECTION_NAME} already exists.")

    def store_documents(self, documents: List[Any]) -> None:
        """
        Store document embeddings in the Qdrant collection.
        
        Args:
            documents (List): List of LangChain documents.
        """
        try:
            for doc in documents:
                embedding = list(self.embedding_model.embed([doc.page_content]))[0]
                self.client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=[
                        models.PointStruct(
                            id=str(uuid.uuid4()),
                            vector=embedding.tolist(),
                            payload={
                                "content": doc.page_content,
                                **doc.metadata
                            }
                        )
                    ]
                )
            logger.info(f"Successfully stored {len(documents)} document chunks.")
        except Exception as e:
            logger.error(f"Failed to store documents: {e}")
            raise StorageError(f"Storage failed: {e}")

    def query(self, query: str, limit: int = 3) -> List[Any]:
        """
        Search for documents relevant to the query.
        
        Args:
            query (str): The user search string.
            limit (int): Max number of results.
            
        Returns:
            List: Matching points from Qdrant.
        """
        try:
            query_embedding = list(self.embedding_model.embed([query]))[0]
            
            search_response = self.client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_embedding.tolist(),
                limit=limit,
                with_payload=True
            )
            
            points = search_response.points if hasattr(search_response, 'points') else []
            logger.info(f"Found {len(points)} results for query: '{query}'")
            return points
        except Exception as e:
            logger.error(f"Query operation failed: {e}")
            return []

    def clear_collection(self) -> None:
        """
        Remove all data by deleting and recreating the collection.
        """
        try:
            self.client.delete_collection(collection_name=COLLECTION_NAME)
            self._init_collection()
            logger.info("Collection cleared and re-initialized.")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise CollectionError(f"Clear operation failed: {e}")
