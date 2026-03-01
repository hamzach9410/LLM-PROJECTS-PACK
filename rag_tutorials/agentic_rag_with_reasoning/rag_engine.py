class ReasoningEngine:
    def __init__(self, knowledge_base, agent):
        self.kb = knowledge_base
        self.agent = agent

    def add_knowledge_source(self, url):
        """Add a URL to the knowledge base."""
        try:
            self.kb.add_content(url=url)
            return True, f"Successfully indexed: {url}"
        except Exception as e:
            return False, f"Failed to index source: {str(e)}"

    def run_reasoning_query(self, query):
        """Execute query with streaming and event tracking."""
        return self.agent.run(
            query,
            stream=True,
            stream_events=True
        )
