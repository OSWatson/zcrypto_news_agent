import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from modules.fetch_news import fetch_news

def summarize_articles():
    # Fetch articles from your local news fetcher
    articles = fetch_news()
    if not articles:
        return []

    # Initialize the LLM (ensure your OPENAI_API_KEY is set in your environment)
    llm = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    summaries = []
    # Limit to first 5 articles for efficiency
    for article in articles[:5]:
        prompt = (
            "Summarize the following news article in two sentences:\n\n"
            f"Title: {article.get('title', 'No title')}\n"
            f"Content: {article.get('content', 'No content')}"
        )
        # Create a human message with the prompt
        message = HumanMessage(content=prompt)
        # Get the summary from the LLM
        summary = llm([message]).content
        summaries.append({
            "title": article.get("title", "No title"),
            "summary": summary,
            "url": article.get("url", "#")
        })
    return summaries

if __name__ == "__main__":
    results = summarize_articles()
    for res in results:
        print("Title:", res["title"])
        print("Summary:", res["summary"])
        print("URL:", res["url"])
        print("---")
