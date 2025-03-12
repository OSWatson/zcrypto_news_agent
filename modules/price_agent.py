import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")

class PriceAgent:
    BASE_URL = "https://api.financialdatasets.ai/crypto/prices"

    def __init__(self):
        if not API_KEY:
            raise ValueError("❌ ERROR: Financial Datasets API Key is missing!")

    def get_crypto_price(self, ticker: str, interval: str = "day", interval_multiplier: int = 1) -> str:
        """Fetches the latest cryptocurrency price from Financial Datasets API."""
        headers = {"X-API-KEY": API_KEY}

        # Get today's date and a past date (7 days ago)
        today = datetime.today().strftime('%Y-%m-%d')
        seven_days_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

        params = {
            "ticker": f"{ticker}-USD",
            "interval": "day",  # ✅ Using 'day' instead of 'minute'
            "interval_multiplier": 1,
            "start_date": seven_days_ago,  # ✅ Fetch last 7 days of data
            "end_date": today
        }

        print(f"🔍 DEBUG: Sending request to {self.BASE_URL}")
        print(f"🔍 DEBUG: Headers = {headers}")
        print(f"🔍 DEBUG: Params = {params}")

        response = requests.get(self.BASE_URL, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"🔍 DEBUG: API Response JSON = {data}")  # ✅ Prints full API response

            # ✅ Fix: Correctly access the list of prices
            prices = data.get("prices", {}).get("prices", [])

            if not prices:  # ✅ Prevents KeyError if no data is returned
                return f"⚠️ No price data available for {ticker} in the selected date range."

            latest_price = prices[-1]  # ✅ Get the most recent price entry
            return f"The latest price for {ticker} is ${latest_price['close']:.2f} USD."
        else:
            return f"❌ API Error {response.status_code}: {response.text}"
