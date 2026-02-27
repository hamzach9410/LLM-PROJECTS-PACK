from agno.agent import Agent
from agno.models.openai import OpenAIChat

def get_regular_agent(api_key: str, model_id: str = "gpt-4o-mini"):
    return Agent(
        name="Standard Agent",
        role="Provides direct, concise answers to user queries.",
        model=OpenAIChat(id=model_id, api_key=api_key),
        markdown=True,
    )

def get_reasoning_agent(api_key: str, model_id: str = "gpt-4o"):
    return Agent(
        name="Reasoning Agent",
        role="Provides deep, logical, and step-by-step reasoning for complex queries.",
        model=OpenAIChat(id=model_id, api_key=api_key),
        reasoning=True,
        markdown=True,
        structured_outputs=True,
        description="I am an advanced logical reasoning agent. I break down complex problems into verifiable steps before providing a final answer."
    )
