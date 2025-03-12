import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = {
    "newsapi": os.getenv("NEWSAPI_KEY"),  # ✅ Ensure this matches your `.env` key
    "openai": os.getenv("OPENAI_API_KEY"),
    "financialdatasets": os.getenv("FINANCIAL_DATASETS_API_KEY"),
}

NEWS_SOURCES = [
    "https://newsapi.org/v2/everything?q=cryptocurrency"
]

# Optional debug messages clearly verifying keys
if not API_KEYS["openai"]:
    print("❌ ERROR: OpenAI API Key is missing!")
else:
    print(f"✅ OpenAI API Key Loaded: {API_KEYS['openai'][:10]}********")

if not API_KEYS["newsapi"]:
    print("❌ ERROR: NewsAPI Key is missing!")
else:
    print(f"✅ NewsAPI Key Loaded: {API_KEYS['newsapi'][:10]}********")

if not API_KEYS["financialdatasets"]:
    print("❌ ERROR: Financial Datasets API Key is missing!")
else:
    print(f"✅ Financial Datasets API Key Loaded: {API_KEYS['financialdatasets'][:10]}********")
