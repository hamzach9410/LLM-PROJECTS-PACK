from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.exa import ExaTools

def get_gemini_agents(google_key, exa_key=None, search_domains=None):
    """
    Configure Gemini agents for rewriting, searching, and RAG reasoning.
    """
    
    # 1. Query Rewriter Agent
    rewriter = Agent(
        name="Query Rewriter",
        model=Gemini(id="gemini-2.0-flash", api_key=google_key),
        instructions=[
            "Reformulate user questions to be more precise and search-optimized.",
            "Expand acronyms and technical terms.",
            "Return ONLY the rewritten query.",
        ],
    )
    
    # 2. Web Search Agent (Optional)
    web_agent = None
    if exa_key:
        web_agent = Agent(
            name="Exa Search Agent",
            model=Gemini(id="gemini-2.0-flash", api_key=google_key),
            tools=[ExaTools(api_key=exa_key, include_domains=search_domains, num_results=5)],
            instructions=[
                "Search the web for relevant context and synthesize findings.",
                "Always include source URLs.",
            ],
            show_tool_calls=True,
        )
        
    # 3. Main RAG Reasoning Agent
    rag_agent = Agent(
        name="Gemini RAG Agent",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21", api_key=google_key),
        instructions=[
            "You are an expert RAG analyst using Gemini 2.0 Flash Thinking.",
            "Focus on precision and cite specific details from provided context.",
            "Clearly label information originating from web search vs document storage.",
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    return rewriter, web_agent, rag_agent
