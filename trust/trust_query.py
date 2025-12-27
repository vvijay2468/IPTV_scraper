import sqlite3
from storage.db import get_conn

def fetch_validation_rows():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, success, checked_at
        FROM validations
        WHERE stream_type != 'STATIC_ASSET'
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

