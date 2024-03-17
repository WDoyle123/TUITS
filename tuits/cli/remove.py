import os
import sqlite3

def remove_tasks():
    input_ids = input("Give IDs of logs you would like to remove. e.g. 12,13,14: ")

    ids = [id.strip() for id in input_ids.split(',') if id.strip()]
    valid_ids = []
    for id in ids:
        try:
            num_id = int(id)
            if num_id > 0:
                valid_ids.append(num_id)
        except ValueError:
            print(f"Warning: '{id}' is not a valid ID and will be ignored.")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(base_dir, 'data', 'tuits.db')
    
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        for id in valid_ids:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
            if cursor.rowcount == 0:
                print(f"Warning: ID '{id}' is not present in database, ignoring.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
