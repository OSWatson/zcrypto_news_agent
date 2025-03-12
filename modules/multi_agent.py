import os
import re
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI

from modules.langchain_agent import ask_question  # Local news agent
from modules.price_agent import PriceAgent  # Crypto price agent
from modules.fetch_news import fetch_news  # News Fetcher
from modules.sentiment import analyze_sentiment  # Sentiment Analysis

# ✅ Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ✅ Web Search Toggle (Disables if no API Key)
WEB_SEARCH_ENABLED = bool(SERPAPI_API_KEY)
if WEB_SEARCH_ENABLED:
    from modules.web_search_agent import ask_web_search_agent
else:
    ask_web_search_agent = None  # Prevents function call errors

# ✅ Initialize Price Agent
price_agent = PriceAgent()

def ask_price_agent(query: str) -> str:
    """Fetches cryptocurrency prices if the query contains a coin symbol."""
    print(f"🔍 DEBUG: Received query = {query}")  

    matches = re.findall(r"\b[A-Z]{2,5}\b", query.upper())  

    if matches:
        coin_symbol = matches[0]  
        print(f"✅ DEBUG: Detected crypto symbol = {coin_symbol}")  
        return price_agent.get_crypto_price(coin_symbol)

    return "I couldn't detect a cryptocurrency symbol. Please specify a coin like BTC, ETH, or SOL."

def ask_news_agent(query: str) -> str:
    """Fetches news articles from the news API and summarizes relevant results."""
    articles = fetch_news()
    if not articles:
        return "No recent cryptocurrency news available."
    
    response = "\n".join([f"- {article['title']} ({article['url']})" for article in articles[:5]])
    return f"Here are the latest crypto news articles:\n{response}"

def ask_sentiment_agent(query: str) -> str:
    """Analyzes sentiment from the latest fetched crypto news articles."""
    articles = fetch_news()
    if not articles:
        return "No news available to analyze sentiment."

    sentiment_result = analyze_sentiment(" ".join([article.get('content', '') for article in articles]))
    return f"Sentiment Analysis Result: {sentiment_result}"

def create_multi_agent():
    """Creates the multi-agent system with available tools."""
    llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

    tools = [
        Tool(
            name="Local News Retrieval",
            func=ask_news_agent,
            description="Use this tool to retrieve and summarize the latest cryptocurrency news."
        ),
        Tool(
            name="Crypto Price Fetcher",
            func=ask_price_agent,
            description="Use this tool to fetch the latest cryptocurrency prices from the Financial Datasets API."
        ),
        Tool(
            name="Crypto Sentiment Analysis",
            func=ask_sentiment_agent,
            description="Use this tool to analyze the sentiment of the latest crypto news."
        ),
    ]

    # ✅ **Only add Web Search if SerpAPI key exists**
    if WEB_SEARCH_ENABLED:
        tools.append(
            Tool(
                name="Real-Time Web Search",
                func=ask_web_search_agent,
                description="Use this tool to search the web in real time for the latest crypto news and trends."
            )
        )
    else:
        print("⚠️ Web Search is DISABLED because SerpAPI key is missing.")

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    return agent

def ask_multi_agent(query: str) -> str:
    """Runs the multi-agent system for a given query."""
    agent = create_multi_agent()
    return agent.run(query)

if __name__ == "__main__":
    sample_query = "What are the latest trends in cryptocurrency?"
    print("Agent's response:\n", ask_multi_agent(sample_query))
