import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tuits/cli")))
from log_task import log_task

import unittest
from unittest.mock import patch, MagicMock

class TestLogTask(unittest.TestCase):
    @patch('log_task.sqlite3')
    def test_log_task(self, mock_sqlite):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Prepare arguments for the log_task function
        args = MagicMock()
        args.job = "Example Job"
        args.message = "This is a test message"

        # Call the log_task function with the mocked arguments
        log_task(args)
        
        # Assert the SQLite connection was called with the expected database path
        mock_sqlite.connect.assert_called_with('../data/tuits.db')
        
        # Assert the cursor executed an INSERT command with the expected values
        mock_cursor.execute.assert_called()
        sql_call_args = mock_cursor.execute.call_args[0]
        self.assertIn("INSERT INTO tasks (job, message, timestamp) VALUES (?, ?, ?)", sql_call_args[0])
        self.assertEqual(sql_call_args[1][0], args.job)
        self.assertEqual(sql_call_args[1][1], args.message)
        
        # We don't assert the exact timestamp as it's generated during the function call
        # but we can check the SQL structure and the presence of three parameters
        self.assertEqual(len(sql_call_args[1]), 3)

        # Assert the commit was called on the connection
        mock_conn.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

