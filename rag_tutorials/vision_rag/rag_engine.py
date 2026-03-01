import os
import fitz
import numpy as np
import PIL.Image
from utils import pil_to_base64_data

class VisionRAGEngine:
    def __init__(self, co_client, gen_client):
        self.co = co_client
        self.gen = gen_client

    def embed_multimodal(self, b64_img):
        """Compute Cohere V4 multimodal embedding."""
        resp = self.co.embed(
            model="embed-v4.0",
            input_type="search_document",
            embedding_types=["float"],
            images=[b64_img]
        )
        return np.asarray(resp.embeddings.float[0])

    def process_pdf(self, pdf_file, store_path="pdf_vault"):
        """Extract and embed all pages from a PDF."""
        os.makedirs(store_path, exist_ok=True)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        paths, embs = [], []
        
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            p_path = os.path.join(store_path, f"{pdf_file.name}_p{i+1}.png")
            img.save(p_path)
            emb = self.embed_multimodal(pil_to_base64_data(img))
            paths.append(p_path)
            embs.append(emb)
        return paths, embs

    def search_intelligence(self, query, embeddings, paths):
        """Cross-modal search: Text query -> Visual fragments."""
        q_resp = self.co.embed(
            model="embed-v4.0",
            input_type="search_query",
            embedding_types=["float"],
            texts=[query]
        )
        q_emb = np.asarray(q_resp.embeddings.float[0])
        scores = np.dot(q_emb, embeddings.T)
        return paths[np.argmax(scores)]

    def synthesize_answer(self, query, hit_path):
        """Multimodal synthesis using Gemini 2.0 Flash."""
        img = PIL.Image.open(hit_path)
        prompt = [f"Explain based on this image: {query}", img]
        resp = self.gen.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return resp.text
