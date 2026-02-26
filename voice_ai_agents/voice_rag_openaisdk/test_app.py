import os
import pytest
from unittest.mock import MagicMock
from rag_engine import RAGEngine
from utils import process_pdf

def test_utils_pdf_processing_failure():
    """Test utility function handles invalid files gracefully."""
    mock_file = MagicMock()
    mock_file.getvalue.return_value = b"not a pdf"
    mock_file.name = "test.pdf"
    
    chunks = process_pdf(mock_file)
    assert chunks == []

def test_rag_engine_init():
    """Test RAG Engine initialization (mocked)."""
    with pytest.raises(Exception):
        # Should fail without valid keys/network
        RAGEngine("http://invalid", "key")

# More comprehensive tests would require mocking QdrantClient and FastEmbed
