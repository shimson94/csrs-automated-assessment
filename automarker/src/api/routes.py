from flask import request, jsonify
from src.database import connect_database
from src.automarker import AutoMarker

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
