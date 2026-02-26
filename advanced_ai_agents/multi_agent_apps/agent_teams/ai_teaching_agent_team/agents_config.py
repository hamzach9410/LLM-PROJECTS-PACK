from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools
from agno.tools.arxiv import ArxivTools

def get_teaching_team_agents(openai_api_key: str, serpapi_api_key: str, google_docs_tool):
    """
    Configure and return the team of teaching agents.
    """
    model = OpenAIChat(id="gpt-4o-mini", api_key=openai_api_key)

    professor = Agent(
        name="Professor",
        role="Research and Knowledge Specialist",
        model=model,
        tools=[google_docs_tool],
        instructions=[
            "Create a comprehensive knowledge base that covers fundamental concepts, advanced topics, and current developments of the given topic.",
            "Explain the topic from first principles first. Include key terminology, core principles, and practical applications.",
            "Make it a detailed report that anyone starting out can read and get maximum value from.",
            "IMPORTANT: DONT FORGET TO CREATE THE GOOGLE DOCUMENT using the provided tool.",
            "Format the document with a clear structure (Headers, Bullet points).",
            "Include the shared Google Doc link in your final response."
        ],
        markdown=True,
    )

    academic_advisor = Agent(
        name="Academic Advisor",
        role="Learning Path Designer",
        model=model,
        tools=[google_docs_tool],
        instructions=[
            "Using the knowledge base provided for the topic, create a detailed learning roadmap.",
            "Break down the topic into logical subtopics and arrange them in order of progression.",
            "Include estimated time commitments for each section.",
            "IMPORTANT: DONT FORGET TO CREATE THE GOOGLE DOCUMENT.",
            "Include the shared Google Doc link in your response."
        ],
        markdown=True
    )

    research_librarian = Agent(
        name="Research Librarian",
        role="Learning Resource Specialist",
        model=model,
        tools=[google_docs_tool, SerpApiTools(api_key=serpapi_api_key), ArxivTools()],
        instructions=[
            "Curate a list of high-quality learning resources for the given topic.",
            "Use SerpApi for blogs, GitHub repos, and official docs.",
            "Use Arxiv for academic papers and latest research depth.",
            "Present resources in a curated list with descriptions and quality assessments.",
            "IMPORTANT: DONT FORGET TO CREATE THE GOOGLE DOCUMENT.",
            "Include the shared Google Doc link in your response."
        ],
        markdown=True,
    )

    teaching_assistant = Agent(
        name="Teaching Assistant",
        role="Exercise Creator",
        model=model,
        tools=[google_docs_tool, SerpApiTools(api_key=serpapi_api_key)],
        instructions=[
            "Create comprehensive practice materials (quizzes, exercises, projects).",
            "Align materials with the roadmap progression.",
            "Provide detailed solutions and explanations.",
            "IMPORTANT: DONT FORGET TO CREATE THE GOOGLE DOCUMENT.",
            "Include the shared Google Doc link in your response."
        ],
        markdown=True,
    )

    return professor, academic_advisor, research_librarian, teaching_assistant
