import sqlite3
from pkg_resources import resource_filename

def init_db():
    db_path = resource_filename('tuits.data', 'tuits.db')
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

