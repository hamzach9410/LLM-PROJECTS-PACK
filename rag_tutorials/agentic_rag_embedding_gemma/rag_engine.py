class RAGEngine:
    def __init__(self, knowledge_base, agent):
        self.kb = knowledge_base
        self.agent = agent

    def add_source(self, url):
        """Add a PDF URL to the knowledge base."""
        try:
            self.kb.add_content(url=url)
            return True, f"Successfully added: {url}"
        except Exception as e:
            return False, f"Failed to add source: {str(e)}"

    def query_agent(self, query):
        """Run the agent query with streaming output."""
        return self.agent.run(query, stream=True)
