from pathlib import Path

import joblib
import pandas as pd


# Get the absolute path of the app directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model location: app/ml/attrition_model.joblib
MODEL_PATH = BASE_DIR / "ml" / "attrition_model.joblib"

# Load trained attrition model
model = joblib.load(MODEL_PATH)


FEATURES = [
    "age",
    "experienceYears",
    "monthlyIncome",
    "jobSatisfaction",
    "workLifeBalance",
    "overtimeHours",
    "yearsAtCompany",
    "promotionYearsAgo",
    "leaveDays"
]


def predict_attrition(data):

    input_data = {
        "age": data.age,
        "experienceYears": data.experienceYears,
        "monthlyIncome": data.monthlyIncome,
        "jobSatisfaction": data.jobSatisfaction,
        "workLifeBalance": data.workLifeBalance,
        "overtimeHours": data.overtimeHours,
        "yearsAtCompany": data.yearsAtCompany,
        "promotionYearsAgo": data.promotionYearsAgo,
        "leaveDays": data.leaveDays
    }

    df = pd.DataFrame([input_data], columns=FEATURES)

    prediction = model.predict(df)[0]

    probabilities = model.predict_proba(df)[0]
    confidence = float(max(probabilities))

    score = round(confidence * 100, 2)

    return {
        "employeeId": data.employeeId,
        "prediction": prediction,
        "score": score,
        "confidence": round(confidence, 2)
    }