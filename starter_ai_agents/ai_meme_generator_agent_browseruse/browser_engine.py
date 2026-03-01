import asyncio
from browser_use import Agent
from agents_config import get_llm, get_task_description
from utils import setup_logger, extract_meme_url

logger = setup_logger(__name__)

class MemeGeneratorEngine:
    """Engine to orchestrate browser-based meme generation."""
    
    def __init__(self, model_choice: str, api_key: str):
        self.llm = get_llm(model_choice, api_key)
        self.model_choice = model_choice

    async def generate_meme(self, query: str) -> str:
        """Runs the browser-use agent to generate a meme."""
        task = get_task_description(query)
        
        agent = Agent(
            task=task,
            llm=self.llm,
            max_actions_per_step=5,
            max_failures=25,
            use_vision=(self.model_choice != "Deepseek")
        )

        logger.info(f"Starting meme generation for: {query}")
        history = await agent.run()
        
        final_result = history.final_result()
        meme_url = extract_meme_url(final_result)
        
        if meme_url:
            logger.info(f"Meme generated successfully: {meme_url}")
            return meme_url
        
        logger.error("Failed to extract meme URL from browser-use result.")
        return None
