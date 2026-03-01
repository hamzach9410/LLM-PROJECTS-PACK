import os
import tempfile
import bs4
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DeepSeekRAGEngine:
    def __init__(self, vector_store, rag_agent, web_agent=None):
        self.vstore = vector_store
        self.rag_agent = rag_agent
        self.web_agent = web_agent

    def process_document(self, file_bytes=None, url=None):
        """Process PDF bytes or a Web URL into text chunks."""
        documents = []
        if file_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(file_bytes)
                loader = PyPDFLoader(tmp.name)
                documents = loader.load()
            os.unlink(tmp.name)
        elif url:
            loader = WebBaseLoader(web_paths=(url,), bs_kwargs={"parse_only": bs4.SoupStrainer(class_=("content", "main"))})
            documents = loader.load()
        
        if documents:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            return splitter.split_documents(documents)
        return []

    def run_rag_query(self, query, threshold=0.7, force_web=False):
        """Execute the RAG pipeline with optional web fallback."""
        context = ""
        
        if not force_web and self.vstore:
            retriever = self.vstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": threshold})
            docs = retriever.invoke(query)
            if docs:
                context = "\n\n".join([d.page_content for d in docs])
        
        if (force_web or not context) and self.web_agent:
            web_resp = self.web_agent.run(query)
            context = f"Web Research Context:\n{web_resp.content}"
            
        full_prompt = f"Context: {context}\n\nQuestion: {query}" if context else query
        return self.rag_agent.run(full_prompt)
