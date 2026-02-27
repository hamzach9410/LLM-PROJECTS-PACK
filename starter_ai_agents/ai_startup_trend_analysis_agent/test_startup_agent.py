import pytest
from utils import format_analysis_report

def test_format_analysis_report():
    raw = "No header here."
    formatted = format_analysis_report(raw)
    assert "# Startup Trend Analysis" in formatted
    
    with_header = "# Already has one\nContent"
    assert format_analysis_report(with_header) == with_header

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_startup")
    assert logger.name == "test_startup"
    assert logger.level == 20 # INFO
