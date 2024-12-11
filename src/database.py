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

def create_Assignment(connection, assignment_id, assignment_description, test_id, rubric, threshold, due_date):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Assignments (assignment_id, assignment_description, test_id, rubric, threshold, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (assignment_id, assignment_description, test_id, rubric, threshold, due_date))
    connection.commit()
    print("Assignment created successfully.")

# raw_submission_file can be NULL and can be later added using add_file_to_submission()
def create_Submission(connection, submission_id, student_id, assignment_id, result_id, raw_submission_file):
    cursor = connection.cursor
    cursor.execute("""
        INSERT INTO Submissions(submission_id, student_id, assignment_id, result_id, submission_file)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (submission_id, student_id, assignment_id, result_id, raw_submission_file))
    connection.commit()
    print("Submission created successfully.")

def add_result_to_submission(connection, submission_id, actual_output, expected_output, passed, result):
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO Results (actual_output, expected_output, passed, result)
        VALUES (?, ?, ?, ?)
    """, (actual_output, expected_output, passed, result))

    result_id = cursor.lastrowid
    
    cursor.execute("""
        UPDATE Submissions
        SET result_id = ?
        WHERE submission_id = ?
    """, (result_id, submission_id))
    connection.commit()

def create_result(connection, result_id, actual_output, expected_output, passed, score):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Results (result_id, actual_output, expected_output, passed, result)
        VALUES (?, ?, ?, ?, ?)
    """, (result_id, actual_output, expected_output, passed, score))
    connection.commit()
    print("Result created successfully.")


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

def get_results(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Results")
    return cursor.fetchall()

def get_test_case(connection, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT test_id, test_file, input, expected_output, timeout_seconds 
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

def get_submission_blob(connection, submission_id):
    """
    Retrieve the submisison_file blob associated with a given submission_id.

    Returns:
        bytes: The submission_file blob if found, None otherwise.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT submission_file FROM Submissions WHERE submission_id = ?", (submission_id,))
    file_data = cursor.fetchone()
    return file_data[0] if file_data else None

def get_test_blob(connection, assignment_id):
    """
    Fetches the test_file blob for a given assignment_id.
    
    Returns:
        Bytes: The test_file blob if found, None otherwise.
    """
    cursor = connection.cursor()
    cursor.execute("""
        SELECT t.test_file
        FROM Assignments a
        JOIN Tests t ON a.test_id = t.test_id
        WHERE a.assignment_id = ?
    """, (assignment_id,))
    
    file_data = cursor.fetchone()
    return file_data[0] if file_data else None 

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

def update_assignment(connection, assignment_id, assignment_description, test_id, rubric, threshold, due_date):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Assignments
        SET  assignment_description = ?, test_id = ?, rubric = ?, threshold = ?, due_date = ?
        WHERE assignment_id = ?
    """, (assignment_description, test_id, rubric, threshold, due_date, assignment_id))
    connection.commit()
    print("Assignment updated successfully.")

def update_submission(connection, submission_id, student_id, assignment_id, submission_date, result_id, raw_submission_file):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Submissions
        SET student_id = ?, assignment_id = ?, submission_date = ?, result = ?, feedback = ?, submission_file = ?
        WHERE submission_id = ?
    """, (student_id, assignment_id, submission_date, result_id, raw_submission_file, submission_id))
    connection.commit()
    print("Submission updated successfully.")

def update_result(connection, result_id, actual_output, expected_output, passed, result):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Results
        SET actual_output = ?, expected_output = ?, passed = ?, result = ?
        WHERE result_id = ?
    """, (actual_output, expected_output, passed, result, result_id))
    connection.commit()
    print(f"Submission updated successfully.")


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

def delete_result(connection, result_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Results WHERE result_id = ?", (result_id,))
    connection.commit()
    print("Result deleted successfully.")

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

# Create new test then adds to assignment
def add_test_to_assignment(connection, assignment_id, test_id, test_blob, input, expected_output, timeout_seconds):
    cursor = connection.cursor()
        
    cursor.execute("""
        INSERT INTO Tests (test_id, test_function, input, expected_output, timeout_seconds)
        VALUES (?, ?, ?, ?, ?)
    """, (test_id, test_blob, input, expected_output, timeout_seconds))
        
    cursor.execute("""
        INSERT INTO AssignmentTests (assignment_id, test_id)
        VALUES (?, ?)
    """, (assignment_id, test_id))
        
    connection.commit()
    print("Test added to assignment")

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
def delete_teacher_from_module(connection, teacher_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM TeacherModules WHERE teacher_id = ? AND module_id = ?
    """, (teacher_id, module_id))
    connection.commit()
    print("Teacher removed from module successfully.")

def delete_student_from_module(connection, student_id, module_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM StudentEnrollments WHERE student_id = ? AND module_id = ?
    """, (student_id, module_id))
    connection.commit()
    print("Student removed from module successfully.")

def delete_assignment_from_module(connection, module_id, assignment_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM ModuleAssignments WHERE module_id = ? AND assignment_id = ?
    """, (module_id, assignment_id))
    connection.commit()
    print("Assignment removed from module successfully.")

def delete_test_from_assignment (connection, assignment_id, test_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM AssignmentTests WHERE assignment_id = ? AND test_id = ?
    """, (assignment_id, test_id))
    connection.commit()
    print("Assignment removed from module successfully.")


# Helper Functions

def file_to_blob(file_path):
    """
    Reads a file from the given file path and converts it to a binary BLOB.
    
    Parameters:
        file_path (str): Path to the file to be converted to BLOB.

    Returns:
        bytes: The binary content of the file.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        

def add_file_to_submission(connection, submission_id, file_path):
    """
    Converts a file to BLOB and adds it to the specified submission in the database.

    Parameters:
        db_path (str): Path to the SQLite database file.
        submission_id (int): The submission ID where the file should be added.
        file_path (str): The path to the file to be added to the submission.
    """
    blob_data = file_to_blob(file_path)
    if blob_data is None:
        print("No valid file data to add.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT submission_id FROM Submissions WHERE submission_id = ?", (submission_id,))
        if cursor.fetchone() is None:
            print(f"Error: No submission found with ID {submission_id}")
            return

        # update submission content
        cursor.execute("""
            UPDATE Submissions
            SET submission_content = ?
            WHERE submission_id = ?;
        """, (blob_data, submission_id))
        
        connection.commit()
        print(f"File successfully added to submission {submission_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

def add_file_to_test(connection, test_id, file_path):
    """
    Converts a file to BLOB and adds it to the specified submission in the database.

    Parameters:
        db_path (str): Path to the SQLite database file.
        submission_id (int): The submission ID where the file should be added.
        file_path (str): The path to the file to be added to the submission.
    """
    blob_data = file_to_blob(file_path)
    if blob_data is None:
        print("No valid file data to add.")
        return

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT test_id FROM Tests WHERE test_id = ?", (test_id,))
        if cursor.fetchone() is None:
            print(f"Error: No test found with ID {test_id}")
            return

        # update submission content
        cursor.execute("""
            UPDATE Tests
            SET test_blob = ?
            WHERE test_id = ?;
        """, (blob_data, test_id))
        
        connection.commit()
        print(f"File successfully added to test {test_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()


def save_blob_to_file(file_path, blob):
    try:
        if blob:
            with open(file_path, 'wb') as file:
                file.write(blob[0])
            print("File has been saved successfully.")
            return file_path
        else:
            print("No file found for the given submission ID.")
    except Exception as e:
        print(f"Error: {e}")

def save_submission_file(connection, file_path, submission_id):
    """Saves the test file from the database into file_path."""
    blob = get_submission_blob(connection, submission_id)
    save_blob_to_file(connection, file_path, blob)
        
def save_test_file(connection, file_path, assignment_id):
    blob = get_test_blob(connection, assignment_id)
    save_blob_to_file(connection, file_path, blob)