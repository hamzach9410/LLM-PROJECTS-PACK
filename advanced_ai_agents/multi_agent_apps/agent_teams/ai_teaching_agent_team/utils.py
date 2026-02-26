import logging
import os
from typing import Optional

def setup_logger(name: str) -> logging.Logger:
    """Setup a standard logger with consistent formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def extract_google_doc_link(response_content: str) -> Optional[str]:
    """
    Extract the Google Doc ID from the agent's response content.
    """
    if "https://docs.google.com" in response_content:
        try:
            # Simple extraction logic: find the part after the base URL
            # and before any whitespace or markdown syntax.
            part = response_content.split("https://docs.google.com")[1]
            # Take the first contiguous block of non-whitespace characters
            link_id = part.split()[0]
            # Ensure it starts with /document/d/
            if link_id.startswith("/document/d/"):
                return link_id
        except (IndexError, AttributeError):
            pass
    return None
