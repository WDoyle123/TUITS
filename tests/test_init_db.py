import os
import sys
import sqlite3
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tuits/data")))
from init_db import init_db

class TestDBInit(unittest.TestCase):
    db_path = 'tuits.db'

    def setUp(self):
        # Ensure the database is deleted before each test (if it exists)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_db_and_table_creation(self):
        # Initialise the database
        init_db()

        # Connect to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if the 'tasks' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
        table_exists = cursor.fetchone()
        
        self.assertIsNotNone(table_exists, "The 'tasks' table should exist after initializing the database.")

        # Verify the schema of the 'tasks' table
        cursor.execute("PRAGMA table_info(tasks);")
        columns = cursor.fetchall()

        expected_columns = [
            (0, 'id', 'INTEGER', 0, None, 1),
            (1, 'job', 'TEXT', 1, None, 0),
            (2, 'message', 'TEXT', 0, None, 0),
            (3, 'timestamp', 'DATETIME', 1, None, 0),
        ]
        
        self.assertEqual(columns, expected_columns, "The schema of the 'tasks' table does not match the expected schema.")

        # Close the connection
        conn.close()

    def tearDown(self):
        # Clean up by deleting the database file after each test
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

if __name__ == '__main__':
    unittest.main()

