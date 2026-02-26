from pydantic import BaseModel
from typing import List, Optional

class ResearchPlan(BaseModel):
    """Plan for a research operation."""
    topic: str
    search_queries: List[str]
    focus_areas: List[str]

class ResearchReport(BaseModel):
    """The final generated research report."""
    title: str
    outline: List[str]
    report: str
    sources: List[str]
    word_count: int
