import os
from dotenv import load_dotenv

load_dotenv()

# LLM Providers Configuration
PROVIDERS = {
    "OpenAI": {
        "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "default_model": "gpt-4o"
    },
    "Ollama (Local)": {
        "models": ["llama3.2", "llama3.1", "mistral"],
        "default_model": "llama3.2",
        "base_url": "http://localhost:11434"
    }
}

# Default Scraper Config
DEFAULT_CONFIG = {
    "verbose": True,
    "headless": True
}
