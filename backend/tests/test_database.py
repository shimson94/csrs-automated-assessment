import unittest
import sqlite3

from src import database

DB_SCHEMA_FILE = "src/db/setup.sql"

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Use in-memory database for testing
        self.connection = sqlite3.connect(":memory:")
        with open(DB_SCHEMA_FILE, "r") as f:
            self.connection.executescript(f.read())
               
    def tearDown(self):
        self.connection.close()

    # Teachers Table
    def test_teacher_create(self):
        """Test inserting and retrieving a teacher."""
        cursor = self.connection.cursor()
        database.create_teacher(self.connection, 1, "Testname", "Testsurname")

        cursor.execute("""SELECT * FROM Teachers""")
        teachers = cursor.fetchall()
        self.assertEqual(teachers[0][0], 1)
        self.assertEqual(teachers[0][1], "Testname")
        self.assertEqual(teachers[0][2], "Testsurname")

    def test_get_teachers(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO Teachers (first_name, surname) VALUES (?, ?)
        """, ("John", "Doe"))
        self.connection.commit()

        teachers = database.get_teachers(self.connection)
        self.assertEqual(teachers[0][1], "John")
        self.assertEqual(teachers[0][2], "Doe")

    # Students Table
    def test_student_add(self):
        """Test inserting and retrieving a teacher."""
        cursor = self.connection.cursor()
        database.create_student(self.connection, 1, "John", "Doe")

        cursor.execute("""SELECT * FROM Students""")
        students = cursor.fetchall()
        self.assertEqual(students[0][0], 1)
        self.assertEqual(students[0][1], "John")
        self.assertEqual(students[0][2], "Doe")

    # Modules Table
    def test_module_create(self):
        """Test inserting and retrieving a teacher."""
        cursor = self.connection.cursor()
        database.create_module(self.connection, 1, "Java Module")

        cursor.execute("""SELECT * FROM Modules""")
        modules = cursor.fetchall()
        self.assertEqual(modules[0][0], 1)
        self.assertEqual(modules[0][1], "Java Module")

    # Assignments Table
    def test_create_assignment(self):
        """Test inserting and retrieving an assignment."""
        cursor = self.connection.cursor()
        database.create_Assignment(self.connection, 1,
        "Assignment description", "Test Rubric", 100, "2024-12-15")

        cursor.execute("""SELECT * FROM Assignments""")
        assignments = cursor.fetchall()
        self.assertEqual(assignments[0][1], "Assignment description")
        self.assertEqual(assignments[0][2], "Test Rubric")
        self.assertEqual(assignments[0][3], 100)
        self.assertEqual(assignments[0][4], "2024-12-15")

    def test_get_assignments(self):
        cursor = self.connection.cursor()
        database.create_Assignment(self.connection, 1, 
        "Assignment description", "Test Rubric", 100, "2024-12-15")

    
        assignments = database.get_assignments(self.connection)
        self.assertEqual(assignments[0][1], "Assignment description")
        self.assertEqual(assignments[0][2], "Test Rubric")
        self.assertEqual(assignments[0][3], 100)
        self.assertEqual(assignments[0][4], "2024-12-15")

    def test_update_assignment(self):
        cursor = self.connection.cursor()
        database.create_Assignment(self.connection, 1, 
            "Assignment description", "Rubric", 100, "2024-12-15")
    
        database.update_assignment(self.connection, 1, 
            "Updated description", "Updated Rubric", 90, "2024-12-20")
    
        cursor.execute("""SELECT * FROM Assignments WHERE assignment_id = ?""", (1,))
        assignment = cursor.fetchone()
        self.assertEqual(assignment[1], "Updated description")
        self.assertEqual(assignment[2], "Updated Rubric")
        self.assertEqual(assignment[3], 90)
        self.assertEqual(assignment[4], "2024-12-20")

    def test_delete_assignment(self):
        cursor = self.connection.cursor()
        database.create_module(self.connection, 2, "Test Module")
        database.create_Assignment(self.connection, 1, 
            "Assignment description", "Rubric", 100, "2024-12-15")
    
        database.delete_assignment(self.connection, 1)
    
        cursor.execute("""SELECT * FROM Assignments WHERE assignment_id = ?""", (1,))
        assignment = cursor.fetchone()
        self.assertIsNone(assignment)

    # Results Table
    def test_create_result(self):
        cursor = self.connection.cursor()
        database.create_result(self.connection, 1, "Actual output", "Expected output",
                               True, 100)

        
        cursor.execute("""SELECT * FROM Results WHERE result_id = 1""")
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "Actual output")
        self.assertEqual(result[2], "Expected output")
        self.assertEqual(result[3], True)
        self.assertEqual(result[4], 100)

    def test_get_results(self):
        cursor = self.connection.cursor()
        database.create_result(self.connection, 1, "Actual output", "Expected output", True, 100)
        
        result = database.get_results(self.connection)
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0][1], "Actual output")
        self.assertEqual(result[0][2], "Expected output")
        self.assertEqual(result[0][3], True)
        self.assertEqual(result[0][4], 100)

    def test_update_result(self):
        cursor = self.connection.cursor()
        database.create_result(self.connection, 1, "Actual output", "Expected output", True, 100)
        
        database.update_result(self.connection, 1, "Updated output", "Updated expected", False, 50)
        
        cursor.execute("""SELECT * FROM Results WHERE result_id = 1""")
        result = cursor.fetchone()
        
        self.assertEqual(result[1], "Updated output")
        self.assertEqual(result[2], "Updated expected")
        self.assertEqual(result[3], False)
        self.assertEqual(result[4], 50)

    def test_delete_result(self):
        cursor = self.connection.cursor()
        database.create_result(self.connection, 1, "Actual output", "Expected output", True, 100)
        
        database.delete_result(self.connection, 1)
        
        cursor.execute("""SELECT * FROM Results WHERE result_id = 1""")
        result = cursor.fetchone()
        
        self.assertIsNone(result) 

    # Enroll Student
    def test_enroll_student(self):
        database.create_student(self.connection, 2720941, "student1", "studentsurname")
        database.create_module(self.connection, 1334, "Java Module")
        database.enroll_student_in_module(self.connection, 2720941, 1334)

        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM StudentEnrollments""")
        result = cursor.fetchall()
        self.assertEqual(result[0][0], 2720941)
        self.assertEqual(result[0][1], 1334)

    # Add Teacher to Module
    def add_teacher_to_module(self):
        database.create_teacher(self.connection, 2, "teacher1", "teachersurname")
        database.create_module(self.connection, 1222, "Java Module 2")
        database.add_teacher_to_module(self.connection, 2, 1222)

        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM TeacherModules""")
        result = cursor.fetchall()
        self.assertEqual(result[0][0], 2)
        self.assertEqual(result[0][1], 1222)


if __name__ == "__main__":
    unittest.main()