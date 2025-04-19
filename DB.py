import sqlite3

conn = sqlite3.connect('IoTDashboard.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rfid_tag TEXT UNIQUE NOT NULL,
    temp_threshold INTEGER,
    light_threshold INTEGER
)
''')

conn.commit()
conn.close()

