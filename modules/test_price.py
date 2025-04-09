import os
from price_agent import PriceAgent

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize PriceAgent
price_agent = PriceAgent()

# Fetch Bitcoin price
bitcoin_price = price_agent.get_crypto_price("BTC")

# Print the Bitcoin price
print("Bitcoin Price:", bitcoin_price) 