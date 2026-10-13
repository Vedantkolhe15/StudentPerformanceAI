import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from io import BytesIO
from database import (
    create_table,
    save_prediction,
    get_predictions
)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOGIN PROTECTION
# =========================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔐 Please login to access the dashboard.")

    st.info(
        "Go to the Login page from the sidebar and enter your credentials."
    )

    st.stop()


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return joblib.load(
        "models/student_performance_model.pkl"
    )


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/student_performance.csv"
    )


model = load_model()
df = load_data()
create_table()
# =========================================================
# GENERATE PDF REPORT
# =========================================================

def generate_pdf_report(
    student_name,
    predicted_score,
    performance,
    risk,
    attendance,
    study_hours,
    assignment_score,
    internal_marks,
    previous_marks,
    participation,
    recommendations
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    story = []

    # Title
    story.append(
        Paragraph(
            "STUDENT PERFORMANCE REPORT",
            title_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "Student Performance AI",
            heading_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # Student Information
    student_info = [
        ["Student Name", student_name],
        ["Report Type", "AI Performance Prediction"],
    ]

    student_table = Table(
        student_info,
        colWidths=[150, 300]
    )

    student_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(student_table)

    story.append(
        Spacer(1, 20)
    )

    # Prediction Result
    story.append(
        Paragraph(
            "Prediction Result",
            heading_style
        )
    )

    prediction_data = [
        ["Predicted Score", f"{predicted_score}%"],
        ["Performance", performance],
        ["Risk Level", risk],
    ]

    prediction_table = Table(
        prediction_data,
        colWidths=[180, 270]
    )

    prediction_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(prediction_table)

    story.append(
        Spacer(1, 20)
    )

    # Academic Factors
    story.append(
        Paragraph(
            "Academic Factors",
            heading_style
        )
    )

    academic_data = [
        ["Factor", "Score"],
        ["Attendance", f"{attendance}%"],
        ["Study Hours", f"{study_hours} hours/day"],
        ["Assignment Score", f"{assignment_score}%"],
        ["Internal Marks", f"{internal_marks}%"],
        ["Previous Marks", f"{previous_marks}%"],
        ["Class Participation", f"{participation}%"],
    ]

    academic_table = Table(
        academic_data,
        colWidths=[250, 200]
    )

    academic_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(academic_table)

    story.append(
        Spacer(1, 20)
    )

    # Recommendations
    story.append(
        Paragraph(
            "AI Recommendations",
            heading_style
        )
    )

    for recommendation in recommendations:

        story.append(
            Paragraph(
                f"• {recommendation}",
                normal_style
            )
        )

        story.append(
            Spacer(1, 5)
        )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Generated by Student Performance AI - BCA Final Year Project",
            normal_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .risk-box {
        padding: 20px;
        border-radius: 15px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 20px;
        border-radius: 15px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* =====================================================
   PROFESSIONAL METRIC CARDS
   ===================================================== */

[data-testid="stMetric"] {
    background: #ffffff;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    transition: 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.10);
}

[data-testid="stMetricLabel"] {
    font-size: 15px;
    font-weight: 600;
    color: #374151 !important;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
    color: #111827 !important;
}

[data-testid="stMetricDelta"] {
    color: #374151 !important;
}

        /* =====================================================
       PROFESSIONAL DASHBOARD HERO
       ===================================================== */

    .dashboard-hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 100%
        );
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 25px;
    }

    .hero-icon {
        width: 85px;
        height: 85px;
        border-radius: 20px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 45px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        flex-shrink: 0;
    }

    .hero-content {
        flex: 1;
    }

    .hero-title {
        font-size: 36px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 18px;
        font-weight: 550;
        margin-bottom: 10px;
    }

    .hero-description {
        font-size: 15px;
        color: #64748b;
        line-height: 1.6;
        max-width: 850px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CREATE RISK LEVEL
# =========================================================

def get_risk_level(score):

    if score < 45:
        return "High Risk"

    elif score < 60:
        return "Medium Risk"

    else:
        return "Low Risk"


df["Risk_Level"] = df["Final_Score"].apply(
    get_risk_level
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Student Performance AI")

st.sidebar.caption(
    "Academic Intelligence System"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🤖 Performance Prediction",
        "📊 Academic Analytics",
        "🚨 At-Risk Students",
        "👤 Student Profile",
        "👨‍🎓 Student Records",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")

# =========================================================
# USER LOGIN INFORMATION
# =========================================================

logged_user = st.session_state.get(
    "username",
    "Admin"
)

st.sidebar.success(
    f"🔐 Logged in as: {logged_user}"
)


# =========================================================
# LOGOUT BUTTON
# =========================================================

if st.sidebar.button(
    "🚪 Logout",
    width="stretch",
    key="logout_button"
):
    st.session_state["logged_in"] = False
    st.session_state.pop("username", None)
    st.rerun()


st.sidebar.markdown("---")

st.sidebar.markdown("---")

st.sidebar.caption(
    "BCA Final Year Project"
)

# =========================================================
# DASHBOARD
# =========================================================

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    # -----------------------------------------------------
    # PROFESSIONAL DASHBOARD HEADER
    # -----------------------------------------------------

    st.markdown(
        """
        <div style="
            padding: 28px;
            border-radius: 18px;
            background: linear-gradient(135deg, #eef2ff, #f8fafc);
            border: 1px solid #dbeafe;
            margin-bottom: 25px;
        ">
            <h1 style="
                color: #1e3a8a;
                font-size: 36px;
                margin-bottom: 8px;
            ">
                🎓 Student Performance AI
            </h1>
            <p style="
                color: #475569;
                font-size: 17px;
                margin-bottom: 5px;
            ">
                Machine Learning Based Student Performance
                Prediction & Academic Analytics System
            </p>
            <p style="
                color: #64748b;
                font-size: 14px;
                margin-bottom: 0;
            ">
                Monitor academic performance, analyze student data,
                and identify students who may need additional support.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    total_students = len(df)

    average_score = df["Final_Score"].mean()

    average_attendance = df["Attendance"].mean()

    at_risk_students = (
        df["Risk_Level"] != "Low Risk"
    ).sum()

    # -----------------------------------------------------
    # TOP METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "📈 Average Score",
            f"{average_score:.2f}%"
        )

    with col3:
        st.metric(
            "📅 Avg Attendance",
            f"{average_attendance:.2f}%"
        )

    with col4:
        st.metric(
            "⚠️ At-Risk Students",
            at_risk_students
        )

    # -----------------------------------------------------
    # PERFORMANCE OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 Performance Overview'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # PERFORMANCE PIE CHART
    # -----------------------------------------------------

    with col1:

        performance_counts = (
            df["Performance"]
            .value_counts()
            .reset_index()
        )

        performance_counts.columns = [
            "Performance",
            "Students"
        ]

        fig = px.pie(
            performance_counts,
            names="Performance",
            values="Students",
            hole=0.5,
            title="Performance Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            title_x=0.05,
            legend_title_text="Performance",
            margin=dict(t=60, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # -----------------------------------------------------
    # ATTENDANCE VS SCORE
    # -----------------------------------------------------

    with col2:

        fig = px.scatter(
            df,
            x="Attendance",
            y="Final_Score",
            color="Performance",
            hover_data=[
                "Student_ID",
                "Study_Hours"
            ],
            title="Attendance vs Final Score",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            title_x=0.05,
            xaxis_title="Attendance (%)",
            yaxis_title="Final Score",
            legend_title_text="Performance",
            margin=dict(t=60, b=30, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # -----------------------------------------------------
    # RISK DISTRIBUTION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🚨 Student Risk Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk_Level",
        "Students"
    ]

    fig = px.bar(
        risk_counts,
        x="Risk_Level",
        y="Students",
        color="Risk_Level",
        text_auto=True,
        title="Student Risk Distribution",
        color_discrete_map={
            "High Risk": "#ef4444",
            "Medium Risk": "#f59e0b",
            "Low Risk": "#22c55e"
        }
    )

    fig.update_layout(
        title_x=0.05,
        xaxis_title="Risk Category",
        yaxis_title="Number of Students",
        showlegend=False,
        margin=dict(t=60, b=30, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------------------------------------
    # SCORE DISTRIBUTION
    # -----------------------------------------------------

    fig = px.histogram(
        df,
        x="Final_Score",
        nbins=20,
        title="Final Score Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # -----------------------------------------------------
    # AT-RISK STUDENTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '⚠️ Students Requiring Attention'
        '</div>',
        unsafe_allow_html=True
    )


    risk_students = df[
        df["Risk_Level"] != "Low Risk"
    ].copy()


    if len(risk_students) > 0:

        risk_students = risk_students[
            [
                "Student_ID",
                "Attendance",
                "Study_Hours",
                "Internal_Marks",
                "Final_Score",
                "Performance",
                "Risk_Level"
            ]
        ]

        risk_students = risk_students.sort_values(
            "Final_Score"
        )

        st.dataframe(
            risk_students.head(10),
            width="stretch",
            hide_index=True
        )

        st.info(
            f"Showing the 10 students with the lowest "
            f"predicted/recorded performance. "
            f"Total students requiring attention: "
            f"{len(risk_students)}"
        )

    else:

        st.success(
            "No students currently require attention."
        )

# =========================================================
# AT-RISK STUDENTS
# =========================================================

elif page == "🚨 At-Risk Students":

    st.markdown(
        '<div class="dashboard-title">'
        '🚨 At-Risk Students'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Identify students who may require additional academic attention.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # CREATE RISK DATA
    # -----------------------------------------------------

    risk_data = df.copy()

    high_risk = risk_data[
        risk_data["Risk_Level"] == "High Risk"
    ]

    medium_risk = risk_data[
        risk_data["Risk_Level"] == "Medium Risk"
    ]

    low_risk = risk_data[
        risk_data["Risk_Level"] == "Low Risk"
    ]


    # -----------------------------------------------------
    # RISK SUMMARY
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Risk Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🔴 High Risk",
            len(high_risk)
        )

    with col2:

        st.metric(
            "🟠 Medium Risk",
            len(medium_risk)
        )

    with col3:

        st.metric(
            "🟢 Low Risk",
            len(low_risk)
        )

    with col4:

        total_risk = len(high_risk) + len(medium_risk)

        st.metric(
            "⚠️ Total At-Risk",
            total_risk
        )


    # -----------------------------------------------------
    # RISK DISTRIBUTION CHART
    # -----------------------------------------------------

    st.markdown(
        "### 📈 Risk Distribution"
    )

    risk_chart_data = pd.DataFrame({
        "Risk Level": [
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ],
        "Students": [
            len(high_risk),
            len(medium_risk),
            len(low_risk)
        ]
    })

    fig = px.bar(
        risk_chart_data,
        x="Risk Level",
        y="Students",
        text_auto=True,
        title="Student Risk Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # -----------------------------------------------------
    # RISK FILTER
    # -----------------------------------------------------

    st.markdown(
        "### 🔎 Filter Students"
    )

    selected_risk = st.selectbox(
        "Select Risk Level",
        [
            "All At-Risk Students",
            "High Risk",
            "Medium Risk"
        ],
        key="risk_filter"
    )


    if selected_risk == "High Risk":

        filtered_students = high_risk.copy()

    elif selected_risk == "Medium Risk":

        filtered_students = medium_risk.copy()

    else:

        filtered_students = risk_data[
            risk_data["Risk_Level"] != "Low Risk"
        ].copy()


    # -----------------------------------------------------
    # SORT BY SCORE
    # -----------------------------------------------------

    filtered_students = filtered_students.sort_values(
        "Final_Score"
    )


    # -----------------------------------------------------
    # DISPLAY STUDENTS
    # -----------------------------------------------------

    st.markdown(
        "### 👨‍🎓 Students Requiring Attention"
    )


    if len(filtered_students) > 0:

        display_columns = [
            "Student_ID",
            "Attendance",
            "Study_Hours",
            "Assignment_Score",
            "Internal_Marks",
            "Previous_Marks",
            "Participation",
            "Final_Score",
            "Performance",
            "Risk_Level"
        ]

        st.dataframe(
            filtered_students[display_columns],
            width="stretch",
            height=450,
            hide_index=True
        )


        # -------------------------------------------------
        # AI RECOMMENDATIONS
        # -------------------------------------------------

        st.markdown(
            "### 🤖 AI Academic Recommendations"
        )

        st.info(
            "Students listed above may benefit from "
            "additional academic support based on their "
            "attendance, study habits and academic scores."
        )


        # -------------------------------------------------
        # DOWNLOAD REPORT
        # -------------------------------------------------

        csv_data = filtered_students[
            display_columns
        ].to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="📥 Download At-Risk Student Report",
            data=csv_data,
            file_name="at_risk_students_report.csv",
            mime="text/csv",
            width="stretch",
            key="download_risk_report"
        )


    else:

        st.success(
            "🎉 No students found in the selected risk category."
        )


    # -----------------------------------------------------
    # HIGH RISK DETAILS
    # -----------------------------------------------------

    if len(high_risk) > 0:

        st.markdown("---")

        st.markdown(
            "### 🔴 High Risk Student Details"
        )

        top_risk = high_risk.sort_values(
            "Final_Score"
        ).head(10)


        for _, student in top_risk.iterrows():

            with st.expander(
                f"🔴 {student['Student_ID']} — "
                f"Score: {student['Final_Score']:.2f}%"
            ):

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:

                    st.write(
                        f"**Attendance:** "
                        f"{student['Attendance']}%"
                    )

                    st.write(
                        f"**Study Hours:** "
                        f"{student['Study_Hours']} hours/day"
                    )

                    st.write(
                        f"**Assignment Score:** "
                        f"{student['Assignment_Score']}%"
                    )

                with detail_col2:

                    st.write(
                        f"**Internal Marks:** "
                        f"{student['Internal_Marks']}%"
                    )

                    st.write(
                        f"**Previous Marks:** "
                        f"{student['Previous_Marks']}%"
                    )

                    st.write(
                        f"**Participation:** "
                        f"{student['Participation']}%"
                    )


                # AI recommendation based on factors

                recommendations = []


                if student["Attendance"] < 75:

                    recommendations.append(
                        "Improve class attendance."
                    )


                if student["Study_Hours"] < 3:

                    recommendations.append(
                        "Increase daily study hours."
                    )


                if student["Assignment_Score"] < 60:

                    recommendations.append(
                        "Focus more on assignments."
                    )


                if student["Internal_Marks"] < 60:

                    recommendations.append(
                        "Improve internal examination preparation."
                    )


                if student["Previous_Marks"] < 60:

                    recommendations.append(
                        "Work on improving previous academic performance."
                    )


                if student["Participation"] < 60:

                    recommendations.append(
                        "Increase classroom participation."
                    )


                if not recommendations:

                    recommendations.append(
                        "Provide regular academic monitoring."
                    )


                st.markdown(
                    "**💡 Recommended Actions:**"
                )


                for recommendation in recommendations:

                    st.info(
                        f"• {recommendation}"
                    )

# =========================================================
# PROFESSIONAL STUDENT PROFILE
# =========================================================

elif page == "👤 Student Profile":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '👤 Student Profile'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Detailed academic profile, performance analysis, '
        'and personalized academic recommendations.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # STUDENT SELECTION
    # -----------------------------------------------------

    st.markdown("### 🔎 Select Student")

    student_ids = df["Student_ID"].tolist()

    selected_student = st.selectbox(
        "Select Student ID",
        student_ids,
        key="student_profile_select"
    )

    student = df[
        df["Student_ID"] == selected_student
    ].iloc[0]

    # -----------------------------------------------------
    # STUDENT PROFILE HEADER
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            padding: 25px;
            border-radius: 15px;
            margin: 15px 0;
        ">
            <div style="
                color: #dbeafe;
                font-size: 14px;
                font-weight: 600;
            ">
                STUDENT ACADEMIC PROFILE
            </div>
            <div style="
                color: white;
                font-size: 30px;
                font-weight: 700;
                margin-top: 8px;
            ">
                👨‍🎓 {selected_student}
            </div>
            <div style="
                color: #eff6ff;
                font-size: 15px;
                margin-top: 6px;
            ">
                Performance insights and academic progress
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # PERFORMANCE METRICS
    # -----------------------------------------------------

    st.markdown("### 📌 Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🎯 Final Score",
            f"{student['Final_Score']:.2f}%"
        )

    with col2:
        st.metric(
            "🏆 Performance",
            str(student["Performance"])
        )

    with col3:
        st.metric(
            "🚦 Risk Level",
            str(student["Risk_Level"])
        )

    with col4:
        st.metric(
            "📅 Attendance",
            f"{student['Attendance']:.1f}%"
        )

    st.markdown("### 📈 Final Score Indicator")

    st.progress(
        min(100, max(0, int(round(float(student["Final_Score"]))))),
        text=f"Final Academic Score: {student['Final_Score']:.2f}%"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # ACADEMIC INFORMATION
    # -----------------------------------------------------

    st.markdown("### 📋 Academic Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown("#### 📚 Learning & Attendance")

        st.write(
            f"**📅 Attendance:** {student['Attendance']:.1f}%"
        )

        st.write(
            f"**⏱️ Daily Study Hours:** {student['Study_Hours']:.1f} hours"
        )

        st.write(
            f"**📝 Assignment Score:** {student['Assignment_Score']:.1f}%"
        )

    with info_col2:

        st.markdown("#### 🎓 Assessment & Participation")

        st.write(
            f"**📖 Internal Marks:** {student['Internal_Marks']:.1f}%"
        )

        st.write(
            f"**📊 Previous Marks:** {student['Previous_Marks']:.1f}%"
        )

        st.write(
            f"**🙋 Class Participation:** {student['Participation']:.1f}%"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # ACADEMIC FACTORS CHART
    # -----------------------------------------------------

    st.markdown("### 📊 Academic Performance Analysis")

    st.caption(
        f"Academic factor analysis for {selected_student}."
    )

    factor_data = pd.DataFrame({
        "Factor": [
            "Attendance",
            "Assignment Score",
            "Internal Marks",
            "Previous Marks",
            "Participation"
        ],
        "Score": [
            student["Attendance"],
            student["Assignment_Score"],
            student["Internal_Marks"],
            student["Previous_Marks"],
            student["Participation"]
        ]
    })

    fig = px.bar(
        factor_data,
        x="Factor",
        y="Score",
        text_auto=".1f",
        range_y=[0, 110],
        color="Score",
        color_continuous_scale="Blues",
        title=f"{selected_student} - Academic Factors",
        labels={
            "Factor": "Academic Factor",
            "Score": "Score (%)"
        }
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Score: %{y:.1f}%"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title_x=0.02,
        title_font_size=20,
        xaxis_title="Academic Factor",
        yaxis_title="Score (%)",
        yaxis=dict(
            range=[0, 110],
            dtick=20
        ),
        coloraxis_showscale=False,
        margin=dict(
            t=70,
            b=70,
            l=30,
            r=30
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # PERSONALIZED ACADEMIC RECOMMENDATIONS
    # -----------------------------------------------------

    st.markdown("### 🤖 AI Academic Recommendations")

    st.caption(
        "Personalized suggestions based on the student's academic indicators."
    )

    recommendations = []

    if student["Attendance"] < 75:
        recommendations.append(
            "Improve class attendance to maintain consistent academic progress."
        )

    if student["Study_Hours"] < 3:
        recommendations.append(
            "Increase daily study hours and follow a regular study schedule."
        )

    if student["Assignment_Score"] < 60:
        recommendations.append(
            "Focus on assignments and submit academic work regularly."
        )

    if student["Internal_Marks"] < 60:
        recommendations.append(
            "Improve preparation for internal examinations."
        )

    if student["Previous_Marks"] < 60:
        recommendations.append(
            "Work on weaker subjects and strengthen academic fundamentals."
        )

    if student["Participation"] < 60:
        recommendations.append(
            "Increase classroom participation and interaction with teachers."
        )

    if not recommendations:
        recommendations.append(
            "Maintain the current academic performance and study habits."
        )

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.markdown(
            f"""
            <div style="
                background-color: #f0f7ff;
                border-left: 5px solid #2563eb;
                padding: 15px 18px;
                border-radius: 10px;
                margin-bottom: 12px;
            ">
                <div style="
                    color: #1e40af;
                    font-size: 13px;
                    font-weight: 700;
                    margin-bottom: 6px;
                ">
                    RECOMMENDATION {index}
                </div>
                <div style="
                    color: #1f2937;
                    font-size: 16px;
                ">
                    💡 {recommendation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # -----------------------------------------------------
    # STUDENT RISK STATUS
    # -----------------------------------------------------

    st.markdown("### 🚦 Academic Risk Assessment")

    if student["Risk_Level"] == "High Risk":

        st.error(
            "🔴 High Risk: This student may require additional academic support."
        )

    elif student["Risk_Level"] == "Medium Risk":

        st.warning(
            "🟠 Medium Risk: Monitor academic progress and encourage improvement."
        )

    else:

        st.success(
            "🟢 Low Risk: The student is currently in the low-risk category."
        )

    # -----------------------------------------------------
    # DOWNLOAD STUDENT PROFILE PDF
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown("### 📄 Student Profile Report")

    profile_pdf = generate_pdf_report(
        student_name=str(selected_student),
        predicted_score=round(
            float(student["Final_Score"]),
            2
        ),
        performance=str(student["Performance"]),
        risk=str(student["Risk_Level"]),
        attendance=float(student["Attendance"]),
        study_hours=float(student["Study_Hours"]),
        assignment_score=float(student["Assignment_Score"]),
        internal_marks=float(student["Internal_Marks"]),
        previous_marks=float(student["Previous_Marks"]),
        participation=float(student["Participation"]),
        recommendations=recommendations.copy()
    )

    st.download_button(
        label="📥 Download Student Profile Report",
        data=profile_pdf,
        file_name=f"{selected_student}_Profile_Report.pdf",
        mime="application/pdf",
        width="stretch",
        key="download_profile_pdf"
    )

# =========================================================
# PERFORMANCE PREDICTION
# =========================================================

elif page == "🤖 Performance Prediction":

    # -----------------------------------------------------
    # SUCCESS MESSAGE
    # -----------------------------------------------------

    if "save_success" in st.session_state:

        st.success(
            st.session_state["save_success"]
        )

        del st.session_state["save_success"]


    # -----------------------------------------------------
    # PAGE TITLE
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '🤖 Performance Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Enter student academic information to predict performance using Machine Learning.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # INPUT SECTION
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        student_name = st.text_input(
            "👤 Student Name",
            placeholder="Enter student name",
            key="prediction_student_name"
        )

        attendance = st.slider(
            "📅 Attendance (%)",
            0,
            100,
            75,
            key="prediction_attendance"
        )

        study_hours = st.slider(
            "📚 Daily Study Hours",
            0.0,
            12.0,
            3.0,
            0.5,
            key="prediction_study_hours"
        )

        assignment_score = st.slider(
            "📝 Assignment Score",
            0,
            100,
            70,
            key="prediction_assignment"
        )


    with col2:

        internal_marks = st.slider(
            "📖 Internal Marks",
            0,
            100,
            70,
            key="prediction_internal"
        )

        previous_marks = st.slider(
            "📊 Previous Marks",
            0,
            100,
            70,
            key="prediction_previous"
        )

        participation = st.slider(
            "🙋 Class Participation",
            0,
            100,
            70,
            key="prediction_participation"
        )


    st.markdown("")


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    predict_button = st.button(
        "🤖 Predict Student Performance",
        width="stretch",
        key="predict_student_button"
    )


    # -----------------------------------------------------
    # RUN PREDICTION
    # -----------------------------------------------------

    if predict_button:

        if not student_name.strip():

            st.warning(
                "Please enter student name."
            )

        else:

            student_data = pd.DataFrame({
                "Attendance": [attendance],
                "Study_Hours": [study_hours],
                "Assignment_Score": [assignment_score],
                "Internal_Marks": [internal_marks],
                "Previous_Marks": [previous_marks],
                "Participation": [participation]
            })


            predicted_score = model.predict(
                student_data
            )[0]


            predicted_score = max(
                0,
                min(100, predicted_score)
            )

            predicted_score = round(
                predicted_score,
                2
            )


            # -------------------------------------------------
            # PERFORMANCE CATEGORY
            # -------------------------------------------------

            if predicted_score >= 75:

                performance = "Excellent"

            elif predicted_score >= 60:

                performance = "Good"

            elif predicted_score >= 45:

                performance = "Average"

            else:

                performance = "At Risk"


            # -------------------------------------------------
            # RISK LEVEL
            # -------------------------------------------------

            risk = get_risk_level(
                predicted_score
            )


            # -------------------------------------------------
            # AI RECOMMENDATIONS
            # -------------------------------------------------

            recommendations = []


            if attendance < 75:

                recommendations.append(
                    "Improve attendance."
                )


            if study_hours < 3:

                recommendations.append(
                    "Increase daily study hours."
                )


            if assignment_score < 60:

                recommendations.append(
                    "Focus more on assignments."
                )


            if internal_marks < 60:

                recommendations.append(
                    "Improve internal examination preparation."
                )


            if previous_marks < 60:

                recommendations.append(
                    "Work on previous academic performance."
                )


            if participation < 60:

                recommendations.append(
                    "Participate more actively in class."
                )


            if not recommendations:

                recommendations.append(
                    "Maintain the current academic performance."
                )


            # -------------------------------------------------
            # SAVE RESULT IN SESSION STATE
            # -------------------------------------------------

            st.session_state["prediction_result"] = {
                "student_name": student_name,
                "attendance": attendance,
                "study_hours": study_hours,
                "assignment_score": assignment_score,
                "internal_marks": internal_marks,
                "previous_marks": previous_marks,
                "participation": participation,
                "predicted_score": predicted_score,
                "performance": performance,
                "risk": risk,
                "recommendations": recommendations
            }


    # =====================================================
    # DISPLAY PREDICTION RESULT
    # =====================================================

    if "prediction_result" in st.session_state:

        result = st.session_state["prediction_result"]


        student_name = result["student_name"]
        attendance = result["attendance"]
        study_hours = result["study_hours"]
        assignment_score = result["assignment_score"]
        internal_marks = result["internal_marks"]
        previous_marks = result["previous_marks"]
        participation = result["participation"]
        predicted_score = result["predicted_score"]
        performance = result["performance"]
        risk = result["risk"]
        recommendations = result["recommendations"]


        st.success(
            f"Prediction completed for {student_name}!"
        )


        # -------------------------------------------------
        # RESULT TITLE
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📊 Prediction Result'
            '</div>',
            unsafe_allow_html=True
        )


        result1, result2, result3 = st.columns(3)


        with result1:

            st.metric(
                "🎯 Predicted Score",
                f"{predicted_score}%"
            )


        with result2:

            st.metric(
                "🏆 Performance",
                performance
            )


        with result3:

            st.metric(
                "⚠️ Risk Level",
                risk
            )


        # -------------------------------------------------
        # PROGRESS BAR
        # -------------------------------------------------

                # -------------------------------------------------
        # PROFESSIONAL PREDICTION RESULT
        # -------------------------------------------------

        st.markdown(
            "## 📊 Prediction Result"
        )

        st.caption(
            f"AI-generated academic assessment for {student_name}"
        )

        result1, result2, result3 = st.columns(3)

        with result1:
            st.metric(
                label="🎯 Predicted Score",
                value=f"{predicted_score:.2f}%",
                help="Score predicted by the trained machine learning model."
            )

        with result2:
            st.metric(
                label="🏆 Performance Category",
                value=performance
            )

        with result3:
            st.metric(
                label="🚦 Academic Risk",
                value=risk
            )

        # Performance indicator

        st.markdown("### 📈 Performance Indicator")

        st.progress(
            int(round(predicted_score)),
            text=f"Predicted Academic Score: {predicted_score:.2f}%"
        )

        if performance == "Excellent":
            st.success("🌟 Excellent performance! Keep up the good work.")

        elif performance == "Good":
            st.info("👍 Good performance! Consistent effort can improve results further.")

        elif performance == "Average":
            st.warning("📚 Average performance. Focus on weaker academic areas.")

        else:
            st.error("⚠️ The predicted score indicates that additional academic support may be needed.")


                # -------------------------------------------------
        # PROFESSIONAL ACADEMIC FACTORS CHART
        # -------------------------------------------------

        st.markdown("---")

        st.markdown(
            "### 📊 Academic Performance Analysis"
        )

        st.caption(
            f"Academic factor analysis for {student_name}"
        )

        factor_data = pd.DataFrame({
            "Factor": [
                "Attendance",
                "Assignment Score",
                "Internal Marks",
                "Previous Marks",
                "Participation"
            ],
            "Score": [
                attendance,
                assignment_score,
                internal_marks,
                previous_marks,
                participation
            ]
        })

        fig = px.bar(
            factor_data,
            x="Factor",
            y="Score",
            text_auto=".1f",
            range_y=[0, 110],
            color="Score",
            color_continuous_scale="Blues",
            title=f"{student_name} - Academic Factors",
            labels={
                "Factor": "Academic Factor",
                "Score": "Score (%)"
            }
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Score: %{y:.1f}%"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            title_x=0.02,
            title_font_size=20,
            xaxis_title="Academic Factor",
            yaxis_title="Score (%)",
            yaxis=dict(
                range=[0, 110],
                dtick=20
            ),
            coloraxis_showscale=False,
            margin=dict(
                t=70,
                b=70,
                l=30,
                r=30
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                size=13
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # PDF REPORT
        # =================================================

        st.markdown("---")

        st.markdown(
            "### 📄 Student Performance Report"
        )


        pdf_file = generate_pdf_report(
            student_name=student_name,
            predicted_score=predicted_score,
            performance=performance,
            risk=risk,
            attendance=attendance,
            study_hours=study_hours,
            assignment_score=assignment_score,
            internal_marks=internal_marks,
            previous_marks=previous_marks,
            participation=participation,
            recommendations=recommendations
        )


        st.download_button(
            label="📥 Download Student Performance Report",
            data=pdf_file,
            file_name=f"{student_name}_Performance_Report.pdf",
            mime="application/pdf",
            width="stretch",
            key="download_student_pdf"
        )


        # =================================================
        # SAVE TO DATABASE
        # =================================================

        st.markdown("---")

        st.markdown(
            "### 💾 Save Student Record"
        )


        if st.button(
            "💾 Save Prediction to Database",
            width="stretch",
            key="save_prediction_button"
        ):

            save_prediction(
                student_name=student_name,
                attendance=attendance,
                study_hours=study_hours,
                assignment_score=assignment_score,
                internal_marks=internal_marks,
                previous_marks=previous_marks,
                participation=participation,
                predicted_score=predicted_score,
                performance=performance,
                risk_level=risk
            )


            st.session_state["save_success"] = (
                f"✅ {student_name}'s prediction has been "
                f"saved successfully to the database!"
            )


            st.rerun()           

# =========================================================
# PROFESSIONAL ACADEMIC ANALYTICS
# =========================================================

elif page == "📊 Academic Analytics":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '📊 Academic Analytics Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Explore student performance trends, academic factors, '
        'and the relationship between study habits and results.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # ACADEMIC SUMMARY METRICS
    # -----------------------------------------------------

    st.markdown("### 📌 Academic Summary")

    avg_attendance = df["Attendance"].mean()
    avg_assignment = df["Assignment_Score"].mean()
    avg_internal = df["Internal_Marks"].mean()
    avg_previous = df["Previous_Marks"].mean()
    avg_participation = df["Participation"].mean()
    avg_study_hours = df["Study_Hours"].mean()
    avg_final_score = df["Final_Score"].mean()

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "📚 Average Final Score",
            f"{avg_final_score:.1f}%"
        )

    with metric2:
        st.metric(
            "📅 Average Attendance",
            f"{avg_attendance:.1f}%"
        )

    with metric3:
        st.metric(
            "⏱️ Daily Study Hours",
            f"{avg_study_hours:.1f} hrs"
        )

    metric4, metric5, metric6 = st.columns(3)

    with metric4:
        st.metric(
            "📝 Assignment Score",
            f"{avg_assignment:.1f}%"
        )

    with metric5:
        st.metric(
            "📖 Internal Marks",
            f"{avg_internal:.1f}%"
        )

    with metric6:
        st.metric(
            "🙋 Participation",
            f"{avg_participation:.1f}%"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # AVERAGE ACADEMIC FACTORS
    # -----------------------------------------------------

    st.markdown("### 📊 Average Academic Factors")

    st.caption(
        "Comparison of average scores across different academic factors."
    )

    factors = pd.DataFrame({
        "Metric": [
            "Attendance",
            "Assignment Score",
            "Internal Marks",
            "Previous Marks",
            "Participation"
        ],
        "Average": [
            avg_attendance,
            avg_assignment,
            avg_internal,
            avg_previous,
            avg_participation
        ]
    })

    fig = px.bar(
        factors,
        x="Metric",
        y="Average",
        text_auto=".1f",
        color="Average",
        color_continuous_scale="Blues",
        range_y=[0, 110],
        labels={
            "Metric": "Academic Factor",
            "Average": "Average Score (%)"
        },
        title="Average Performance Across Academic Factors"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average: %{y:.1f}%"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title_x=0.02,
        title_font_size=20,
        xaxis_title="Academic Factor",
        yaxis_title="Average Score (%)",
        yaxis=dict(
            range=[0, 110],
            dtick=20
        ),
        coloraxis_showscale=False,
        margin=dict(
            t=80,
            b=70,
            l=30,
            r=30
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # STUDY HOURS VS FINAL SCORE
    # -----------------------------------------------------

    st.markdown("### ⏱️ Study Hours vs Final Score")

    st.caption(
        "Explore how daily study hours relate to students' final scores."
    )

    fig = px.scatter(
        df,
        x="Study_Hours",
        y="Final_Score",
        color="Performance",
        hover_data=[
            "Student_ID",
            "Attendance"
        ],
        color_discrete_map={
            "Excellent": "#16a34a",
            "Good": "#2563eb",
            "Average": "#f59e0b",
            "At Risk": "#dc2626"
        },
        labels={
            "Study_Hours": "Daily Study Hours",
            "Final_Score": "Final Score (%)",
            "Performance": "Performance Category"
        },
        title="Relationship Between Study Hours and Final Score"
    )

    fig.update_traces(
        marker=dict(size=9, opacity=0.75),
        hovertemplate=(
            "Study Hours: %{x}<br>"
            "Final Score: %{y:.1f}%"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title_x=0.02,
        title_font_size=20,
        xaxis_title="Daily Study Hours",
        yaxis_title="Final Score (%)",
        margin=dict(
            t=80,
            b=50,
            l=30,
            r=30
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # INTERNAL MARKS VS FINAL SCORE
    # -----------------------------------------------------

    st.markdown("### 📝 Internal Marks vs Final Score")

    st.caption(
        "Compare internal assessment marks with students' final scores."
    )

    fig = px.scatter(
        df,
        x="Internal_Marks",
        y="Final_Score",
        color="Performance",
        hover_data=[
            "Student_ID",
            "Attendance",
            "Study_Hours"
        ],
        color_discrete_map={
            "Excellent": "#16a34a",
            "Good": "#2563eb",
            "Average": "#f59e0b",
            "At Risk": "#dc2626"
        },
        labels={
            "Internal_Marks": "Internal Marks (%)",
            "Final_Score": "Final Score (%)",
            "Performance": "Performance Category"
        },
        title="Internal Assessment vs Final Score"
    )

    fig.update_traces(
        marker=dict(size=9, opacity=0.75)
    )

    fig.update_layout(
        title_x=0.02,
        title_font_size=20,
        xaxis_title="Internal Marks (%)",
        yaxis_title="Final Score (%)",
        margin=dict(
            t=80,
            b=50,
            l=30,
            r=30
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------------------------------------
    # ACADEMIC INSIGHTS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown("### 💡 Academic Insights")

    insight1, insight2 = st.columns(2)

    with insight1:
        st.info(
            f"📚 **Average Study Time:** Students study for "
            f"approximately {avg_study_hours:.1f} hours daily on average."
        )

    with insight2:
        st.info(
            f"🎯 **Average Final Score:** The dataset's average "
            f"final score is {avg_final_score:.1f}%."
        )

    st.caption(
        "Note: These insights describe the available dataset. "
        "Relationships in the charts do not by themselves prove causation."
    )


# =========================================================
# PROFESSIONAL AT-RISK STUDENTS DASHBOARD
# =========================================================

elif page == "🚨 At-Risk Students":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '🚨 At-Risk Students Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Identify students who may need additional academic '
        'support and monitor their performance indicators.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # RISK CATEGORIES
    # -----------------------------------------------------

    high_risk = df[df["Risk_Level"] == "High Risk"].copy()
    medium_risk = df[df["Risk_Level"] == "Medium Risk"].copy()
    low_risk = df[df["Risk_Level"] == "Low Risk"].copy()

    total_students = len(df)
    total_at_risk = len(high_risk) + len(medium_risk)

    high_risk_pct = (
        len(high_risk) / total_students * 100
        if total_students > 0 else 0
    )

    medium_risk_pct = (
        len(medium_risk) / total_students * 100
        if total_students > 0 else 0
    )

    low_risk_pct = (
        len(low_risk) / total_students * 100
        if total_students > 0 else 0
    )

    # -----------------------------------------------------
    # SUMMARY METRICS
    # -----------------------------------------------------

    st.markdown("### 📌 Student Risk Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "🔴 High Risk",
            len(high_risk),
            help="Students with a final score below 45."
        )

    with col3:
        st.metric(
            "🟠 Medium Risk",
            len(medium_risk),
            help="Students with a final score from 45 to below 60."
        )

    with col4:
        st.metric(
            "🟢 Low Risk",
            len(low_risk),
            help="Students with a final score of 60 or above."
        )

    st.markdown("---")

    # -----------------------------------------------------
    # RISK DISTRIBUTION
    # -----------------------------------------------------

    st.markdown("### 📊 Risk Distribution Analysis")

    risk_data = pd.DataFrame({
        "Risk Level": [
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ],
        "Students": [
            len(high_risk),
            len(medium_risk),
            len(low_risk)
        ],
        "Percentage": [
            high_risk_pct,
            medium_risk_pct,
            low_risk_pct
        ]
    })

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        fig = px.pie(
            risk_data,
            names="Risk Level",
            values="Students",
            hole=0.55,
            color="Risk Level",
            color_discrete_map={
                "High Risk": "#dc2626",
                "Medium Risk": "#f59e0b",
                "Low Risk": "#16a34a"
            },
            title="Student Risk Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Students: %{value}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            title_x=0.02,
            title_font_size=18,
            showlegend=False,
            margin=dict(t=65, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with chart_col2:

        fig = px.bar(
            risk_data,
            x="Risk Level",
            y="Students",
            text="Students",
            color="Risk Level",
            color_discrete_map={
                "High Risk": "#dc2626",
                "Medium Risk": "#f59e0b",
                "Low Risk": "#16a34a"
            },
            title="Number of Students by Risk Level",
            labels={
                "Risk Level": "Academic Risk",
                "Students": "Number of Students"
            }
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )

        fig.update_layout(
            title_x=0.02,
            title_font_size=18,
            showlegend=False,
            yaxis=dict(
                rangemode="tozero",
                dtick=5
            ),
            margin=dict(t=65, b=40, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # STUDENT FILTERS
    # -----------------------------------------------------

    st.markdown("### 🔍 Find Students")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        selected_risk = st.selectbox(
            "Select Risk Level",
            [
                "All At-Risk Students",
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ]
        )

    with filter_col2:

        search_student = st.text_input(
            "Search Student ID",
            placeholder="Enter student ID, e.g. STU001"
        )

    # Select students according to risk level
    if selected_risk == "High Risk":
        filtered_df = high_risk.copy()

    elif selected_risk == "Medium Risk":
        filtered_df = medium_risk.copy()

    elif selected_risk == "Low Risk":
        filtered_df = low_risk.copy()

    else:
        filtered_df = df[
            df["Risk_Level"].isin(
                ["High Risk", "Medium Risk"]
            )
        ].copy()

    # Search by Student ID
    if search_student.strip():
        filtered_df = filtered_df[
            filtered_df["Student_ID"]
            .astype(str)
            .str.contains(
                search_student.strip(),
                case=False,
                na=False
            )
        ]

    # Sort from lowest score to highest
    filtered_df = filtered_df.sort_values(
        "Final_Score",
        ascending=True
    )

    st.markdown(
        f"**Students found: {len(filtered_df)}**"
    )

    # -----------------------------------------------------
    # STUDENT TABLE
    # -----------------------------------------------------

    display_columns = [
        "Student_ID",
        "Attendance",
        "Study_Hours",
        "Assignment_Score",
        "Internal_Marks",
        "Previous_Marks",
        "Final_Score",
        "Risk_Level"
    ]

    available_columns = [
        column for column in display_columns
        if column in filtered_df.columns
    ]

    if not filtered_df.empty:

        st.dataframe(
            filtered_df[available_columns],
            width="stretch",
            hide_index=True,
            column_config={
                "Student_ID": st.column_config.TextColumn(
                    "Student ID"
                ),
                "Attendance": st.column_config.ProgressColumn(
                    "Attendance (%)",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                ),
                "Study_Hours": st.column_config.NumberColumn(
                    "Daily Study Hours",
                    format="%.1f hrs"
                ),
                "Assignment_Score": st.column_config.NumberColumn(
                    "Assignment Score",
                    format="%.1f%%"
                ),
                "Internal_Marks": st.column_config.NumberColumn(
                    "Internal Marks",
                    format="%.1f%%"
                ),
                "Previous_Marks": st.column_config.NumberColumn(
                    "Previous Marks",
                    format="%.1f%%"
                ),
                "Final_Score": st.column_config.ProgressColumn(
                    "Final Score (%)",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                ),
                "Risk_Level": st.column_config.TextColumn(
                    "Risk Category"
                )
            }
        )

        # -------------------------------------------------
        # CSV DOWNLOAD
        # -------------------------------------------------

        csv_data = filtered_df[available_columns].to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 Download Filtered Student Report (CSV)",
            data=csv_data,
            file_name="at_risk_students_report.csv",
            mime="text/csv",
            width="stretch",
            key="download_at_risk_report"
        )

    else:

        st.info(
            "No students match the selected risk level or search."
        )

    st.markdown("---")

    # -----------------------------------------------------
    # ACADEMIC SUPPORT RECOMMENDATIONS
    # -----------------------------------------------------

    st.markdown("### 💡 Academic Support Recommendations")

    recommendation_col1, recommendation_col2 = st.columns(2)

    with recommendation_col1:

        st.markdown(
            """
            <div style="
                background-color: #fef2f2;
                border-left: 5px solid #dc2626;
                padding: 16px;
                border-radius: 10px;
                margin-bottom: 12px;
            ">
                <h4 style="color: #991b1b; margin-top: 0;">
                    🔴 High Risk Students
                </h4>
                <p style="color: #374151;">
                    Review academic progress, identify weak subjects,
                    arrange additional guidance and monitor improvement
                    regularly.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with recommendation_col2:

        st.markdown(
            """
            <div style="
                background-color: #fffbeb;
                border-left: 5px solid #f59e0b;
                padding: 16px;
                border-radius: 10px;
                margin-bottom: 12px;
            ">
                <h4 style="color: #92400e; margin-top: 0;">
                    🟠 Medium Risk Students
                </h4>
                <p style="color: #374151;">
                    Encourage consistent study routines, assignment
                    completion, attendance and regular assessment review.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Risk levels are based on the project's configured score thresholds. "
        "They are indicators for academic support, not definitive judgments "
        "about a student's ability."
    )


# =========================================================
# PROFESSIONAL STUDENT RECORDS
# =========================================================

elif page == "👨‍🎓 Student Records":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '👨‍🎓 Student Records Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Search, filter and export student records and saved AI predictions.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # LOAD DATABASE RECORDS
    # -----------------------------------------------------

    saved_df = get_predictions()

    if saved_df is None:
        saved_df = pd.DataFrame()

    # -----------------------------------------------------
    # RECORD SUMMARY
    # -----------------------------------------------------

    st.markdown("### 📌 Records Overview")

    total_dataset_students = len(df)
    total_saved_predictions = len(saved_df)

    if (
        not saved_df.empty
        and "predicted_score" in saved_df.columns
    ):
        saved_average_score = pd.to_numeric(
            saved_df["predicted_score"],
            errors="coerce"
        ).mean()
    else:
        saved_average_score = None

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "👨‍🎓 Dataset Students",
            total_dataset_students
        )

    with metric2:
        st.metric(
            "💾 Saved Predictions",
            total_saved_predictions
        )

    with metric3:
        st.metric(
            "🎯 Average Saved Prediction",
            (
                f"{saved_average_score:.1f}%"
                if pd.notna(saved_average_score)
                else "N/A"
            )
        )

    st.markdown("---")

    # =====================================================
    # SAVED AI PREDICTIONS
    # =====================================================

    st.markdown("### 💾 Saved AI Predictions")

    st.caption(
        "Predictions saved through the Performance Prediction page."
    )

    if not saved_df.empty:

        st.success(
            f"✅ {total_saved_predictions} saved prediction(s) found."
        )

        saved_display = saved_df.copy()

        # -------------------------------------------------
        # SEARCH SAVED PREDICTIONS
        # -------------------------------------------------

        search_saved = st.text_input(
            "🔍 Search by Student Name",
            placeholder="Enter student name...",
            key="search_saved_student"
        )

        if "student_name" in saved_display.columns:
            saved_display = saved_display[
                saved_display["student_name"]
                .astype(str)
                .str.contains(
                    search_saved.strip(),
                    case=False,
                    na=False
                )
            ]

        # -------------------------------------------------
        # SAVED PREDICTION FILTERS
        # -------------------------------------------------

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:

            if "risk_level" in saved_display.columns:

                available_risks = saved_display[
                    "risk_level"
                ].dropna().astype(str).unique().tolist()

                selected_saved_risk = st.selectbox(
                    "🚦 Filter by Risk Level",
                    ["All"] + sorted(available_risks),
                    key="saved_prediction_risk_filter"
                )

                if selected_saved_risk != "All":

                    saved_display = saved_display[
                        saved_display["risk_level"].astype(str)
                        == selected_saved_risk
                    ]

        with filter_col2:

            if "performance" in saved_display.columns:

                available_performance = saved_display[
                    "performance"
                ].dropna().astype(str).unique().tolist()

                selected_performance = st.selectbox(
                    "🏆 Filter by Performance",
                    ["All"] + sorted(available_performance),
                    key="saved_prediction_performance_filter"
                )

                if selected_performance != "All":

                    saved_display = saved_display[
                        saved_display["performance"].astype(str)
                        == selected_performance
                    ]

        st.markdown(
            f"**Matching saved predictions: {len(saved_display)}**"
        )

        # -------------------------------------------------
        # DISPLAY SAVED RECORDS
        # -------------------------------------------------

        st.dataframe(
            saved_display,
            width="stretch",
            height=350,
            hide_index=True
        )

        # -------------------------------------------------
        # DOWNLOAD SAVED RECORDS
        # -------------------------------------------------

        saved_csv = saved_display.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 Download Saved Predictions (CSV)",
            data=saved_csv,
            file_name="saved_student_predictions.csv",
            mime="text/csv",
            width="stretch",
            key="download_saved_predictions"
        )

    else:

        st.info(
            "No saved AI predictions found. "
            "Generate a prediction and use Save Prediction to Database "
            "to add a record."
        )

    # =====================================================
    # ORIGINAL DATASET RECORDS
    # =====================================================

    st.markdown("---")

    st.markdown("### 📊 Original Student Dataset")

    st.caption(
        "Browse and filter students from the original academic dataset."
    )

    display_df = df.copy()

    # -----------------------------------------------------
    # SEARCH AND FILTERS
    # -----------------------------------------------------

    search_dataset = st.text_input(
        "🔍 Search Student ID",
        placeholder="Enter student ID, e.g. STU001",
        key="search_student_id"
    )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        available_categories = sorted(
            display_df["Performance"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "🏆 Filter by Performance",
            ["All"] + available_categories,
            key="dataset_performance_filter"
        )

    with filter_col2:

        available_risk_levels = sorted(
            display_df["Risk_Level"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_dataset_risk = st.selectbox(
            "🚦 Filter by Risk Level",
            ["All"] + available_risk_levels,
            key="dataset_risk_filter"
        )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    if search_dataset.strip():

        display_df = display_df[
            display_df["Student_ID"]
            .astype(str)
            .str.contains(
                search_dataset.strip(),
                case=False,
                na=False
            )
        ]

    if selected_category != "All":

        display_df = display_df[
            display_df["Performance"].astype(str)
            == selected_category
        ]

    if selected_dataset_risk != "All":

        display_df = display_df[
            display_df["Risk_Level"].astype(str)
            == selected_dataset_risk
        ]

    display_df = display_df.sort_values(
        "Final_Score",
        ascending=False
    )

    st.markdown(
        f"**Matching dataset records: {len(display_df)}**"
    )

    # -----------------------------------------------------
    # DATASET TABLE
    # -----------------------------------------------------

    st.dataframe(
        display_df,
        width="stretch",
        height=450,
        hide_index=True,
        column_config={
            "Student_ID": st.column_config.TextColumn(
                "Student ID"
            ),
            "Attendance": st.column_config.ProgressColumn(
                "Attendance (%)",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "Study_Hours": st.column_config.NumberColumn(
                "Study Hours",
                format="%.1f hrs"
            ),
            "Assignment_Score": st.column_config.NumberColumn(
                "Assignment Score",
                format="%.1f%%"
            ),
            "Internal_Marks": st.column_config.NumberColumn(
                "Internal Marks",
                format="%.1f%%"
            ),
            "Previous_Marks": st.column_config.NumberColumn(
                "Previous Marks",
                format="%.1f%%"
            ),
            "Participation": st.column_config.NumberColumn(
                "Participation",
                format="%.1f%%"
            ),
            "Final_Score": st.column_config.ProgressColumn(
                "Final Score (%)",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "Performance": st.column_config.TextColumn(
                "Performance Category"
            ),
            "Risk_Level": st.column_config.TextColumn(
                "Academic Risk"
            )
        }
    )

    # -----------------------------------------------------
    # DOWNLOAD ORIGINAL DATASET
    # -----------------------------------------------------

    dataset_csv = display_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Filtered Student Dataset (CSV)",
        data=dataset_csv,
        file_name="student_performance_report.csv",
        mime="text/csv",
        width="stretch",
        key="download_student_dataset"
    )


# =========================================================
# ABOUT PROJECT
# =========================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="dashboard-title">'
        'ℹ️ About Project'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        ## Student Performance Prediction & Academic Analytics System

        This is a Machine Learning based academic analytics
        application developed as a BCA Final Year Project.

        ### 🎯 Objectives

        - Predict student academic performance
        - Identify students who may require academic attention
        - Analyze attendance and academic factors
        - Generate data-driven recommendations
        - Visualize student performance
        - Support academic monitoring

        ### 🤖 Machine Learning

        The system uses a **Random Forest Regression**
        model to predict expected final scores.

        ### 📊 Analytics

        The application provides:

        - Performance distribution
        - Attendance analysis
        - Study hours analysis
        - Internal marks analysis
        - Risk-level analysis
        - Student records

        ### 🛠 Technologies

        - Python
        - Pandas
        - NumPy
        - Scikit-learn
        - Streamlit
        - Plotly
        - Machine Learning

        ### 📌 Project Type

        BCA Final Year Project
        """
    )