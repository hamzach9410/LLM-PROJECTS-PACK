from agents import Agent, WebSearchTool, handoff
from models import ResearchPlan, ResearchReport
from utils import save_important_fact

# Define the agents with optimized instructions
research_agent = Agent(
    name="Research Agent",
    instructions=(
        "You are a research assistant. Given a search term, you search the web for that term and "
        "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
        "words. Capture the main points succinctly. Ignore fluff. Use the save_important_fact tool "
        "whenever you find a critical piece of information with its source."
    ),
    model="gpt-4o-mini",
    tools=[
        WebSearchTool(),
        save_important_fact
    ],
)

editor_agent = Agent(
    name="Editor Agent",
    handoff_description="A senior researcher who writes comprehensive research reports",
    instructions=(
        "You are a senior researcher tasked with writing a cohesive report for a research query. "
        "You will be provided with initial research collected by assistants.\n"
        "1. Create a detailed outline for the report.\n"
        "2. Generate the full report in markdown format.\n"
        "3. Ensure the report is lengthy, detailed, and at least 1000 words.\n"
        "4. List all sources clearly at the end."
    ),
    model="gpt-4o-mini",
    output_type=ResearchReport,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are the coordinator of this research operation. Your job is to:\n"
        "1. Understand the user's research topic.\n"
        "2. Create a research plan with topic, search queries (3-5), and focus areas (3-5).\n"
        "3. Hand off to the Research Agent to collect information.\n"
        "4. After research is complete, hand off to the Editor Agent for the final report."
    ),
    handoffs=[
        handoff(research_agent),
        handoff(editor_agent)
    ],
    model="gpt-4o-mini",
    output_type=ResearchPlan,
)
