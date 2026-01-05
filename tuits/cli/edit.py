import sqlite3

from tuits.cli.utils import (
    fetch_recent_tasks,
    fetch_task_by_id,
    parse_time_input,
    print_task_table,
    prompt_with_default,
)
from tuits.data.db import get_db_path


def select_task_id(rows):
    print_task_table(rows, show_index=True)
    selection = input("Select an entry by # or ID. Enter to cancel: ").strip()
    if not selection:
        return None

    if selection.startswith("#"):
        selection = selection[1:]

    try:
        num_id = int(selection)
    except ValueError:
        print("Invalid selection.")
        return None

    index_map = {idx: row[0] for idx, row in enumerate(rows, start=1)}
    valid_ids = {row[0] for row in rows}

    if num_id in index_map:
        return index_map[num_id]
    if num_id in valid_ids:
        return num_id

    print("Invalid selection.")
    return None


def edit_task(args):
    if args.id is not None:
        task = fetch_task_by_id(args.id)
        if not task:
            print(f"ID '{args.id}' not found.")
            return
    else:
        rows = fetch_recent_tasks(args.limit)
        if not rows:
            print("No logs found.")
            return
        task_id = select_task_id(rows)
        if task_id is None:
            print("Cancelled.")
            return
        task = fetch_task_by_id(task_id)
        if not task:
            print("Selected entry not found.")
            return

    task_id, current_job, current_message, current_timestamp = task

    new_job = prompt_with_default("Job", current_job, allow_empty=False)
    new_message = prompt_with_default("Message", current_message)
    new_time_input = prompt_with_default(
        "Time (HH:MM or YYYY-MM-DD HH:MM)", current_timestamp
    )

    parsed_time = parse_time_input(new_time_input)
    if not parsed_time:
        print("Invalid time format. Use HH:MM or YYYY-MM-DD HH:MM.")
        return

    new_timestamp = parsed_time.strftime("%Y-%m-%d %H:%M:%S")

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET job = ?, message = ?, timestamp = ? WHERE id = ?",
        (new_job, new_message, new_timestamp, task_id),
    )
    conn.commit()
    conn.close()

    print(f"Updated entry ID {task_id}.")
