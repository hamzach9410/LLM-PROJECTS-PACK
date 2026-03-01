import os
from agno.agent import Agent
from agno.models.together import TogetherChat
from dotenv import load_dotenv

load_dotenv()

def get_moa_agents():
    """
    Define the reference models and the aggregator agent.
    """
    
    # Reference models for diverse perspectives
    reference_models = [
        "Qwen/Qwen2-72B-Instruct",
        "Qwen/Qwen1.5-72B-Chat",
        "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "databricks/dbrx-instruct",
    ]
    
    # Aggregator persona for final synthesis
    aggregator_agent = Agent(
        name="MOA Aggregator",
        model=TogetherChat(id="mistralai/Mixtral-8x22B-Instruct-v0.1"),
        description="A specialized synthesis agent that aggregates multiple model responses into a single high-quality answer.",
        instructions=[
            "You have been provided with a set of responses from various open-source models.",
            "Your task is to synthesize these responses into a single, high-quality, and accurate response.",
            "Critically evaluate the information, resolving contradictions and removing biases.",
            "Offer a refined, comprehensive reply that adheres to the highest standards of reliability.",
            "Ensure the final output is well-structured and easy to read."
        ],
        markdown=True
    )
    
    return reference_models, aggregator_agent
