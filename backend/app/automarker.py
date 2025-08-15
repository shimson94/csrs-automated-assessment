import subprocess
import unittest
import os
import io
import tempfile
import shutil
from contextlib import redirect_stdout
from datetime import datetime, timezone
from flask import current_app

# Import SQLAlchemy models and database instance
from models.models import db, Submission, Assignment, Test, Result, SubmissionStatus, GradeStatus


class AutoMarker:
    def __init__(self):
        """Initialize the AutoMarker with SQLAlchemy database session."""
        pass  # No need to store anything - we'll use the Flask app context and db session

    def get_assignment_from_submission(self, submission_id):
        """Get assignment details from submission ID using SQLAlchemy."""
        submission = db.session.get(Submission, submission_id)
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")
        return submission.assignment

    def get_test_file_from_assignment(self, assignment):
        """Get test file content from assignment using SQLAlchemy."""
        if not assignment.test or not assignment.test.test_file:
            raise ValueError(f"No test file found for assignment {assignment.assignment_id}")
        return assignment.test.test_file

    def save_submission_file_to_temp(self, submission):
        """Save submission file BLOB to a temporary file and return the path."""
        if not submission.submission_file:
            raise ValueError(f"No submission file found for submission {submission.submission_id}")
        
        # Create temporary file with proper extension
        file_extension = '.py'  # Default to Python, could be enhanced based on file_type
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_extension, prefix='submission_')
        
        try:
            with os.fdopen(temp_fd, 'wb') as temp_file:
                temp_file.write(submission.submission_file)
            return temp_path
        except Exception as e:
            os.close(temp_fd)  # Make sure to close if writing fails
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    def save_test_file_to_temp(self, test_file_blob):
        """Save test file BLOB to a temporary file and return the path."""
        if not test_file_blob:
            raise ValueError("No test file content provided")
        
        # Create temporary file with .py extension for test files
        temp_fd, temp_path = tempfile.mkstemp(suffix='_test.py', prefix='test_')
        
        try:
            with os.fdopen(temp_fd, 'wb') as temp_file:
                temp_file.write(test_file_blob)
            return temp_path
        except Exception as e:
            os.close(temp_fd)  # Make sure to close if writing fails
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    def run_student_code(self, file_path, test_input="", timeout=10):
        """Run the student's code with the given input and capture the output."""
        try:
            # Use python3 on Unix-like systems, python on Windows
            python_cmd = 'python' if os.name == 'nt' else 'python3'
            
            result = subprocess.run(
                [python_cmd, file_path],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=os.path.dirname(file_path)  # Set working directory to file location
            )
            return result.stdout.strip(), result.stderr.strip() if result.stderr else None
        except subprocess.TimeoutExpired:
            return None, "Execution timed out"
        except Exception as e:
            return None, str(e)

    def run_unit_tests(self, test_file_path, student_file_path=None):
        """Run the unit tests in the specified test file and return results."""
        try:
            # Get the directory and filename
            test_dir = os.path.dirname(test_file_path)
            test_filename = os.path.basename(test_file_path)
            
            # If student file path is provided, modify the test file to include it
            if student_file_path:
                # Read the test file content
                with open(test_file_path, 'r') as f:
                    test_content = f.read()
                
                # Replace the student_file placeholder with actual path
                test_content = test_content.replace(
                    "self.student_file = None",
                    f"self.student_file = r'{student_file_path}'"
                )
                
                # Write the modified content back
                with open(test_file_path, 'w') as f:
                    f.write(test_content)
            
            # Load the test suite
            loader = unittest.TestLoader()
            suite = loader.discover(test_dir, pattern=test_filename)
            
            # Capture test results
            results = io.StringIO()
            with redirect_stdout(results):
                runner = unittest.TextTestRunner(stream=results, verbosity=2)
                test_results = runner.run(suite)

            return {
                "total": test_results.testsRun,
                "failures": len(test_results.failures),
                "errors": len(test_results.errors),
                "passed": test_results.testsRun - len(test_results.failures) - len(test_results.errors),
                "results": results.getvalue(),
                "failure_details": [str(failure) for failure in test_results.failures],
                "error_details": [str(error) for error in test_results.errors]
            }
        except Exception as e:
            return {
                "total": 0,
                "failures": 1,
                "errors": 0,
                "passed": 0,
                "results": f"Failed to run tests: {str(e)}",
                "failure_details": [str(e)],
                "error_details": []
            }

    def create_or_update_result(self, submission, test_results, score, feedback):
        """Create or update the Result record for a submission."""
        try:
            # Check if result already exists
            if submission.result:
                result = submission.result
            else:
                result = Result()
                db.session.add(result)
            
            # Update result fields
            result.actual_output = test_results.get("results", "")[:2000]  # Limit length
            result.expected_output = "Unit tests executed"  # Could be enhanced with specific expected outputs
            result.passed = test_results["passed"] == test_results["total"]
            result.score = score
            result.percentage = score
            result.test_cases_passed = test_results["passed"]
            result.test_cases_total = test_results["total"]
            result.feedback = feedback[:2000]  # Limit length
            result.feedback_summary = f"Passed {test_results['passed']}/{test_results['total']} tests"
            result.grade_status = GradeStatus.GRADED
            result.graded_at = datetime.now(timezone.utc)
            result.graded_by = 'AUTOMARKER'
            
            # Handle errors
            if test_results["errors"] > 0:
                result.error_message = "; ".join(test_results["error_details"][:3])  # Limit errors shown
            
            # Link result to submission if new
            if not submission.result:
                submission.result = result
                submission.result_id = result.result_id
            
            return result
            
        except Exception as e:
            current_app.logger.error(f"Error creating/updating result: {str(e)}")
            raise

    def mark_submission(self, submission_id):
        """
        Main method to run the automarker for a given submission.
        This replaces the old mark_submission methods.
        """
        submission_temp_path = None
        test_temp_path = None
        
        try:
            # Get submission with all related data
            submission = db.session.get(Submission, submission_id)
            if not submission:
                raise ValueError(f"Submission {submission_id} not found")
            
            # Update submission status
            submission.status = SubmissionStatus.GRADING
            db.session.commit()
            
            # Get assignment and test file
            assignment = self.get_assignment_from_submission(submission_id)
            test_file_blob = self.get_test_file_from_assignment(assignment)
            
            # Save files to temporary locations
            submission_temp_path = self.save_submission_file_to_temp(submission)
            test_temp_path = self.save_test_file_to_temp(test_file_blob)
            
            current_app.logger.info(f"Running automarker for submission {submission_id}")
            current_app.logger.info(f"Submission file: {submission_temp_path}")
            current_app.logger.info(f"Test file: {test_temp_path}")
            
            # Run the unit tests with student file path
            test_results = self.run_unit_tests(test_temp_path, submission_temp_path)
            
            # Calculate base score
            if test_results["total"] > 0:
                base_score = (test_results["passed"] / test_results["total"]) * assignment.max_score
                base_percentage = (test_results["passed"] / test_results["total"]) * 100
            else:
                base_score = 0
                base_percentage = 0
            
            # Apply late penalty if submission is late
            penalty_applied = 0.0
            penalty_description = ""
            
            if submission.is_late and submission.days_late > 0:
                # Late penalty configuration
                penalty_per_day = 0.10    # 10% per day late
                max_penalty = 0.50        # Maximum 50% penalty
                grace_days = 0           # No grace period
                
                # Calculate penalty rate
                days_for_penalty = max(0, submission.days_late - grace_days)
                penalty_rate = min(days_for_penalty * penalty_per_day, max_penalty)
                
                # Apply penalty to scores
                score = base_score * (1 - penalty_rate)
                percentage = base_percentage * (1 - penalty_rate)
                penalty_applied = penalty_rate
                
                penalty_description = f"\n\n⚠️ LATE SUBMISSION PENALTY:\n" \
                                    f"- Days late: {submission.days_late}\n" \
                                    f"- Penalty rate: {penalty_rate*100:.1f}%\n" \
                                    f"- Base score: {base_score:.2f} ({base_percentage:.1f}%)\n" \
                                    f"- Final score after penalty: {score:.2f} ({percentage:.1f}%)"
                
                current_app.logger.info(f"Late penalty applied to submission {submission_id}: "
                                       f"{penalty_rate*100:.1f}% for {submission.days_late} days late. "
                                       f"Score: {base_score:.2f} -> {score:.2f}")
            else:
                score = base_score
                percentage = base_percentage
            
            # Create detailed feedback
            feedback_parts = [
                f"Automarker Results for {assignment.title}",
                f"Tests Run: {test_results['total']}",
                f"Tests Passed: {test_results['passed']}",
                f"Tests Failed: {test_results['failures']}",
                f"Tests with Errors: {test_results['errors']}",
                f"Score: {score:.2f}/{assignment.max_score}",
                f"Percentage: {percentage:.1f}%",
                penalty_description,
                "",
                "Detailed Results:",
                test_results["results"]
            ]
            
            if test_results["failure_details"]:
                feedback_parts.extend(["", "Failure Details:"] + test_results["failure_details"])
            
            if test_results["error_details"]:
                feedback_parts.extend(["", "Error Details:"] + test_results["error_details"])
            
            feedback = "\n".join(feedback_parts)
            
            # Create or update result
            result = self.create_or_update_result(submission, test_results, score, feedback)
            
            # Update submission status
            if test_results["passed"] == test_results["total"]:
                submission.status = SubmissionStatus.PASSED
            elif test_results["passed"] > 0:
                submission.status = SubmissionStatus.PARTIAL
            else:
                submission.status = SubmissionStatus.FAILED
            
            # Commit all changes
            db.session.commit()
            
            current_app.logger.info(f"Automarker completed for submission {submission_id}. Score: {score:.2f}")
            
            return {
                "success": True,
                "submission_id": submission_id,
                "score": score,
                "percentage": percentage,
                "max_score": assignment.max_score,
                "tests_total": test_results["total"],
                "tests_passed": test_results["passed"],
                "tests_failed": test_results["failures"],
                "tests_errors": test_results["errors"],
                "feedback": feedback,
                "status": submission.status.value
            }
            
        except Exception as e:
            # Update submission status to indicate grading failed
            try:
                submission = db.session.get(Submission, submission_id)
                if submission:
                    submission.status = SubmissionStatus.ERROR
                    
                    # Create an error result
                    if not submission.result:
                        result = Result(
                            actual_output="",
                            expected_output="",
                            passed=False,
                            score=0,
                            percentage=0,
                            test_cases_passed=0,
                            test_cases_total=0,
                            error_message=str(e)[:500],
                            feedback=f"Grading failed: {str(e)}",
                            feedback_summary="Grading failed due to system error",
                            grade_status=GradeStatus.ERROR,
                            graded_at=datetime.now(timezone.utc),
                            graded_by='AUTOMARKER'
                        )
                        db.session.add(result)
                        submission.result = result
                    
                    db.session.commit()
            except Exception as inner_e:
                current_app.logger.error(f"Failed to update submission status after error: {str(inner_e)}")
                db.session.rollback()
            
            current_app.logger.error(f"Automarker failed for submission {submission_id}: {str(e)}")
            
            return {
                "success": False,
                "submission_id": submission_id,
                "error": str(e),
                "score": 0,
                "percentage": 0
            }
            
        finally:
            # Clean up temporary files
            if submission_temp_path and os.path.exists(submission_temp_path):
                try:
                    os.remove(submission_temp_path)
                except Exception as e:
                    current_app.logger.warning(f"Failed to remove temp submission file: {str(e)}")
            
            if test_temp_path and os.path.exists(test_temp_path):
                try:
                    os.remove(test_temp_path)
                except Exception as e:
                    current_app.logger.warning(f"Failed to remove temp test file: {str(e)}")
