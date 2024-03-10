import sqlite3
import os

def dump_db():
    database = 'tuits.db'  # Path to your SQLite database file

    # Check if the dump file already exists and remove it
    if os.path.exists(database):
        os.remove(database)
        print(f"'{database}' has been removed.")

dump_db()

