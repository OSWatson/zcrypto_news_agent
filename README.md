📢 zCrypto News Agent - AI-Powered Cryptocurrency News & Analysis
🚀 zCrypto News Agent is an AI-powered application designed to fetch, analyze, and summarize the latest cryptocurrency news using LangChain and OpenAI. It integrates multiple agents to provide both local and real-time web-based insights into cryptocurrency trends.

📌 Features
🔹 News Fetching & Sentiment Analysis

Retrieves cryptocurrency news articles from NewsAPI.
Performs sentiment analysis on articles to determine market sentiment.
Displays news headlines, content summaries, and sentiment scores in a Streamlit dashboard.
🔹 Local AI Chatbot (LangChain)

Uses OpenAI GPT-4 to answer questions based on locally stored news articles.
Implements FAISS vector search for efficient article retrieval.
🔹 Real-Time Web Search Agent

Uses SerpAPI to retrieve the latest web-based cryptocurrency news.
Enhances responses by combining real-time web search with AI-based analysis.
🔹 Multi-Agent System

Combines local news retrieval and real-time web search into a single agent.
Determines whether to use stored news or conduct a live web search based on the query.
🛠️ Installation
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/YOUR_USERNAME/zcrypto_news_agent.git
cd zcrypto_news_agent
2️⃣ Create a Virtual Environment
sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up API Keys
Create a .env file in the project root and add your API keys:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
NEWSAPI_API_KEY=your_newsapi_key
SERPAPI_API_KEY=your_serpapi_key
⚠️ Ensure the .env file is listed in .gitignore to keep your keys secure!

🚀 Running the Application
Start the Streamlit dashboard:

sh
Copy
Edit
streamlit run app/dashboard.py
The app will be accessible at http://localhost:8501.

📂 Project Structure
bash
Copy
Edit
zcrypto_news_agent/
│── app/
│   ├── dashboard.py       # Streamlit UI for news and chatbot
│
├── config/
│   ├── settings.py        # Configuration settings
│
├── data/
│   ├── articles.json      # Locally stored crypto news articles
│
├── logs/
│   ├── app.log            # Log file for debugging
│
├── modules/
│   ├── fetch_news.py      # Fetches news from NewsAPI
│   ├── sentiment.py       # Sentiment analysis module
│   ├── langchain_agent.py # Local AI chatbot using LangChain
│   ├── web_search_agent.py # Real-time web search agent (SerpAPI)
│   ├── multi_agent.py     # Multi-agent combining local & web search
│
├── .env                   # API keys (not pushed to GitHub)
├── .gitignore             # Excludes `.env` file from Git tracking
├── README.md              # Project documentation
├── requirements.txt       # Required dependencies
🧠 How It Works
1️⃣ Fetching Crypto News & Sentiment Analysis
The fetch_news.py script pulls articles from NewsAPI.
The sentiment.py script analyzes the tone of each article (positive, neutral, negative).
The news and sentiment scores are displayed in the Streamlit dashboard.
2️⃣ Local AI Chatbot (LangChain)
Uses GPT-4 to answer questions based on stored news articles.
Implements FAISS vector search for efficient retrieval.
Handles direct user queries related to recent cryptocurrency news.
3️⃣ Real-Time Web Search Agent
Uses SerpAPI to perform live web searches for crypto news.
Returns real-time results when local news articles are insufficient.
4️⃣ Multi-Agent System
Integrates local news retrieval and real-time web search.
Automatically determines whether to fetch stored articles or perform a live search.
🔒 Security Considerations
✅ .env File

📌 Future Enhancements
✅ Integration with Blockchain APIs
✅ Predictive Sentiment Analysis
✅ Crypto Price Trend Visualization

💡 Contributing
🚀 Contributions are welcome!

Fork the repo
Create a new branch
Submit a pull request
📄 License
This project is licensed under the MIT License.

