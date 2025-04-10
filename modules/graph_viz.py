import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from modules.gov_news_agent import fetch_regulations_gov_news  # ✅ Updated source
from modules.fetch_news import fetch_news
from modules.sentiment import analyze_sentiment

load_dotenv()

def fetch_crypto_price_data(
    ticker: str = "BTC-USD",
    days: int = 365,
    interval: str = "day",
    interval_multiplier: int = 1
) -> pd.DataFrame:
    """
    Fetches historical crypto price data for the given ticker.
    """
    api_key = os.getenv("FINANCIAL_DATASETS_API_KEY")
    if not api_key:
        st.error("API key not found. Please set your FINANCIAL_DATASETS_API_KEY in the environment.")
        return pd.DataFrame()

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')

    params = {
        "ticker": ticker,
        "interval": interval,
        "interval_multiplier": interval_multiplier,
        "start_date": start_date,
        "end_date": end_date,
        "limit": 5000
    }

    headers = {"X-API-KEY": api_key}

    response = requests.get("https://api.financialdatasets.ai/crypto/prices/",
                            headers=headers, params=params)

    if response.status_code != 200:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    prices = data.get('prices', {}).get('prices', [])

    if not prices:
        st.warning("No price data found.")
        return pd.DataFrame()

    df = pd.DataFrame(prices)
    if 'time' in df.columns:
        df.rename(columns={'time': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

    return df

def fetch_article_data(price_dates: list) -> pd.DataFrame:
    """
    Fetches recent cryptocurrency-related regulatory articles from Regulations.gov
    and aligns their timestamps with the closest available price date.
    """
    API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")
    if not API_KEY:
        return pd.DataFrame()

    articles = fetch_regulations_gov_news(API_KEY)

    if not articles:
        return pd.DataFrame()

    df_news = pd.DataFrame(articles)

    if 'posted_date' in df_news.columns:
        df_news['posted_date'] = pd.to_datetime(df_news['posted_date'], errors='coerce')
        df_news = df_news.dropna(subset=['posted_date'])
        df_news['posted_date'] = df_news['posted_date'].dt.date

        # Snap article timestamps to closest available price date
        df_news['closest_price_date'] = df_news['posted_date'].apply(
            lambda x: min(price_dates, key=lambda d: abs(d - x))
        )

        df_news.set_index('closest_price_date', inplace=True)

    return df_news

def display_crypto_graph(ticker: str, days: int = 365):
    """
    Fetches crypto price data and overlays article events as dots.
    Numbered annotations will indicate which article corresponds to each dot.
    """
    df = fetch_crypto_price_data(ticker=ticker, days=days)

    if df.empty:
        st.warning("No price data available to display.")
        return

    # Convert price timestamps to date-only format
    df.index = df.index.date  

    # Get available price dates
    price_dates = df.index.tolist()  

    # Fetch news and align with closest price dates
    df_news = fetch_article_data(price_dates)

    # Prepare article info for display
    article_list = []

    # Plot price data
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['close'], label="Closing Price", color="blue")

    # Overlay article events as dots only (with numbering)
    if not df_news.empty:
        for i, (date, row) in enumerate(df_news.iterrows(), start=1):
            ax.scatter(date, df.loc[date, "close"], color="red", s=100)  # Larger dots for visibility
            ax.annotate(str(i), (date, df.loc[date, "close"]), textcoords="offset points",
                        xytext=(0,10), ha='center', fontsize=10, color="white",
                        bbox=dict(facecolor="red", alpha=0.5, edgecolor="none", boxstyle="circle"))

            article_list.append(f"🔴 **{i}. {date}: {row['title']}**")

    ax.set_title(f"{ticker} Price Chart with News Events")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the article list with matching numbers
    if article_list:
        left, right = st.columns(2)  # Split screen into two columns
        mid_point = len(article_list) // 2

        with left:
            st.subheader("🔹 News Impact (Left)")
            for article in article_list[:mid_point]:  # First half of articles
                st.markdown(article)

        with right:
            st.subheader("🔹 News Impact (Right)")
            for article in article_list[mid_point:]:  # Second half of articles
                st.markdown(article)

def run_module_ui(existing_tabs, all_tab_objects):
    # Display content for each new module tab
    for i, file in enumerate(module_files, start=len(existing_tabs)):
        with all_tab_objects[i]:
            st.subheader(f"Agent for {file}")
            
            if f"{file}_messages" not in st.session_state:
                st.session_state[f"{file}_messages"] = []

            for msg in st.session_state[f"{file}_messages"]:
                st.chat_message(msg["role"]).markdown(msg["content"])

            user_input = st.chat_input(f"Ask the {file} agent...")
            if user_input:
                st.session_state[f"{file}_messages"].append({"role": "user", "content": user_input})
                st.chat_message("user").markdown(user_input)

                # Specific logic for sentiment.py
                if file == 'sentiment.py':
                    try:
                        # Simulate asking the fetch_news agent
                        articles = fetch_news()
                        if not articles:
                            response = "No articles available for sentiment analysis."
                        else:
                            words = user_input.split()
                            num_articles = next((int(word) for word in words if word.isdigit()), len(articles))

                            # Select articles based on user input
                            selected_articles = articles[:num_articles]

                            # Display selected articles
                            st.subheader("Selected Articles for Sentiment Analysis")
                            for article in selected_articles:
                                st.markdown(f"**{article['title']}**: {article.get('content', 'No content available')}")

                            # Perform sentiment analysis
                            sentiments = [analyze_sentiment(article.get('content', '')) for article in selected_articles]
                            response = "Sentiment Analysis Results:\n" + "\n".join([f"- {article['title']}: {sentiment}" for article, sentiment in zip(selected_articles, sentiments)])
                            
                            # Display sentiment analysis results
                            st.subheader("Sentiment Analysis Results")
                            st.markdown(response)
                    except Exception as e:
                        response = f"Could not perform sentiment analysis. Error: {str(e)}"
                else:
                    # Default response logic
                    response = f"The {file} agent received your question: {user_input}"

                st.session_state[f"{file}_messages"].append({"role": "assistant", "content": response})
                st.chat_message("assistant").markdown(response)
