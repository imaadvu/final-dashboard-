import requests
from bs4 import BeautifulSoup
import sqlite3

# Step 1: Define the URL
url = "https://f10.vcaa.vic.edu.au/learning-areas/mathematics/curriculum"

# Step 2: Define headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Step 3: Fetch the page content
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Step 4: Extract data
buttons = soup.find_all("button", class_="flex flex-1 items-center justify-between py-4")
dataset = []
for button in buttons:
    title = button.get_text(strip=True)
    description = button.find_next("div").get_text(strip=True) if button.find_next("div") else "No description"
    dataset.append((title, description))

# Step 5: Connect to SQLite database
conn = sqlite3.connect("education_data.db")
cursor = conn.cursor()

# Step 6: Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS victorian_curriculum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    )
''')
conn.commit()

# Step 7: Insert data into table
for title, description in dataset:
    cursor.execute("INSERT INTO victorian_curriculum (title, description) VALUES (?, ?)", (title, description))
conn.commit()
conn.close()
