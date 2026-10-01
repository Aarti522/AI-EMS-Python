import joblib
import pandas as pd

model = joblib.load("models/performance_model.joblib")

FEATURES = [
    "attendancePercentage",
    "experienceYears",
    "projectsCompleted",
    "tasksCompleted",
    "previousRating",
    "trainingCompleted",
    "overtimeHours",
    "leaveDays"
]


def predict_performance(data):

    values = [[
        data.attendancePercentage,
        data.experienceYears,
        data.projectsCompleted,
        data.tasksCompleted,
        data.previousRating,
        data.trainingCompleted,
        data.overtimeHours,
        data.leaveDays
    ]]

    df = pd.DataFrame(values, columns=FEATURES)

    prediction = model.predict(df)[0]

    probabilities = model.predict_proba(df)[0]
    confidence = float(max(probabilities))

    return {
        "employeeId": data.employeeId,
        "prediction": prediction,
        "score": round(confidence * 100, 2),
        "confidence": round(confidence, 2)
    }