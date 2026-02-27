from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools

def get_news_collector(api_key: str, model_id: str = "gemini-2.0-flash"):
    return Agent(
        name="Market Researcher",
        role="Collects recent news and market signals on specific startup niches",
        model=Gemini(id=model_id, api_key=api_key),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Search for the latest 10 news articles and industry reports on the given topic.",
            "Focus on market growth, funding rounds, and technological breakthroughs.",
            "Provide a list of titles and URLs for further processing."
        ],
        markdown=True,
    )

def get_summary_writer(api_key: str, model_id: str = "gemini-2.0-flash"):
    return Agent(
        name="Business Analyst",
        role="Deeply analyzes and summarizes market data for actionable intelligence",
        model=Gemini(id=model_id, api_key=api_key),
        tools=[Newspaper4kTools(enable_read_article=True, include_summary=True)],
        instructions=[
            "Read the provided articles and synthesize high-density summaries.",
            "Highlight specific pain points in the industry and unsolved problems.",
            "Structure summaries by category: Tech, Funding, Regulations, and Consumer Trends."
        ],
        markdown=True,
    )

def get_trend_analyzer(api_key: str, model_id: str = "gemini-2.0-flash"):
    return Agent(
        name="Startup Strategist",
        role="Identifies emerging trends and generates high-potential startup opportunities",
        model=Gemini(id=model_id, api_key=api_key),
        instructions=[
            "Analyze the synthesized summaries to identify 3-5 emerging trends.",
            "For each trend, propose a specific startup opportunity with potential value proposition.",
            "Use professional business language and provide a SWOT summary if applicable.",
            "Always include a 'Why Now?' section for each opportunity."
        ],
        markdown=True,
    )
