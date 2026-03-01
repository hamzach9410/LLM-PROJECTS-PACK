from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def get_llm(model_choice: str, api_key: str):
    """Factory function to initialize the appropriate LLM."""
    if model_choice == "Claude":
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=api_key
        )
    elif model_choice == "Deepseek":
        return ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key=api_key,
            temperature=0.3
        )
    else:  # OpenAI
        return ChatOpenAI(
            model="gpt-4o",
            api_key=api_key,
            temperature=0.0
        )

def get_task_description(query: str) -> str:
    """Generate the structured task description for the browser agent."""
    return (
        "You are a meme generator expert. You are given a query and you need to generate a meme for it.\n"
        "1. Go to https://imgflip.com/memetemplates \n"
        "2. Click on the Search bar in the middle and search for ONLY ONE MAIN ACTION VERB (like 'bully', 'laugh', 'cry') in this query: '{0}'\n"
        "3. Choose any meme template that metaphorically fits the meme topic: '{0}'\n"
        "   by clicking on the 'Add Caption' button below it\n"
        "4. Write a Top Text (setup/context) and Bottom Text (punchline/outcome) related to '{0}'.\n" 
        "5. Check the preview making sure it is funny and a meaningful meme. Adjust text directly if needed. \n"
        "6. Look at the meme and text on it, if it doesnt make sense, PLEASE retry by filling the text boxes with different text. \n"
        "7. Click on the Generate meme button to generate the meme\n"
        "8. Copy the image link and give it as the output\n"
    ).format(query)
