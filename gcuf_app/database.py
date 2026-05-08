import sqlite3
import hashlib
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "gcuf.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin','professor')),
        department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
        full_name TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        title TEXT NOT NULL,
        credit_hours_raw TEXT NOT NULL,
        credit_hours REAL NOT NULL,
        session TEXT NOT NULL,
        semester TEXT DEFAULT '',
        department_id INTEGER NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
        max_marks REAL DEFAULT 60,
        uploaded_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT NOT NULL,
        name TEXT NOT NULL,
        father_name TEXT DEFAULT '',
        cnic TEXT DEFAULT '',
        session TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
        course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        internal_marks REAL DEFAULT 0,
        mid_term REAL DEFAULT 0,
        final_term REAL DEFAULT 0,
        practical_work REAL DEFAULT 0,
        total_obtained REAL DEFAULT 0,
        percentage REAL DEFAULT 0,
        grade TEXT DEFAULT '',
        grade_point REAL DEFAULT 0,
        status TEXT DEFAULT 'Pass',
        UNIQUE(student_id, course_id)
    );
    """)
    conn.commit()

    # Seed default admin
    pw = _hash("admin123")
    try:
        c.execute("INSERT OR IGNORE INTO users (username, password_hash, role, full_name) VALUES (?,?,?,?)",
                  ("admin", pw, "admin", "System Administrator"))
    except Exception:
        pass

    conn.commit()
    conn.close()


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ─── Auth ───────────────────────────────────────────────────────────────────

def authenticate(username: str, password: str) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute(
        "SELECT u.*, d.name as dept_name FROM users u "
        "LEFT JOIN departments d ON u.department_id = d.id "
        "WHERE u.username=? AND u.password_hash=?",
        (username, _hash(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username, password, role, full_name="", department_id=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO users (username, password_hash, role, full_name, department_id) VALUES (?,?,?,?,?)",
        (username, _hash(password), role, full_name, department_id)
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_conn()
    rows = conn.execute(
        "SELECT u.*, d.name as dept_name FROM users u LEFT JOIN departments d ON u.department_id=d.id ORDER BY u.role, u.username"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM users WHERE id=? AND role != 'admin'", (user_id,))
    conn.commit()
    conn.close()


# ─── Departments ─────────────────────────────────────────────────────────────

def get_departments():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM departments ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_department(name: str):
    conn = get_conn()
    conn.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def rename_department(dept_id: int, new_name: str):
    conn = get_conn()
    conn.execute("UPDATE departments SET name=? WHERE id=?", (new_name, dept_id))
    conn.commit()
    conn.close()


def delete_department(dept_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM departments WHERE id=?", (dept_id,))
    conn.commit()
    conn.close()


# ─── Courses ─────────────────────────────────────────────────────────────────

def save_course(code, title, credit_hours_raw, credit_hours, session, semester, department_id, max_marks, uploaded_by):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO courses (code, title, credit_hours_raw, credit_hours, session, semester, department_id, max_marks, uploaded_by) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (code, title, credit_hours_raw, credit_hours, session, semester, department_id, max_marks, uploaded_by)
    )
    course_id = c.lastrowid
    conn.commit()
    conn.close()
    return course_id


def get_courses_for_department(dept_id: int):
    conn = get_conn()
    rows = conn.execute(
        "SELECT c.*, u.full_name as uploader FROM courses c "
        "LEFT JOIN users u ON c.uploaded_by=u.id "
        "WHERE c.department_id=? ORDER BY c.created_at DESC", (dept_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_courses():
    conn = get_conn()
    rows = conn.execute(
        "SELECT c.*, d.name as dept_name, u.full_name as uploader FROM courses c "
        "LEFT JOIN departments d ON c.department_id=d.id "
        "LEFT JOIN users u ON c.uploaded_by=u.id "
        "ORDER BY c.created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_course(course_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT c.*, d.name as dept_name FROM courses c LEFT JOIN departments d ON c.department_id=d.id WHERE c.id=?",
        (course_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── Students ────────────────────────────────────────────────────────────────

def get_or_create_student(roll_no, name, father_name, cnic, session):
    conn = get_conn()
    c = conn.cursor()
    row = c.execute("SELECT * FROM students WHERE roll_no=? AND session=?", (roll_no, session)).fetchone()
    if row:
        sid = row["id"]
        # Update info
        c.execute("UPDATE students SET name=?, father_name=?, cnic=? WHERE id=?",
                  (name, father_name, cnic, sid))
    else:
        c.execute("INSERT INTO students (roll_no, name, father_name, cnic, session) VALUES (?,?,?,?,?)",
                  (roll_no, name, father_name, cnic, session))
        sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid


def save_result(student_id, course_id, internal, mid, final, practical, total, pct, grade, grade_point, status):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO results "
        "(student_id, course_id, internal_marks, mid_term, final_term, practical_work, total_obtained, percentage, grade, grade_point, status) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (student_id, course_id, internal, mid, final, practical, total, pct, grade, grade_point, status)
    )
    conn.commit()
    conn.close()


def get_results_for_course(course_id: int):
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.*, s.roll_no, s.name, s.father_name, s.cnic, s.session "
        "FROM results r JOIN students s ON r.student_id=s.id "
        "WHERE r.course_id=? ORDER BY r.percentage DESC",
        (course_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_results(roll_no: str, session: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.*, s.name, s.roll_no, s.father_name, s.cnic, s.session, "
        "c.code, c.title, c.credit_hours, c.credit_hours_raw, c.session as course_session, "
        "d.name as dept_name "
        "FROM results r "
        "JOIN students s ON r.student_id=s.id "
        "JOIN courses c ON r.course_id=c.id "
        "LEFT JOIN departments d ON c.department_id=d.id "
        "WHERE s.roll_no=? AND s.session=? ORDER BY c.code",
        (roll_no, session)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_department_results(dept_id: int):
    """All results for a department, for analytics."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.*, s.roll_no, s.name, s.session, c.code, c.title, c.credit_hours, c.session as csession "
        "FROM results r "
        "JOIN students s ON r.student_id=s.id "
        "JOIN courses c ON r.course_id=c.id "
        "WHERE c.department_id=? ORDER BY r.percentage DESC",
        (dept_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_session_toppers(session: str, limit=10):
    """Ranked by percentage across all departments for a session."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT s.roll_no, s.name, s.session, d.name as dept_name, "
        "AVG(r.percentage) as avg_pct, "
        "SUM(CASE WHEN r.status='Pass' THEN r.grade_point * c.credit_hours ELSE 0 END) / "
        "SUM(c.credit_hours) as gpa "
        "FROM results r "
        "JOIN students s ON r.student_id=s.id "
        "JOIN courses c ON r.course_id=c.id "
        "LEFT JOIN departments d ON c.department_id=d.id "
        "WHERE s.session=? "
        "GROUP BY s.id ORDER BY avg_pct DESC LIMIT ?",
        (session, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_department_toppers(dept_id: int, limit=10):
    conn = get_conn()
    rows = conn.execute(
        "SELECT s.roll_no, s.name, s.session, d.name as dept_name, "
        "AVG(r.percentage) as avg_pct, "
        "SUM(CASE WHEN r.status='Pass' THEN r.grade_point * c.credit_hours ELSE 0 END) / "
        "SUM(c.credit_hours) as gpa "
        "FROM results r "
        "JOIN students s ON r.student_id=s.id "
        "JOIN courses c ON r.course_id=c.id "
        "LEFT JOIN departments d ON c.department_id=d.id "
        "WHERE c.department_id=? "
        "GROUP BY s.id ORDER BY avg_pct DESC LIMIT ?",
        (dept_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dept_avg_gpa():
    """Average GPA per department for analytics chart."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT d.name as dept_name, d.id as dept_id, "
        "AVG(r.percentage) as avg_pct, "
        "COUNT(DISTINCT s.id) as student_count "
        "FROM results r "
        "JOIN students s ON r.student_id=s.id "
        "JOIN courses c ON r.course_id=c.id "
        "JOIN departments d ON c.department_id=d.id "
        "GROUP BY d.id ORDER BY avg_pct DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_sessions():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT session FROM students ORDER BY session DESC").fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_students_in_course(course_id: int):
    return get_results_for_course(course_id)
