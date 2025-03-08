import sqlite3

# Connect to the database
conn = sqlite3.connect("education_data.db")
cursor = conn.cursor()

# Prepare the INSERT statement
insert_query = "INSERT INTO datasets (title, file_type, year, url) VALUES (?, ?, ?, ?)"

# Define the data to insert (example datasets)
data = [
    ('Schools, Australia, 2024', 'PDF', 2024, 'https://www.abs.gov.au/statistics/people/education/schools/2024.pdf'),
    ('Higher Education Student Data, 2023', 'Excel', 2023, 'https://www.education.gov.au/higherEducationStatistics/student-data/2023.xlsx'),
    ('National Schools Statistics Collection, 2022', 'Excel', 2022, 'https://data.gov.au/data/dataset/national-schools-statistics-collection-2022'),
    ('Education and Work, Australia, May 2024', 'PDF', 2024, 'https://www.abs.gov.au/statistics/people/education/education-and-work-australia/2024.pdf'),
    ('Australian Schools List', 'CSV', 2025, 'https://www.acara.edu.au/docs/default-source/schooling/australian-schools-list.csv')
]

# Execute the INSERT statement for each dataset
for row in data:
    cursor.execute(insert_query, row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data added successfully!")