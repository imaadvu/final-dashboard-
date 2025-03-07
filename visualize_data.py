import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("education_data.db")

# Retrieve dataset counts per year
query = "SELECT year, COUNT(*) as count FROM datasets GROUP BY year ORDER BY year;"
df = pd.read_sql(query, conn)

# Close connection
conn.close()

# Plot the data
plt.figure(figsize=(10, 5))
plt.bar(df["year"], df["count"], color="skyblue")

plt.xlabel("Year")
plt.ylabel("Number of Datasets")
plt.title("Number of Educational Datasets per Year")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the chart
plt.show()
