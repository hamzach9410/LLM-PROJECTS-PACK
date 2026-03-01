import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class PharmaRAGEngine:
    def __init__(self, config, vector_db):
        self.config = config
        self.db = vector_db
        self.splitter = SentenceTransformersTokenTextSplitter(
            model_name="sentence-transformers/all-mpnet-base-v2",
            chunk_size=100,
            chunk_overlap=50
        )

    def ingest_pdfs(self, uploaded_files):
        """Process and add specialized pharma docs to the vault."""
        for f in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(f.getbuffer())
                loader = PyPDFLoader(tmp.name)
                data = loader.load()
                os.unlink(tmp.name)
                
                chunks = self.splitter.create_documents(
                    [d.page_content for d in data],
                    [d.metadata for d in data]
                )
                self.db.add_documents(chunks)

    def query_vault(self, query):
        """Execute protected pharma research query."""
        retriever = self.db.as_retriever(search_type="similarity", search_kwargs={'k': 5})
        
        prompt = ChatPromptTemplate.from_template("""
            You are a senior pharmaceutical research scientist.
            Answer the technical question based ONLY on the provided research context:
            Context: {context}
            Question: {question}
            Provide a precise, concise response without introductory fluff.
        """)

        chain = (
            {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
             "question": RunnablePassthrough()}
            | prompt 
            | self.config.get_chat_model() 
            | StrOutputParser()
        )
        return chain.invoke(query)
