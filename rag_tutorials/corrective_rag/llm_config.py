from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LLMConfig:
    def __init__(self, openai_api_key, anthropic_api_key):
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key

    def get_embeddings(self):
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=self.openai_api_key
        )

    def get_anthropic_llm(self, model_name="claude-3-5-sonnet-20240620"):
        return ChatAnthropic(
            model=model_name,
            api_key=self.anthropic_api_key,
            temperature=0,
            max_tokens=1000
        )

    def get_openai_llm(self, model_name="gpt-4o"):
        return ChatOpenAI(
            model=model_name,
            api_key=self.openai_api_key,
            temperature=0
        )
