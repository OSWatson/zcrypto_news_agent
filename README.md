# 📢 zCrypto News Agent - AI-Powered Cryptocurrency News & Analysis

🚀 **zCrypto News Agent** is a modular AI-powered Streamlit app that fetches, analyzes, and summarizes cryptocurrency news, prices, and government regulation documents using a system of intelligent agents. Powered by OpenAI, LangChain, and real-time APIs, it helps you stay informed about crypto market trends.

---

## 📌 Features

### 🔹 News Fetching & Sentiment Analysis
- Retrieves cryptocurrency news from **NewsAPI**
- Retrieves government regulation documents from **Regulations.gov**
- Analyzes overall market sentiment using **TextBlob**
- Highlights positivity, negativity, and subjectivity of news

### 💬 Local AI Chatbot (LangChain)
- Powered by **OpenAI GPT-4** for contextual responses
- Utilizes **FAISS** vector search to ground answers in real documents
- Understands queries like “What is the sentiment for Bitcoin today?”

### 🌐 Government News Agent
- Uses `gov_news_agent.py` to fetch regulatory documents related to crypto
- Integrated into sentiment analysis when appropriate

### 📉 Price & Graph Agent
- Uses `PriceAgent` to retrieve current crypto prices
- Supports dynamic graph generation via Streamlit (e.g., BTC-USD trends)

### 🤖 Multi-Agent System (In Progress)
- Plans to intelligently route queries to the right agent
- Handles compound requests (e.g., “Give me a chart and summary of Bitcoin sentiment”)

---

## 🛠️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/zcrypto_news_agent.git
cd zcrypto_news_agent
2️⃣ Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
# Then activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up API Keys
Create a .env file in the root directory:

env
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
NEWSAPI_API_KEY=your_newsapi_key
REGULATIONS_GOV_API_KEY=your_regulations_api_key
✅ Ensure .env is listed in .gitignore

🚀 Running the App
bash
Copy
Edit
streamlit run app/dashboard.py
Visit http://localhost:8501 in your browser.

📂 Project Structure
bash
Copy
Edit
zcrypto_news_agent/
├── app/
│   └── dashboard.py         # Main Streamlit UI
├── config/
│   └── settings.py          # API keys and source URLs
├── data/
│   └── articles.json        # Locally cached articles
├── logs/
│   └── app.log              # Debug logs
├── modules/
│   ├── fetch_news.py        # Fetches general news
│   ├── gov_news_agent.py    # Fetches government news
│   ├── sentiment.py         # Performs sentiment analysis
│   ├── price_agent.py       # Crypto price retrieval
│   ├── langchain_agent.py   # LangChain + FAISS local chatbot
│   ├── ai_agent.py          # Query interpreter + router
│   ├── summarizer.py        # Article summarization
│   └── ... (other agents)
├── .env                     # 🔒 API credentials (excluded from Git)
├── .env.example             # Safe template for others
├── .gitignore               # Prevents key leaks
├── requirements.txt         # Dependencies
└── README.md                # This file
🧠 How It Works
📰 News + Sentiment
fetch_news.py pulls crypto articles

sentiment.py analyzes tone: Positive, Neutral, Negative

🏛️ Gov News + Analysis
gov_news_agent.py pulls documents from Regulations.gov

Can optionally pass these into the sentiment pipeline

💬 Local AI Agent
ai_agent.py listens for keywords (e.g., "sentiment", "price", "chart")

Routes to the appropriate module

Supports compound queries (e.g., “Show me the price and sentiment of Bitcoin”)

📈 Graph Generation
Uses graph_viz.py to show historical charts for coins

🔒 Security Notes
Never commit .env files with real API keys

Use .env.example to share expected keys with collaborators

🧪 Example Queries to Try
“What is the current sentiment for Bitcoin?”

“Show me the latest government crypto documents”

“Give me the sentiment of the top 5 crypto articles”

“What’s the price of Ethereum?”

“Display a graph of Bitcoin over the last 90 days”

✅ Future Enhancements
🔁 Real-time news refresh scheduler

📊 Deeper NLP for emotion and entity tracking

🔗 Blockchain API integration (on-chain metrics)

🤹 Streamlit chatbot memory across sessions

💡 Contributing
Pull requests are welcome!

Fork the repo

Create a feature branch

Submit a PR with a clear description