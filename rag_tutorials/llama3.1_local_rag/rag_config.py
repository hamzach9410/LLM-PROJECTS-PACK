import os

class OllamaConfig:
    def __init__(self, model="llama3.1", base_url="http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url

    def get_settings(self):
        return {
            "model": self.model,
            "base_url": self.base_url
        }
