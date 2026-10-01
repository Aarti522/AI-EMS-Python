from google import genai
from app.config import GEMINI_API_KEY
import json


client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_attendance(data):

    prompt = f"""
You are an AI HR attendance analyst.

Analyze the following employee attendance information.

Employee:
{data.employeeName}

Employee ID:
{data.employeeId}

Current Month Attendance:
{data.currentMonthAttendance}%

Previous Month Attendance:
{data.previousMonthAttendance}%

Late Days:
{data.lateDays}

Absent Days:
{data.absentDays}

Leave Days:
{data.leaveDays}

Your task:
1. Identify unusual attendance patterns.
2. Identify attendance decline if present.
3. Identify excessive absence or late-coming patterns.
4. Give a short HR recommendation.

IMPORTANT:
- Do not invent information.
- Do not make disciplinary decisions.
- This is only decision-support.
- riskLevel must be LOW, MEDIUM or HIGH.
- Return ONLY valid JSON.

Return exactly:

{{
  "employeeId": {data.employeeId},
  "riskLevel": "LOW",
  "summary": "string",
  "observations": [
    "string"
  ],
  "recommendation": "string"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)