import sqlite3

from tuits.cli.utils import fetch_last_task, print_task_table
from tuits.data.db import get_db_path


def undo_last(args):
    task = fetch_last_task()
    if not task:
        print("No logs found.")
        return

    if not args.yes:
        print_task_table([task], show_index=False)
        confirm = input("Remove the latest entry? (y/N): ").strip().lower()
        if confirm not in ["y", "yes"]:
            print("Cancelled.")
            return

    task_id = task[0]
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Removed entry ID {task_id}.")
