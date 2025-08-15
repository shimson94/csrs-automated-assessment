import sys
from pathlib import Path
from flask import request, Blueprint, jsonify, current_app
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

# Add the root directory of the project to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from models.models import (
    db, Student, Teacher, Module, Assignment, Submission, Result, Test,
    SubmissionStatus, ProgrammingLanguage, TestType, GradeStatus, SubmissionFileType
)
from automarker import AutoMarker

submissions_blueprint = Blueprint("submissions", __name__)

# Utility functions for better error handling
def error_response(message, status_code=400):
    """Standardized error response format"""
    return jsonify({"error": message}), status_code

def success_response(data, message="Success"):
    """Standardized success response format"""
    return jsonify({"message": message, "data": data}), 200

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present in request data"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return error_response(f"Missing required fields: {', '.join(missing_fields)}")
    return None

# Endpoint: GET /api/submissions
@submissions_blueprint.route("/submissions", methods=["GET"])
def get_submissions():
    """
    Get paginated list of submissions with optional filtering
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 100)
    - student_id: Filter by student
    - assignment_id: Filter by assignment
    - status: Filter by submission status
    """
    try:
        # Parse pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 items per page
        
        if page < 1 or per_page < 1:
            return error_response("Page and per_page must be positive integers")
        
        # Parse filter parameters
        student_id = request.args.get('student_id', type=int)
        assignment_id = request.args.get('assignment_id', type=int)
        status = request.args.get('status')
        
        # Build query with filters
        query = Submission.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if assignment_id:
            query = query.filter_by(assignment_id=assignment_id)
        if status:
            try:
                status_enum = SubmissionStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return error_response(f"Invalid status. Valid options: {[s.value for s in SubmissionStatus]}")
        
        # Order by submission date (newest first)
        query = query.order_by(Submission.submission_date.desc())
        
        # Execute paginated query
        submissions_query = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to JSON with related data
        submissions_data = []
        for submission in submissions_query.items:
            submission_dict = submission.to_dict()
            # Add student and assignment info
            if submission.student:
                submission_dict['student_name'] = f"{submission.student.first_name} {submission.student.surname}"
            if submission.assignment:
                submission_dict['assignment_title'] = submission.assignment.title
            submissions_data.append(submission_dict)
        
        return jsonify({
            "submissions": submissions_data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": submissions_query.total,
                "pages": submissions_query.pages,
                "has_next": submissions_query.has_next,
                "has_prev": submissions_query.has_prev
            }
        }), 200
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error in get_submissions: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        current_app.logger.error(f"Unexpected error in get_submissions: {e}")
        return error_response("An unexpected error occurred", 500)

# Endpoint: POST /api/submissions
@submissions_blueprint.route("/submissions", methods=["POST"])
def create_submission():
    """
    Create a new submission
    Required fields: student_id, assignment_id
    Optional fields: file_content, file_name, file_type
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("Request body must be JSON")
        
        # Validate required fields
        validation_error = validate_required_fields(data, ['student_id', 'assignment_id'])
        if validation_error:
            return validation_error
        
        # Validate student exists
        student = Student.query.get(data['student_id'])
        if not student:
            return error_response("Student not found", 404)
            
        # Validate assignment exists
        assignment = Assignment.query.get(data['assignment_id'])
        if not assignment:
            return error_response("Assignment not found", 404)
        
        # Check assignment due date
        current_time = datetime.now(timezone.utc)
        if assignment.due_date:
            # Convert assignment due_date to timezone-aware for comparison
            assignment_due_date_utc = assignment.due_date.replace(tzinfo=timezone.utc) if assignment.due_date.tzinfo is None else assignment.due_date
            is_late = current_time > assignment_due_date_utc
            days_late = (current_time - assignment_due_date_utc).days if is_late else 0
        else:
            is_late = False
            days_late = 0
        
        # Check if student has reached max attempts
        existing_attempts = Submission.query.filter_by(
            student_id=data['student_id'],
            assignment_id=data['assignment_id']
        ).count()
        
        if existing_attempts >= assignment.max_attempts:
            return error_response(f"Maximum attempts ({assignment.max_attempts}) reached")
        
        # Validate file type if provided
        file_type = data.get('file_type')
        if file_type and file_type not in [ft.value for ft in SubmissionFileType]:
            return error_response(f"Invalid file type. Valid options: {[ft.value for ft in SubmissionFileType]}")
        
        # Create new submission
        submission = Submission(
            student_id=data['student_id'],
            assignment_id=data['assignment_id'],
            file_name=data.get('file_name'),
            file_type=SubmissionFileType(file_type) if file_type else SubmissionFileType.PYTHON_FILE,
            attempt_number=existing_attempts + 1,
            submission_date=current_time,
            is_late=is_late,
            days_late=days_late,
            status=SubmissionStatus.SUBMITTED,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        # Handle file content (if provided)
        if 'file_content' in data:
            file_content_bytes = data['file_content'].encode('utf-8')
            submission.submission_file = file_content_bytes
            submission.file_size = len(file_content_bytes)
        
        db.session.add(submission)
        db.session.commit()
        
        current_app.logger.info(f"Submission created: ID {submission.submission_id} by student {data['student_id']}")
        
        return success_response(
            submission.to_dict(), 
            "Submission created successfully"
        )
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in create_submission: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in create_submission: {e}")
        return error_response("An unexpected error occurred", 500)

# Endpoint: GET /api/submissions/{submission_id}
@submissions_blueprint.route("/submissions/<int:submission_id>", methods=["GET"])
def get_submission(submission_id):
    """Get detailed information about a specific submission"""
    try:
        submission = Submission.query.get(submission_id)
        if not submission:
            return error_response("Submission not found", 404)
        
        # Build detailed response
        submission_data = submission.to_dict()
        
        # Add related data
        if submission.student:
            submission_data['student'] = {
                'student_id': submission.student.student_id,
                'name': f"{submission.student.first_name} {submission.student.surname}",
                'email': submission.student.email
            }
        
        if submission.assignment:
            submission_data['assignment'] = {
                'assignment_id': submission.assignment.assignment_id,
                'title': submission.assignment.title,
                'due_date': submission.assignment.due_date.isoformat() if submission.assignment.due_date else None,
                'max_score': submission.assignment.max_score
            }
        
        if submission.result:
            submission_data['result'] = submission.result.to_dict()
        
        return success_response(submission_data)
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error in get_submission: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        current_app.logger.error(f"Unexpected error in get_submission: {e}")
        return error_response("An unexpected error occurred", 500)

# Endpoint: GET /api/results
@submissions_blueprint.route("/results", methods=["GET"])
def get_results():
    """
    Get paginated list of results with optional filtering
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    - submission_id: Filter by submission
    - grade_status: Filter by grading status
    """
    try:
        # Parse pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        submission_id = request.args.get('submission_id', type=int)
        grade_status = request.args.get('grade_status')
        
        if page < 1 or per_page < 1:
            return error_response("Page and per_page must be positive integers")
        
        # Build query
        query = Result.query
        
        if submission_id:
            # Find the result_id for the given submission_id first
            submission = Submission.query.filter_by(submission_id=submission_id).first()
            if submission and submission.result_id:
                query = query.filter(Result.result_id == submission.result_id)
            else:
                # No results for this submission_id
                return jsonify({
                    "results": [],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": 0,
                        "pages": 0,
                        "has_next": False,
                        "has_prev": False
                    }
                }), 200
                
        if grade_status:
            try:
                status_enum = GradeStatus(grade_status)
                query = query.filter_by(grade_status=status_enum)
            except ValueError:
                return error_response(f"Invalid grade status. Valid options: {[gs.value for gs in GradeStatus]}")
        
        # Order by graded date (newest first)
        query = query.order_by(Result.graded_at.desc())
        
        # Execute paginated query
        results_query = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Convert to JSON with related data
        results_data = []
        for result in results_query.items:
            result_dict = result.to_dict()
            # Add submission info by finding the submission that references this result
            submission = Submission.query.filter_by(result_id=result.result_id).first()
            if submission:
                result_dict['submission'] = {
                    'submission_id': submission.submission_id,
                    'student_id': submission.student_id,
                    'assignment_id': submission.assignment_id,
                    'file_name': submission.file_name,
                    'submission_date': submission.submission_date.isoformat() if submission.submission_date else None
                }
            results_data.append(result_dict)
        
        return jsonify({
            "results": results_data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": results_query.total,
                "pages": results_query.pages,
                "has_next": results_query.has_next,
                "has_prev": results_query.has_prev
            }
        }), 200
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error in get_results: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        current_app.logger.error(f"Unexpected error in get_results: {e}")
        return error_response("An unexpected error occurred", 500)

# Endpoint: POST /api/submissions/{submission_id}/grade
@submissions_blueprint.route("/submissions/<int:submission_id>/grade", methods=["POST"])
def grade_submission(submission_id):
    """
    Trigger automated grading for a submission
    This endpoint will run the automarker on the submission
    """
    try:
        # Get submission
        submission = Submission.query.get(submission_id)
        if not submission:
            return error_response("Submission not found", 404)
        
        # Check if submission has file content
        if not submission.submission_file:
            return error_response("No code file found in submission")
        
        # Get associated assignment and test
        assignment = Assignment.query.get(submission.assignment_id)
        if not assignment:
            return error_response("Assignment not found", 404)
        
        test = assignment.test
        if not test:
            return error_response("No test found for this assignment", 404)
        
        # Check if already graded
        if submission.result and submission.result.grade_status == GradeStatus.GRADED:
            return error_response("Submission already graded. Use PUT to re-grade.")
        
        # Check if submission has required files
        if not submission.submission_file:
            return error_response("No submission file found to grade")
        
        # Get associated assignment and test
        assignment = submission.assignment
        if not assignment:
            return error_response("Assignment not found", 404)
        
        if not assignment.test or not assignment.test.test_file:
            return error_response("No test file found for this assignment", 404)
        
        # Update submission status to grading
        submission.status = SubmissionStatus.GRADING
        db.session.commit()
        
        # Initialize AutoMarker and run grading
        automarker = AutoMarker()
        
        current_app.logger.info(f"Starting automated grading for submission {submission_id}")
        
        # Run the automarker (this now handles everything internally)
        grading_result = automarker.mark_submission(submission_id)
        
        if grading_result.get('success', False):
            current_app.logger.info(f"Submission {submission_id} graded successfully. Score: {grading_result.get('score', 0)}")
            
            # Refresh submission to get updated result
            db.session.refresh(submission)
            
            return success_response({
                "submission": submission.to_dict(),
                "result": submission.result.to_dict() if submission.result else None,
                "grading_details": {
                    "score": grading_result.get('score', 0),
                    "percentage": grading_result.get('percentage', 0),
                    "max_score": grading_result.get('max_score', 0),
                    "tests_total": grading_result.get('tests_total', 0),
                    "tests_passed": grading_result.get('tests_passed', 0),
                    "tests_failed": grading_result.get('tests_failed', 0),
                    "tests_errors": grading_result.get('tests_errors', 0),
                    "status": grading_result.get('status', 'unknown')
                }
            }, "Submission graded successfully")
        else:
            # Grading failed
            current_app.logger.error(f"Grading failed for submission {submission_id}: {grading_result.get('error', 'Unknown error')}")
            
            # Refresh submission to get updated status
            db.session.refresh(submission)
            
            return error_response(
                f"Grading failed: {grading_result.get('error', 'Unknown error')}", 
                500
            )
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in grade_submission: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in grade_submission: {e}")
        return error_response("Grading failed", 500)

# Endpoint: PUT /api/submissions/{submission_id}/regrade
@submissions_blueprint.route("/submissions/<int:submission_id>/regrade", methods=["PUT"])
def regrade_submission(submission_id):
    """Re-grade an already graded submission (teacher override)"""
    try:
        submission = Submission.query.get(submission_id)
        if not submission:
            return error_response("Submission not found", 404)
        
        current_app.logger.info(f"Re-grading submission {submission_id}")
        
        # Delete existing result if present
        if submission.result:
            db.session.delete(submission.result)
            submission.result_id = None
        
        # Reset submission status
        submission.status = SubmissionStatus.SUBMITTED
        db.session.commit()
        
        # Initialize AutoMarker and run grading
        automarker = AutoMarker()
        grading_result = automarker.mark_submission(submission_id)
        
        if grading_result.get('success', False):
            current_app.logger.info(f"Submission {submission_id} re-graded successfully. Score: {grading_result.get('score', 0)}")
            
            # Refresh submission to get updated result
            db.session.refresh(submission)
            
            return success_response({
                "submission": submission.to_dict(),
                "result": submission.result.to_dict() if submission.result else None,
                "grading_details": {
                    "score": grading_result.get('score', 0),
                    "percentage": grading_result.get('percentage', 0),
                    "max_score": grading_result.get('max_score', 0),
                    "tests_total": grading_result.get('tests_total', 0),
                    "tests_passed": grading_result.get('tests_passed', 0),
                    "tests_failed": grading_result.get('tests_failed', 0),
                    "tests_errors": grading_result.get('tests_errors', 0),
                    "status": grading_result.get('status', 'unknown')
                }
            }, "Submission re-graded successfully")
        else:
            # Re-grading failed
            current_app.logger.error(f"Re-grading failed for submission {submission_id}: {grading_result.get('error', 'Unknown error')}")
            
            return error_response(
                f"Re-grading failed: {grading_result.get('error', 'Unknown error')}", 
                500
            )
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in regrade_submission: {e}")
        return error_response("Database error occurred", 500)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in regrade_submission: {e}")
        return error_response("Re-grading failed", 500)

# Health check endpoint
@submissions_blueprint.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "submissions",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }), 200