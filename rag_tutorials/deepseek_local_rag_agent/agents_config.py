from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.exa import ExaTools

def get_deepseek_agents(model_version, exa_api_key=None, search_domains=None):
    """
    Configure the DeepSeek RAG agent and an optional web search agent.
    """
    
    # Main DeepSeek RAG Agent
    rag_agent = Agent(
        name="DeepSeek RAG Agent",
        model=Ollama(id=model_version),
        instructions=[
            "You are an Intelligent Agent specializing in local RAG with DeepSeek-R1.",
            "Analyze questions deeply and providing reasoning-rich answers.",
            "Focus on information from the provided documents when available.",
            "Cite specific details from the context.",
            "If information is from a web search, label it clearly.",
            "Maintain high precision and technical clarity.",
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Optional Web Search Agent (Exa)
    web_agent = None
    if exa_api_key:
        web_agent = Agent(
            name="Exa Search Agent",
            model=Ollama(id="llama3.2"), # Use a faster model for search synthesis
            tools=[ExaTools(
                api_key=exa_api_key,
                include_domains=search_domains or ["arxiv.org", "wikipedia.org"],
                num_results=5
            )],
            instructions=[
                "Perform high-fidelity web searches using Exa UI.",
                "Summarize the most relevant findings related to the query.",
                "Always include source URLs in your findings.",
            ],
            show_tool_calls=True,
            markdown=True,
        )
        
    return rag_agent, web_agent
