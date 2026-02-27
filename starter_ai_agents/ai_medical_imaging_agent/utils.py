import logging
import os
from PIL import Image as PILImage
from typing import Tuple

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

def resize_medical_image(image: PILImage.Image, target_width: int = 500) -> PILImage.Image:
    """Resizes an image while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height
    new_height = int(target_width / aspect_ratio)
    return image.resize((target_width, new_height))

def save_temp_image(image: PILImage.Image, filename: str = "temp_medical_image.png") -> str:
    """Saves a PIL image to a temporary file and returns the path."""
    image.save(filename)
    return filename

def cleanup_temp_files(filepaths: list):
    """Removes temporary files."""
    for path in filepaths:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
