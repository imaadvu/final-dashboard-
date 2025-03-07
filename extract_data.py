import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Define the website URL
url = "https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia"

# Step 2: Fetch the website content
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Extract educational data
# Example: Finding all links to downloadable datasets
dataset_links = []
for link in soup.find_all("a", href=True):
    if "pdf" in link["href"] or "xls" in link["href"]:  # Look for PDF/Excel files
        dataset_links.append({"title": link.text.strip(), "url": link["href"]})

# Step 4: Convert extracted data into a DataFrame
df = pd.DataFrame(dataset_links)

# Step 5: Save data to a CSV file
df.to_csv("acara_datasets.csv", index=False)

# Step 6: Print extracted data
print(df)
print("\n✅ Data scraping complete! Saved as acara_datasets.csv")
