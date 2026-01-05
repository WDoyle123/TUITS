import sqlite3
from datetime import datetime

from tuits.cli.utils import fetch_last_task, offset_time, parse_time_input, prompt_with_default
from tuits.data.db import get_db_path

def log_task(args):
    # Get the args from the command
    job_name = args.job
    if not job_name:
        last_task = fetch_last_task()
        last_job = last_task[1] if last_task else None
        job_name = prompt_with_default("Job name (use '.' to repeat last)", last_job, allow_empty=False)
        if not job_name:
            print("Job name is required.")
            return

    message = args.message
    if message is None:
        last_task = fetch_last_task()
        last_message = last_task[2] if last_task else ""
        message = prompt_with_default("Message (optional, '.' repeats last)", last_message)

    # locate database
    database_path = get_db_path()

    # set the time the command was issued
    if args.at and args.mins is not None:
        print("Use either --at or --mins, not both.")
        return

    timestamp_dt = None
    if args.at:
        timestamp_dt = parse_time_input(args.at)
        if not timestamp_dt:
            print("Invalid time format. Use HH:MM or YYYY-MM-DD HH:MM.")
            return

    if args.mins is not None:
        timestamp_dt = offset_time(args.mins)

    if not timestamp_dt:
        timestamp_dt = datetime.now()

    timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

    # connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # add row to the database
    cursor.execute("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)", (job_name, message, timestamp))
    
    # save and close db
    conn.commit()
    conn.close()

    date_part, time_part = timestamp.split(' ')

    # print for debugging 
    print(f"{job_name} - {message} - {time_part}")
