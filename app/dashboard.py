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

# Create three tabs: News & Sentiment, Local Chatbot, and Multi-Agent Chat
tab1, tab2, tab3 = st.tabs(["📰 News & Sentiment", "💬 Chatbot", "🌐 Multi-Agent Chat"])

with tab1:
    st.info("🔄 Fetching latest news...")
    articles = fetch_news()

    # Check if articles were fetched
    if not articles:
        st.error("❌ No articles found. Please check the API connection.")
        st.stop()

    # Convert articles to DataFrame
    df = pd.DataFrame(articles)

    # Replace None values in 'content' column
    df["content"] = df["content"].fillna("")

    # Perform Sentiment Analysis
    df["sentiment"] = df["content"].apply(lambda x: analyze_sentiment(x))

    # Display News Table
    st.subheader("📰 Latest Cryptocurrency News")
    st.write(df[["title", "content", "url", "sentiment"]])

    # Show Sentiment Analysis Chart
    st.subheader("📊 Sentiment Analysis Breakdown")
    st.bar_chart(df["sentiment"].value_counts())

    st.success("✅ Latest news successfully loaded!")

with tab2:
    st.subheader("💬 Chat with the Crypto News AI")
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Get user input for local chatbot
    user_input = st.chat_input("Ask about crypto news, trends, or summaries...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        # Get AI response from local chatbot
        response = ask_question(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").markdown(response)

with tab3:
    st.subheader("🌐 Chat with the Multi-Agent (Local & Web Search)")
    
    # Initialize multi-agent chat history if not already done
    if "multi_messages" not in st.session_state:
        st.session_state.multi_messages = []

    # Display multi-agent chat history
    for msg in st.session_state.multi_messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Get user input for multi-agent chat
    user_input_multi = st.chat_input("Ask the multi-agent about crypto trends or news...")

    if user_input_multi:
        st.session_state.multi_messages.append({"role": "user", "content": user_input_multi})
        st.chat_message("user").markdown(user_input_multi)

        # Get AI response from the multi-agent
        response_multi = ask_multi_agent(user_input_multi)
        st.session_state.multi_messages.append({"role": "assistant", "content": response_multi})
        st.chat_message("assistant").markdown(response_multi)
