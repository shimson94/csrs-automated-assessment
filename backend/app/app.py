import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Add the root directory of the project to the Python path
sys.path.append(str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS
from models.models import (
    db, Institution, Department, Subject, Module, Teacher, Student, Assignment, Test,
    InstitutionType, SubjectType, TeacherRole, AcademicYear, UKModuleGrade, EnrollmentStatus,
    teacher_modules, student_enrollments
)
from blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db", "automarker.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Initialise extensions
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    @app.route("/", methods=["GET"])
    def root():
        return "Flask API running with SQLAlchemy models!"
    
    # Initialise database and sample data
    with app.app_context():
        # Ensure db directory exists
        os.makedirs(os.path.join(basedir, "db"), exist_ok=True)
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Add sample data if database is empty
        if Institution.query.count() == 0:
            create_sample_data()
    
    return app

def create_sample_data():
    """Create comprehensive sample data for development/testing"""
    try:
        # Create institution
        institution = Institution(
            name="Sample University",
            code="SU",
            country="UK",
            contact_email="admin@sampleuni.ac.uk"
        )
        db.session.add(institution)
        db.session.flush()
        
        # Create department
        department = Department(
            name="Computer Science",
            code="CS",
            description="Department of Computer Science",
            institution_id=institution.institution_id,
            contact_email="cs@sampleuni.ac.uk"
        )
        db.session.add(department)
        db.session.flush()
        
        # Create subject
        subject = Subject(
            name="Programming",
            code="COMP",
            description="Programming and Software Development",
            department_id=department.department_id,
            has_automated_marking=True
        )
        db.session.add(subject)
        db.session.flush()
        
        # Create sample teacher
        teacher = Teacher(
            first_name="Dr. John",
            surname="Smith",
            email="john.smith@sampleuni.ac.uk",
            employee_id="T001",
            institution_id=institution.institution_id,
            department_id=department.department_id,
            phone="555-0100",
            office_location="Room 301, CS Building",
            is_active=True
        )
        db.session.add(teacher)
        db.session.flush()
        
        # Create sample students with UK academic structure
        students = []
        student_data = [
            {"first_name": "Alice", "surname": "Johnson", "email": "alice.johnson@student.sampleuni.ac.uk", 
             "student_number": "STU001", "academic_year": AcademicYear.YEAR_2},
            {"first_name": "Bob", "surname": "Williams", "email": "bob.williams@student.sampleuni.ac.uk", 
             "student_number": "STU002", "academic_year": AcademicYear.YEAR_1},
            {"first_name": "Carol", "surname": "Davis", "email": "carol.davis@student.sampleuni.ac.uk", 
             "student_number": "STU003", "academic_year": AcademicYear.YEAR_3},
            {"first_name": "David", "surname": "Miller", "email": "david.miller@student.sampleuni.ac.uk", 
             "student_number": "STU004", "academic_year": AcademicYear.YEAR_1},
            {"first_name": "Emma", "surname": "Wilson", "email": "emma.wilson@student.sampleuni.ac.uk", 
             "student_number": "STU005", "academic_year": AcademicYear.FOUNDATION}
        ]
        
        for i, student_info in enumerate(student_data):
            student = Student(
                first_name=student_info["first_name"],
                surname=student_info["surname"],
                email=student_info["email"],
                student_number=student_info["student_number"],
                institution_id=institution.institution_id,
                phone=f"555-010{i+1}",
                enrollment_year=2024,
                current_academic_year=student_info["academic_year"],
                is_active=True
            )
            db.session.add(student)
            students.append(student)
        
        db.session.flush()
        
        # Create sample module
        module = Module(
            name="Introduction to Python Programming",
            code="COMP101",
            description="Basic Python programming concepts and fundamentals",
            subject_id=subject.subject_id,
            semester="Fall 2024",
            year=2024,
            start_date=datetime(2024, 9, 1),
            end_date=datetime(2024, 12, 15),
            max_students=50,
            is_active=True
        )
        db.session.add(module)
        db.session.flush()
        
        # Create sample tests
        tests = []
        test_data = [
            {
                "name": "Basic Addition Test",
                "description": "Test student's ability to add two numbers",
                "input_data": "2 3",
                "expected_output": "5",
                "timeout_seconds": 5
            },
            {
                "name": "String Concatenation Test",
                "description": "Test string manipulation skills",
                "input_data": "Hello World",
                "expected_output": "Hello World",
                "timeout_seconds": 3
            },
            {
                "name": "Loop Implementation Test",
                "description": "Test basic loop structures",
                "input_data": "5",
                "expected_output": "0\n1\n2\n3\n4",
                "timeout_seconds": 10
            }
        ]
        
        for test_info in test_data:
            test = Test(
                name=test_info["name"],
                description=test_info["description"],
                input_data=test_info["input_data"],
                expected_output=test_info["expected_output"],
                timeout_seconds=test_info["timeout_seconds"],
                created_by=teacher.teacher_id
            )
            db.session.add(test)
            tests.append(test)
        
        db.session.flush()
        
        # Create sample assignments
        assignments = []
        assignment_data = [
            {
                "title": "Python Basics: Add Two Numbers",
                "description": "Write a Python function that adds two numbers and prints the result",
                "instructions": "Create a function called 'add_numbers(a, b)' that returns the sum of a and b. Then call the function with inputs 2 and 3.",
                "test_id": tests[0].test_id,
                "max_score": 100.0,
                "pass_threshold": 70.0,
                "due_date": datetime(2024, 9, 15),
                "max_attempts": 3
            },
            {
                "title": "String Operations",
                "description": "Basic string manipulation exercises",
                "instructions": "Write a program that takes a string input and prints it exactly as received.",
                "test_id": tests[1].test_id,
                "max_score": 100.0,
                "pass_threshold": 75.0,
                "due_date": datetime(2024, 9, 22),
                "max_attempts": 2
            },
            {
                "title": "For Loops Practice",
                "description": "Implement basic for loop structures",
                "instructions": "Write a program that prints numbers from 0 to n-1, where n is the input.",
                "test_id": tests[2].test_id,
                "max_score": 100.0,
                "pass_threshold": 80.0,
                "due_date": datetime(2024, 9, 29),
                "max_attempts": 3
            }
        ]
        
        for assignment_info in assignment_data:
            assignment = Assignment(
                title=assignment_info["title"],
                description=assignment_info["description"],
                instructions=assignment_info["instructions"],
                test_id=assignment_info["test_id"],
                rubric="Code functionality (70%), Code style (20%), Documentation (10%)",
                max_score=assignment_info["max_score"],
                pass_threshold=assignment_info["pass_threshold"],
                due_date=assignment_info["due_date"],
                max_attempts=assignment_info["max_attempts"],
                created_by=teacher.teacher_id,
                is_active=True
            )
            db.session.add(assignment)
            assignments.append(assignment)
        
        db.session.flush()
        
        # Create UK academic structure enrollments with realistic academic progress
        from sqlalchemy import text
        
        # Add students to module with UK academic year context and realistic coursework marks
        enrollment_data = [
            # Alice (Year 2 student) - performing well
            {"student": students[0], "academic_year": AcademicYear.YEAR_2, "coursework_avg": 68.5, "status": EnrollmentStatus.ACTIVE},
            # Bob (Year 1 student) - average performance
            {"student": students[1], "academic_year": AcademicYear.YEAR_1, "coursework_avg": 58.2, "status": EnrollmentStatus.ACTIVE},
            # Carol (Year 3 student) - excellent performance
            {"student": students[2], "academic_year": AcademicYear.YEAR_3, "coursework_avg": 74.8, "status": EnrollmentStatus.ACTIVE},
            # David (Year 1 student) - struggling
            {"student": students[3], "academic_year": AcademicYear.YEAR_1, "coursework_avg": 42.1, "status": EnrollmentStatus.ACTIVE},
            # Emma (Foundation student) - improving
            {"student": students[4], "academic_year": AcademicYear.FOUNDATION, "coursework_avg": 55.7, "status": EnrollmentStatus.ACTIVE}
        ]
        
        # Insert enrollment data with UK academic context
        for enrollment in enrollment_data:
            db.session.execute(text("""
                INSERT INTO student_enrollments 
                (student_id, module_id, academic_year, enrollment_date, final_coursework_average, 
                 coursework_weight, exam_weight, status)
                VALUES (:student_id, :module_id, :academic_year, :enrollment_date, 
                        :coursework_avg, :coursework_weight, :exam_weight, :status)
            """), {
                'student_id': enrollment["student"].student_id,
                'module_id': module.module_id,
                'academic_year': enrollment["academic_year"].value,
                'enrollment_date': datetime.now(timezone.utc),
                'coursework_avg': enrollment["coursework_avg"],
                'coursework_weight': 100.0,  # Pure coursework module
                'exam_weight': 0.0,
                'status': enrollment["status"].value
            })
        
        # Link teacher to module with instructor role
        db.session.execute(text("""
            INSERT INTO teacher_modules 
            (teacher_id, module_id, role, assigned_date, is_active)
            VALUES (:teacher_id, :module_id, :role, :assigned_date, :is_active)
        """), {
            'teacher_id': teacher.teacher_id,
            'module_id': module.module_id,
            'role': TeacherRole.INSTRUCTOR.value,
            'assigned_date': datetime.now(timezone.utc),
            'is_active': True
        })
        
        # Update student academic averages based on their enrollments
        for student in students:
            student.update_academic_averages()
        
        db.session.flush()
        
        # Link assignments to module
        for assignment in assignments:
            module.assignments.append(assignment)
        
        db.session.flush()
        
        # Create sample submissions
        from models.models import Submission, SubmissionStatus, ProgrammingLanguage, SubmissionFileType
        
        sample_submissions = [
            {
                "student": students[0],  # Alice
                "assignment": assignments[0],  # Basic Addition Test
                "file_name": "addition.py",
                "file_type": SubmissionFileType.PYTHON_FILE,
                "file_content": "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(2, 3)\nprint(result)",
                "status": SubmissionStatus.SUBMITTED
            },
            {
                "student": students[1],  # Bob
                "assignment": assignments[0],  # Basic Addition Test
                "file_name": "my_solution.py", 
                "file_type": SubmissionFileType.PYTHON_FILE,
                "file_content": "# My addition program\na = int(input())\nb = int(input())\nprint(a + b)",
                "status": SubmissionStatus.GRADED
            },
            {
                "student": students[2],  # Carol
                "assignment": assignments[1],  # String Operations
                "file_name": "strings.py",
                "file_type": SubmissionFileType.PYTHON_FILE, 
                "file_content": "user_input = input()\nprint(user_input)",
                "status": SubmissionStatus.SUBMITTED
            },
            {
                "student": students[0],  # Alice
                "assignment": assignments[2],  # For Loops Practice
                "file_name": "loops.py",
                "file_type": SubmissionFileType.PYTHON_FILE,
                "file_content": "n = int(input())\nfor i in range(n):\n    print(i)",
                "status": SubmissionStatus.PROCESSING
            },
            {
                "student": students[3],  # David
                "assignment": assignments[0],  # Basic Addition Test
                "file_name": "test.py",
                "file_type": SubmissionFileType.PYTHON_FILE,
                "file_content": "print(2 + 3)  # Simple solution",
                "status": SubmissionStatus.SUBMITTED
            }
        ]
        
        submissions = []
        for i, sub_data in enumerate(sample_submissions):
            # Convert file content to bytes for BLOB storage
            file_content_bytes = sub_data["file_content"].encode('utf-8')
            
            submission = Submission(
                student_id=sub_data["student"].student_id,
                assignment_id=sub_data["assignment"].assignment_id,
                file_name=sub_data["file_name"],
                file_type=sub_data["file_type"],
                submission_file=file_content_bytes,
                file_size=len(file_content_bytes),
                status=sub_data["status"],
                ip_address=f"192.168.1.{110 + i}",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                submission_date=datetime.now(timezone.utc)
            )
            db.session.add(submission)
            submissions.append(submission)
        
        db.session.flush()
        
        # Create sample activity logs
        from models.models import ActivityLog, ActivityAction, UserType
        
        activity_logs = [
            ActivityLog(
                user_id=teacher.teacher_id,
                user_type=UserType.TEACHER,
                action=ActivityAction.CREATE_MODULE,
                details=f"Created module: {module.name}",
                ip_address="192.168.1.100"
            ),
            ActivityLog(
                user_id=students[0].student_id,
                user_type=UserType.STUDENT, 
                action=ActivityAction.VIEW_ASSIGNMENT,
                details=f"Viewed assignment: {assignments[0].title}",
                ip_address="192.168.1.101"
            )
        ]
        
        for log in activity_logs:
            db.session.add(log)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print(f"   - Institution: {institution.name}")
        print(f"   - Department: {department.name}")
        print(f"   - Subject: {subject.name}")
        print(f"   - Module: {module.name}")
        print(f"   - Teacher: {teacher.first_name} {teacher.surname} (ID: {teacher.teacher_id})")
        print(f"   - Students: {len(students)} students created (IDs: {[s.student_id for s in students]})")
        print(f"   - Tests: {len(tests)} tests created")
        print(f"   - Assignments: {len(assignments)} assignments created")
        print(f"   - Submissions: {len(submissions)} submissions created")
        print(f"   - Student-Module links: {len(students)} created")
        print(f"   - Activity Logs: {len(activity_logs)} logs created")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating sample data: {e}")
        raise

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True, reloader_type='stat')
