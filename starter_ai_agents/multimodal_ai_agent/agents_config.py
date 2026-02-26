from agno.agent import Agent
from agno.models.google import Gemini

def get_multimodal_agent(api_key: str, model_id: str = "gemini-2.5-flash"):
    """
    Returns a configured Gemini-powered Multimodal Agent.
    """
    return Agent(
        name="Multimodal Intelligence Analyst",
        model=Gemini(id=model_id, api_key=api_key),
        markdown=True,
        instructions=[
            "You are a sophisticated Multimodal Intelligence Analyst.",
            "Analyze provided media (Images, Videos, or Documents) with high precision.",
            "Focus on practical, actionable insights and detailed reasoning.",
            "For videos, summarize key timestamps and visual events.",
            "For images, perform deep optical and contextual analysis.",
            "If multiple files are provided, correlate information between them.",
            "Always respond in clean markdown format."
        ]
    )
