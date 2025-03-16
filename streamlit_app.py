import streamlit as st
import pandas as pd
import sqlite3
from search_scrape import google_search, scrape_page
from database import save_result, get_results, create_database

# Initialize database
create_database()

# Set page configuration
st.set_page_config(page_title="KidsSmart+ Educational Database", layout="wide")

# Load Victoria University Logo
logo_path = "logo.png"  # Ensure the logo is in the same folder as streamlit_app.py

# Sidebar Navigation
st.sidebar.image(logo_path, width=150)
st.sidebar.title("📚 KidsSmart+ Educational Database")
page = st.sidebar.radio("Navigate", ["Home", "Download Data"])

# Home Page
if page == "Home":
    # Display Logo and Centered Title
    st.image(logo_path, width=120)  # Properly display the logo
    st.markdown("<h1 style='text-align: center; font-size: 28px; font-weight: bold;'>KidsSmart+ Educational Database</h1>", unsafe_allow_html=True)

    st.write("### 🔍 Search for Educational Data")

    # Search Input
    search_query = st.text_input("Enter your search query:")

    if st.button("Search"):
        if search_query:
            st.write("**Searching Google...** 🔎")
            results = google_search(search_query)

            if results:
                st.write(f"**Found {len(results)} results. Scraping content...** 🛠️")

                search_data = []  # Store search results for display
                for res in results:
                    title, link = res["title"], res["link"]
                    content = scrape_page(link)
                    save_result(search_query, title, link, content)

                    # Append data to list for immediate preview
                    search_data.append({"Title": title, "Link": link, "Content": content[:300] + "..."})  # Show only first 300 chars

                st.success("Search and scraping completed! ✅ Data saved to database.")

                # Display Results
                st.write("### 🔍 Search Results Preview")
                for item in search_data:
                    st.markdown(f"#### 📌 [{item['Title']}]({item['Link']})")
                    st.write(item["Content"])
                    st.write("---")  # Separator for readability

            else:
                st.warning("No search results found. Try another query.")

# Download Data Page
elif page == "Download Data":
    st.write("### 📥 Download Stored Data")

    rows = get_results()

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Query", "Title", "Link", "Content"])
        
        # Display table with sorting
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Data as CSV", csv, "search_results.csv", "text/csv")
    
    else:
        st.info("No results stored yet. Perform a search to get data.")

# Footer with Credits (Dark Background + White Text)
st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
                background-color: black; color: white; 
                text-align: center; font-size: 14px; padding: 10px;">
        Created by <b>Mohamed Imaad Muhinudeen (s8078260)</b> & <b>Kavin Nanthakumar (s8049341)</b> | 
        All Rights Reserved | KidsSmart+
    </div>
    """,
    unsafe_allow_html=True
)
