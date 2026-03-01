from langchain_cohere import CohereEmbeddings, ChatCohere
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun

class CohereAgentConfig:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_embeddings(self):
        return CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=self.api_key)

    def get_chat_model(self):
        return ChatCohere(model="command-r7b-12-2024", temperature=0.1, cohere_api_key=self.api_key)

    def get_fallback_agent(self):
        """Create a LangGraph agent for web research fallback."""
        model = self.get_chat_model()
        search_tool = DuckDuckGoSearchRun(num_results=5)
        return create_react_agent(model=model, tools=[search_tool])
