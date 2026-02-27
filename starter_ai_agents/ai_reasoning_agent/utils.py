import logging
import time
from typing import Dict, Any

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

class Timer:
    """Utility to measure execution time."""
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start

def format_metrics(interval: float, response: Any) -> Dict[str, Any]:
    """Extract metrics from an agent response."""
    metrics = {
        "latency_sec": round(interval, 2),
    }
    # Attempt to extract token usage if available in response
    if hasattr(response, 'usage'):
        metrics["tokens"] = response.usage
    return metrics
