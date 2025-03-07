import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import mysql.connector
import re  # For extracting year

# Step 1: Define the website URL
url = "https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia"

# Step 2: Fetch the website content
response = requests.get(url)
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

        # Append data to list
        dataset_links.append((title, file_url, file_type, year, description))

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

# Step 8: Close SQLite connection
conn.commit()
conn.close()

print("\n✅ Data successfully stored in 'education_data.db' with descriptions!")

# Step 9: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="imaad",  # Change if using a different MySQL user
    password="Imaad123.",  # Change if your password is different
    database="education_data"
)
cursor = conn.cursor()

# Step 10: Ensure the MySQL table exists
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

# Step 11: Insert data into MySQL
cursor.execute("DELETE FROM datasets")  # Clear old data
sql = "INSERT INTO datasets (title, url, file_type, year, description) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(sql, dataset_links)  # Now MySQL gets 5 columns

conn.commit()
cursor.close()
conn.close()

print("\n✅ Data successfully stored in MySQL database!")
