from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.exa import ExaTools

def get_web_search_agent(exa_key, domains=None):
    """Initialize a specialized web search agent."""
    return Agent(
        name="Web Intelligence Agent",
        model=Ollama(id="llama3.2"),
        tools=[ExaTools(api_key=exa_key, include_domains=domains, num_results=5)],
        instructions=[
            "Search the web for relevant intelligence data.",
            "Synthesize findings with clear source attribution.",
        ],
        markdown=True
    )

def get_qwen_rag_agent(model_id):
    """Initialize the main reasoning RAG agent."""
    return Agent(
        name="Qwen Strategic Agent",
        model=Ollama(id=model_id),
        instructions=[
            "You are a strategic intelligence analyst.",
            "Base your reasoning on the provided document context or web search results.",
            "Maintain high precision and cite specific technical details.",
        ],
        markdown=True
    )
