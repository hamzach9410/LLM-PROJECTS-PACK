class GPT5RAGEngine:
    def __init__(self, agent, knowledge_base):
        self.agent = agent
        self.kb = knowledge_base

    def add_knowledge_url(self, url):
        """Ingest a new URL into the knowledge base."""
        try:
            self.kb.add_content(url=url)
            return True, f"Successfully indexed: {url}"
        except Exception as e:
            return False, str(e)

    def query_agent_stream(self, query):
        """Execute a streaming query against the agent."""
        return self.agent.run(query, stream=True)
