import requests
from bs4 import BeautifulSoup
import os

class ContentEngine:
    @staticmethod
    def scrape_blog(url: str):
        """Extract text content from a blog URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic content extraction logic
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
            return content
        except Exception as e:
            raise Exception(f"Failed to scrape blog: {str(e)}")

    def transform_to_script(self, analyst, writer, blog_content: str):
        """Orchestrate the transformation from blog text to podcast script."""
        # Step 1: Analyze content
        analysis = analyst.run(blog_content)
        
        # Step 2: Write script
        script = writer.run(f"Analyzed Content: {analysis.content}\n\nOriginal Text: {blog_content}")
        
        return script
