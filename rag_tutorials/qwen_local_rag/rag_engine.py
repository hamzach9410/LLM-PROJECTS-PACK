import bs4
import tempfile
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class QwenRAGLogic:
    def __init__(self, vector_store=None):
        self.vector_store = vector_store
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def process_pdf(self, file_bytes, file_name):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file_bytes)
            docs = PyPDFLoader(tmp.name).load()
            for d in docs:
                d.metadata.update({"source": file_name, "type": "pdf", "ts": datetime.now().isoformat()})
            return self.splitter.split_documents(docs)

    def process_web(self, url):
        loader = WebBaseLoader(web_paths=(url,), bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("content", "main"))))
        docs = loader.load()
        for d in docs:
            d.metadata.update({"source": url, "type": "web", "ts": datetime.now().isoformat()})
        return self.splitter.split_documents(docs)

    def retrieve_context(self, query, threshold=0.7):
        if not self.vector_store: return ""
        retriever = self.vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": threshold})
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs]), docs
