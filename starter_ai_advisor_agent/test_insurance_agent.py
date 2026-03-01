import pytest
from advisor_engine import compute_local_math
from utils import format_currency, parse_percentage

def test_coverage_math_basic():
    profile = {
        "annual_income": 100000,
        "income_replacement_years": 10,
        "total_debt": 200000,
        "available_savings": 50000,
        "existing_life_insurance": 0
    }
    # With 0% discount, should be 100k*10 + 200k - 50k = 1.15M
    res = compute_local_math(profile, 0.0)
    assert res['recommended'] == 1150000.0

def test_currency_formatting():
    assert format_currency(1234.56, "USD") == "$1,235"
    assert format_currency(1000, "EUR") == "€1,000"

def test_percentage_parsing():
    assert parse_percentage("2%") == 0.02
    assert parse_percentage(0.05) == 0.05
    assert parse_percentage(10) == 0.1
