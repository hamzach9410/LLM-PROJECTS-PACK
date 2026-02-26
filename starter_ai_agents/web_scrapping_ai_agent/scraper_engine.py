from scrapegraphai.graphs import SmartScraperGraph
from typing import Any, Dict, Optional
from utils import setup_logger

logger = setup_logger(__name__)

class ScraperEngine:
    """
    Unified engine for handling SmartScraperGraph with different providers.
    """
    
    def __init__(self, provider: str, api_key: Optional[str] = None, model: str = "gpt-4o", base_url: str = None):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.config = self._build_config()
        logger.info(f"ScraperEngine initialized for {provider} using {model}")

    def _build_config(self) -> Dict[str, Any]:
        if "OpenAI" in self.provider:
            return {
                "llm": {
                    "api_key": self.api_key,
                    "model": self.model,
                },
                "verbose": True,
                "headless": True
            }
        elif "Ollama" in self.provider:
            return {
                "llm": {
                    "model": f"ollama/{self.model}",
                    "temperature": 0,
                    "format": "json",
                    "base_url": self.base_url or "http://localhost:11434",
                },
                "embeddings": {
                    "model": "ollama/nomic-embed-text",
                    "base_url": self.base_url or "http://localhost:11434",
                },
                "verbose": True,
                "headless": True
            }
        return {}

    def run(self, url: str, prompt: str) -> Any:
        """Execute the scrape graph."""
        try:
            logger.info(f"Running scrape for URL: {url}")
            graph = SmartScraperGraph(
                prompt=prompt,
                source=url,
                config=self.config
            )
            result = graph.run()
            return result
        except Exception as e:
            logger.error(f"Scrape failed: {e}")
            raise e
