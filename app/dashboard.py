import sys
import os

# Ensure Python can find the `modules/` folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from modules.fetch_news import fetch_news
from modules.sentiment import analyze_sentiment
from modules.langchain_agent import ask_question  # Local Chatbot
from modules.multi_agent import ask_multi_agent    # Multi-agent integrating local and web search

st.title("📢 Crypto News Agent - AI-Powered Insights")

# Now we have four tabs: News & Sentiment, Local Chatbot, Multi-Agent Chat, and Graph
tab1, tab2, tab3, tab4 = st.tabs([
    "📰 News & Sentiment",
    "💬 Chatbot",
    "🌐 Multi-Agent Chat",
    "📈 Graph"
])

with tab1:
    st.info("🔄 Fetching latest news...")
    articles = fetch_news()

    if not articles:
        st.error("❌ No articles found. Please check the API connection.")
        st.stop()

    df = pd.DataFrame(articles)
    df["content"] = df["content"].fillna("")
    df["sentiment"] = df["content"].apply(lambda x: analyze_sentiment(x))

    st.subheader("📰 Latest Cryptocurrency News")
    st.write(df[["title", "content", "url", "sentiment"]])

    st.subheader("📊 Sentiment Analysis Breakdown")
    st.bar_chart(df["sentiment"].value_counts())

    st.success("✅ Latest news successfully loaded!")

with tab2:
    st.subheader("💬 Chat with the Crypto News AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Ask about crypto news, trends, or summaries...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        response = ask_question(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").markdown(response)

with tab3:
    st.subheader("🌐 Chat with the Multi-Agent (Local & Web Search)")
    
    if "multi_messages" not in st.session_state:
        st.session_state.multi_messages = []

    for msg in st.session_state.multi_messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input_multi = st.chat_input("Ask the multi-agent about crypto trends or news...")
    if user_input_multi:
        st.session_state.multi_messages.append({"role": "user", "content": user_input_multi})
        st.chat_message("user").markdown(user_input_multi)

        response_multi = ask_multi_agent(user_input_multi)
        st.session_state.multi_messages.append({"role": "assistant", "content": response_multi})
        st.chat_message("assistant").markdown(response_multi)

# Update the Graph tab to fetch and display crypto price data.
from modules.graph_viz import display_crypto_graph

with tab4:
    st.subheader("📈 Graph")
    
    ticker = st.text_input("Enter a crypto ticker (e.g., BTC-USD):", value="BTC-USD")
    
    days = st.number_input("How many days of historical data?", min_value=1, max_value=5000, value=365)

    if ticker:
        display_crypto_graph(ticker, days)


