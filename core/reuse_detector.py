import sqlite3
import hashlib
from difflib import SequenceMatcher

DB_PATH = "storage/history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            hash TEXT
        )
    """)
    conn.commit()
    conn.close()

def check_reuse(password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT hash FROM passwords")
    stored = cur.fetchall()
    conn.close()

    for (old_hash,) in stored:
        similarity = SequenceMatcher(None, hashed, old_hash).ratio()
        if similarity > 0.8:
            return True

    return False

def store_password(password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO passwords VALUES (?)", (hashed,))
    conn.commit()
    conn.close()
