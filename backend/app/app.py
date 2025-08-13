import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Add the root directory of the project to the Python path
sys.path.append(str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS
from models.models import db, Institution, Department, Subject, Module, Teacher, Student, Assignment, Test
from routes import api_blueprint

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
    app.register_blueprint(api_blueprint, url_prefix="/api")
    
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
    """Create sample data for development/testing"""
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
        
        # Create a sample teacher
        teacher = Teacher(
            first_name="Dr. John",
            surname="Smith",
            email="john.smith@sampleuni.ac.uk",
            employee_id="T001",
            institution_id=institution.institution_id,
            department_id=department.department_id
        )
        db.session.add(teacher)
        db.session.flush()
        
        # Create a sample module
        module = Module(
            name="Introduction to Python Programming",
            code="COMP101",
            description="Basic Python programming concepts",
            subject_id=subject.subject_id,
            semester="Fall 2024",
            year=2024,
            start_date=datetime(2024, 9, 1),
            end_date=datetime(2024, 12, 15),
            max_students=50
        )
        db.session.add(module)
        db.session.flush()
        
        # Create a sample test
        test = Test(
            name="Basic Addition Test",
            description="Test student's ability to add two numbers",
            input_data="2 3",
            expected_output="5",
            timeout_seconds=5,
            created_by=teacher.teacher_id
        )
        db.session.add(test)
        db.session.flush()
        
        # Create a sample assignment
        assignment = Assignment(
            title="Python Basics: Add Two Numbers",
            description="Write a Python function that adds two numbers",
            instructions="Create a function called 'add_numbers(a, b)' that returns the sum of a and b",
            test_id=test.test_id,
            rubric="Function works correctly, proper syntax, good variable names",
            max_score=100.0,
            pass_threshold=70.0,
            due_date=datetime(2024, 9, 15),
            max_attempts=3,
            created_by=teacher.teacher_id
        )
        db.session.add(assignment)
        db.session.flush()
        
        # Link teacher to module
        module.teachers.append(teacher)
        
        # Link assignment to module
        module.assignments.append(assignment)
        
        db.session.commit()
        print("✅ Sample data created successfully!")
        print(f"   - Institution: {institution.name}")
        print(f"   - Department: {department.name}")
        print(f"   - Subject: {subject.name}")
        print(f"   - Module: {module.name}")
        print(f"   - Teacher: {teacher.first_name} {teacher.surname}")
        print(f"   - Assignment: {assignment.title}")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating sample data: {e}")

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True, reloader_type='stat')
