from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

load_dotenv()

def get_visualisation_agents():
    """
    Define specialized agents for data visualization and aesthetic design.
    """
    
    # Viz Specialist Agent
    viz_specialist = Agent(
        name="Data Visualization Architect",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A specialized agent that suggests the most effective visualization types based on data patterns.",
        instructions=[
            "Thoroughly analyze the data structure provided.",
            "Recommend specific chart types (Bar, Line, Scatter, Heatmap, etc.) that best represent the findings.",
            "Provide Python snippets using Plotly or Matplotlib if requested.",
            "Focus on clarity, accessibility, and visual impact."
        ],
        markdown=True
    )
    
    # Narrative Designer Agent
    narrative_designer = Agent(
        name="Data Narrative Designer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A design agent that crafts a compelling story around the data visualizations.",
        instructions=[
            "Transform raw charts and data into a cohesive narrative.",
            "Write engaging captions, titles, and summaries for the visualizations.",
            "Explain exactly WHY a specific trend is important to the user.",
            "Ensure the visual story is professional and impactful."
        ],
        markdown=True
    )
    
    return viz_specialist, narrative_designer
