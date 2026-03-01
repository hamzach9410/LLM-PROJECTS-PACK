from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder

def get_gpt5_agent(openai_key):
    """
    Configure the GPT-5 (Agentic) RAG agent and its knowledge base.
    """
    
    # Knowledge Base Configuration
    kb = Knowledge(
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="gpt5_agentic_rag",
            search_type=SearchType.vector,
            embedder=OpenAIEmbedder(api_key=openai_key),
        ),
    )
    
    # Agent Configuration
    agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=openai_key), # Using gpt-4o as real model
        knowledge=kb,
        search_knowledge=True,
        instructions=[
            "Always search your knowledge before answering.",
            "Synthesize information into professional, markdown-formatted responses.",
            "Use headers and bullet points to organize complex data.",
        ],
        markdown=True,
    )
    
    return agent, kb
