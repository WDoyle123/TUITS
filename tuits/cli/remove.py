import sqlite3

from tuits.cli.utils import fetch_recent_tasks, print_task_table
from tuits.data.db import get_db_path

def parse_ids_from_tokens(tokens, rows):
    valid_ids = {row[0] for row in rows}
    index_map = {idx: row[0] for idx, row in enumerate(rows, start=1)}

    selected_ids = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token.startswith("#"):
            token = token[1:]

        try:
            num_id = int(token)
        except ValueError:
            print(f"Warning: '{token}' is not a valid number and will be ignored.")
            continue

        if num_id in index_map:
            selected_ids.append(index_map[num_id])
        elif num_id in valid_ids:
            selected_ids.append(num_id)
        else:
            print(f"Warning: '{token}' is not a valid index or ID and will be ignored.")

    return selected_ids


def remove_tasks(args):
    rows = fetch_recent_tasks(args.limit)
    if not rows:
        print("No logs found.")
        return

    if args.ids:
        tokens = [part.strip() for part in args.ids.split(",")]
        valid_ids = {row[0] for row in rows}
        selected_ids = []
        for token in tokens:
            if not token:
                continue
            if token.startswith("#"):
                token = token[1:]
            try:
                num_id = int(token)
            except ValueError:
                print(f"Warning: '{token}' is not a valid ID and will be ignored.")
                continue
            if num_id in valid_ids:
                selected_ids.append(num_id)
            else:
                print(f"Warning: ID '{num_id}' not found in recent list, ignoring.")
    else:
        print_task_table(rows, show_index=True)
        selection = input("Select entries by # or ID (e.g. 1,3 or #12). Enter to cancel: ").strip()
        if not selection:
            print("Cancelled.")
            return
        tokens = selection.split(",")
        selected_ids = parse_ids_from_tokens(tokens, rows)

    if not selected_ids:
        print("No valid entries selected.")
        return

    if not args.yes:
        confirm = input(f"Remove {len(selected_ids)} entr{'y' if len(selected_ids) == 1 else 'ies'}? (y/N): ")
        if confirm.strip().lower() not in ["y", "yes"]:
            print("Cancelled.")
            return

    database_path = get_db_path()

    conn = None
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        for task_id in selected_ids:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount == 0:
                print(f"Warning: ID '{task_id}' is not present in database, ignoring.")
        
        conn.commit()
        print(f"Removed {len(selected_ids)} entr{'y' if len(selected_ids) == 1 else 'ies'}.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
