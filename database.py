import sqlite3

# Create database
def create_database():
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            title TEXT,
            link TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save search results
def save_result(query, title, link, content):
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (query, title, link, content) VALUES (?, ?, ?, ?)", 
                   (query, title, link, content))
    conn.commit()
    conn.close()

# Get stored results
def get_results():
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize database
if __name__ == "__main__":
    create_database()
    print("Database setup completed.")
