import json
import logging
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

def safe_number(value: Any) -> float:
    """Best-effort conversion to float."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        if isinstance(value, str):
            stripped = value
            for token in [",", "$", "€", "£", "₹", "C$", "A$"]:
                stripped = stripped.replace(token, "")
            stripped = stripped.strip()
            try:
                return float(stripped)
            except ValueError:
                return 0.0
        return 0.0

def format_currency(amount: float, currency_code: str) -> str:
    """Formats amount as currency string."""
    symbol_map = {
        "USD": "$", "EUR": "€", "GBP": "£",
        "CAD": "C$", "AUD": "A$", "INR": "₹",
    }
    code = (currency_code or "USD").upper()
    symbol = symbol_map.get(code, "")
    formatted = f"{amount:,.0f}"
    return f"{symbol}{formatted}" if symbol else f"{formatted} {code}"

def extract_json(payload: str) -> Optional[Dict[str, Any]]:
    """Strictly extracts JSON from LLM response payload."""
    if not payload:
        return None
    content = payload.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None

def parse_percentage(value: Any, fallback: float = 0.02) -> float:
    """Convert percentage strings or values to decimal."""
    if value is None:
        return fallback
    if isinstance(value, (int, float)):
        return float(value) if value < 1 else float(value) / 100
    if isinstance(value, str):
        cleaned = value.strip().replace("%", "")
        try:
            numeric = float(cleaned)
            return numeric if numeric < 1 else numeric / 100
        except ValueError:
            return fallback
    return fallback
