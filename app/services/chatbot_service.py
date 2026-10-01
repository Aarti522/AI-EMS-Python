from google import genai
from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_chat_response(
    message: str,
    role: str,
    employeeId: int,
    context=None
):
    context_text = (
        str(context)
        if context
        else "No employee data was provided by the EMS backend."
    )

    prompt = f"""
You are an AI HR assistant for an Employee Management System.

User role: {role}
Employee ID: {employeeId}

AUTHORIZED EMS DATA:
{context_text}

ACCESS RULES:

EMPLOYEE:
- Answer only questions about their own authorized data.
- Never provide another employee's information.
- Employee cannot access attrition prediction or resume screening.

MANAGER:
- Answer only using authorized team data provided by the backend.
- Do not expose restricted salary information.

HR:
- Answer using authorized HR data provided by the backend.

IMPORTANT:
- Use ONLY the EMS data provided above for factual employee-specific answers.
- Never invent attendance, salary, leave, performance, or employee information.
- If required data is missing, clearly say that the required information
  is not available.
- Do not claim that you accessed the database yourself.

User question:
{message}

Give a concise and professional response.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()