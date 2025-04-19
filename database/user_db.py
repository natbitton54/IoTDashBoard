import sqlite3
import os

#db path
DB = os.path.join(os.path.dirname(__file__), "users.db")

# add user
def add_user(name, rfid_tag, temp_threshold, light_threshold):
    try:
        connect = sqlite3.connect(DB)
        cursor = connect.cursor()
        cursor.execute("""
                       INSERT INTO users(name, rfid_tag, temp_threshold, light_threshold) VALUES (?, ?, ?, ?)
                       """, (name, rfid_tag, temp_threshold, light_threshold))
        connect.commit()
        print(f"User '{name}' added to the db!")
    except sqlite3.IntegrityError:
        print(f"A user with RFID '{rfid_tag}' already exists in the db!")
    finally:
        connect.close()

# fetch user RFID tag
def get_user_by_rfid(rfid_tag):
    connect = sqlite3.connect(DB)
    cursor = connect.cursor()
    cursor.execute("SELECT name, temp_threshold, light_threshold FROM users WHERE rfid_tag = ?", (rfid_tag,))
    result = cursor.fetchone()
    connect.close()
    if result:
        return {
            "name": result[0],
            "temp_threshold": result[1],
            "light_threshold": result[2]
        }
    return None