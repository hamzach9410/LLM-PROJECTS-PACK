from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from typing import Optional

def get_xai_finance_agent(api_key: str, model_id: str = "grok-4-1-fast"):
    """
    Returns a configured xAI Finance Agent.
    """
    return Agent(
        name="xAI Financial Intelligence",
        model=xAI(id=model_id, api_key=api_key),
        tools=[DuckDuckGoTools(), YFinanceTools()],
        instructions=[
            "You are a professional financial analyst. Provide deep technical insights and market analysis.",
            "Always use tables to display financial/numerical data.",
            "For text data, use clear bullet points and concise paragraphs.",
            "When asked for technical analysis, include support/resistance levels, RSI, and moving averages if available.",
            "Analyze market sentiment based on recent news provided by DuckDuckGo.",
            "If a stock ticker is not provided, ask for one."
        ],
        debug_mode=True,
        markdown=True,
    )
