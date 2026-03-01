import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain_community.tools import TavilySearchResults
from langchain.schema import Document
from tenacity import retry, stop_after_attempt, wait_exponential

class RAGLogic:
    @staticmethod
    def load_document(file_path_or_url, is_url=True):
        """Load documents from URL or local file."""
        try:
            if is_url:
                loader = WebBaseLoader(file_path_or_url)
            else:
                ext = os.path.splitext(file_path_or_url)[1].lower()
                if ext == '.pdf': loader = PyPDFLoader(file_path_or_url)
                elif ext in ['.txt', '.md']: loader = TextLoader(file_path_or_url)
                else: raise ValueError("Unsupported format")
            return loader.load()
        except Exception:
            return []

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def web_search(query, api_key):
        """Perform search using Tavily."""
        if not api_key: return None
        tool = TavilySearchResults(api_key=api_key, max_results=3)
        return tool.invoke({"query": query})
