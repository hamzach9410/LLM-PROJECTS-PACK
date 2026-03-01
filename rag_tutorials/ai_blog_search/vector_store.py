from uuid import uuid4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class BlogVectorManager:
    def __init__(self, vector_store):
        self.vs = vector_store
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=100)

    def ingest_blog(self, url):
        """Crawl and index AI blog content."""
        docs = WebBaseLoader(url).load()
        splits = self.splitter.split_documents(docs)
        ids = [str(uuid4()) for _ in range(len(splits))]
        self.vs.add_documents(documents=splits, ids=ids)
        return len(splits)
