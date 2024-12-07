import sqlite3

DB_FILE = "src/db/prototype.db"
SQL_FILE = "src/db/setup.sql"

# Remember to close connection
def connect_database():
    return sqlite3.connect(DB_FILE)

# Setup Database
def setup_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor

    with open(SQL_FILE, "r") as sql_file:
        schema = sql_file.read()

    cursor.executescript(schema)

    connection.commit()
    connection.close()
    print('Database setup completed using setup.sql.')


# Checks whether database is setup already
def is_database_setup(connection):
    cursor = connection.cursor()
    cursor.execute()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name IN (
            'Students', 'Teachers', 'Modules', 'Assignments', 'Submissions'
        );
    """)
    tables = cursor.fetchall()

    # check if all required tables exist
    required_tables = {'Student', 'Teacher', 'Module', 'Assignment', 'Submission'}
    existing_tables = {table[0] for table in tables}
    return required_tables.issubset(existing_tables)


# CREATE

def create_student(connection, student_id, first_name, surname):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Students (student_id, first_name, surname)
        VALUES (?, ?, ?)
    """, (student_id, first_name, surname))
    connection.commit()
    print("Student created successfully.")

def create_teacher(connection, teacher_id, first_name, surname):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Teachers (teacher_id, first_name, surname)
        VALUES (?, ?, ?)
    """, (teacher_id, first_name, surname))
    connection.commit()
    print("Teacher created successfully.")

def create_module(connection, module_id, module_name):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Modules(module_id, module_name)
        VALUES (?, ?)
    """, (module_id, module_name))
    connection.commit()
    print("Module created successfully.")

def create_Assignment(connection, assignment_id, module_id, assignment_description, rubric, threshold, due_date):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Assignments (assignment_id, module_id, assignment_description, rubric, threshold, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (assignment_id, module_id, assignment_description, rubric, threshold, due_date))
    connection.commit()
    print("Assignment created successfully.")

def create_Submission(connection, submission_id, student_id, assignment_id, submission_date, result_id, submission_content):
    cursor = connection.cursor
    cursor.execute("""
        INSERT INTO Submissions(submission_id, student_id, assignment_id, submission_date, result, feedback)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (submission_id, student_id, assignment_id, submission_date, result_id, submission_content))
    connection.commit()
    print("Submission created successfully.")

def create_results(connection, submission_id, test_id, actual_output, passed, feedback):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Results (submission_id, test_id, actual_output, passed, feedback)
        VALUES (?, ?, ?, ?, ?)
    """, (submission_id, test_id, actual_output, passed, feedback))
    connection.commit()
    print("Test result recorded successfully.")


# READ
def get_students(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students")
    return cursor.fetchall()

def get_teachers(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Teachers")
    return cursor.fetchall()

def get_modules(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Modules")
    return cursor.fetchall()

def get_assignments(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Assignments")
    return cursor.fetchall()

def get_submissions(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Submissions")
    return cursor.fetchall()

def get_test_cases(connection, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT test_id, input, expected_output, timeout_seconds 
        FROM AssignmentTests 
        WHERE assignment_id = ?
    """, (assignment_id,))
    return cursor.fetchall()

def get_assignment_id_for_submission (connection, submission_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT assignment_id FROM Submissions WHERE submission_id = ?
    """, (submission_id,))
    result = cursor.fetchone()
    return result[0] if result else None


# UPDATE
def update_student(connection, student_id, first_name, surname):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Students
        SET first_name = ?, surname = ?
        WHERE student_id = ?
    """, (first_name, surname, student_id))
    connection.commit()
    print("Student updated successfully.")

def update_teacher(connection, teacher_id, first_name, surname):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Teachers
        SET first_name = ?, surname = ?
        WHERE teacher_id = ?
    """, (first_name, surname, teacher_id))
    connection.commit()
    print("Teacher updated successfully.")

def update_module(connection, module_id, module_name):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Modules
        SET module_name = ?
        WHERE module_id = ?
    """, (module_name, module_id))
    connection.commit()
    print("Module updated successfully.")

def update_assignment(connection, assignment_id, module_id, assignment_description, rubric, threshold, due_date):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Assignments
        SET module_id = ?, assignment_description = ?, rubric = ?, threshold = ?, due_date = ?
        WHERE assignment_id = ?
    """, (module_id, assignment_description, rubric, threshold, due_date, assignment_id))
    connection.commit()
    print("Assignment updated successfully.")

def update_submission(connection, submission_id, student_id, assignment_id, submission_date, result_id, submission_content):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Submissions
        SET student_id = ?, assignment_id = ?, submission_date = ?, result = ?, feedback = ?
        WHERE submission_id = ?
    """, (student_id, assignment_id, submission_date, result_id, submission_content, submission_id))
    connection.commit()
    print("Submission updated successfully.")

def update_submission_score(connection, submission_id, score, feedback):
    """Update the result and feedback for a submission."""
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Submissions
        SET result = ?, feedback = ?
        WHERE submission_id = ?
    """, (score, feedback, submission_id))
    connection.commit()
    print(f"Submission {submission_id} updated with score: {score}%")


# DELETE
def delete_student(connection, student_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    connection.commit()
    print("Student deleted successfully.")

def delete_teacher(connection, teacher_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Teachers WHERE teacher_id = ?", (teacher_id,))
    connection.commit()
    print("Teacher deleted successfully.")

def delete_module(connection, module_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Modules WHERE module_id = ?", (module_id,))
    connection.commit()
    print("Module deleted successfully.")

def delete_assignment(connection, assignment_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Assignments WHERE assignment_id = ?", (assignment_id,))
    connection.commit()
    print("Assignment deleted successfully.")

def delete_submission(connection, submission_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Submissions WHERE submission_id = ?", (submission_id,))
    connection.commit()
    print("Submission deleted successfully.")


# CREATE for relational tables
def add_teacher_to_module(connection, teacher_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO TeacherModules (teacher_id, module_id)
        VALUES (?, ?)
    """, (teacher_id, module_id))
    connection.commit()
    print("Teacher added to module successfully.")

def enroll_student_in_module(connection, student_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO StudentEnrollments (student_id, module_id)
        VALUES (?, ?)
    """, (student_id, module_id))
    connection.commit()
    print("Student enrolled in module successfully.")

def add_assignment_to_module(connection, module_id, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO ModuleAssignments (module_id, assignment_id)
        VALUES (?, ?)
    """, (module_id, assignment_id))
    connection.commit()
    print("Assignment added to module successfully.")

def add_test_to_assignment (connection, assignment_id, test_id):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO AssignmentTests (assignment_id, test_id)
        VALUES (?, ?)
    """, (assignment_id, test_id))
    connection.commit()
    print("Assignment added to module successfully.")

# READ for relational tables
def get_teacher_modules(connection, teacher_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT module_id FROM TeacherModules WHERE teacher_id = ?
    """, (teacher_id,))
    return cursor.fetchall()

def get_student_enrollments(connection, student_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT module_id FROM StudentEnrollments WHERE student_id = ?
    """, (student_id,))
    return cursor.fetchall()

def get_module_assignments(connection, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT assignment_id FROM ModuleAssignments WHERE module_id = ?
    """, (module_id,))
    return cursor.fetchall()

def get_assignment_tests (connection, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT test_id FROM AssignmentTests WHERE assignment_id = ?
    """, (assignment_id,))
    return cursor.fetchall()

# DELETE for relational tables
def remove_teacher_from_module(connection, teacher_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM TeacherModules WHERE teacher_id = ? AND module_id = ?
    """, (teacher_id, module_id))
    connection.commit()
    print("Teacher removed from module successfully.")

def remove_student_from_module(connection, student_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM StudentEnrollments WHERE student_id = ? AND module_id = ?
    """, (student_id, module_id))
    connection.commit()
    print("Student removed from module successfully.")

def remove_assignment_from_module(connection, module_id, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM ModuleAssignments WHERE module_id = ? AND assignment_id = ?
    """, (module_id, assignment_id))
    connection.commit()
    print("Assignment removed from module successfully.")

def remove_test_from_assignment (connection, assignment_id, test_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM AssignmentTests WHERE assignment_id = ? AND test_id = ?
    """, (assignment_id, test_id))
    connection.commit()
    print("Assignment removed from module successfully.")