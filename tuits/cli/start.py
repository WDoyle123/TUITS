import sqlite3
from datetime import datetime

from tuits.data.db import get_db_path

def start_day(args=None):
    # locate database
    database_path = get_db_path()

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    start_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM tasks WHERE job='Start' AND date(timestamp)=?", (start_date,))
    if cursor.fetchone():
        print("Start for today has already been logged")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES ('Start', '##########', ?)", (timestamp,))

    conn.commit()
    conn.close()

    date_part, time_part = timestamp.split(' ')

    print(f"Workday started at {time_part}.")
