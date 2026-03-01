from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

class LocalRAGEngine:
    def __init__(self, config):
        self.model = config.model
        self.url = config.base_url
        self._init_llm()

    def _init_llm(self):
        self.llm = ChatOllama(model=self.model, base_url=self.url)
        self.embeddings = OllamaEmbeddings(model=self.model, base_url=self.url)

    def ingest_web_page(self, url):
        """Load and index a web page."""
        loader = WebBaseLoader(url)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = splitter.split_documents(docs)
        self.vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        self.retriever = self.vectorstore.as_retriever()

    def query(self, question):
        """Retrieve context and generate answer."""
        if not hasattr(self, 'retriever'): return "No knowledge loaded."
        docs = self.retriever.invoke(question)
        context = "\n\n".join(d.page_content for d in docs)
        prompt = f"Context: {context}\n\nQuestion: {question}"
        resp = self.llm.invoke([('human', prompt)])
        return resp.content
