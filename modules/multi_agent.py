import os
from langchain.agents import initialize_agent, Tool  # <-- Change here
from langchain_community.llms import OpenAI

from modules.langchain_agent import ask_question  # Local news agent
from modules.web_search_agent import ask_web_search_agent  # Real-time web search agent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_multi_agent():
    llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
    
    tools = [
        Tool(
            name="Local News Retrieval",
            func=ask_question,
            description=(
                "Use this tool to answer questions based on locally stored crypto news "
                "from your articles.json and associated sentiment analysis."
            )
        ),
        Tool(
            name="Real-Time Web Search",
            func=ask_web_search_agent,
            description=(
                "Use this tool to search the web in real time for the latest crypto news and trends."
            )
        )
    ]
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    return agent

def ask_multi_agent(query: str) -> str:
    agent = create_multi_agent()
    return agent.run(query)

if __name__ == "__main__":
    sample_query = "What are the latest trends and news on Bitcoin, and what is the local sentiment?"
    print("Agent's response:\n", ask_multi_agent(sample_query))
