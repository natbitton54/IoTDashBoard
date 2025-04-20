import sqlite3
import os

#db path
DB = os.path.join(os.path.dirname(__file__), "users.db")

# connect to sqlite (if file not exist, create one)
connect = sqlite3.connect(DB)
cursor = connect.cursor()

# create users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
rfid_tag TEXT NOT NULL UNIQUE,
temp_threshold INTEGER NOT NULL,
light_threshold INTEGER NOT NULL
);
""")


connect.commit()
connect.close()

print("DB INIT: ", DB)