import os
import shutil

from tuits.data.db import get_db_path

def backup_tasks(args):
    job_name = args.job

    if job_name not in ["save", "load"]:
        print("Invalid job name.")
        return

    while True:
        dir_path = input("Enter the directory path to save/load the database: ").strip()
        dir_path = os.path.expanduser(dir_path)

        database_filename = 'tuits.db'
        path = os.path.join(dir_path, database_filename)

        if job_name == "save":
            if not os.path.isdir(dir_path):
                print("Invalid directory path. Example: ~/Documents")
                continue

            try:
                source_database_path = get_db_path()
                backup_database_path = path
                shutil.copyfile(source_database_path, backup_database_path)
                print(f"Database saved successfully to: {backup_database_path}")
                break  # Exit loop after successful operation
            except Exception as e:
                print(f"Failed to save the database: {e}")

        elif job_name == "load":
            if not os.path.isfile(path):
                print(f"Database not found in the given directory. Expected file: {path}")
                continue

            try:
                target_database_path = get_db_path()
                shutil.copyfile(path, target_database_path)
                print(f"Database loaded successfully from: {path}")
                break  # Exit loop after successful operation
            except Exception as e:
                print(f"Failed to load the database: {e}")
