import sqlite3

conn = sqlite3.connect('week12.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        marks INTEGER
    )
''')

cursor.execute("INSERT INTO students (name, marks) VALUES ('Ali', 85)")
cursor.execute("INSERT INTO students (name, marks) VALUES ('Sara', 90)")
cursor.execute("INSERT INTO students (name, marks) VALUES ('Ahmed', 78)")

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()
