CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Modules (
    module_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_description TEXT NOT NULL,
    rubric TEXT NOT NULL,
    threshold REAL NOT NULL,
    due_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    assignment_id INTEGER NOT NULL,
    submission_date DATE NOT NULL,
    result_id INTEGER,
    submission_file BLOB,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id),
    FOREIGN KEY (result_id) REFERENCES Results (result_id)
);

CREATE TABLE IF NOT EXISTS Results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    actual_output TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    passed BOOLEAN NOT NULL,
    result INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_function TEXT NOT NULL,
    input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    timeout_seconds INTEGER DEFAULT 5
);

-- Relationship table: Many-to-many between Assignment and Tests they contain
CREATE TABLE IF NOT EXISTS AssignmentTests (
    assignment_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    PRIMARY KEY (assignment_id, test_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id),
    FOREIGN KEY (test_id) REFERENCES Tests (test_id)
);

-- Relationship table: Many-to-many between Teachers and Modules they teach
CREATE TABLE IF NOT EXISTS TeacherModules (
    teacher_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    PRIMARY KEY (teacher_id, module_id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);

-- Relationship table: Many-to-many between Students and Modules they are enrolled in
CREATE TABLE IF NOT EXISTS StudentEnrollments (
    student_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, module_id),
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);

-- Relationship table: Many-to-many between Modules and Assignments they contain
CREATE TABLE IF NOT EXISTS ModuleAssignments (
    module_id INTEGER NOT NULL,
    assignment_id INTEGER NOT NULL,
    PRIMARY KEY (module_id, assignment_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id)
);