import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI
from langchain.utilities import SerpAPIWrapper

# 1. Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def create_web_search_agent():
    """Creates a LangChain agent with a SerpAPI-based search tool."""
    # 2. Create an LLM (OpenAI)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    # 3. Create the search tool (SerpAPI)
    search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

    # 4. Wrap the search tool as a LangChain Tool
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Use this tool to search the web for current news or any other information."
        )
    ]

    # 5. Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",  # or "chat-zero-shot-react-description"
        verbose=True
    )
    return agent

def ask_web_search_agent(query: str) -> str:
    """Asks the web search agent a question, returning a string answer."""
    agent = create_web_search_agent()
    return agent.run(query)

if __name__ == "__main__":
    # Example usage
    question = "What are the latest cryptocurrency news headlines?"
    response = ask_web_search_agent(question)
    print("Agent's answer:\n", response)
