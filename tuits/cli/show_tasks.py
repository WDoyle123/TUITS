import sqlite3
import os
from datetime import datetime, timedelta
from tabulate import tabulate

def get_tasks_text_for_time_frame(time_frame):
    start_date = get_start_date(time_frame)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(base_dir, 'data', 'tuits.db')

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    start_date_str = start_date.strftime("%Y-%m-%d %H:%M")

    query = "SELECT job, message FROM tasks WHERE date(timestamp) >= date(?) ORDER BY timestamp DESC"
    cursor.execute(query, (start_date_str,))

    rows = cursor.fetchall()

    tasks_text = '\n'.join([f"{row[0]}: {row[1]}" for row in rows])

    conn.close()

    return tasks_text

def get_start_date(date_range):
    now = datetime.now()

    # Example date_range = day. We only show logs from 00:00 until the time now
    if date_range == 'day':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Example date_range = week. We only show logs from Monday until the time now
    elif date_range == 'week':
        start_of_week = now - timedelta(days=now.weekday())
        start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Example date_range = month. We only show logs from beginning of the month until now
    elif date_range == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Example date_range = year. We only show the logs from the beginning of the year until now
    elif date_range == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    else:
        raise ValueError(f"Unsupported date range: '{date_range}', Choose from: day, week, month, year")

    return start_date

def format_output(row, date_range, include_id=False, max_message_length=0):

    # Extract information from the row.
    id, job, message, timestamp_str = row

    # Parse the timestamp string from the database format to a datetime object
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    # Check if job is one of the specified types and adjust message if necessary
    if job in ["Start", "Finish"] and (message == "" or message.startswith("###")):
        # Replace message with a string of '#' characters matching the length of the longest message
        message = "#" * max_message_length

    if job in ["Break"] and (message == "" or message.startswith("###")):
        # Replace message with a string of '-' characters matching the length of the longest message
        message = "/" * max_message_length

    # Initialise the output list, conditionally including the ID
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

def get_terminal_size(include_id=False):
    try:
        size = os.get_terminal_size()
        space = 50 if include_id else 65  
        usable_width = max(size.columns - space, 20) 
        return usable_width
    except OSError:
        return 80  

def show_tasks(args):
    # Get the args from the command
    date_range = args.show

    # locate database
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(base_dir, 'data', 'tuits.db')

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        start_date = get_start_date(date_range)
    except ValueError as e:
        print(e)
        return

    query = "SELECT * FROM tasks WHERE date(timestamp) >= date(?) ORDER BY timestamp DESC"
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M")
    cursor.execute(query, (start_date_str,))

    rows = cursor.fetchall()

    max_message_length = get_terminal_size(args.identifier)

    formatted_rows = [format_output(row, date_range, args.identifier, max_message_length) for row in rows]

    # Determine headers based on the date range and identifier
    headers = ["Job", "Message", "Time", "Day"] if date_range == 'week' else ["Job", "Message", "Time", "Date"]
    if args.identifier:
        headers.insert(0, "ID")

    print(tabulate(formatted_rows, headers=headers, tablefmt="grid", maxcolwidths=[None, get_terminal_size(args.identifier)]))

    conn.close()
