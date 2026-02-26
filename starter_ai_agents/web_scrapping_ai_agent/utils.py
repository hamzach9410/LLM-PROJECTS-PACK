import logging
import json
import pandas as pd
from typing import Any, Dict, Optional

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

def clean_scrape_result(result: Any) -> Dict[str, Any]:
    """Ensure the scrape result is a dictionary/list and not a raw string."""
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"raw_output": result}
    return result

def convert_to_csv(data: Any) -> str:
    """Convert JSON-like data to CSV string if possible."""
    try:
        if isinstance(data, list):
            return pd.DataFrame(data).to_csv(index=False)
        elif isinstance(data, dict):
            # Check for common patterns like {"items": [...]}
            for val in data.values():
                if isinstance(val, list):
                    return pd.DataFrame(val).to_csv(index=False)
            return pd.DataFrame([data]).to_csv(index=False)
    except Exception:
        pass
    return ""
