from google import genai
from app.config import GEMINI_API_KEY
import json


client = genai.Client(api_key=GEMINI_API_KEY)


def screen_resume(resume_text: str, job_description: str):

    prompt = f"""
You are an AI recruitment assistant.

Analyze the candidate resume against the given job description.

IMPORTANT:
- Evaluate only job-related qualifications.
- Do not use gender, religion, caste, race, disability,
  marital status, or other sensitive characteristics.
- Do not invent information.
- Return ONLY valid JSON.
- matchScore must be between 0 and 100.
- recommendation must be SHORTLIST, REVIEW, or REJECT.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return exactly:

{{
  "candidateName": "string",
  "skills": ["string"],
  "education": "string",
  "experience": "string",
  "matchingSkills": ["string"],
  "missingSkills": ["string"],
  "matchScore": 0,
  "recommendation": "REVIEW"
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