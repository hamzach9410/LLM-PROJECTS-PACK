from contextual import ContextualAI

class ContextualConfig:
    def __init__(self, api_key, base_url="https://api.contextual.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = ContextualAI(api_key=api_key, base_url=base_url)

    def get_client(self):
        return self.client

    @staticmethod
    def verify_credentials(api_key, base_url):
        """Verify the provided credentials with a simple list agents call."""
        try:
            client = ContextualAI(api_key=api_key, base_url=base_url)
            client.agents.list()
            return True
        except Exception:
            return False
