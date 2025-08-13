from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from enum import Enum

db = SQLAlchemy()

# Enums for better data integrity
class InstitutionType(Enum):
    UNIVERSITY = "university"
    COLLEGE = "college"
    SCHOOL = "school"
    TRAINING_CENTER = "training_center"

class SubjectType(Enum):
    PROGRAMMING = "programming"
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    ENGINEERING = "engineering"
    BUSINESS = "business"
    ARTS = "arts"

class AssignmentType(Enum):
    CODING = "coding"
    THEORY = "theory"
    PROJECT = "project"
    EXAM = "exam"

class TeacherRole(Enum):
    INSTRUCTOR = "instructor"
    ASSISTANT = "assistant"
    COORDINATOR = "coordinator"

class SubmissionStatus(Enum):
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    GRADED = "graded"
    ERROR = "error"
    LATE = "late"

class EnrollmentStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"

class UserType(Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"

# Association tables for many-to-many relationships with enhanced metadata
teacher_modules = db.Table('teacher_modules',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.teacher_id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('role', db.Enum(TeacherRole), default=TeacherRole.INSTRUCTOR),
    db.Column('assigned_date', db.DateTime, default=datetime.utc),
    db.Column('is_active', db.Boolean, default=True)
)

student_enrollments = db.Table('student_enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('students.student_id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=datetime.utc),
    db.Column('completion_date', db.DateTime),
    db.Column('final_grade', db.Float),
    db.Column('status', db.Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
)

module_assignments = db.Table('module_assignments',
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.assignment_id'), primary_key=True),
    db.Column('weight', db.Float, default=1.0),  # Assignment weight for grading
    db.Column('visible', db.Boolean, default=True),
    db.Column('assigned_date', db.DateTime, default=datetime.utc)
)

class Institution(db.Model):
    __tablename__ = 'institutions'
    
    institution_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)  # e.g., "UoB", "MIT", "UCL"
    type = db.Column(db.Enum(InstitutionType), nullable=False, default=InstitutionType.UNIVERSITY)
    country = db.Column(db.String(100), nullable=False, default='UK')
    city = db.Column(db.String(100))
    website = db.Column(db.String(200))
    contact_email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    departments = db.relationship('Department', back_populates='institution', cascade='all, delete-orphan')
    teachers = db.relationship('Teacher', back_populates='institution')
    students = db.relationship('Student', back_populates='institution')
    
    def to_dict(self):
        return {
            'institution_id': self.institution_id,
            'name': self.name,
            'code': self.code,
            'type': self.type.value,
            'country': self.country,
            'city': self.city,
            'contact_email': self.contact_email,
            'is_active': self.is_active
        }

class Department(db.Model):
    __tablename__ = 'departments'
    
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False)  # e.g., "CS", "MATH", "ENG"
    description = db.Column(db.Text)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False)
    head_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    contact_email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    office_location = db.Column(db.String(100))
    budget = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    institution = db.relationship('Institution', back_populates='departments')
    subjects = db.relationship('Subject', back_populates='department', cascade='all, delete-orphan')
    head_teacher = db.relationship('Teacher', foreign_keys=[head_teacher_id])
    
    def to_dict(self):
        return {
            'department_id': self.department_id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'institution_id': self.institution_id,
            'contact_email': self.contact_email,
            'is_active': self.is_active
        }

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), nullable=False)  # e.g., "COMP", "MATH", "PHYS"
    description = db.Column(db.Text)
    type = db.Column(db.Enum(SubjectType), nullable=False, default=SubjectType.PROGRAMMING)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    has_automated_marking = db.Column(db.Boolean, default=True)  # Only programming subjects need this
    credit_hours = db.Column(db.Integer, default=3)
    prerequisite_subjects = db.Column(db.Text)  # JSON list of prerequisite subject IDs
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    department = db.relationship('Department', back_populates='subjects')
    modules = db.relationship('Module', back_populates='subject', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'subject_id': self.subject_id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'type': self.type.value,
            'has_automated_marking': self.has_automated_marking,
            'credit_hours': self.credit_hours,
            'department_id': self.department_id,
            'is_active': self.is_active
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    teacher_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # CRITICAL: For login/contact
    password_hash = db.Column(db.String(255))  # CRITICAL: For authentication
    employee_id = db.Column(db.String(50), unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    phone = db.Column(db.String(20))
    office_location = db.Column(db.String(100))
    hire_date = db.Column(db.DateTime, default=datetime.utc)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    institution = db.relationship('Institution', back_populates='teachers')
    modules = db.relationship('Module', secondary=teacher_modules, back_populates='teachers')
    
    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'first_name': self.first_name,
            'surname': self.surname,
            'email': self.email,
            'employee_id': self.employee_id,
            'institution_id': self.institution_id,
            'department_id': self.department_id,
            'phone': self.phone,
            'office_location': self.office_location,
            'is_active': self.is_active
        }

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # CRITICAL: For login/contact
    password_hash = db.Column(db.String(255))  # CRITICAL: For authentication
    student_number = db.Column(db.String(50), nullable=False, unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    enrollment_year = db.Column(db.Integer)
    graduation_date = db.Column(db.Date)
    gpa = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    institution = db.relationship('Institution', back_populates='students')
    modules = db.relationship('Module', secondary=student_enrollments, back_populates='students')
    submissions = db.relationship('Submission', back_populates='student')
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'first_name': self.first_name,
            'surname': self.surname,
            'email': self.email,
            'student_number': self.student_number,
            'institution_id': self.institution_id,
            'phone': self.phone,
            'enrollment_year': self.enrollment_year,
            'gpa': self.gpa,
            'is_active': self.is_active
        }
class Module(db.Model):
    __tablename__ = 'modules'
    
    module_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), nullable=False)  # e.g., "COMP101", "MATH201"
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)  # e.g., "Fall 2024", "Spring 2025"
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    max_students = db.Column(db.Integer, default=100)
    credits = db.Column(db.Integer, default=3)
    location = db.Column(db.String(100))  # Classroom/venue
    schedule = db.Column(db.Text)  # JSON: days/times
    prerequisites = db.Column(db.Text)  # JSON list of prerequisite module IDs
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    subject = db.relationship('Subject', back_populates='modules')
    teachers = db.relationship('Teacher', secondary=teacher_modules, back_populates='modules')
    students = db.relationship('Student', secondary=student_enrollments, back_populates='modules')
    assignments = db.relationship('Assignment', secondary=module_assignments, back_populates='modules')
    
    def to_dict(self):
        return {
            'module_id': self.module_id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'subject_id': self.subject_id,
            'semester': self.semester,
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'max_students': self.max_students,
            'credits': self.credits,
            'location': self.location,
            'is_active': self.is_active
        }

class Test(db.Model):
    __tablename__ = 'tests'
    
    test_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    test_file = db.Column(db.LargeBinary)  # BLOB for test files
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    timeout_seconds = db.Column(db.Integer, default=5)
    programming_language = db.Column(db.String(50), default='python')
    test_type = db.Column(db.String(50), default='unit_test')  # unit_test, integration, performance
    version = db.Column(db.String(20), default="1.0")
    created_by = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    assignments = db.relationship('Assignment', back_populates='test')
    creator = db.relationship('Teacher', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'test_id': self.test_id,
            'name': self.name,
            'description': self.description,
            'input_data': self.input_data,
            'expected_output': self.expected_output,
            'timeout_seconds': self.timeout_seconds,
            'programming_language': self.programming_language,
            'version': self.version,
            'is_active': self.is_active
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # CRITICAL: Assignment title
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text)  # CRITICAL: Detailed instructions
    test_id = db.Column(db.Integer, db.ForeignKey('tests.test_id'))
    rubric = db.Column(db.Text, nullable=False)
    max_score = db.Column(db.Float, default=100.0)  # CRITICAL: Maximum possible score
    pass_threshold = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    late_penalty = db.Column(db.Float, default=0.1)  # % penalty per day late
    max_attempts = db.Column(db.Integer, default=3)  # CRITICAL: How many tries allowed
    weight = db.Column(db.Float, default=1.0)  # Weight in final grade
    type = db.Column(db.Enum(AssignmentType), nullable=False, default=AssignmentType.CODING)
    is_published = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    test = db.relationship('Test', back_populates='assignments')
    modules = db.relationship('Module', secondary=module_assignments, back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment')
    creator = db.relationship('Teacher', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'title': self.title,
            'description': self.description,
            'instructions': self.instructions,
            'test_id': self.test_id,
            'rubric': self.rubric,
            'max_score': self.max_score,
            'pass_threshold': self.pass_threshold,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'late_penalty': self.late_penalty,
            'max_attempts': self.max_attempts,
            'weight': self.weight,
            'type': self.type.value,
            'is_published': self.is_published,
            'is_active': self.is_active
        }

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    submission_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utc)
    submission_file = db.Column(db.LargeBinary)  # BLOB for submission files
    file_name = db.Column(db.String(255))  # CRITICAL: Original filename
    file_size = db.Column(db.Integer)  # CRITICAL: File size in bytes
    attempt_number = db.Column(db.Integer, default=1)  # CRITICAL: Which attempt this is
    is_late = db.Column(db.Boolean, default=False)  # CRITICAL: Submitted after deadline
    days_late = db.Column(db.Integer, default=0)  # How many days late
    ip_address = db.Column(db.String(45))  # Where submitted from
    user_agent = db.Column(db.Text)  # Browser info
    status = db.Column(db.Enum(SubmissionStatus), default=SubmissionStatus.SUBMITTED)  # Processing status
    result_id = db.Column(db.Integer, db.ForeignKey('results.result_id'))
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    student = db.relationship('Student', back_populates='submissions')
    assignment = db.relationship('Assignment', back_populates='submissions')
    result = db.relationship('Result', back_populates='submission', uselist=False)
    
    def to_dict(self):
        return {
            'submission_id': self.submission_id,
            'student_id': self.student_id,
            'assignment_id': self.assignment_id,
            'submission_date': self.submission_date.isoformat(),
            'file_name': self.file_name,
            'file_size': self.file_size,
            'attempt_number': self.attempt_number,
            'is_late': self.is_late,
            'days_late': self.days_late,
            'status': self.status.value,
            'result_id': self.result_id
        }

class Result(db.Model):
    __tablename__ = 'results'
    
    result_id = db.Column(db.Integer, primary_key=True)
    actual_output = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Float, nullable=False)  # Out of max_score
    percentage = db.Column(db.Float, nullable=False)  # CRITICAL: 0-100 percentage score
    execution_time = db.Column(db.Float)  # CRITICAL: How long tests took to run (seconds)
    memory_usage = db.Column(db.Integer)  # Memory usage during execution (KB)
    test_cases_passed = db.Column(db.Integer, default=0)  # CRITICAL: Number of tests passed
    test_cases_total = db.Column(db.Integer, default=0)  # CRITICAL: Total number of tests
    error_message = db.Column(db.Text)  # Runtime errors
    feedback = db.Column(db.Text)  # Detailed feedback
    feedback_summary = db.Column(db.Text)  # AI-generated summary
    graded_at = db.Column(db.DateTime, default=datetime.utc)
    graded_by = db.Column(db.String(50), default='AUTOMARKER')  # AUTOMARKER vs teacher_id
    created_at = db.Column(db.DateTime, default=datetime.utc)
    updated_at = db.Column(db.DateTime, default=datetime.utc, onupdate=datetime.utc)
    
    # Relationships
    submission = db.relationship('Submission', back_populates='result')
    
    def to_dict(self):
        return {
            'result_id': self.result_id,
            'actual_output': self.actual_output,
            'expected_output': self.expected_output,
            'passed': self.passed,
            'score': self.score,
            'percentage': self.percentage,
            'execution_time': self.execution_time,
            'memory_usage': self.memory_usage,
            'test_cases_passed': self.test_cases_passed,
            'test_cases_total': self.test_cases_total,
            'error_message': self.error_message,
            'feedback': self.feedback,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None,
            'graded_by': self.graded_by
        }

# NICE TO HAVE: Activity Logging and Session Management
class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    session_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)  # TEACHER, STUDENT, ADMIN
    created_at = db.Column(db.DateTime, default=datetime.utc)
    expires_at = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=datetime.utc)
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'user_type': self.user_type.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_active': self.is_active,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # LOGIN, SUBMIT, GRADE, CREATE_ASSIGNMENT, etc.
    resource_type = db.Column(db.String(50))  # assignment, submission, test, etc.
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON details about the action
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utc)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'user_type': self.user_type.value,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success
        }