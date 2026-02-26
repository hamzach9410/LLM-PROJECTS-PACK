import pytest
from utils import format_currency, format_percentage

def test_format_currency():
    assert format_currency(1234.567) == "$1,234.57"
    assert format_currency(None) == "N/A"

def test_format_percentage():
    assert format_percentage(5.234) == "+5.23%"
    assert format_percentage(-2.1) == "-2.10%"
    assert format_percentage(None) == "N/A"

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test")
    assert logger.name == "test"
