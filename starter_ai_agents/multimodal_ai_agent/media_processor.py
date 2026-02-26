import tempfile
from pathlib import Path
from agno.media import Image, Video, Document
from typing import Tuple, Optional

class MediaProcessor:
    """
    Handles file saving and creation of Agno media objects.
    """
    
    @staticmethod
    def process_upload(uploaded_file) -> Tuple[str, str]:
        """Save uploaded file to a temporary location and return path and type."""
        ext = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(uploaded_file.read())
            return tmp.name, ext.lower().replace('.', '')

    @staticmethod
    def get_agno_media(file_path: str, file_type: str):
        """Map file type to Agno media object."""
        if file_type in ['jpg', 'jpeg', 'png']:
            return Image(filepath=file_path)
        elif file_type in ['mp4', 'mov', 'avi']:
            return Video(filepath=file_path)
        elif file_type == 'pdf':
            return Document(filepath=file_path)
        return None
