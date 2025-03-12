import sys
import os

# Ensure Python finds the `config` module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import logging
import requests
from config.settings import API_KEYS, NEWS_SOURCES

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_news():
    url = f"{NEWS_SOURCES[0]}&apiKey={API_KEYS['newsapi']}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()

        # 🔍 Debug: Print API response
        print("\n🔹 Full API Response:\n", json.dumps(data, indent=2))

        if "articles" not in data or not data["articles"]:
            logging.warning("⚠️ API returned no articles.")
            return []

        articles = [
            {
                "title": a.get("title", "No title"),
                "content": a.get("description", "No content"),
                "url": a.get("url", "#"),
                "published_at": a.get("publishedAt", None)  # ✅ Include the article's published date
            }
            for a in data["articles"]
        ]

        # Ensure `data/` folder exists
        os.makedirs("data", exist_ok=True)

        # Save articles to JSON file
        with open("data/articles.json", "w") as f:
            json.dump(articles, f, indent=4)

        print(f"✅ Successfully saved {len(articles)} articles to data/articles.json")
        logging.info(f"✅ Successfully saved {len(articles)} articles.")

        return articles

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error fetching news: {e}")
        print(f"❌ Error fetching news: {e}")
        return []

if __name__ == "__main__":
    fetch_news()
