import os
import requests

# Get API key from environment variable
BRAVE_API_KEY = os.getenv('BRAVE_API_KEY')

if not BRAVE_API_KEY:
    print("Error: BRAVE_API_KEY not found in environment variables")
    print("Make sure you've sourced your .zshrc or .env file")
    exit(1)

def search_brave_news(query, count=5):
    try:
        """
        Searches Brave News API for the latest news links.
        """
        url = "https://api.search.brave.com/res/v1/news/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        params = {
            "q": query,
            "count": count,
            "freshness": "pd",  # 'pd' = Past Day, 'pw' = Past Week
            "search_lang": "en"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as error:
        print(f"Error @ {search_brave_news.__name__} : {error}")
    

def test_brave_search(query):
    """Test Brave Search API with a query"""
    url = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": 5  # Number of results to return
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\n🔍 Search Query: {query}")
        print(f"📊 Found {len(data.get('web', {}).get('results', []))} results\n")
        
        # Print search results
        for i, result in enumerate(data.get('web', {}).get('results', []), 1):
            print(f"{i}. {result.get('title')}")
            print(f"   URL: {result.get('url')}")
            print(f"   Description: {result.get('description')[:150]}...")
            print()
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    # Test the API
    print("Testing Brave Search API...")
    test_brave_search("latest AI news")


