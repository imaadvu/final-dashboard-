import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("education_data.db")
cursor = conn.cursor()

# Retrieve and print stored data
cursor.execute("SELECT title, file_type, year, url FROM datasets LIMIT 10;")  # Fetch first 10 rows
rows = cursor.fetchall()

print("\n📊 Extracted Data from Database:")
print("------------------------------------------------------")
print("{:<50} {:<10} {:<6} {:<60}".format("Title", "Type", "Year", "URL"))
print("------------------------------------------------------")

for row in rows:
    print("{:<50} {:<10} {:<6} {:<60}".format(row[0], row[1], row[2], row[3]))

# Close connection
conn.close()
