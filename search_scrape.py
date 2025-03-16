import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import sqlite3

# Get API Key from Streamlit Secrets
API_KEY = st.secrets["SERPAPI_KEY"]

# Initialize database
def create_database():
    conn = sqlite3.connect("search_results.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  query TEXT,
                  title TEXT,
                  link TEXT,
                  content TEXT)''')
    conn.commit()
    conn.close()

# Save search result to database
def save_result(query, title, link, content):
    conn = sqlite3.connect("search_results.db")
    c = conn.cursor()
    c.execute("INSERT INTO results (query, title, link, content) VALUES (?, ?, ?, ?)",
              (query, title, link, content))
    conn.commit()
    conn.close()

# Fetch all results from the database
def fetch_all_results():
    conn = sqlite3.connect("search_results.db")
    c = conn.cursor()
    c.execute("SELECT * FROM results")
    results = c.fetchall()
    conn.close()
    return results

# Export database to a file (e.g., CSV)
def export_database():
    results = fetch_all_results()
    if results:
        with open("search_results.csv", "w", encoding="utf-8") as file:
            file.write("ID,Query,Title,Link,Content\n")
            for result in results:
                file.write(f"{result[0]},{result[1]},{result[2]},{result[3]},{result[4]}\n")
        st.success("Data exported to search_results.csv")
    else:
        st.warning("No data to export.")

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

# Streamlit UI
def home_page():
    # Add logo to the top-right corner
    col1, col2 = st.columns([3, 1])  # Adjust the ratio for layout
    with col1:
        st.title("KidsSmart+ Educational Database")
    with col2:
        st.image("logo.png", width=100)  # Ensure logo.png is in the same directory

    st.write("Welcome to KidsSmart+ Educational Database. Use the search bar below to find educational content.")

    query = st.text_input("Enter your search query:")

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            st.write("🔎 Searching Google...")
            results = google_search(query)

            if not results:
                st.error("No search results found.")
            else:
                st.subheader("Search Results & Scraped Content")
                for idx, res in enumerate(results, 1):
                    title, link = res["title"], res["link"]
                    content = scrape_page(link)

                    # Save to database
                    save_result(query, title, link, content)

                    st.markdown(f"### {idx}. [{title}]({link})")
                    st.write(content[:500] + "...")  # Show first 500 chars

def database_page():
    st.title("Database Page")
    st.write("Download the search results from the database.")

    # Fetch all results from the database
    results = fetch_all_results()

    if results:
        st.write("Search Results:")
        for idx, res in enumerate(results, 1):
            st.markdown(f"### {idx}. {res[2]}")  # res[2] is the title
            st.write(f"**Link:** {res[3]}")  # res[3] is the link
            st.write(f"**Content:** {res[4][:500]}...")  # res[4] is the content
    else:
        st.write("No results found in the database.")

    # Add a download button
    if st.button("Download Data"):
        export_database()

# Footer
def footer():
    st.markdown("---")
    st.markdown("**All rights reserved KidsSmart+**")
    st.markdown("**Mohamed Imaad Muhinudeen (s8078260) & Kavin Nanthakumar (s8049341)**")

# Main function to handle page navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Database"])

    if page == "Home":
        home_page()
    elif page == "Database":
        database_page()

    footer()

if __name__ == "__main__":
    main()