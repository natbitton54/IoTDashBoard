import sqlite3
import os
import random


# db path
DB = os.path.join(os.path.dirname(__file__), "users.db")

pfps = [
    "https://m.gettywallpapers.com/wp-content/uploads/2023/11/Sung-Jin-Woo-pfp.jpg",
    "https://i.pinimg.com/736x/60/38/e8/6038e8a871b21521499cdef74e00a734.jpg",
    "https://i.pinimg.com/736x/97/36/80/9736806e978c1eb7a43e7cd68534566d.jpg",
    "https://avatarfiles.alphacoders.com/121/thumb-1920-121995.jpg",
    "https://wallpapers.com/images/featured/tony-tony-chopper-xebwojdkrjyi10sf.jpg",
]


# add user
def add_user(name, rfid_tag, temp_threshold, light_threshold):
    pfp_url = random.choice(pfps)
    try:
        connect = sqlite3.connect(DB)
        cursor = connect.cursor()
        cursor.execute(
            """
                       INSERT INTO users(name, rfid_tag, temp_threshold, light_threshold, pfp_url) VALUES (?, ?, ?, ?, ?)
                       """,
            (name, rfid_tag, temp_threshold, light_threshold, pfp_url),
        )
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
    cursor.execute(
        "SELECT name, temp_threshold, light_threshold, pfp_url FROM users WHERE rfid_tag = ?",
        (rfid_tag,),
    )
    result = cursor.fetchone()
    connect.close()
    if result:
        return {
            "name": result[0],
            "temp_threshold": result[1],
            "light_threshold": result[2],
            "pfp_url": result[3],
        }
    return None
