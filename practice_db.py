import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("practice.db")
    cur = conn.cursor()
    cur.execute("""
    	CREATE TABLE IF NOT EXISTS users (
    		id INTEGER PRIMARY KEY AUTOINCREMENT,
    		user_id INTEGER UNIQUE,
    		username TEXT,
    		first_name TEXT,
    		reg_date TEXT
    	)
    """)
    conn.commit()
    conn.close()

def add_user(user_id, first_name):
    conn = sqlite3.connect("practice.db")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (user_id, username, first_name, reg_date) "
            "VALUES (?, ?, ?, ?)",
            (user_id, "Нет", first_name, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
