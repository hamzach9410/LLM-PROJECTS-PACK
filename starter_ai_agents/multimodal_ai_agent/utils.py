import logging
import streamlit as st
from pathlib import Path
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

def get_file_extension(file_path: str) -> str:
    """Get the normalized extension for a file path."""
    return Path(file_path).suffix.lower().replace('.', '')

def cleanup_temp_file(file_path: Optional[str]):
    """Safely remove a temporary file if it exists."""
    if file_path and Path(file_path).exists():
        try:
            Path(file_path).unlink()
        except Exception as e:
            logging.error(f"Failed to delete temp file {file_path}: {e}")
