from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType

def get_rag_reasoning_config(google_key, openai_key):
    """
    Configure the knowledge base and reasoning agent.
    """
    
    # Knowledge Base Configuration
    knowledge_base = Knowledge(
        vector_db=LanceDb(
            table_name="agentic_rag_reasoning",
            uri="tmp/lancedb",
            search_type=SearchType.vector,
            embedder=OpenAIEmbedder(api_key=openai_key),
        ),
    )
    
    # Agent Configuration with Reasoning Tools
    agent = Agent(
        model=Gemini(id="gemini-2.5-flash", api_key=google_key),
        knowledge=knowledge_base,
        search_knowledge=True,
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "Search the knowledge base for relevant information before answering.",
            "Reason through the information step-by-step for complex requests.",
            "Include sources and citations in your response.",
            "Always respond in clean markdown format.",
        ],
        markdown=True,
    )
    
    return knowledge_base, agent
