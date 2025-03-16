import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from database import save_result, create_database

# Get API Key from Environment Variable
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("Error: SerpAPI key not found. Set the API key as an environment variable.")

# Initialize database
create_database()

# Google Search Function
def google_search(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": 5
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

# Web Scraping Function
def scrape_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join([p.get_text() for p in paragraphs])
        return text[:1000]
    except Exception as e:
        return f"Scraping failed: {str(e)}"

# Run the script
if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = google_search(query)

    if not results:
        print("No search results found.")
    else:
        print("\n=== Search Results & Scraped Content ===")
        for idx, res in enumerate(results, 1):
            title, link = res["title"], res["link"]
            content = scrape_page(link)

            # Save to database
            save_result(query, title, link, content)

            print(f"\n{idx}. {title} - {link}")
            print(f"Extracted Content: {content[:300]}...")
