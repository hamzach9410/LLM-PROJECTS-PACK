class LocalAgentEngine:
    def __init__(self, agent, knowledge_base):
        self.agent = agent
        self.kb = knowledge_base

    def ingest_document(self, url=None, file_path=None):
        """Add documentation into the local knowledge vault."""
        try:
            if url:
                self.kb.add_content(url=url)
            elif file_path:
                self.kb.add_content(path=file_path)
            return True, "Knowledge indexed locally."
        except Exception as e:
            return False, str(e)

    def query_stream(self, query):
        """Stream response from local agent."""
        return self.agent.run(query, stream=True)
