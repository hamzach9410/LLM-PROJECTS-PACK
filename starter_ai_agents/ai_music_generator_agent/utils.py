import logging
import os
import shutil
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

def ensure_dir(directory: str):
    """Ensure a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def cleanup_generations(directory: str):
    """Cleanup generated audio files."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)
