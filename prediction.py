import pandas as pd
import joblib


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "models/student_performance_model.pkl"
)


# ==========================================
# 2. PREDICTION FUNCTION
# ==========================================

def predict_student_performance(
    attendance,
    study_hours,
    assignment_score,
    internal_marks,
    previous_marks,
    participation
):

    # Create student data
    student_data = pd.DataFrame({
        "Attendance": [attendance],
        "Study_Hours": [study_hours],
        "Assignment_Score": [assignment_score],
        "Internal_Marks": [internal_marks],
        "Previous_Marks": [previous_marks],
        "Participation": [participation]
    })

    # Predict final score
    predicted_score = model.predict(student_data)[0]

    # Keep score between 0 and 100
    predicted_score = max(
        0,
        min(100, predicted_score)
    )

    predicted_score = round(
        predicted_score,
        2
    )


    # ==========================================
    # PERFORMANCE CATEGORY
    # ==========================================

    if predicted_score >= 75:
        performance = "Excellent"

    elif predicted_score >= 60:
        performance = "Good"

    elif predicted_score >= 45:
        performance = "Average"

    else:
        performance = "At Risk"


    # ==========================================
    # RISK LEVEL
    # ==========================================

    if predicted_score < 45:
        risk = "High Risk"

    elif predicted_score < 60:
        risk = "Medium Risk"

    else:
        risk = "Low Risk"


    # ==========================================
    # RECOMMENDATION
    # ==========================================

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
            "Work on improving previous academic performance."
        )

    if participation < 60:
        recommendations.append(
            "Participate more actively in class."
        )

    if not recommendations:
        recommendations.append(
            "Maintain the current academic performance."
        )


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {
        "predicted_score": predicted_score,
        "performance": performance,
        "risk": risk,
        "recommendations": recommendations
    }


# ==========================================
# TEST PREDICTION
# ==========================================

if __name__ == "__main__":

    result = predict_student_performance(
        attendance=85,
        study_hours=4,
        assignment_score=80,
        internal_marks=75,
        previous_marks=70,
        participation=80
    )

    print("\n====================================")
    print(" STUDENT PERFORMANCE PREDICTION")
    print("====================================")

    print(
        f"\nPredicted Score: "
        f"{result['predicted_score']}%"
    )

    print(
        f"Performance: "
        f"{result['performance']}"
    )

    print(
        f"Risk Level: "
        f"{result['risk']}"
    )

    print("\nRecommendations:")

    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")