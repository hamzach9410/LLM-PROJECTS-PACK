from agno.agent import Agent
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
import numpy as np

class MultiSourceRouter:
    def __init__(self, config):
        self.config = config
        self.collections = {
            "products": "Product Specs & Manuals",
            "support": "Customer Operations & FAQ",
            "finance": "Financial Reports & Revenue"
        }

    def get_routing_agent(self):
        return Agent(
            model=self.config.get_agno_model(),
            description="Expert query router for Product, Support, and Finance silos.",
            instructions=[
                "Return exactly one: 'products', 'support', or 'finance'.",
                "Products: Specs, features, manuals.",
                "Support: Help, guides, troubleshooting.",
                "Finance: Costs, revenue, reports.",
                "Return ONLY the keyword."
            ]
        )

    def route_query(self, query):
        """Hybrid routing: Semantic confidence -> Agentic classification."""
        best_score, best_db = -1, None
        for key in self.collections:
            vs = self.config.get_vector_store(key)
            hits = vs.similarity_search_with_score(query, k=1)
            if hits and hits[0][1] > best_score:
                best_score, best_db = hits[0][1], key
        
        if best_score > 0.7:
            return best_db
        
        # Fallback to Agent
        agent = self.get_routing_agent()
        res = agent.run(query)
        return res.content.strip().lower()

    def execute_rag(self, query, source):
        """Execute RAG against a specific data silo."""
        vs = self.config.get_vector_store(source)
        retriever = vs.as_retriever(search_kwargs={"k": 4})
        
        prompt = ChatPromptTemplate.from_template("""
            Answer using the following context only: {context}
            Question: {input}
        """)
        
        chain = create_retrieval_chain(retriever, create_stuff_documents_chain(self.config.get_llm(), prompt))
        return chain.invoke({"input": query})

    def web_fallback(self, query):
        """Emergency web research fallback."""
        tool = DuckDuckGoSearchRun()
        agent = create_react_agent(self.config.get_llm(), tools=[tool])
        res = agent.invoke({"messages": [HumanMessage(content=query)]})
        return res["messages"][-1].content
