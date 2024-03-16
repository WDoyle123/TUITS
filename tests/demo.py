import sqlite3
import os
from datetime import datetime, timedelta

def create_demo_database():
    # Create or locate the demo database
    base_dir = os.getcwd()  # For simplicity, use the current working directory
    database_path = os.path.join(base_dir, 'tuits.db')

    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Ensure the tasks table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        job TEXT NOT NULL,
        message TEXT,
        timestamp TEXT NOT NULL
    );
    """)

    # Populate the database with a week's worth of work logs
    for i in range(7):  # Last 7 days, including today
        day = datetime.now() - timedelta(days=i)
        start_timestamp = day.replace(hour=9, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        finish_timestamp = day.replace(hour=17, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

        # Start of day
        cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)",
                       ('Start', 'Workday start', start_timestamp))

        # Sample tasks
        for j in range(3):  # 3 sample tasks per day
            task_timestamp = day.replace(hour=10+j, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)",
                           (f'Task {j+1}', f'Sample task {j+1} description', task_timestamp))

        # End of day
        cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)",
                       ('Finish', 'Workday finish', finish_timestamp))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Demo database created with a week's worth of logs at {database_path}")

if __name__ == "__main__":
    create_demo_database()

