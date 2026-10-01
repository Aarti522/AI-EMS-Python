import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATA_PATH = "data/attrition_data.csv"
MODEL_PATH = "models/attrition_model.joblib"

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

TARGET = "attritionRisk"


def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()