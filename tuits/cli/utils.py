import sqlite3
from datetime import datetime, timedelta
from tabulate import tabulate

from tuits.data.db import get_db_path


def fetch_recent_tasks(limit=10):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, job, message, timestamp FROM tasks ORDER BY timestamp DESC, id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_task_by_id(task_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, job, message, timestamp FROM tasks WHERE id = ?",
        (task_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_last_task():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, job, message, timestamp FROM tasks ORDER BY timestamp DESC, id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    return row


def prompt_with_default(prompt, default=None, allow_empty=True):
    if default not in [None, ""]:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    value = input(prompt_text).strip()
    if value == "." and default not in [None, ""]:
        return default
    if value == "" and default is not None:
        return default
    if value == "" and not allow_empty:
        return None
    return value


def parse_time_input(value, now=None):
    if not value:
        return None

    now = now or datetime.now()
    value = value.strip()

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            parsed = datetime.strptime(value, fmt)
            if fmt == "%Y-%m-%d %H:%M":
                parsed = parsed.replace(second=0)
            return parsed
        except ValueError:
            continue

    try:
        parsed = datetime.strptime(value, "%H:%M")
        return now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
    except ValueError:
        return None


def offset_time(minutes, now=None):
    now = now or datetime.now()
    return now + timedelta(minutes=minutes)


def print_task_table(rows, show_index=True):
    table_rows = []
    for idx, row in enumerate(rows, start=1):
        task_id, job, message, timestamp = row
        entry = [idx, task_id, job, message, timestamp] if show_index else [task_id, job, message, timestamp]
        table_rows.append(entry)

    headers = ["#", "ID", "Job", "Message", "Time"] if show_index else ["ID", "Job", "Message", "Time"]
    print(tabulate(table_rows, headers=headers, tablefmt="grid"))
