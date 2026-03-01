import json
import re
from typing import Dict, TypedDict, List
from langgraph.graph import END, StateGraph
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class GraphState(TypedDict):
    keys: Dict[str, any]

class CorrectiveGraph:
    def __init__(self, llm_manager, retriever, tavily_key):
        self.llm_manager = llm_manager
        self.retriever = retriever
        self.tavily_key = tavily_key
        self.llm = llm_manager.get_anthropic_llm()

    def retrieve(self, state):
        question = state["keys"]["question"]
        documents = self.retriever.get_relevant_documents(question)
        return {"keys": {"documents": documents, "question": question}}

    def grade_documents(self, state):
        question = state["keys"]["question"]
        documents = state["keys"]["documents"]
        
        prompt = PromptTemplate(template="""Grade relevance of document to question. 
        Return JSON: {{"score": "yes"/"no"}}. 
        Context: {context} Question: {question}""", input_variables=["context", "question"])
        
        chain = prompt | self.llm | StrOutputParser()
        filtered_docs = []
        search = "No"
        
        for d in documents:
            resp = chain.invoke({"question": question, "context": d.page_content})
            score = json.loads(re.search(r'\{.*\}', resp).group())
            if score.get("score") == "yes":
                filtered_docs.append(d)
            else:
                search = "Yes"
        
        return {"keys": {"documents": filtered_docs, "question": question, "run_web_search": search}}

    def generate(self, state):
        question, documents = state["keys"]["question"], state["keys"]["documents"]
        prompt = PromptTemplate(template="Answer based on context: {context}\nQuestion: {question}", input_variables=["context", "question"])
        context = "\n\n".join(d.page_content for d in documents)
        chain = prompt | self.llm | StrOutputParser()
        return {"keys": {"documents": documents, "question": question, "generation": chain.invoke({"context": context, "question": question})}}

    def transform_query(self, state):
        question = state["keys"]["question"]
        prompt = PromptTemplate(template="Optimize this search query: {question}. Return only the query.", input_variables=["question"])
        chain = prompt | self.llm | StrOutputParser()
        return {"keys": {"documents": state["keys"]["documents"], "question": chain.invoke({"question": question})}}

    def web_search_node(self, state):
        from rag_logic import RAGLogic
        question = state["keys"]["question"]
        results = RAGLogic.web_search(question, self.tavily_key)
        content = "\n".join([r.get('content', '') for r in results]) if results else ""
        state["keys"]["documents"].append(Document(page_content=content, metadata={"source": "web"}))
        return state

    def compile_workflow(self):
        workflow = StateGraph(GraphState)
        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("grade_documents", self.grade_documents)
        workflow.add_node("generate", self.generate)
        workflow.add_node("transform_query", self.transform_query)
        # Simplified web search node for modularity
        def web_search_wrapper(state):
             from langchain.schema import Document
             from rag_logic import RAGLogic
             results = RAGLogic.web_search(state["keys"]["question"], self.tavily_key)
             new_doc = Document(page_content="\n".join([r.get('content', '') for r in results]), metadata={"source": "web"})
             state["keys"]["documents"].append(new_doc)
             return state
        
        workflow.add_node("web_search", web_search_wrapper)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges("grade_documents", lambda x: "transform_query" if x["keys"]["run_web_search"] == "Yes" else "generate", {"transform_query": "transform_query", "generate": "generate"})
        workflow.add_edge("transform_query", "web_search")
        workflow.add_edge("web_search", "generate")
        workflow.add_edge("generate", END)
        return workflow.compile()
