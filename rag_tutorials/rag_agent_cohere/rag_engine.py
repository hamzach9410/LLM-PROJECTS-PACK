import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_core.messages import HumanMessage

class CohereRAGEngine:
    def __init__(self, chat_model, vector_store, fallback_agent):
        self.model = chat_model
        self.vs = vector_store
        self.fallback = fallback_agent

    def process_pdf(self, file_bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file_bytes)
            docs = PyPDFLoader(tmp.name).load()
            os.unlink(tmp.name)
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            return splitter.split_documents(docs)

    def execute_query(self, query):
        """Execute RAG with fallback to web search."""
        retriever = self.vs.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": 0.7})
        relevant_docs = retriever.invoke(query)

        if relevant_docs:
            qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            combine_chain = create_stuff_documents_chain(self.model, qa_prompt)
            chain = create_retrieval_chain(retriever, combine_chain)
            resp = chain.invoke({"input": query})
            return resp['answer'], relevant_docs
        else:
            # Fallback to web search agent
            input_msg = {"messages": [HumanMessage(content=f"Research and answer: {query}")]}
            resp = self.fallback.invoke(input_msg)
            answer = resp["messages"][-1].content
            return f"Web Intelligence: {answer}", []
