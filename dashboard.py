import streamlit as st
import sqlite3
import pandas as pd
import os  # To check file paths
from cryptography.fernet import Fernet  # For decryption

# Set Page Config (Title & Layout)
st.set_page_config(page_title="Educational Dashboard", layout="wide")

# Define logo paths
vic_logo_path = "viclogo.png"  # Ensure this is in the same folder as `dashboard.py`
cc_logo_path = "cc_logo.png"  # Add a Creative Commons logo if needed

# Load encryption key (Use the same key from `scrape_acara.py`)
key = b'ejlFEAhslsWI2J0zer_OFwXexzf3woq4Qzgg0_vX5Wk='  # Replace with your actual key
cipher_suite = Fernet(key)

# Function to decrypt data
def decrypt_data(data):
    try:
        return cipher_suite.decrypt(data.encode()).decode()
    except:
        return data  # If decryption fails, return raw data

# CSS for styling
st.markdown("""
    <style>
    .big-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 2px; /* Reduced space below Kidssmart+ */
    }
    .sub-title {
        text-align: center;
        font-size: 30px;
        font-weight: normal;
        margin-top: 2px;  /* Pull it up closer */
        margin-bottom: 30px;
    }
    .welcome-text {
        text-align: center;
        font-size: 18px;
        margin-bottom: 50px; /* Adjust gap before feature list */
    }
    .feature-list {
        font-size: 22px; /* Increased feature list font size */
        font-weight: bold;
        line-height: 2; /* Adds spacing between feature items */
    }
    .centered-footer {
        text-align: center;
        font-size: 16px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "National Reports", "Schooling Data", "Additional Resources"])

# Connect to SQLite database
conn = sqlite3.connect("education_data.db")

# Home Page with Updated UI
if page == "Home":
    # Display the Victoria University logo (Ensure it's in the same folder)
    if os.path.exists(vic_logo_path):
        st.image(vic_logo_path, width=200)
    else:
        st.warning("⚠️ Logo not found. Please check the file name and path.")

    # Centered Title
    st.markdown("<h1 class='big-title'>Kidssmart+</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Educational Dashboard</h2>", unsafe_allow_html=True)

    # Welcome Section
    st.markdown("""
        <div class="welcome-text">
            Kidssmart+ is a cutting-edge educational data management system designed to automate the collection, processing, and management of program data.
            Empower your institution with seamless data integration and smart insights.
        </div>
    """, unsafe_allow_html=True)

    # Features List
    st.markdown("""
        <div class="feature-list">
        📊 Access comprehensive educational datasets <br>
        🔍 Filter data by year or file type <br>
        📂 Download detailed reports
        </div>
    """, unsafe_allow_html=True)

    # Centered Footer with CC Logo
    st.markdown("---")
    st.markdown("""
        <div class="centered-footer">
            <strong>IT CAPSTONE PROJECT</strong> <br>
            Made by <strong>Mohamed Imaad Muhinudeen (s8078260)</strong> & <strong>Kavin Nanthakumar (s8049341)</strong> <br>
        </div>
    """, unsafe_allow_html=True)

    # Display Creative Commons Logo if exists
    if os.path.exists(cc_logo_path):
        st.image(cc_logo_path, width=100)

    # All Rights Reserved Notice
    st.markdown("<div class='centered-footer'>© 2024 Kidssmart+. All Rights Reserved.</div>", unsafe_allow_html=True)

elif page == "National Reports":
    st.header("📂 National Reports")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type='PDF'"
    df = pd.read_sql(query, conn)

    # Decrypt all columns before displaying
    df["title"] = df["title"].apply(decrypt_data)
    df["file_type"] = df["file_type"].apply(decrypt_data)
    df["year"] = df["year"].apply(decrypt_data)
    df["url"] = df["url"].apply(decrypt_data)

    st.dataframe(df)

elif page == "Schooling Data":
    st.header("📂 Schooling Data")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type='Excel'"
    df = pd.read_sql(query, conn)

    # Decrypt all columns before displaying
    df["title"] = df["title"].apply(decrypt_data)
    df["file_type"] = df["file_type"].apply(decrypt_data)
    df["year"] = df["year"].apply(decrypt_data)
    df["url"] = df["url"].apply(decrypt_data)

    st.dataframe(df)

elif page == "Additional Resources":
    st.header("📂 Additional Resources")
    query = "SELECT title, file_type, year, url FROM datasets WHERE file_type IS NOT NULL"
    df = pd.read_sql(query, conn)

    # Decrypt all columns before displaying
    df["title"] = df["title"].apply(decrypt_data)
    df["file_type"] = df["file_type"].apply(decrypt_data)
    df["year"] = df["year"].apply(decrypt_data)
    df["url"] = df["url"].apply(decrypt_data)

    st.dataframe(df)

# Close database connection
conn.close()
