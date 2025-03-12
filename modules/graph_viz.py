import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


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
    Fetches recent crypto-related articles and aligns their timestamps with the closest available price date.
    """
    from modules.fetch_news import fetch_news  # Ensure this is correctly implemented
    articles = fetch_news()


    if not articles:
        return pd.DataFrame()


    df_news = pd.DataFrame(articles)


    if 'published_at' in df_news.columns:
        df_news['published_at'] = pd.to_datetime(df_news['published_at'])  # Convert to datetime
        df_news['published_at'] = df_news['published_at'].dt.date  # Strip time component


        # ✅ Snap article timestamps to the closest available price date
        df_news['closest_price_date'] = df_news['published_at'].apply(lambda x: min(price_dates, key=lambda d: abs(d - x)))


        # Set the closest price date as index
        df_news.set_index('closest_price_date', inplace=True)


    return df_news


def display_crypto_graph(ticker: str, days: int = 365):
    """
    Fetches crypto price data and overlays article events as dots.
    Article details are displayed separately on the screen.
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


    # Overlay article events as dots only (no text)
    if not df_news.empty:
        for date, row in df_news.iterrows():
            ax.scatter(date, df.loc[date, "close"], color="red", s=100)  # Larger dots for visibility
            article_list.append(f"📅 {date}: **{row['title']}**")


    ax.set_title(f"{ticker} Price Chart with News Events")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid()


    # Display the plot in Streamlit
    st.pyplot(fig)


    # Display the article list in two columns (left & right)
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


