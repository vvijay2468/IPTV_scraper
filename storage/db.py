import sqlite3
from pathlib import Path

DB_PATH = Path("iptv.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS validations (
        url TEXT,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        success INTEGER,
        reason TEXT
    )
    """)
    return conn
