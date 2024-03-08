import sqlite3 

def init_db():
    conn = sqlite3.connect('tuits.db')
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
