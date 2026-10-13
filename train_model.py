import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/student_performance.csv")


# ==========================================
# 2. SELECT FEATURES
# ==========================================

features = [
    "Attendance",
    "Study_Hours",
    "Assignment_Score",
    "Internal_Marks",
    "Previous_Marks",
    "Participation"
]

X = df[features]

y = df["Final_Score"]


# ==========================================
# 3. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ==========================================
# 4. CREATE MACHINE LEARNING MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# ==========================================
# 5. TRAIN MODEL
# ==========================================

print("\nTraining Machine Learning Model...")

model.fit(X_train, y_train)


# ==========================================
# 6. MAKE PREDICTIONS
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# 7. MODEL EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n====================================")
print(" STUDENT PERFORMANCE ML MODEL")
print("====================================")

print(f"Mean Absolute Error : {mae:.2f}")

print(f"R2 Score            : {r2:.2f}")


# ==========================================
# 9. SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/student_performance_model.pkl"
)


print("\n====================================")
print(" MODEL TRAINING COMPLETED")
print("====================================")

print("Model saved successfully!")

print("\nLocation:")
print("models/student_performance_model.pkl")