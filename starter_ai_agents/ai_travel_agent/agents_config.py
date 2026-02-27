from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

def get_researcher_agent(openai_api_key: str, serp_api_key: str):
    return Agent(
        name="Travel Researcher",
        role="Searches for travel destinations, activities, and accommodations",
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        description=dedent("""
            You are a world-class travel researcher. Your goal is to find the most relevant 
            activities, accommodations, and travel tips for a specific destination.
        """),
        instructions=[
            "Generate 3-5 specific search terms for the destination and duration.",
            "Use `search_google` for each term and analyze the top results.",
            "Return the 10 most relevant results with sources.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_context=True,
    )

def get_planner_agent(openai_api_key: str):
    return Agent(
        name="Itinerary Planner",
        role="Synthesizes research into a cohesive travel itinerary",
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        description=dedent("""
            You are a senior travel planner. You transform raw research data into 
            engaging, well-structured travel itineraries.
        """),
        instructions=[
            "Create a day-by-day itinerary (e.g., 'Day 1: ...').",
            "Include suggested activities, dining, and accommodations.",
            "Ensure nuanced descriptions and proper attribution of facts.",
            "Format the output in clean Markdown.",
        ],
        add_datetime_to_context=True,
    )
