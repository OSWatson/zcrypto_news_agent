import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

# Ensure Python can find the `modules/` folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from modules.fetch_news import fetch_news
from modules.sentiment import analyze_sentiment
from modules.gov_news_agent import fetch_regulations_gov_news
from modules.langchain_agent import ask_question  # Local Chatbot
from modules.multi_agent import ask_multi_agent    # Multi-agent integrating local and web search
from modules.ai_agent import interpret_query
from modules.price_agent import PriceAgent

def generate_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available to you
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# Custom CSS for scrolling tabs
st.markdown(
    """
    <style>
    .stTabs [role="tablist"] {
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
    }
    .stTabs [role="tab"] {
        flex: 0 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📢 Crypto News Agent - AI-Powered Insights")

# Define module files
module_files = [
    'ai_agent.py',
    'test_price.py',
    'sentiment.py',
    'gov_news_agent.py',
    'graph_viz.py',
    'fetch_news.py',
    'multi_agent.py',
    'web_search_agent.py',
    'price_agent.py',
    'langchain_agent.py',
    'notifier.py',
    'scraper.py',
    'summarizer.py',
]

# Existing tabs
existing_tabs = [
    "📰 News & Sentiment",
    "💬 Chatbot",
    "🌐 Multi-Agent Chat",
    "📈 Graph",
    "🤖 AI Agent"
]

# Combine existing and new tabs
all_tabs = existing_tabs + [f"{file}" for file in module_files]

# Create tab objects
all_tab_objects = st.tabs(all_tabs)

# Display content for each existing tab
with all_tab_objects[0]:
    st.info("🔄 Fetching latest news...")
    articles = fetch_news()

    if not articles:
        st.error("❌ No articles found. Please check the API connection.")
        st.stop()

    # Create DataFrame
    df = pd.DataFrame(articles)
    df["content"] = df["content"].fillna("")
    
    # Combine title and content for better sentiment analysis
    df["full_text"] = df["title"] + " " + df["content"]
    
    # Process sentiment analysis for all articles
    sentiments = []
    sentiment_scores = []

    for text in df["full_text"]:
        sentiment_result = analyze_sentiment(text)
        print(f"Sentiment Result: {sentiment_result}")  # Debugging line
        sentiment_lines = sentiment_result.split('\n')
        
        if len(sentiment_lines) > 1 and ': ' in sentiment_lines[0]:
            overall_sentiment = sentiment_lines[0].split(': ')[1]
        else:
            overall_sentiment = "Neutral"
        
        if len(sentiment_lines) > 1 and ': ' in sentiment_lines[1]:
            polarity_score = float(sentiment_lines[1].split(': ')[1])
        else:
            polarity_score = 0.0
        
        sentiments.append(overall_sentiment)
        sentiment_scores.append(polarity_score)
    
    df["sentiment"] = sentiments
    df["sentiment_score"] = sentiment_scores

    # Display news with sentiment
    st.subheader("📰 Latest Cryptocurrency News")
    news_display = df[["title", "content", "url", "sentiment"]].copy()
    news_display["sentiment"] = news_display["sentiment"].apply(lambda x: f"🟢 {x}" if x == "Positive" else f"🔴 {x}" if x == "Negative" else f"⚪ {x}")
    st.write(news_display)

    # Display sentiment analysis
    st.subheader("📊 Sentiment Analysis Breakdown")
    
    # Create sentiment distribution chart
    sentiment_counts = df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)
    
    # Display average sentiment score
    avg_sentiment = df["sentiment_score"].mean()
    st.metric("Average Sentiment Score", f"{avg_sentiment:.2f}", 
              delta="Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral")

    st.success("✅ Latest news successfully loaded!")

with all_tab_objects[1]:
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

with all_tab_objects[2]:
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

with all_tab_objects[3]:
    st.subheader("📈 Graph")
    
    ticker = st.text_input("Enter a crypto ticker (e.g., BTC-USD):", value="BTC-USD")
    
    days = st.number_input("How many days of historical data?", min_value=1, max_value=5000, value=365)

    if ticker:
        display_crypto_graph(ticker, days)

with all_tab_objects[4]:
    st.subheader("🤖 AI Agent Chat")
    st.info("Chat with the AI agent to get insights, graphs, and news updates.")
    
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for msg in st.session_state.ai_messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input_ai = st.chat_input("Ask the AI agent about crypto trends, news, or request a graph...")
    if user_input_ai:
        st.session_state.ai_messages.append({"role": "user", "content": user_input_ai})
        st.chat_message("user").markdown(user_input_ai)

        # Use interpret_query to generate response
        response_ai = interpret_query(user_input_ai)
        st.session_state.ai_messages.append({"role": "assistant", "content": response_ai})
        st.chat_message("assistant").markdown(response_ai)

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
                    # Extract keyword and number from user input
                    words = user_input.split()
                    keyword = next((word for word in words if word.isalpha()), None)
                    num_articles = next((int(word) for word in words if word.isdigit()), None)

                    # Check for government-related keywords
                    government_keywords = {"government", "FEMA", "SEC", "IRS", "NASA", "regulations", "agency"}
                    if keyword and keyword.lower() in government_keywords:
                        # Fetch government news articles
                        articles = fetch_regulations_gov_news(api_key=os.getenv("REGULATIONS_GOV_API_KEY"), query=keyword, page_size=num_articles or 10)
                    else:
                        # Fetch regular news articles
                        articles = fetch_news()

                    if not articles:
                        response = "No articles available for sentiment analysis."
                    else:
                        # Perform sentiment analysis
                        response = analyze_sentiment(articles)
                except Exception as e:
                    response = f"Could not perform sentiment analysis. Error: {str(e)}"
            elif file == 'gov_news_agent.py':
                try:
                    # Extract keyword and number from user input
                    words = user_input.split()
                    keyword = next((word for word in words if word.isalpha()), "crypto")
                    num_articles = next((int(word) for word in words if word.isdigit()), 10)

                    # Fetch articles using the government news agent
                    articles = fetch_regulations_gov_news(api_key=os.getenv("REGULATIONS_GOV_API_KEY"), query=keyword, page_size=num_articles)

                    if not articles:
                        response = "No articles found for that topic."
                    else:
                        # Format the results into a clean string
                        response = "\n".join([f"{article['title']} ({article['posted_date']})\n{article['url']}" for article in articles])
                except Exception as e:
                    response = f"Could not fetch articles. Error: {str(e)}"
            else:
                # Default response logic
                response = f"The {file} agent received your question: {user_input}"

            st.session_state[f"{file}_messages"].append({"role": "assistant", "content": response})
            st.chat_message("assistant").markdown(response)


