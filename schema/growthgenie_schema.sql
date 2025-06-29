-- =============================================
-- CREATE ENUM TYPES FIRST
-- =============================================

CREATE TYPE user_type_enum AS ENUM ('student', 'parent', 'teacher', 'admin');
CREATE TYPE relationship_type_enum AS ENUM ('father', 'mother', 'guardian', 'grandparent', 'other');
CREATE TYPE family_role_enum AS ENUM ('head', 'parent', 'child', 'guardian');
CREATE TYPE target_type_enum AS ENUM ('family', 'classroom');
CREATE TYPE request_status_enum AS ENUM ('pending', 'approved', 'rejected');
CREATE TYPE task_category_enum AS ENUM ('homework', 'project', 'study', 'personal', 'chore', 'health', 'financial');
CREATE TYPE priority_enum AS ENUM ('low', 'medium', 'high');
CREATE TYPE task_status_enum AS ENUM ('pending', 'in_progress', 'completed', 'overdue');
CREATE TYPE repeat_pattern_enum AS ENUM ('never', 'daily', 'weekly', 'monthly');
CREATE TYPE transaction_type_enum AS ENUM ('income', 'expense');
CREATE TYPE payment_method_enum AS ENUM ('cash', 'debit_card', 'mobile_payment', 'gift_card', 'bank_transfer');
CREATE TYPE goal_status_enum AS ENUM ('active', 'completed', 'paused', 'cancelled');
CREATE TYPE mood_enum AS ENUM ('very_sad', 'sad', 'neutral', 'happy', 'very_happy');
CREATE TYPE energy_level_enum AS ENUM ('low', 'medium', 'high');
CREATE TYPE sleep_quality_enum AS ENUM ('poor', 'fair', 'great');
CREATE TYPE stress_level_enum AS ENUM ('relaxed', 'moderate', 'high');
CREATE TYPE sender_type_enum AS ENUM ('user', 'ai_bot');
CREATE TYPE contact_type_enum AS ENUM ('crisis', 'teen_support', 'text_line', 'bullying', 'family_crisis', 'local_emergency');
CREATE TYPE severity_enum AS ENUM ('mild', 'moderate', 'severe');
CREATE TYPE meal_type_enum AS ENUM ('breakfast', 'lunch', 'dinner', 'snack');
CREATE TYPE unit_enum AS ENUM ('cup', 'piece', 'tablespoon', 'grams', 'bowl', 'plate');
CREATE TYPE container_type_enum AS ENUM ('glass', 'bottle', 'cup');
CREATE TYPE report_type_enum AS ENUM ('blood_test', 'allergy_test', 'physical_exam', 'specialist_consultation', 'other');
CREATE TYPE alert_type_enum AS ENUM ('critical', 'high_sodium', 'high_sugar', 'missed_medication', 'low_water', 'appointment_reminder');
CREATE TYPE alert_severity_enum AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE notification_type_enum AS ENUM ('info', 'warning', 'error', 'success', 'reminder');
CREATE TYPE notification_category_enum AS ENUM ('task', 'financial', 'health', 'emotion', 'system');
CREATE TYPE privacy_level_enum AS ENUM ('private', 'anonymous_sharing');

-- =============================================
-- USER MANAGEMENT TABLES
-- =============================================

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    user_type user_type_enum NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_picture_url VARCHAR(500)
);

-- Students table (extends users)
CREATE TABLE students (
    student_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    student_number VARCHAR(50) UNIQUE,
    grade_level VARCHAR(10),
    school_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    can_exist_independently BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Parents table (extends users)
CREATE TABLE parents (
    parent_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    relationship_type relationship_type_enum NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teachers table (extends users)
CREATE TABLE teachers (
    teacher_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    school_name VARCHAR(255) NOT NULL,
    school_district VARCHAR(255) NOT NULL,
    subject_grade VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    approval_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family Groups
CREATE TABLE family_groups (
    family_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_name VARCHAR(255) NOT NULL,
    family_key VARCHAR(50) UNIQUE NOT NULL,
    family_head_id UUID REFERENCES parents(parent_id) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family Members (relationship between students/parents and family groups)
CREATE TABLE family_members (
    member_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID REFERENCES family_groups(family_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    role family_role_enum NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(family_id, user_id)
);

-- Classrooms
CREATE TABLE classrooms (
    classroom_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    classroom_name VARCHAR(255) NOT NULL,
    classroom_key VARCHAR(50) UNIQUE NOT NULL,
    teacher_id UUID REFERENCES teachers(teacher_id) NOT NULL,
    subject VARCHAR(255),
    grade_level VARCHAR(50),
    school_name VARCHAR(255),
    max_students INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Classroom Students (many-to-many relationship)
CREATE TABLE classroom_students (
    enrollment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    classroom_id UUID REFERENCES classrooms(classroom_id) ON DELETE CASCADE,
    student_id UUID REFERENCES students(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(classroom_id, student_id)
);

-- Join Requests (for family groups and classrooms)
CREATE TABLE join_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requester_id UUID REFERENCES users(user_id) NOT NULL,
    target_type target_type_enum NOT NULL,
    target_id UUID NOT NULL, -- family_id or classroom_id
    relationship_type VARCHAR(50),
    message TEXT,
    status request_status_enum DEFAULT 'pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    responded_by UUID REFERENCES users(user_id)
);

-- =============================================
-- TASK MANAGEMENT TABLES
-- =============================================

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to UUID REFERENCES students(student_id) NOT NULL,
    assigned_by UUID REFERENCES users(user_id) NOT NULL,
    category task_category_enum NOT NULL,
    priority priority_enum DEFAULT 'medium',
    due_date TIMESTAMP,
    due_time TIME,
    status task_status_enum DEFAULT 'pending',
    completion_date TIMESTAMP,
    reward_points INTEGER DEFAULT 0,
    attachment_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE task_completions (
    completion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(task_id) ON DELETE CASCADE,
    student_id UUID REFERENCES students(student_id) NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    verified_by UUID REFERENCES users(user_id),
    verification_date TIMESTAMP
);

CREATE TABLE reminders (
    reminder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_id UUID REFERENCES users(user_id) NOT NULL,
    reminder_date DATE NOT NULL,
    reminder_time TIME NOT NULL,
    repeat_pattern repeat_pattern_enum DEFAULT 'never',
    related_task_id UUID REFERENCES tasks(task_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- FINANCIAL LITERACY TABLES
-- =============================================

CREATE TABLE categories (
    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    name VARCHAR(255) NOT NULL,
    type transaction_type_enum NOT NULL,
    budget_limit DECIMAL(10,2),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    category_id UUID REFERENCES categories(category_id) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type transaction_type_enum NOT NULL,
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    transaction_time TIME DEFAULT CURRENT_TIME,
    payment_method payment_method_enum NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE savings_goals (
    goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0.00,
    target_date DATE,
    category VARCHAR(100),
    status goal_status_enum DEFAULT 'active',
    created_by UUID REFERENCES users(user_id), -- parent can create for child
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budgets (
    budget_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    category_id UUID REFERENCES categories(category_id) NOT NULL,
    monthly_limit DECIMAL(10,2) NOT NULL,
    current_spent DECIMAL(10,2) DEFAULT 0.00,
    budget_month INTEGER NOT NULL,
    budget_year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, category_id, budget_month, budget_year)
);

-- =============================================
-- EMOTION MANAGEMENT TABLES
-- =============================================

CREATE TABLE emotional_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    title VARCHAR(255),
    content TEXT NOT NULL,
    mood mood_enum NOT NULL,
    intensity INTEGER CHECK (intensity >= 1 AND intensity <= 10),
    triggers TEXT[], -- array of trigger categories
    tags TEXT[], -- array of tags
    privacy_level privacy_level_enum DEFAULT 'private',
    entry_date DATE DEFAULT CURRENT_DATE,
    entry_time TIME DEFAULT CURRENT_TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mood_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    mood mood_enum NOT NULL,
    energy_level energy_level_enum,
    sleep_quality sleep_quality_enum,
    stress_level stress_level_enum,
    notes TEXT,
    log_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    session_title VARCHAR(255),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE chat_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    sender_type sender_type_enum NOT NULL,
    message_content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emergency_contacts (
    contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    description TEXT,
    contact_type contact_type_enum NOT NULL,
    is_available_24_7 BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- HEALTH/DIET MANAGEMENT TABLES
-- =============================================

CREATE TABLE health_conditions (
    condition_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    condition_name VARCHAR(255) NOT NULL,
    severity severity_enum NOT NULL,
    diagnosed_date DATE,
    doctor_clinic VARCHAR(255),
    dietary_restrictions TEXT,
    symptoms_to_monitor TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medications (
    medication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    condition_id UUID REFERENCES health_conditions(condition_id),
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100), -- e.g., "Before meals", "Once daily"
    start_date DATE,
    end_date DATE,
    prescribing_doctor VARCHAR(255),
    instructions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medication_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    medication_id UUID REFERENCES medications(medication_id) NOT NULL,
    user_id UUID REFERENCES students(student_id) NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity_taken VARCHAR(50),
    notes TEXT,
    logged_by UUID REFERENCES users(user_id) -- parent or student
);

CREATE TABLE food_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    meal_type meal_type_enum NOT NULL,
    food_item VARCHAR(255) NOT NULL,
    quantity VARCHAR(100),
    unit unit_enum NOT NULL,
    calories INTEGER,
    carbs_g DECIMAL(6,2),
    protein_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    sodium_mg DECIMAL(8,2),
    sugar_g DECIMAL(6,2),
    fiber_g DECIMAL(6,2),
    meal_date DATE DEFAULT CURRENT_DATE,
    meal_time TIME DEFAULT CURRENT_TIME,
    photo_url VARCHAR(500),
    notes TEXT,
    logged_by UUID REFERENCES users(user_id), -- parent or student
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE water_intake (
    intake_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    amount_ml INTEGER NOT NULL,
    container_type container_type_enum NOT NULL,
    intake_date DATE DEFAULT CURRENT_DATE,
    intake_time TIME DEFAULT CURRENT_TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE health_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    weight_kg DECIMAL(5,2),
    height_cm DECIMAL(5,2),
    bmi DECIMAL(4,2),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    blood_sugar_mg_dl INTEGER,
    heart_rate_bpm INTEGER,
    measurement_date DATE DEFAULT CURRENT_DATE,
    measurement_time TIME DEFAULT CURRENT_TIME,
    notes TEXT,
    recorded_by UUID REFERENCES users(user_id), -- parent or student
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medical_reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    report_title VARCHAR(255) NOT NULL,
    report_type report_type_enum NOT NULL,
    report_date DATE NOT NULL,
    doctor_name VARCHAR(255),
    clinic_hospital VARCHAR(255),
    summary TEXT,
    file_url VARCHAR(500),
    uploaded_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE health_alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES students(student_id) NOT NULL,
    alert_type alert_type_enum NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity alert_severity_enum NOT NULL,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP,
    acknowledged_by UUID REFERENCES users(user_id),
    resolved_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================================
-- SYSTEM TABLES
-- =============================================

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type notification_type_enum NOT NULL,
    category notification_category_enum NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    action_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(100),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- User management indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_type ON users(user_type);
CREATE INDEX idx_family_members_family_id ON family_members(family_id);
CREATE INDEX idx_classroom_students_classroom_id ON classroom_students(classroom_id);

-- Task management indexes
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_reminders_user_id ON reminders(user_id);
CREATE INDEX idx_reminders_date_time ON reminders(reminder_date, reminder_time);

-- Financial indexes
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_savings_goals_user_id ON savings_goals(user_id);

-- Health/emotion indexes
CREATE INDEX idx_emotional_entries_user_id ON emotional_entries(user_id);
CREATE INDEX idx_emotional_entries_date ON emotional_entries(entry_date);
CREATE INDEX idx_food_logs_user_id ON food_logs(user_id);
CREATE INDEX idx_food_logs_date ON food_logs(meal_date);
CREATE INDEX idx_health_metrics_user_id ON health_metrics(user_id);
CREATE INDEX idx_health_alerts_user_id ON health_alerts(user_id);
CREATE INDEX idx_health_alerts_active ON health_alerts(is_active);

-- System indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);