import logging
import pandas as pd
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

def format_currency(value: float) -> str:
    """Format numeric values as currency."""
    if value is None:
        return "N/A"
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Format numeric values as percentage."""
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"
