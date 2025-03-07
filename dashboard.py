import streamlit as st
import sqlite3
import pandas as pd

# Title of the dashboard
st.title("📊 Educational Datasets Dashboard")

# Connect to SQLite database
conn = sqlite3.connect("education_data.db")

# Fetch data
query = "SELECT title, file_type, year, description, url FROM datasets"
df = pd.read_sql(query, conn)
conn.close()

# Sidebar filters
year_filter = st.sidebar.selectbox("Filter by Year", ["All"] + sorted(df["year"].unique().tolist()))
file_type_filter = st.sidebar.radio("Filter by File Type", ["All", "PDF", "Excel"])

# Apply filters
if year_filter != "All":
    df = df[df["year"] == year_filter]
if file_type_filter != "All":
    df = df[df["file_type"] == file_type_filter]

# Display Data
st.write(f"Showing {len(df)} datasets")
st.dataframe(df)

# Provide download links
for index, row in df.iterrows():
    st.markdown(f"📄 **[{row['title']}]({row['url']})** ({row['file_type']}, {row['year']})")
    st.write(row['description'])

