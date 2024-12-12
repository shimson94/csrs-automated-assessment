import subprocess
import database
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

    def fetch_test_cases(self, assignment_id):
        """Fetch test cases for a given assignment."""
        return database.get_test_cases(self.connection, assignment_id)

    def run_student_code(self, file_path, test_input, timeout):
        """Run the student's code with the given input and capture the output."""
        try:
            result = subprocess.run(
                ['python3', file_path],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=timeout
            )
            return result.stdout.strip(), result.stderr.strip(),  # Return output and no error
        except subprocess.TimeoutExpired:
            return None, "Execution timed out"
        except Exception as e:
            return None, str(e)  # Return the exception message as an error

    def mark_submission(self, submission_id, file_path):
        """Run the automarker for a given submission."""
        # Fetch the assignment ID associated with this submission
        assignment_id = database.get_assignment_id_for_submission(self.connection, submission_id)

        # Fetch all test cases for the assignment
        test_cases = self.fetch_test_cases(assignment_id)

        total_tests = len(test_cases)
        passed_tests = 0
        feedback = []

        for test_id, test_input, expected_output, timeout in test_cases:
            actual_output, error = self.run_student_code(file_path, test_input, timeout)

            if error:
                feedback.append(f"Test {test_id} failed with error: {error}")
                passed = False
            elif actual_output == expected_output:
                passed_tests += 1
                feedback.append(f"Test {test_id} passed.")
                passed = True
            else:
                feedback.append(
                    f"Test {test_id} failed. Expected: {expected_output}, Got: {actual_output}"
                )
                passed = False

            # Record the result of this test case
            database.create_results(self.connection, submission_id, test_id, actual_output or "", passed, feedback[-1])

        # Calculate overall score and update submission
        score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        database.update_submission_score(self.connection, submission_id, score, "\n".join(feedback))
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
