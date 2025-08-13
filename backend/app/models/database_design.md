# CSRS Automated Assessment Database Design

## Design Philosophy: Production-Ready Architecture

This system provides a **unified, production-ready model** that handles both simple and enterprise-scale educational deployments with complete feature coverage.

## ✅ **Enhanced Model Features (All Implemented)**

### 🔐 **CRITICAL Features**
- ✅ **Authentication**: `email` and `password_hash` fields for Teachers and Students
- ✅ **Assignment Management**: `title`, `instructions`, `max_score`, `max_attempts` 
- ✅ **Submission Tracking**: `attempt_number`, `file_name`, `file_size`, `is_late`
- ✅ **Result Scoring**: `percentage`, `test_cases_passed/total`, `execution_time`

### 📊 **IMPORTANT Features** 
- ✅ **Audit Timestamps**: `created_at`, `updated_at` on all major tables
- ✅ **Active/Inactive Flags**: `is_active` for soft deletes and status management
- ✅ **Contact Information**: `email`, `phone`, `office_location` for Teachers/Students
- ✅ **Enrollment Metadata**: Enhanced junction tables with status and dates

### � **NICE TO HAVE Features**
- ✅ **Activity Logging**: Complete audit trail with `ActivityLog` table
- ✅ **Session Management**: User sessions with `UserSession` table
- ✅ **Performance Metrics**: `execution_time`, `memory_usage` tracking

## 📊 Enhanced Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  INSTITUTIONS   │    │   DEPARTMENTS   │    │    SUBJECTS     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ 🔑 institution_id│    │ 🔑 department_id│    │ 🔑 subject_id   │
│ 📝 name         │    │ 📝 name         │    │ 📝 name         │
│ 📝 type         │    │ 📝 code         │    │ 📝 code         │
│ 🌍 country      │    │ 🔗 institution_id│   │ 📝 description  │
│ 📧 contact_email│    │ 📧 contact_email│    │ 📝 type         │
│ 📞 phone        │    │ 📞 phone        │    │ 🔗 department_id│
│ ✅ is_active    │    │ 🏢 office_loc   │    │ 🤖 has_automark │
│ 📅 created_at   │    │ 💰 budget       │    │ 📚 credit_hours │
│ 📅 updated_at   │    │ ✅ is_active    │    │ 📋 prerequisites│
└─────────────────┘    │ 📅 created_at   │    │ ✅ is_active    │
                       │ 📅 updated_at   │    │ 📅 created_at   │
                       └─────────────────┘    │ 📅 updated_at   │
                                              └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐           │
│     TEACHERS    │    │     MODULES     │    ┌──────┘
├─────────────────┤    ├─────────────────┤    │
│ 🔑 teacher_id   │    │ 🔑 module_id    │    │   ┌─────────────────┐
│ 📝 first_name   │    │ 📝 name         │    │   │   ASSIGNMENTS   │
│ 📝 surname      │    │ 📝 code         │    │   ├─────────────────┤
│ 📧 email        │🔐  │ 📝 description  │    │   │ 🔑 assignment_id│
│ 🔒 password_hash│    │ 📝 semester     │    │   │ 📝 title        │🔐
│ 👤 employee_id  │    │ 📅 year         │    │   │ 📝 description  │
│ 🔗 institution_id│   │ 🔗 subject_id   │────┘   │ 📝 instructions │🔐
│ 🔗 department_id│    │ 📅 start_date   │        │ 🔗 test_id      │
│ 📞 phone        │    │ 📅 end_date     │        │ 📝 rubric       │
│ 🏢 office_loc   │    │ 👥 max_students │        │ 🎯 max_score    │🔐
│ ✅ is_active    │    │ 📚 credits      │        │ 📊 pass_thresh  │
│ 📅 created_at   │    │ 🏢 location     │        │ 📅 due_date     │
│ 📅 updated_at   │    │ 📅 schedule     │        │ ⚖️ late_penalty │
└─────────────────┘    │ 📋 prerequisites│        │ 🔢 max_attempts │🔐
         │              │ ✅ is_active    │        │ ⚖️ weight       │
         │              │ 📅 created_at   │        │ 📝 type         │
         └───────┐      │ 📅 updated_at   │        │ 📰 is_published │
                 │      └─────────────────┘        │ ✅ is_active    │
            ┌─────────────────┐ │                  │ 👤 created_by   │
            │ teacher_modules │ │                  │ 📅 created_at   │
            ├─────────────────┤ │                  │ 📅 updated_at   │
            │ teacher_id (FK) │ │                  └─────────────────┘
            │ module_id (FK)  │ │                           │
            │ 👑 role         │ │                           │
            │ 📅 assigned_date│ │                           │
            │ ✅ is_active    │ │                           │
            └─────────────────┘ │                           │
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│    STUDENTS     │    │      TESTS      │             │
├─────────────────┤    ├─────────────────┤             │
│ 🔑 student_id   │    │ 🔑 test_id      │─────────────┘
│ 📝 first_name   │    │ 📝 name         │
│ 📝 surname      │    │ 📝 description  │
│ 📧 email        │🔐  │ 📄 test_file    │
│ 🔒 password_hash│    │ 📝 input_data   │
│ 📊 student_number│   │ 📝 expected_out │
│ 🔗 institution_id│   │ ⏱️ timeout_sec  │
│ 📞 phone        │    │ 💻 prog_lang    │
│ 🎂 date_of_birth│    │ 🧪 test_type    │
│ 📅 enroll_year  │    │ 📌 version      │
│ 🎓 graduation   │    │ 👤 created_by   │
│ 📊 gpa          │    │ ✅ is_active    │
│ ✅ is_active    │    │ 📅 created_at   │
│ 📅 created_at   │    │ 📅 updated_at   │
│ 📅 updated_at   │    └─────────────────┘
└─────────────────┘
         │
         │
    ┌─────────────────┐
    │student_enrollmt │
    ├─────────────────┤
    │ student_id (FK) │
    │ module_id (FK)  │
    │ 📅 enroll_date  │
    │ 📅 complete_date│
    │ 🎯 final_grade  │
    │ 📊 status       │
    └─────────────────┘
         │
         │
┌─────────────────┐    ┌─────────────────┐
│   SUBMISSIONS   │    │     RESULTS     │
├─────────────────┤    ├─────────────────┤
│ 🔑 submission_id│    │ 🔑 result_id    │
│ 🔗 student_id   │    │ 📝 actual_output│
│ 🔗 assignment_id│    │ 📝 expected_out │
│ 📅 submit_date  │    │ ✅ passed       │
│ 📄 submit_file  │    │ 🎯 score        │
│ 📝 file_name    │🔐  │ 📊 percentage   │🔐
│ 📊 file_size    │🔐  │ ⏱️ exec_time    │🔐
│ 🔢 attempt_num  │🔐  │ 💾 memory_usage │
│ ⏰ is_late      │🔐  │ ✅ tests_passed │🔐
│ 📅 days_late    │    │ 📊 tests_total  │🔐
│ 🌐 ip_address   │    │ ❌ error_message│
│ 🖥️ user_agent   │    │ 💬 feedback     │
│ 📊 status       │    │ 📝 feedback_sum │
│ 🔗 result_id    │────│ 📅 graded_at    │
│ 📅 created_at   │    │ 👤 graded_by    │
│ 📅 updated_at   │    │ 📅 created_at   │
└─────────────────┘    │ 📅 updated_at   │
                       └─────────────────┘

    ┌─────────────────┐
    │module_assignmnt │
    ├─────────────────┤
    │ module_id (FK)  │
    │ assignmnt_id(FK)│
    │ ⚖️ weight       │
    │ 👁️ visible      │
    │ 📅 assigned_date│
    └─────────────────┘

🔐 = Critical enhancements added
```

## 🚀 **NICE TO HAVE: Audit & Session Tables**

```
┌─────────────────┐    ┌─────────────────┐
│  USER_SESSIONS  │    │  ACTIVITY_LOGS  │
├─────────────────┤    ├─────────────────┤
│ 🔑 session_id   │    │ 🔑 log_id       │
│ 👤 user_id      │    │ 👤 user_id      │
│ 👥 user_type    │    │ 👥 user_type    │
│ 📅 created_at   │    │ 🎬 action       │
│ ⏰ expires_at   │    │ 📦 resource_type│
│ 🌐 ip_address   │    │ 🔗 resource_id  │
│ 🖥️ user_agent   │    │ 📝 details      │
│ ✅ is_active    │    │ 🌐 ip_address   │
│ 📅 last_activity│    │ 🖥️ user_agent   │
└─────────────────┘    │ 📅 timestamp    │
                       │ ✅ success      │
                       │ ❌ error_msg    │
                       └─────────────────┘
```

## 🎯 **Complete Feature Matrix**

| Feature Category | Field/Table | Purpose | Status |
|-----------------|-------------|---------|--------|
| **🔐 Authentication** | `email`, `password_hash` | User login system | ✅ Implemented |
| **📝 Assignment Management** | `title`, `instructions` | Clear assignment details | ✅ Implemented |
| **🎯 Scoring System** | `max_score`, `percentage` | Comprehensive grading | ✅ Implemented |
| **🔢 Attempt Tracking** | `attempt_number`, `max_attempts` | Multiple submission handling | ✅ Implemented |
| **⏰ Deadline Management** | `is_late`, `days_late`, `late_penalty` | Late submission handling | ✅ Implemented |
| **📊 Performance Metrics** | `execution_time`, `memory_usage` | Code performance tracking | ✅ Implemented |
| **📧 Contact Management** | `phone`, `office_location` | Communication details | ✅ Implemented |
| **✅ Status Management** | `is_active` flags | Soft delete/enable-disable | ✅ Implemented |
| **📅 Audit Trail** | `created_at`, `updated_at` | Change tracking | ✅ Implemented |
| **👥 Enrollment Tracking** | Enhanced junction tables | Student-module relationships | ✅ Implemented |
| **🔍 Activity Logging** | `ActivityLog` table | Complete audit trail | ✅ Implemented |
| **🎫 Session Management** | `UserSession` table | Secure user sessions | ✅ Implemented |

## 🏗️ **Production Readiness Checklist**

### ✅ **Database Design**
- [x] Proper foreign key relationships
- [x] Normalized structure (3NF compliance)
- [x] Junction tables with metadata
- [x] Comprehensive indexing strategy
- [x] Enum constraints for data integrity

### ✅ **Security Features**
- [x] Password hashing support
- [x] Session management
- [x] IP address tracking
- [x] User agent logging
- [x] Activity audit trail

### ✅ **Business Logic Support**
- [x] Multiple attempt handling
- [x] Late submission penalties
- [x] Grade calculation fields
- [x] Assignment weight system
- [x] Test case result tracking

### ✅ **Operational Features**
- [x] Soft delete (is_active flags)
- [x] Audit timestamps
- [x] Performance monitoring
- [x] Error message logging
- [x] File metadata tracking

## 🔗 Relationships

### 1. **institutions one-to-many departments** ✅
```sql
Institution (1) ----< Department (many)
institution_id (PK) ----< institution_id (FK)
```

### 2. **departments one-to-many subjects** ✅
```sql
Department (1) ----< Subject (many)
department_id (PK) ----< department_id (FK)
```

### 3. **subjects one-to-many modules** ✅
```sql
Subject (1) ----< Module (many)
subject_id (PK) ----< subject_id (FK)
```

### 4. **modules one-to-many assignments** ✅
```sql
Module (many) ----< Assignment (many)
Via junction table: module_assignments
```

### 5. **teachers junction table to modules** ✅
```sql
Teacher (many) ><--< Module (many)
Via junction table: teacher_modules
+ role (instructor/assistant/coordinator)
+ created_at
```

### 6. **students junction table to modules** ✅
```sql
Student (many) ><--< Module (many)
Via junction table: student_enrollments
+ enrolled_date
+ status (active/completed/dropped)
```

### 7. **assignments junction table to modules** ✅
```sql
Assignment (many) ><--< Module (many)
Via junction table: module_assignments
+ weight (for grading)
+ visible (published or not)
```

### 8. **assignments one-to-many submissions** ✅
```sql
Assignment (1) ----< Submission (many)
assignment_id (PK) ----< assignment_id (FK)
```

### 9. **assignments one-to-many tests** ✅
```sql
Assignment (1) ----< Test (1)
Actually: Assignment belongs_to Test
test_id (FK) ----< test_id (PK)
```
*Note: I modeled it as Assignment belongs_to Test since a test can be reused across multiple assignments*

### 10. **submissions one-to-one results** ✅
```sql
Submission (1) ----< Result (1)
submission_id ----< result_id (FK)
```

## 🚀 Why This Unified Approach is Brilliant

1. **Flexibility**: You can use it simple (create 1 institution, 1 department, 1 subject) or complex (multiple institutions)

2. **No Code Changes**: Your application logic doesn't change - you just create the minimal hierarchy

3. **Future-Proof**: When you need to scale, you just add more institutions/departments
## 📋 Table Details

### **Core Tables:**

| Table | Purpose | Key Features |
|-------|---------|--------------|
| **Teachers** | Faculty management | Manages modules and creates assignments |
| **Students** | Learner accounts | Enrolls in modules, submits assignments |
| **Modules** | Courses/Subjects | Container for assignments and enrollments |
| **Assignments** | Learning tasks | Contains description, rubric, and test reference |
| **Tests** | Automated testing | Stores test files, inputs, expected outputs |
| **Submissions** | Student work | File uploads with timestamps |
| **Results** | Grading outcomes | Automated scoring and feedback |

### **Junction Tables:**
- `teacher_modules` - Links teachers to their managed modules
- `student_enrollments` - Links students to enrolled modules  
- `module_assignments` - Links modules to their assignments

## 🎯 Design Benefits

### ✅ **For Automated Assessment:**
1. **File Storage**: BLOB fields for test files and submissions
2. **Test Execution Pipeline**: Clear flow from assignment → test → submission → result
3. **Automated Grading**: Score calculation with pass/fail thresholds
4. **Audit Trail**: Complete tracking of submissions and results

### ✅ **For Application Features:**
1. **Dashboard Views**: Students see enrolled modules and assignments
2. **Assignment Management**: Teachers create and manage assignments
3. **File Upload**: Secure storage of Python files and test scripts
4. **Results Display**: Detailed feedback and scoring

### ✅ **For Scalability:**
1. **Multi-institutional Support**: Can handle multiple schools
2. **Role-based Access**: Clear teacher/student separation
3. **Performance**: Proper indexing on primary/foreign keys
4. **Extensibility**: Easy to add new features
