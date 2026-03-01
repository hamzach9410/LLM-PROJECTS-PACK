from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.ollama import OllamaEmbedder

def get_local_agent(model_id="llama3.2", collection="local-research-index"):
    """Configure the local Ollama agent with Qdrant storage."""
    
    # Vector DB Setup
    vector_db = Qdrant(
        collection=collection,
        url="http://localhost:6333/",
        embedder=OllamaEmbedder()
    )
    
    # Knowledge Base
    kb = Knowledge(vector_db=vector_db)
    
    # Agent
    agent = Agent(
        name="Local Privacy Agent",
        model=Ollama(id=model_id),
        knowledge=kb,
        search_knowledge=True,
        instructions=[
            "Search local knowledge base for accurate recipes or data.",
            "Maintain privacy and provide clear, structured responses.",
        ],
        markdown=True
    )
    
    return agent, kb
