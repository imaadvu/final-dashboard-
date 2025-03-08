import streamlit as st
import sqlite3
import pandas as pd
import os

# Set Page Config
st.set_page_config(page_title="Educational Dashboard", layout="wide")

# Define logo paths
vic_logo_path = "viclogo.png"
cc_logo_path = "cc_logo.png"

# CSS for styling
st.markdown("""
    <style>
    .big-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .sub-title {
        text-align: center;
        font-size: 30px;
        font-weight: normal;
        margin-top: 2px;
        margin-bottom: 30px;
    }
    .welcome-text {
        text-align: center;
        font-size: 18px;
        margin-bottom: 50px;
    }
    .feature-list {
        font-size: 22px;
        font-weight: bold;
        line-height: 2;
    }
    .centered-footer {
        text-align: center;
        font-size: 16px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to display DataFrame with clickable URLs
def display_clickable_dataframe(df):
    html = "<table border='1'><thead><tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            if col == "url":
                html += f"<td><a href='{row[col]}' target='_blank'>{row[col]}</a></td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    
    st.markdown(html, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "National Reports", "Schooling Data", "Additional Resources", "New Datasets"])

# Connect to SQLite database
conn = sqlite3.connect("education_data.db")

# Home Page
if page == "Home":
    if os.path.exists(vic_logo_path):
        st.image(vic_logo_path, width=200)
    else:
        st.warning("⚠️ Logo not found. Please check the file name and path.")

    st.markdown("<h1 class='big-title'>Kidssmart+</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Educational Dashboard</h2>", unsafe_allow_html=True)

    st.markdown("""
        <div class="welcome-text">
            Kidssmart+ is a cutting-edge educational data management system designed to automate the collection, processing, and management of program data.
            Empower your institution with seamless data integration and smart insights.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-list">
        📊 Access comprehensive educational datasets <br>
        🔍 Filter data by year or file type <br>
        📂 Download detailed reports
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
        <div class="centered-footer">
            <strong>IT CAPSTONE PROJECT</strong> <br>
            Made by <strong>Mohamed Imaad Muhinudeen (s8078260)</strong> & <strong>Kavin Nanthakumar (s8049341)</strong> <br>
        </div>
    """, unsafe_allow_html=True)

    if os.path.exists(cc_logo_path):
        st.image(cc_logo_path, width=100)

    st.markdown("<div class='centered-footer'>© 2024 Kidssmart+. All Rights Reserved.</div>", unsafe_allow_html=True)

elif page == "National Reports":
    st.header("📂 National Reports")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type='PDF'"
    df = pd.read_sql(query, conn)
    display_clickable_dataframe(df)

elif page == "Schooling Data":
    st.header("📂 Schooling Data")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type='Excel'"
    df = pd.read_sql(query, conn)
    display_clickable_dataframe(df)

elif page == "Additional Resources":
    st.header("📂 Additional Resources")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type IS NOT NULL"
    df = pd.read_sql(query, conn)
    display_clickable_dataframe(df)

elif page == "New Datasets":
    st.header("📂 New Datasets")
    query = "SELECT title, file_type, year, url FROM datasets WHERE year >= 2022"  # Adjust filter as needed
    df = pd.read_sql(query, conn)
    display_clickable_dataframe(df)

# Close database connection
conn.close()