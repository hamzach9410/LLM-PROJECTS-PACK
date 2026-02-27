from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.e2b import E2BTools
from agno.tools.firecrawl import FirecrawlTools

def get_insurance_advisor_agent(openai_key: str, firecrawl_key: str, e2b_key: str, model_id: str = "gpt-4o"):
    """Returns a specialized life insurance advisory agent."""
    return Agent(
        name="Life Insurance Advisor",
        model=OpenAIChat(id=model_id, api_key=openai_key),
        tools=[
            E2BTools(api_key=e2b_key, timeout=180),
            FirecrawlTools(
                api_key=firecrawl_key,
                enable_search=True,
                enable_crawl=True,
                enable_scrape=False,
                search_params={"limit": 5, "lang": "en"},
            ),
        ],
        instructions=[
            "You provide conservative life insurance guidance. Your workflow is strictly:",
            "1. ALWAYS call `run_python_code` from the E2B tools to compute the coverage recommendation using the provided client JSON.",
            "   - Treat missing numeric values as 0.",
            "   - Use a default real discount rate of 2% when discounting income replacement cash flows.",
            "   - Compute: discounted_income = annual_income * ((1 - (1 + r)**(-income_replacement_years)) / r).",
            "   - Recommended coverage = max(0, discounted_income + total_debt - savings - existing_life_insurance).",
            "   - Print a JSON with keys: coverage_amount, coverage_currency, breakdown, assumptions.",
            "2. Use Firecrawl `search` to gather up-to-date term life insurance options for the client's region.",
            "3. Respond ONLY with JSON containing the following top-level keys: coverage_amount, coverage_currency, breakdown, assumptions, recommendations, research_notes, timestamp.",
            "   - `coverage_amount`: integer of total recommended coverage.",
            "   - `coverage_currency`: 3-letter currency code.",
            "   - `breakdown`: include income_replacement, debt_obligations, assets_offset, methodology.",
            "   - `assumptions`: include income_replacement_years, real_discount_rate, additional_notes.",
            "   - `recommendations`: list of up to three objects (name, summary, link, source).",
            "   - `research_notes`: brief disclaimer + recency of sources.",
            "   - `timestamp`: ISO 8601 date-time string.",
            "Do not include markdown, commentary, or tool call traces in the final JSON output.",
        ],
        markdown=False,
    )
