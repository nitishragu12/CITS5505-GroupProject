import sqlite3

# Create or open a database called app.db
conn = sqlite3.connect('./app.db')
c = conn.cursor()

# Create a table named users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    birthday DATE,
    gender TEXT,
    phone TEXT
)
''')

conn.commit()
conn.close()

if __name__ == "__main__":
    setup_database()

