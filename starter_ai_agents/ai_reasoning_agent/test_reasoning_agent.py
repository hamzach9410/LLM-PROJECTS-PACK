import pytest
from utils import Timer, format_metrics

def test_timer_logic():
    with Timer() as t:
        import time
        time.sleep(0.1)
    assert t.interval >= 0.1

def test_metrics_formatting():
    class MockResponse:
        def __init__(self):
            self.usage = "100 tokens"
    
    res = MockResponse()
    metrics = format_metrics(1.23, res)
    assert metrics['latency_sec'] == 1.23
    assert metrics['tokens'] == "100 tokens"

def test_agents_init():
    from agents_config import get_regular_agent, get_reasoning_agent
    reg = get_regular_agent("fake_key")
    reas = get_reasoning_agent("fake_key")
    assert reg.name == "Standard Agent"
    assert reas.reasoning is True
