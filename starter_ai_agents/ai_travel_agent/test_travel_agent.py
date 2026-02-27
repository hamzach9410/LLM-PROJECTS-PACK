import pytest
from datetime import datetime
from utils import generate_ics_content

def test_ics_generation_basic():
    itinerary = "Day 1: Arrival in Paris and Eiffel Tower visit."
    ics_bytes = generate_ics_content(itinerary)
    assert b"BEGIN:VCALENDAR" in ics_bytes
    assert b"SUMMARY:Day 1 Itinerary" in ics_bytes

def test_ics_generation_no_days():
    itinerary = "A general travel plan without day markers."
    ics_bytes = generate_ics_content(itinerary)
    assert b"BEGIN:VCALENDAR" in ics_bytes
    assert b"SUMMARY:Travel Itinerary" in ics_bytes

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_travel")
    assert logger.name == "test_travel"
