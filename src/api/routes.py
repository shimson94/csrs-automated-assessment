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
    # Connect to the database
    connection = connect_database()
    cursor = connection.cursor()
    
    # Pagination parameters (default: page 1, 10 items per page)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
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

@api_blueprint.route("/mark-submission", methods=["POST"])
def mark_submission():
    data = request.json
    submission_id = data.get("submission_id")
    file_path = data.get("file_path")

    # Initialize AutoMarker
    connection = connect_database()
    automarker = AutoMarker(connection)

    # Run marking logic
    result = automarker.mark_submission(submission_id, file_path)

    return jsonify(result)
