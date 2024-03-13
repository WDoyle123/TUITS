import sqlite3
import os
from datetime import datetime, timedelta
from tabulate import tabulate

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

def format_output(row, date_range, include_id=False):
    # Extract information from the row.
    id, job, message, timestamp_str = row

    # Parse the timestamp string from the database format to a datetime object
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    # Initialize the output list, conditionally including the ID
    output = [id] if include_id else []

    # Add job and message based on the date_range
    output.append(job)

    # Format and append the timestamp based on the date_range
    if date_range == 'day':
        output.append(message)
        output.append(timestamp.strftime('%H:%M'))
    elif date_range == 'week':
        day_name = timestamp.strftime('%A')
        output.extend([message, timestamp.strftime('%H:%M'), day_name])
    elif date_range == 'month' or date_range == 'year':
        output.extend([message, timestamp.strftime('%H:%M - %d/%m/%y')])

    return output

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
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M")  # Adjust format to YYYY-MM-DD for better compatibility
    cursor.execute(query, (start_date_str,))

    rows = cursor.fetchall()
    formatted_rows = [format_output(row, date_range, args.identifier) for row in rows]

    # Determine headers based on the date range and identifier
    headers = ["Job", "Message", "Time", "Day"] if date_range == 'week' else ["Job", "Message", "Time", "Date"]
    if args.identifier:
        headers.insert(0, "ID")  

    print(tabulate(formatted_rows, headers=headers, tablefmt="grid"))

    conn.close()
