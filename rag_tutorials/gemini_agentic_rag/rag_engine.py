import os
import tempfile
import bs4
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class GeminiRAGEngine:
    def __init__(self, vector_store, rewriter, rag_agent, web_agent=None):
        self.vstore = vector_store
        self.rewriter = rewriter
        self.rag_agent = rag_agent
        self.web_agent = web_agent

    def process_source(self, file_bytes=None, url=None):
        """Process PDF or Web URL into split document chunks."""
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

    def execute_rag_flow(self, query, threshold=0.7, force_web=False):
        """Orchestrate query rewriting, retrieval, and generation."""
        # 1. Rewrite Query
        rewritten = self.rewriter.run(query).content
        
        context = ""
        # 2. Document Search
        if not force_web and self.vstore:
            retriever = self.vstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": threshold})
            docs = retriever.invoke(rewritten)
            if docs:
                context = "\n\n".join([d.page_content for d in docs])
        
        # 3. Web Search Fallback
        if (force_web or not context) and self.web_agent:
            web_resp = self.web_agent.run(rewritten)
            context = f"Web Research Context:\n{web_resp.content}"
            
        # 4. Final Reasoning
        full_prompt = f"Original Query: {query}\nRewritten: {rewritten}\nContext: {context}"
        return self.rag_agent.run(full_prompt), rewritten
