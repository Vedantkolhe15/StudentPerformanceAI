import sqlite3
from datetime import datetime


DB_NAME = "student_performance.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================================================
# CREATE DATABASE TABLE
# =========================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_name TEXT NOT NULL,

            attendance REAL,
            study_hours REAL,
            assignment_score REAL,
            internal_marks REAL,
            previous_marks REAL,
            participation REAL,

            predicted_score REAL,
            performance TEXT,
            risk_level TEXT,

            created_at TEXT

        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# SAVE PREDICTION
# =========================================================

def save_prediction(
    student_name,
    attendance,
    study_hours,
    assignment_score,
    internal_marks,
    previous_marks,
    participation,
    predicted_score,
    performance,
    risk_level
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student_predictions (

            student_name,
            attendance,
            study_hours,
            assignment_score,
            internal_marks,
            previous_marks,
            participation,
            predicted_score,
            performance,
            risk_level,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        student_name,
        attendance,
        study_hours,
        assignment_score,
        internal_marks,
        previous_marks,
        participation,
        predicted_score,
        performance,
        risk_level,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# =========================================================
# GET SAVED PREDICTIONS
# =========================================================

def get_predictions():

    conn = get_connection()

    query = """
        SELECT
            id,
            student_name,
            attendance,
            study_hours,
            assignment_score,
            internal_marks,
            previous_marks,
            participation,
            predicted_score,
            performance,
            risk_level,
            created_at
        FROM student_predictions
        ORDER BY id DESC
    """

    df = __import__("pandas").read_sql_query(
        query,
        conn
    )

    conn.close()

    return df