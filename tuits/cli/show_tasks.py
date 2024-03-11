import sqlite3
import os
from datetime import datetime, timedelta

def get_start_date(date_range):
    now = datetime.now()

    # Example date_range = day. We only show logs from 00:00 until the time now
    if date_range == 'day':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Example date_range = week. We only show logs from Monday until the time now
    elif date_range == 'week':
        start_date = now - timedelta(days=now.weekday())
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Example date_range = month. We only show logs from beginning of the month until now
    elif date_range == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Example date_range = year. We only show the logs from the beginning of the year until now
    elif date_range == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    else:
        raise ValueError(f"Unsupported date range: '{date_range}', Choose from: day, week, month, year")

    return start_date

def format_output(row, date_range):
    # Extract information from the row
    job, message, timestamp_str = row[1], row[2], row[3]

    # Parse the timestamp string from the database format to a datetime object
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")

    # Format the output based on the date_range
    if date_range == 'day':
        return f"{job} - {message} - {timestamp.strftime('%H:%M')}"
    elif date_range == 'week':
        # Get the day name (e.g., Monday)
        day_name = timestamp.strftime('%A')
        return f"{job} - {message} - {timestamp.strftime('%H:%M')} - {day_name}"
    elif date_range == 'month':
        # Return the date in the format: hour:minute - day/month/year
        return f"{job} - {message} - {timestamp.strftime('%H:%M - %d/%m/%y')}"
    else:
        # Default format if not 'day', 'week', or 'month' (handles 'year' or any unexpected range)
        return f"{job} - {message} - {timestamp.strftime('%H:%M - %d/%m/%y')}"

def show_tasks(args):
    # Get the args from the command
    date_range = args.show

    # locate database
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(base_dir,'data', 'tuits.db')

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        start_date = get_start_date(date_range)
    except ValueError as e:
        print(e)
        return

    if start_date is None:
        print(f"Error: start_date is None for date_range '{date_range}")
        return
    
    query = "SELECT * FROM tasks WHERE date(timestamp) >= date(?) ORDER BY timestamp DESC"
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M") # Adjust format to YYYY-MM-DD for better compatibility
    cursor.execute(query, (start_date_str,))

    rows = cursor.fetchall()
    for row in rows:
        formatted_row = format_output(row, date_range)
        print(formatted_row)

    conn.close()
