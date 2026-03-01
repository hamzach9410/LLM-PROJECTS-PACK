from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

load_dotenv()

def get_recovery_agents():
    """
    Define specialized agents for emotional recovery and wellness.
    """
    
    # Empathetic Listener Agent
    empathetic_listener = Agent(
        name="Empathetic Counselor",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A compassionate and non-judgmental counselor specializing in emotional recovery.",
        instructions=[
            "Provide a safe, supportive space for users to express their feelings.",
            "Use validating and empathetic language.",
            "Help users identify their emotions and validate their experiences.",
            "Avoid giving unsolicited advice; instead, offer perspective and comfort."
        ],
        markdown=True
    )
    
    # Wellness Strategist Agent
    wellness_strategist = Agent(
        name="Wellness Strategist",
        model=Gemini(id="gemini-2.0-flash-exp"),
        description="A strategic wellness coach focused on practical steps for moving forward.",
        instructions=[
            "Suggest actionable, healthy coping mechanisms and self-care routines.",
            "Help users set small, achievable goals for personal growth.",
            "Provide resources and strategies for rebuilding independence and confidence.",
            "Encourage professional help if needed."
        ],
        markdown=True
    )
    
    return empathetic_listener, wellness_strategist
