import requests
from urllib.parse import urlparse

class RagieClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ragie.ai"

    def upload_url(self, url, name=None, mode="fast"):
        """Index a document from a URL into Ragie."""
        if not name:
            name = urlparse(url).path.split('/')[-1] or "document"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"mode": mode, "name": name, "url": url}
        resp = requests.post(f"{self.base_url}/documents/url", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def retrieve_scored_chunks(self, query, scope="tutorial"):
        """Get relevant chunks from Ragie's managed index."""
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"query": query, "filters": {"scope": scope}}
        resp = requests.post(f"{self.base_url}/retrievals", json=payload, headers=headers)
        resp.raise_for_status()
        return [chunk["text"] for chunk in resp.json()["scored_chunks"]]
