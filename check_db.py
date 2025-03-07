import sqlite3

# Connect to the database
conn = sqlite3.connect("education_data.db")
cursor = conn.cursor()

# Check for existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\n📌 Tables in the database:")
for table in tables:
    print(table[0])  # Print table names

# Close connection
conn.close()
