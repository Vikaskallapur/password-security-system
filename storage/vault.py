import sqlite3
from cryptography.fernet import Fernet
import os

DB_PATH = "storage/vault.db"
KEY_PATH = "storage/master.key"

def generate_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)

def load_key():
    return open(KEY_PATH, "rb").read()

def init_vault():
    generate_key()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            password BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def store_password(service, password):
    cipher = Fernet(load_key())
    encrypted = cipher.encrypt(password.encode())

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO vault (service, password) VALUES (?, ?)",
        (service, encrypted)
    )
    conn.commit()
    conn.close()

def retrieve_password(service):
    cipher = Fernet(load_key())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM vault WHERE service=?",
        (service,)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        return cipher.decrypt(row[0]).decode()
    return None
