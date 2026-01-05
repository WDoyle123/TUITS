import sqlite3

from tuits.data.db import get_db_path

def init_db(db_path=None):
    db_path = db_path or get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS tasks (
                       id INTEGER PRIMARY KEY,
                       job TEXT NOT NULL,
                       message TEXT,
                       timestamp DATETIME NOT NULL
                       )
                   ''')
    conn.commit()
    conn.close()
