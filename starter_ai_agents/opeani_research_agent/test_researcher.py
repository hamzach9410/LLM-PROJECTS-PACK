import pytest
from models import ResearchPlan, ResearchReport

def test_research_plan_model():
    plan = ResearchPlan(
        topic="AI",
        search_queries=["What is AI?"],
        focus_areas=["LLMs"]
    )
    assert plan.topic == "AI"
    assert len(plan.search_queries) == 1

def test_research_report_model():
    report = ResearchReport(
        title="Test Report",
        outline=["Intro", "Body", "Outro"],
        report="Content",
        sources=["Source 1"],
        word_count=7
    )
    assert report.word_count == 7
    assert "Intro" in report.outline

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == 20 # INFO
