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
    
class TestType(Enum):
    UNIT = "unit_test"           # Test individual functions
    FUNCTIONAL = "functional"    # Test complete program behavior  
    PERFORMANCE = "performance"  # Test speed/efficiency
    INTEGRATION = "integration"  # Test multiple components together
    SYNTAX = "syntax"           # Check code compiles/runs
    MEMORY = "memory"           # Test memory usage
    SECURITY = "security"       # Test for security vulnerabilities

class ProgrammingLanguage(Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"

class GradeStatus(Enum):
    NOT_GRADED = "not_graded"
    GRADING = "grading"
    GRADED = "graded"
    NEEDS_REVIEW = "needs_review"
    MANUAL_REVIEW = "manual_review"

class SubmissionFileType(Enum):
    PYTHON_FILE = ".py"
    JAVA_FILE = ".java"
    JAVASCRIPT_FILE = ".js"
    CPP_FILE = ".cpp"
    C_FILE = ".c"
    TEXT_FILE = ".txt"
    ZIP_FILE = ".zip"
    PDF_FILE = ".pdf"

class ActivityAction(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    SUBMIT_ASSIGNMENT = "submit_assignment"
    VIEW_ASSIGNMENT = "view_assignment"
    CREATE_ASSIGNMENT = "create_assignment"
    EDIT_ASSIGNMENT = "edit_assignment"
    DELETE_ASSIGNMENT = "delete_assignment"
    GRADE_SUBMISSION = "grade_submission"
    VIEW_RESULTS = "view_results"
    ENROLL_STUDENT = "enroll_student"
    DISENROLL_STUDENT = "disenroll_student"
    CREATE_MODULE = "create_module"
    DELETE_MODULE = "delete_module"
    UPLOAD_FILE = "upload_file"
    DELETE_UPLOADED_FILE = "delete_uploaded_file"
    DOWNLOAD_FILE = "download_file"

# Association tables for many-to-many relationships with enhanced metadata
teacher_modules = db.Table('teacher_modules',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.teacher_id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('role', db.Enum(TeacherRole), default=TeacherRole.INSTRUCTOR),
    db.Column('assigned_date', db.DateTime, default=lambda: datetime.now(timezone.utc)),
    db.Column('is_active', db.Boolean, default=True)
)

student_enrollments = db.Table('student_enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('students.student_id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=lambda: datetime.now(timezone.utc)),
    db.Column('completion_date', db.DateTime),
    db.Column('final_grade', db.Float),
    db.Column('status', db.Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
)

module_assignments = db.Table('module_assignments',
    db.Column('module_id', db.Integer, db.ForeignKey('modules.module_id'), primary_key=True),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.assignment_id'), primary_key=True),
    db.Column('weight', db.Float, default=1.0),
    db.Column('visible', db.Boolean, default=True),
    db.Column('assigned_date', db.DateTime, default=lambda: datetime.now(timezone.utc))
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    employee_id = db.Column(db.String(50), unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    phone = db.Column(db.String(20))
    office_location = db.Column(db.String(100))
    hire_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    student_number = db.Column(db.String(50), nullable=False, unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    enrollment_year = db.Column(db.Integer)
    graduation_date = db.Column(db.Date)
    gpa = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    programming_language = db.Column(db.Enum(ProgrammingLanguage), default=ProgrammingLanguage.PYTHON)
    test_type = db.Column(db.Enum(TestType), default=TestType.UNIT)
    version = db.Column(db.String(20), default="1.0")
    created_by = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
            'programming_language': self.programming_language.value,
            'test_type': self.test_type.value,
            'version': self.version,
            'is_active': self.is_active
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.test_id'))
    rubric = db.Column(db.Text, nullable=False)
    max_score = db.Column(db.Float, default=100.0)
    pass_threshold = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    late_penalty = db.Column(db.Float, default=0.1)
    max_attempts = db.Column(db.Integer, default=3)
    weight = db.Column(db.Float, default=1.0)
    type = db.Column(db.Enum(AssignmentType), nullable=False, default=AssignmentType.CODING)
    is_published = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
    submission_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    submission_file = db.Column(db.LargeBinary)  # BLOB for submission files
    file_name = db.Column(db.String(255))
    file_type = db.Column(db.Enum(SubmissionFileType), default=SubmissionFileType.PYTHON_FILE)
    file_size = db.Column(db.Integer)
    attempt_number = db.Column(db.Integer, default=1)
    is_late = db.Column(db.Boolean, default=False)
    days_late = db.Column(db.Integer, default=0)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)  # Browser info
    status = db.Column(db.Enum(SubmissionStatus), default=SubmissionStatus.SUBMITTED)
    result_id = db.Column(db.Integer, db.ForeignKey('results.result_id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
            'file_type': self.file_type.value,
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
    score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    execution_time = db.Column(db.Float)
    memory_usage = db.Column(db.Integer)
    test_cases_passed = db.Column(db.Integer, default=0)
    test_cases_total = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    feedback = db.Column(db.Text)
    feedback_summary = db.Column(db.Text)
    grade_status = db.Column(db.Enum(GradeStatus), default=GradeStatus.NOT_GRADED)
    graded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    graded_by = db.Column(db.String(50), default='AUTOMARKER')  # AUTOMARKER vs teacher_id
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
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
            'grade_status': self.grade_status.value,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None,
            'graded_by': self.graded_by
        }

# Activity Logging and Session Management
class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    session_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)  # TEACHER, STUDENT, ADMIN
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
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
    action = db.Column(db.Enum(ActivityAction), nullable=False)
    resource_type = db.Column(db.String(50))  # assignment, submission, test, etc.
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON details about the action
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'user_type': self.user_type.value,
            'action': self.action.value,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success
        }