from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.models_labs import FileType, ModelsLabTools

def get_music_composer_agent(openai_api_key: str, models_lab_api_key: str):
    return Agent(
        name="Audio Maestro",
        agent_id="ml_music_composer",
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        tools=[ModelsLabTools(api_key=models_lab_api_key, wait_for_completion=True, file_type=FileType.MP3)],
        description="You are an elite AI music composer capable of generating high-fidelity instrumental tracks.",
        instructions=[
            "Translate user requests into highly descriptive musical prompts for the `generate_media` tool.",
            "Always specify: Genre, Mood, Tempo, Instruments, and Structural arrangement.",
            "Focus on creating emotive and professional-grade compositions.",
            "Ensure the final response includes the direct URL to the generated audio file."
        ],
        markdown=True,
    )
