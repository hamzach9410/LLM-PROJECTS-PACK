from agno.document.reader.pdf_reader import PDFReader
import io

class AutonomousEngine:
    def __init__(self, knowledge_base, agent):
        self.kb = knowledge_base
        self.agent = agent

    def ingest_pdf(self, file_bytes):
        """Read and load a PDF file into the knowledge base."""
        try:
            reader = PDFReader()
            docs = reader.read(io.BytesIO(file_bytes))
            if docs:
                self.kb.load_documents(docs, upsert=True)
                return True, "Document indexed successfully in database."
            return False, "No content found in PDF."
        except Exception as e:
            return False, f"Ingestion failed: {str(e)}"

    def execute_autonomous_query(self, query):
        """Run the agent with knowledge search and web tools."""
        return self.agent.run(query)
