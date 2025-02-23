import schedule
import time
from modules.fetch_news import fetch_news
from modules.summarizer import summarize_articles

def job():
    fetch_news()  # Fetch & save news
    summarize_articles()  # Summarize articles

schedule.every(1).hours.do(job)

print("🔄 Crypto News Agent is running... (Ctrl+C to stop)")
while True:
    schedule.run_pending()
    time.sleep(60)
