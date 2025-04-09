from modules.fetch_news import fetch_news
from modules.sentiment import analyze_sentiment
from modules.price_agent import PriceAgent
from modules.gov_news_agent import fetch_regulations_gov_news
from modules.summarizer import summarize_articles
from modules.multi_agent import ask_multi_agent
from modules.sentiment_agent import ask_sentiment_agent
import os


def collect_data():
    # Fetch news articles
    articles = fetch_news()
    # Analyze sentiment
    sentiment_results = analyze_sentiment(articles)
    # Fetch price data
    price_agent = PriceAgent()
    price_data = price_agent.get_crypto_price("BTC")
    # Fetch regulatory news
    regulatory_news = fetch_regulations_gov_news("your_api_key")
    # Fetch summarized articles
    summarized_articles = summarize_articles()

    # Use multi-agent to gather additional insights
    multi_agent_insights = ask_multi_agent("Provide insights on current crypto trends.")

    # Initialize PriceAgent
    price_agent = PriceAgent()
    # Fetch Bitcoin price
    bitcoin_price = price_agent.get_crypto_price("BTC")

    return {
        "articles": articles,
        "summarized_articles": summarized_articles,
        "sentiment": sentiment_results,
        "price_data": price_data,
        "regulatory_news": regulatory_news,
        "multi_agent_insights": multi_agent_insights,
        "bitcoin_price": bitcoin_price
    }


def predict_market_trends(data):
    # Placeholder for predictive model
    # Implement your predictive model here
    return "Predicted market trends based on data."


def get_crypto_price(ticker: str) -> str:
    """Fetches the latest price for the specified cryptocurrency ticker."""
    price_agent = PriceAgent()
    return price_agent.get_crypto_price(ticker)


def interpret_query(query: str) -> str:
    """Interprets the user's query and fetches data from the appropriate module."""
    print(f"Received query: {query}")  # Debugging output
    query = query.lower()
    if any(word in query for word in ["sentiment", "tone", "positive", "negative", "emotion", "feeling"]):
        print("Forwarding sentiment query to sentiment agent...")
        return ask_sentiment_agent(query)
    elif "price" in query or "cost" in query or "value" in query:
        print("Interpreting as a price query.")  # Debugging output
        # Map common cryptocurrency names to their ticker symbols
        crypto_map = {
            "bitcoin": "BTC",
            "ethereum": "ETH",
            "litecoin": "LTC",
            "ripple": "XRP",
            "cardano": "ADA",
            # Add more cryptocurrencies as needed
        }
        # Extract ticker symbol or name from query
        words = query.split()
        for word in words:
            print(f"Checking word: {word}")  # Debugging output
            if word.upper() in crypto_map.values():
                print(f"Fetching price for ticker: {word.upper()}")  # Debugging output
                return get_crypto_price(word.upper())
            elif word in crypto_map:
                print(f"Fetching price for cryptocurrency: {word}")  # Debugging output
                return get_crypto_price(crypto_map[word])
        return "Please specify a valid cryptocurrency ticker or name."
    elif "news" in query:
        print("Interpreting as a news query.")  # Debugging output
        articles = fetch_news()
        if not articles:
            return "No recent cryptocurrency news available."
        lines = []
        for article in articles[:5]:
            if not article:
                continue
            title = article.get('title') or 'Untitled'
            url = article.get('url') or '#'
            lines.append(f"- {title} ({url})")
        return "Here are the latest crypto news articles:\n" + "\n".join(lines)
    elif "summarize" in query or "summary" in query:
        print("Interpreting as a summarization query.")  # Debugging output
        summaries = summarize_articles()
        if not summaries:
            return "No articles available to summarize."
        return "Here are the summaries of the latest articles:\n" + "\n".join([f"- {summary.get('title', 'Untitled') or 'Untitled'}: {summary.get('summary', 'No summary available') or 'No summary available'}" for summary in summaries])
    elif "graph" in query or "chart" in query:
        print("Interpreting as a graph query.")  # Debugging output
        # Assuming a default ticker and days for demonstration
        ticker = "BTC-USD"
        days = 365
        display_crypto_graph(ticker, days)
        return "Displaying the graph for Bitcoin (BTC-USD) over the past year."
    elif "day" in query or "date" in query:
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}."
    elif "sentiment" in query:
        print("Interpreting as a sentiment query.")  # Debugging output
        articles = fetch_news()
        if not articles:
            return "No news available to analyze sentiment."
        # Ensure clean articles are passed to analyze_sentiment
        clean_articles = [{
            'title': article.get('title', '') or '',
            'content': article.get('content', '') or ''
        } for article in articles]
        sentiment_result = analyze_sentiment(clean_articles)
        return "Sentiment Analysis Result:\n" + str(sentiment_result)

    else:
        print("Query type not recognized.")  # Debugging output
        return ("I'm sorry, I can't help with that request. "
                "Please ask about cryptocurrency prices, news, sentiment, summarization, graph visualization, or the current date.")


def main():
    data = collect_data()
    prediction = predict_market_trends(data)
    print("Data Collected:", data)
    print("Prediction:", prediction)

    # Example usage of get_crypto_price
    bitcoin_price = get_crypto_price("BTC")
    print("Bitcoin Price:", bitcoin_price)

    # Example usage of interpret_query
    user_query = "What is the price of BTC?"
    response = interpret_query(user_query)
    print("Response:", response)


if __name__ == "__main__":
    main()
