import sqlite3
import os
from datetime import datetime

def start_day(args=None):
    # locate database
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(base_dir,'data', 'tuits.db')

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    start_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM tasks WHERE job='Start' AND date(timestamp)=?", (start_date,))
    if cursor.fetchone():
        print("Start for today has already been logged")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES ('Start', '##########', ?)", (timestamp,))

    conn.commit()
    conn.close()

    date_part, time_part = timestamp.split(' ')

    print(f"Workday started at {time_part}.")
