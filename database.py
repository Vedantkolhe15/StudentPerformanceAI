import os
import pandas as pd
import streamlit as st

from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


# Supabase Connection
def get_connection() -> Client:

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    try:
        url = url or st.secrets["SUPABASE_URL"]
        key = key or st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    if not url or not key:
        raise ValueError("Supabase URL or API Key missing")

    return create_client(url, key)


# Create / Verify Table
def create_table():

    supabase = get_connection()

    response = supabase.table(
        "student_predictions"
    ).select("id").limit(1).execute()

    return True


# Save Prediction
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

    supabase = get_connection()

    student_data = {
        "student_name": student_name,
        "attendance": float(attendance),
        "study_hours": float(study_hours),
        "assignment_score": float(assignment_score),
        "internal_marks": float(internal_marks),
        "previous_marks": float(previous_marks),
        "participation": float(participation),
        "predicted_score": float(predicted_score),
        "performance": performance,
        "risk_level": risk_level,
        "created_at": datetime.now().astimezone().isoformat()
    }

    response = supabase.table(
        "student_predictions"
    ).insert(student_data).execute()

    return response.data


# Get Saved Predictions
def get_predictions():

    supabase = get_connection()

    response = supabase.table(
        "student_predictions"
    ).select("*").order(
        "id",
        desc=True
    ).execute()

    df = pd.DataFrame(response.data)

    return df