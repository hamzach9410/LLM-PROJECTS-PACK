import cohere
from google import genai

class VisionConfig:
    def __init__(self, cohere_key, google_key):
        self.cohere_key = cohere_key
        self.google_key = google_key

    def get_cohere_client(self):
        return cohere.ClientV2(api_key=self.cohere_key)

    def get_gemini_client(self):
        return genai.Client(api_key=self.google_key)
