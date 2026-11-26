import sqlite3
import tomllib
from pathlib import Path
from supabase import create_client

# Load Supabase credentials
secrets = tomllib.loads(
    Path(".streamlit/secrets.toml").read_text()
)

supabase = create_client(
    secrets["SUPABASE_URL"],
    secrets["SUPABASE_KEY"]
)

# Connect to existing SQLite database
conn = sqlite3.connect("student_performance.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# Fetch all existing student records
cursor.execute("""
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
""")

records = [dict(row) for row in cursor.fetchall()]

conn.close()

print("Total SQLite Records:", len(records))

if records:

    # Transfer records to Supabase
    result = supabase.table(
        "student_predictions"
    ).upsert(
        records,
        on_conflict="id"
    ).execute()

    print("Migration Successful!")
    print("Records transferred:", len(result.data))

else:
    print("No records found to migrate.")

# Verify Supabase records
response = supabase.table(
    "student_predictions"
).select("id", count="exact").execute()

print("Total Supabase Records:", response.count)