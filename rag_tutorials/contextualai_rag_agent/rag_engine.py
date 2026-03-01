import os
import tempfile
import time
import requests
from typing import List, Optional, Tuple, Any

class ContextualEngine:
    def __init__(self, client):
        self.client = client

    def create_datastore(self, name: str) -> Optional[str]:
        try:
            ds = self.client.datastores.create(name=name)
            return getattr(ds, "id", None)
        except Exception:
            return None

    def upload_docs(self, datastore_id: str, files: List[bytes], filenames: List[str], metadata: Optional[dict] = None) -> List[str]:
        doc_ids = []
        allowed_exts = {".pdf", ".html", ".htm", ".mhtml", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".md"}
        
        for content, fname in zip(files, filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in allowed_exts:
                continue
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                with open(tmp_path, "rb") as f:
                    result = self.client.datastores.documents.ingest(datastore_id, file=f, metadata=metadata)
                    doc_ids.append(getattr(result, "id", ""))
            finally:
                os.unlink(tmp_path)
        return doc_ids

    def create_agent(self, name: str, description: str, datastore_id: str) -> Optional[str]:
        try:
            agent = self.client.agents.create(name=name, description=description, datastore_ids=[datastore_id])
            return getattr(agent, "id", None)
        except Exception:
            return None

    def query(self, agent_id: str, query_text: str) -> Tuple[str, Any]:
        try:
            resp = self.client.agents.query.create(agent_id=agent_id, messages=[{"role": "user", "content": query_text}])
            if hasattr(resp, "content"):
                return resp.content, resp
            return str(resp), resp
        except Exception as e:
            return f"Query failed: {str(e)}", None
