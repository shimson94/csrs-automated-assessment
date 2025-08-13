import unittest
import os
from unittest.mock import patch
from  src import database
from src import automarker
import sqlite3


class TestAutoMarker(unittest.TestCase):

    def setUp(self):
        """Set up before each test."""

        self.db_file = 'src/tests/test_db.sqlite'
        self.auto_marker = automarker.AutoMarker(self.db_file)

        if not os.path.exists(self.db_file):
            self.connection = sqlite3.connect(self.db_file)
            database.setup_database(self.db_file)
        else:
            self.connection = sqlite3.connect(self.db_file)
            database.setup_database(self.db_file)  # Ensure schema is created
            self.empty_database()

        print(f"Database is connected at: {self.connection.execute('PRAGMA database_list').fetchall()}")

        self.connection.execute("PRAGMA journal_mode=WAL;") 

        self.submission_file = "src/tests/files/submission_file.py"
        self.test_file = "src/tests/files/test_file.py"

        # Populate database with test data
        database.create_Assignment(self.connection, 1, "Python Assignment", None, "No Rubric", 100, "12-12-2024")

        test_blob = database.file_to_blob(self.test_file)
        database.add_test_to_assignment(self.connection, 1, 1, test_blob, 0, 0, 100)

        database.create_student(self.connection, 1, "John", "Doe")

        submission_blob = database.file_to_blob(self.submission_file)
        database.create_Submission(self.connection, 1, 1, 1, None, submission_blob, "12-12-2024")

    def empty_database(self):
        """Empty all tables in the database."""
        cursor = self.connection.cursor()
        
        # Truncate or delete rows from each table to clear them
        cursor.execute("DELETE FROM Submissions;")
        cursor.execute("DELETE FROM Assignments;")
        cursor.execute("DELETE FROM Students;")
        cursor.execute("DELETE FROM Results;")
        cursor.execute("DELETE FROM Modules;")
        cursor.execute("DELETE FROM Results;")
        cursor.execute("DELETE FROM Tests;")

        # Commit the changes to the database
        self.connection.commit()

    def test_mark_submission(self):
        """Test the entire process of marking a submission."""
        score, feedback = self.auto_marker.mark_submission(1, "tmp_submission.py", "tmp_tests.py")

        # Assert score calculation and feedback
        self.assertEqual(score, 66.66666666666666)
        self.assertEqual(feedback, "Test failed")

if __name__ == '__main__':
    unittest.main()