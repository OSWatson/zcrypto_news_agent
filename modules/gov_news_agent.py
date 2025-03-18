import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_regulations_gov_news(api_key, query="crypto", page_size=10):
    """
    Fetch cryptocurrency-related regulatory news from Regulations.gov API.
    
    Args:
        api_key (str): Your API key from Regulations.gov.
        query (str): Search term (e.g., 'crypto', 'blockchain').
        page_size (int): Number of results to fetch.
    
    Returns:
        list: A list of relevant regulatory documents.
    """
    
    base_url = "https://api.regulations.gov/v4/documents"
    params = {
        "api_key": api_key,
        "filter[searchTerm]": query,
        "page[size]": page_size
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant details
        results = []
        for doc in data.get("data", []):
            doc_info = {
                "title": doc.get("attributes", {}).get("title", "No title"),
                "document_type": doc.get("attributes", {}).get("documentType", "Unknown"),
                "posted_date": doc.get("attributes", {}).get("postedDate", "Unknown"),
                "docket_id": doc.get("attributes", {}).get("docketId", "Unknown"),
                "url": f"https://www.regulations.gov/document/{doc.get('id', '')}"
            }
            results.append(doc_info)
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    # Load API key from .env file
    API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")
    
    if not API_KEY:
        print("Please set your Regulations.gov API key in the .env file.")
    else:
        news = fetch_regulations_gov_news(API_KEY)
        print(json.dumps(news, indent=2))
