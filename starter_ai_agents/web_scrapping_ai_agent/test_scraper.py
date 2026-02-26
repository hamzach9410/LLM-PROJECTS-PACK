import pytest
import json
from utils import clean_scrape_result, convert_to_csv

def test_clean_scrape_result_str():
    raw = '{"key": "value"}'
    cleaned = clean_scrape_result(raw)
    assert cleaned == {"key": "value"}

def test_clean_scrape_result_raw():
    raw = "not a json"
    cleaned = clean_scrape_result(raw)
    assert cleaned == {"raw_output": "not a json"}

def test_convert_to_csv():
    data = [{"name": "A", "price": 10}, {"name": "B", "price": 20}]
    csv = convert_to_csv(data)
    assert "name,price" in csv
    assert "A,10" in csv

def test_scraper_engine_init():
    from scraper_engine import ScraperEngine
    engine = ScraperEngine("OpenAI", api_key="test_key")
    assert engine.provider == "OpenAI"
    assert engine.config['llm']['api_key'] == "test_key"
    assert engine.config['headless'] is True
