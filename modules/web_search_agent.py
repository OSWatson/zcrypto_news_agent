import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI

# ✅ Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def create_web_search_agent():
    """Creates a LangChain agent with a SerpAPI-based search tool, only if the API key is available."""
    
    if not SERPAPI_API_KEY:
        print("⚠️ SerpAPI key is missing. Web search will be disabled.")
        return None  # ✅ Prevents the agent from initializing when there's no API key

    from langchain_community.utilities import SerpAPIWrapper  # ✅ Import only when needed
    search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Use this tool to search the web for current news or any other information."
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    return agent

def ask_web_search_agent(query: str) -> str:
    """Asks the web search agent a question, returning a string answer."""
    agent = create_web_search_agent()
    
    if agent is None:
        return "Web search is disabled because SerpAPI key is missing."
    
    return agent.run(query)

if __name__ == "__main__":
    question = "What are the latest cryptocurrency news headlines?"
    response = ask_web_search_agent(question)
    print("Agent's answer:\n", response)
