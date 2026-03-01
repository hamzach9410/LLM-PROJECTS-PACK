from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools

def get_autonomous_rag_config(api_key, db_url):
    """
    Configure the autonomous RAG agent with PostgreSQL storage and knowledge base.
    """
    
    # Storage Configuration
    storage = PostgresAgentStorage(table_name="autonomous_rag_storage", db_url=db_url)
    
    # Knowledge Base Configuration
    knowledge_base = PDFUrlKnowledgeBase(
        vector_db=PgVector(
            db_url=db_url,
            collection="autonomous_rag_docs",
            embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=api_key),
        ),
        num_documents=3,
    )
    
    # Agent Configuration
    agent = Agent(
        id="autonomous_rag_agent",
        model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
        storage=storage,
        knowledge=knowledge_base,
        tools=[DuckDuckGoTools()],
        instructions=[
            "Search your knowledge base first for high-fidelity information.",
            "If the information is missing from the knowledge base, search the internet using DuckDuckGo.",
            "Synthesize both internal and external information into a clear response.",
            "Always include source citations where possible.",
        ],
        search_knowledge=True,
        markdown=True,
    )
    
    return knowledge_base, agent
