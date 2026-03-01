import logging
import re
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

def extract_meme_url(final_result: str) -> Optional[str]:
    """Extract the ImgFlip meme image URL from the agent's final result."""
    if not final_result:
        return None
        
    # Standard ImgFlip page URL
    url_match = re.search(r'https://imgflip\.com/i/(\w+)', final_result)
    if url_match:
        meme_id = url_match.group(1)
        return f"https://i.imgflip.com/{meme_id}.jpg"
        
    # Direct image URL
    direct_match = re.search(r'https://i\.imgflip\.com/\w+\.(jpg|png)', final_result)
    if direct_match:
        return direct_match.group(0)
        
    return None
