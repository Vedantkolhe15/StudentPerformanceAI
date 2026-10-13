import pandas as pd
import numpy as np

np.random.seed(42)

students = 500

data = {
    "Student_ID": [f"STU{i:03d}" for i in range(1, students + 1)],

    "Attendance": np.random.randint(50, 101, students),

    "Study_Hours": np.round(
        np.random.uniform(1, 8, students), 1
    ),

    "Assignment_Score": np.random.randint(40, 101, students),

    "Internal_Marks": np.random.randint(35, 101, students),

    "Previous_Marks": np.random.randint(35, 101, students),

    "Participation": np.random.randint(30, 101, students)
}

df = pd.DataFrame(data)

# Calculate final score
score = (
    df["Attendance"] * 0.15
    + df["Study_Hours"] * 4
    + df["Assignment_Score"] * 0.20
    + df["Internal_Marks"] * 0.25
    + df["Previous_Marks"] * 0.20
    + df["Participation"] * 0.10
)

# Add small random variation
score += np.random.normal(0, 4, students)

df["Final_Score"] = np.clip(score, 0, 100).round(2)


# Performance category
def performance_category(score):

    if score >= 75:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 45:
        return "Average"

    else:
        return "At Risk"


df["Performance"] = df["Final_Score"].apply(
    performance_category
)


# Save dataset
df.to_csv(
    "data/student_performance.csv",
    index=False
)


print("====================================")
print(" DATASET CREATED SUCCESSFULLY")
print("====================================")

print(f"Total Students: {len(df)}")

print("\nFirst 5 Records:")
print(df.head())