import sqlite3
from datetime import datetime

def log_task(args):
    # Get the args from the command
    job_name = args.job
    message = args.message

    # locate database
    database_path = '../data/tuits.db'

    # set the time the command was issued
    timestamp = datetime.now().strftime("%H:%M %d/%m/%y")

    # connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # add row to the database
    cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)", (job_name, message, timestamp))
    
    # save and close db
    conn.commit()
    conn.close()

    time_part, data_part = timestamp.split(' ')

    # print for debugging 
    print(f"{job_name} - {message} - {time_part}")
