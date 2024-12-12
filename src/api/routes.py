import sys
from pathlib import Path
from flask import request, Blueprint, jsonify

#Add the root directory of the project to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
from database import connect_database
from automarker import AutoMarker


api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/submissions", methods=["GET"])
def get_submissions():
    try:
        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()
        
        # Pagination parameters (default: page 1, 10 items per page)
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        if page < 1 or per_page < 1:
                raise ValueError("Page and per_page must be positive integers")
        offset = (page - 1) * per_page

        # Fetch submissions with pagination
        cursor.execute("""
            SELECT submission_id, student_id, assignment_id, submission_date, result, feedback
            FROM Submissions
            LIMIT ? OFFSET ?
        """, (per_page, offset))
        submissions = cursor.fetchall()

        # Convert to JSON-friendly format
        results = [
            {
                "submission_id": row[0],
                "student_id": row[1],
                "assignment_id": row[2],
                "submission_date": row[3],
                "result": row[4],
                "feedback": row[5],
            }
            for row in submissions
        ]

        # Get total count for pagination metadata
        cursor.execute("SELECT COUNT(*) FROM Submissions")
        total = cursor.fetchone()[0]

        # Close the connection
        connection.close()

        # Return JSON response
        return jsonify({
            "data": results,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total,
            }
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching submissions."}), 500


# Endpoint: POST /api/submissions
@api_blueprint.route("/submissions", methods=["POST"])
def create_submission():
    try:
        data = request.json
        student_id = data.get("student_id")
        assignment_id = data.get("assignment_id")
        submission_date = data.get("submission_date")
        result = data.get("result", None)
        feedback = data.get("feedback", None)

        if not student_id or not assignment_id or not submission_date:
            return jsonify({"error": "student_id, assignment_id, and submission_date are required."}), 400

        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        # Insert submission into the database
        cursor.execute("""
            INSERT INTO Submissions (student_id, assignment_id, submission_date, result, feedback)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, assignment_id, submission_date, result, feedback))
        connection.commit()
        connection.close()

        return jsonify({"message": "Submission created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint: GET /api/results
@api_blueprint.route("/results", methods=["GET"])
def get_results():
    try:
        # Optional query parameter for filtering by submission_id
        submission_id = request.args.get("submission_id", None)

        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        if submission_id:
            cursor.execute("""
                SELECT submission_id, result, feedback
                FROM Submissions
                WHERE submission_id = ?
            """, (submission_id,))
        else:
            cursor.execute("""
                SELECT submission_id, result, feedback
                FROM Submissions
            """)

        results = cursor.fetchall()

        # Convert to JSON-friendly format
        response = [
            {
                "submission_id": row[0],
                "result": row[1],
                "feedback": row[2],
            }
            for row in results
        ]

        connection.close()

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint: POST /api/mark-submission
@api_blueprint.route("/mark-submission", methods=["POST"])
def mark_submission():
    try:
        data = request.json
        submission_id = data.get("submission_id")
        file_path = data.get("file_path")

        if not submission_id or not file_path:
            return jsonify({"error": "submission_id and file_path are required."}), 400

        # Initialize AutoMarker
        connection = connect_database()
        automarker = AutoMarker(connection)

        # Run marking logic
        result = automarker.mark_submission(submission_id, file_path)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while marking the submission."}), 500