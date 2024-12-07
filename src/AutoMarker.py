import subprocess
import database


class AutoMarker:
    def __init__(self, db_file):
        """Initialize the AutoMarker with the database file."""
        self.db_file = db_file
        self.connection = database.connect_database

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