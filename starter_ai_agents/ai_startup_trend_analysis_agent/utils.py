import logging
import streamlit as st
from typing import List, Dict

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

def format_analysis_report(analysis_text: str) -> str:
    """Ensure the analysis report has clean markdown structure."""
    if not analysis_text:
        return ""
    # Add common startup analysis headers if not present
    if "#" not in analysis_text[:50]:
        return f"# Startup Trend Analysis\n\n{analysis_text}"
    return analysis_text
