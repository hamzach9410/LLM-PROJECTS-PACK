import requests
import os
from uuid import uuid4
from utils import setup_logger, ensure_dir

logger = setup_logger(__name__)

class MusicEngine:
    """Handles the downloading and local persistence of generated music."""
    
    def __init__(self, save_dir: str = "audio_generations"):
        self.save_dir = save_dir
        ensure_dir(self.save_dir)
        
    def download_audio(self, url: str) -> Optional[str]:
        """Download audio from URL and return the local path."""
        try:
            logger.info(f"Downloading audio from: {url}")
            response = requests.get(url, timeout=30)
            
            if not response.ok:
                logger.error(f"Failed to download audio. Status: {response.status_code}")
                return None
                
            content_type = response.headers.get("Content-Type", "")
            if "audio" not in content_type and "octet-stream" not in content_type:
                logger.warning(f"Unexpected content type: {content_type}")
            
            filename = f"music_{uuid4().hex[:8]}.mp3"
            filepath = os.path.join(self.save_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
                
            logger.info(f"Saved audio to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None
