from anthropic import Anthropic

class AnthropicClient:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def generate_rag_response(self, query, context_chunks):
        """Synthesize a response using Claude based on retrieved chunks."""
        system_prompt = f"""
        You are Ragie AI, a professional intelligence assistant.
        Analyze the following context fragments and answer the user query concisely.
        Context: {context_chunks}
        """
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": query}]
        )
        return message.content[0].text
