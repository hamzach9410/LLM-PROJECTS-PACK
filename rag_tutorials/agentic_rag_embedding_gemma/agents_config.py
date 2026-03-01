from agno.agent import Agent
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama
from agno.vectordb.lancedb import LanceDb, SearchType

def get_rag_config():
    """
    Configure the knowledge base and agent for Agentic RAG.
    """
    
    # Knowledge Base Configuration
    knowledge_base = Knowledge(
        vector_db=LanceDb(
            table_name="agentic_rag_gemma",
            uri="tmp/lancedb",
            search_type=SearchType.vector,
            embedder=OllamaEmbedder(id="embeddinggemma:latest", dimensions=768),
        ),
    )
    
    # Agent Configuration
    agent = Agent(
        model=Ollama(id="llama3.2:latest"),
        knowledge=knowledge_base,
        instructions=[
            "Search the knowledge base for relevant information and base your answers on it.",
            "Be clear, and generate well-structured answers.",
            "Use clear headings, bullet points, or numbered lists where appropriate.",
            "If the information is not in the knowledge base, state that clearly.",
        ],
        search_knowledge=True,
        markdown=True,
    )
    
    return knowledge_base, agent
