import subprocess
from src import database
import unittest

import os
import io
from contextlib import redirect_stdout

class AutoMarker:
    def __init__(self, db_file):
        """Initialize the AutoMarker with the database file."""
        self.db_file = db_file
        self.connection = database.connect_database(db_file)

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        if self.connection:
            self.connection.close()
        if os.path.exists('tmp'):
            os.removedirs('dir')

    def save_test_file(self, assignment_id, temp_file_path):
        """Save the test file BLOB to a temporary file."""
        return database.save_test_file(self.connection, temp_file_path, assignment_id)

    def run_unit_tests(self, test_file_path):
        """Run the unit tests in the specified test file and return results."""
        loader = unittest.TestLoader()
        suite = loader.discover(os.path.dirname(test_file_path), pattern=os.path.basename(test_file_path))
        
        results = io.StringIO()
        with redirect_stdout(results):
            runner = unittest.TextTestRunner(stream=results, verbosity=2)
            test_results = runner.run(suite)

        return {
            "total": test_results.testsRun,
            "failures": len(test_results.failures),
            "errors": len(test_results.errors),
            "results": results.getvalue()
        }

    def mark_submission(self, submission_id, tmp_submission_path, temp_test_path):
        """Run the automarker for a given submission."""
        assignment_id = database.get_assignment_id_for_submission(self.connection, submission_id)

        test_blob = database.get_test_blob(self.connection, assignment_id)
        if not test_blob:
            raise ValueError("No test file found for the assignment.")

        # create tmp files
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        self.save_test_file(test_blob, "tmp/" + temp_test_path)
        database.save_submission_file(self.connection, "tmp/" + tmp_submission_path, submission_id)

        # Run the unit tests and capture results
        test_results = self.run_unit_tests(temp_test_path)

        # Calculate the score
        passed_tests = test_results["total"] - (test_results["failures"] + test_results["errors"])
        score = (passed_tests / test_results["total"]) * 100 if test_results["total"] > 0 else 0

        # Store results in the database
        feedback = test_results["results"]

        database.create_result(self.connection, 1, "placeholder", "placeholder", True, score)
        database.update_submission_result(self.connection, submission_id, 1)

        if os.path.exists(temp_test_path):
            os.remove(temp_test_path)

        return score, feedback
