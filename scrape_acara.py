import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import mysql.connector
import re  # For extracting year
import logging
from cryptography.fernet import Fernet  # For encryption

# Configure logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Use a pre-generated encryption key (store this securely!)
key = b'ejlFEAhslsWI2J0zer_OFwXexzf3woq4Qzgg0_vX5Wk='  # Replace with your actual key
cipher_suite = Fernet(key)


# Function to encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# Function to decrypt data (if needed)
def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

# Step 1: Define the website URL
url = "https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia"

try:
    # Step 2: Fetch the website content
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if request fails
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 3: Extract dataset links with more details
    dataset_links = []
    for link in soup.find_all("a", href=True):
        if "pdf" in link["href"] or "xls" in link["href"]:  # Look for PDF/Excel files
            title = link.text.strip()
            file_url = link["href"]

            # Extract file type (PDF or Excel)
            file_type = "PDF" if "pdf" in file_url else "Excel"

            # Extract publication year from filename (if available)
            match = re.search(r"(\d{4})", file_url)
            year = match.group(1) if match else "Unknown"

            # Extract the description (if available in the next paragraph or sibling element)
            description_tag = link.find_next("p")
            description = description_tag.text.strip() if description_tag else "No description available"

            # Encrypt sensitive fields before storing
            dataset_links.append((
                encrypt_data(title), 
                encrypt_data(file_url), 
                encrypt_data(file_type), 
                encrypt_data(year), 
                encrypt_data(description)
            ))

    # Step 4: Convert to DataFrame
    df = pd.DataFrame(dataset_links, columns=["title", "url", "file_type", "year", "description"])

    # Step 5: Connect to SQLite Database
    conn = sqlite3.connect("education_data.db")
    cursor = conn.cursor()

    # Step 6: Create table with "description" column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            file_type TEXT,
            year TEXT,
            description TEXT
        )
    ''')

    # Step 7: Insert Data into SQLite
    df.to_sql("datasets", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    logging.info("✅ Data successfully stored in 'education_data.db' with descriptions!")

    # Step 8: Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="imaad",  # Change if using a different MySQL user
        password="Imaad123.",  # Change if your password is different
        database="education_data"
    )
    cursor = conn.cursor()

    # Step 9: Ensure the MySQL table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            url TEXT,
            file_type VARCHAR(10),
            year VARCHAR(10),
            description TEXT
        )
    ''')

    # Step 10: Insert data into MySQL
    cursor.execute("DELETE FROM datasets")  # Clear old data
    sql = "INSERT INTO datasets (title, url, file_type, year, description) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, dataset_links)  # Now MySQL gets 5 columns

    conn.commit()
    cursor.close()
    conn.close()

    logging.info("✅ Data successfully stored in MySQL database!")

except Exception as e:
    logging.error(f"❌ Error during scraping: {e}")
    print(f"Error: {e}")
