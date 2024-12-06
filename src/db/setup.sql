CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Students (
    student_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Modules (
    module_id TEXT PRIMARY KEY,
    module_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Assignments (
    assignment_id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL,
    assignment_description TEXT NOT NULL,
    rubric TEXT NOT NULL,
    threshold REAL NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);

CREATE TABLE IF NOT EXISTS Submissions (
    submission_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    assignment_id TEXT NOT NULL,
    submission_date TEXT NOT NULL,
    result REAL NOT NULL,
    feedback TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id)
);

-- Relationship table: Many-to-many between Teachers and Modules they teach
CREATE TABLE IF NOT EXISTS TeacherModules (
    teacher_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    PRIMARY KEY (teacher_id, module_id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);

-- Relationship table: Many-to-many between Students and Modules they are enrolled in
CREATE TABLE IF NOT EXISTS StudentEnrollments (
    student_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    PRIMARY KEY (student_id, module_id),
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);

-- Relationship table: Many-to-many between Modules and Assignments they contain
CREATE TABLE IF NOT EXISTS ModuleAssignments (
    module_id TEXT NOT NULL,
    assignment_id TEXT NOT NULL,
    PRIMARY KEY (module_id, assignment_id),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id)
);