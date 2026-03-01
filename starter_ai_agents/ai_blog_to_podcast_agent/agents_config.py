import os
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

def get_podcast_agents():
    """
    Define the specialized agents for blog-to-podcast transformation.
    """
    
    # Researcher to extract core insights
    content_analyst = Agent(
        name="Content Analyst",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A specialized content analyst that extracts key insights and themes from blog posts.",
        instructions=[
            "Thoroughly analyze the provided blog post content.",
            "Identify the main thesis, key arguments, and supporting data.",
            "Summarize the content in a structured format suitable for script writing.",
            "Highlight any unique terminology or emotional tones present in the text."
        ],
        markdown=True
    )
    
    # Scriptwriter to transform insights into a natural dialogue
    podcast_scriptwriter = Agent(
        name="Podcast Scriptwriter",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A professional podcast scriptwriter that turns structured insights into engaging audio scripts.",
        instructions=[
            "Transform the analyzed blog content into a natural-sounding podcast script.",
            "Use a conversational tone suitable for an audio format.",
            "Include 'Host' and 'Guest' labels (or two hosts) to create dynamic interaction.",
            "Include intro/outro segments and natural transitions between topics.",
            "Ensure the script is engaging and accurately reflects the original blog post's message."
        ],
        markdown=True
    )
    
    return content_analyst, podcast_scriptwriter
