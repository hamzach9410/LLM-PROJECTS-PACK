from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os

load_dotenv()

def get_analysis_agents():
    """
    Define specialized agents for autonomous data analysis and research.
    """
    
    # Data Analyst Agent
    data_analyst = Agent(
        name="Scientific Data Analyst",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A specialized agent that analyzes datasets, extracts patterns, and provides statistical insights.",
        instructions=[
            "Analyze the provided data or description thoroughly.",
            "Identify key trends, anomalies, and correlations.",
            "Provide quantitative insights and structured summaries.",
            "Use clear, professional language suitable for a research report."
        ],
        markdown=True
    )
    
    # Research Integrator Agent
    research_integrator = Agent(
        name="Research Integrator",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGoTools()],
        description="A research agent that finds external context and literature to support data findings.",
        instructions=[
            "Search for relevant scientific literature or market trends related to the data findings.",
            "Synthesize external research with the internal analysis.",
            "Cite sources clearly using DuckDuckGo search results.",
            "Provide a comprehensive 'Contextualized Analysis' report."
        ],
        markdown=True
    )
    
    return data_analyst, research_integrator
