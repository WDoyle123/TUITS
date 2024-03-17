import os
import sqlite3
import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tuits/cli")))
from remove import remove_tasks

class TestRemoveTasks(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_remove_tasks(self, mock_connect):
        # Setup a mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = []

        # Mocking the input to simulate user inputting '1,2,3'
        with patch('builtins.input', return_value='1,2,3'):
            remove_tasks()

        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()

        self.assertTrue(mock_cursor.execute.called)

        expected_calls = [
            unittest.mock.call("DELETE FROM tasks WHERE id = ?", (1,)),
            unittest.mock.call("DELETE FROM tasks WHERE id = ?", (2,)),
            unittest.mock.call("DELETE FROM tasks WHERE id = ?", (3,))
        ]
        mock_cursor.execute.assert_has_calls(expected_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()
