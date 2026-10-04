import json
from io import BytesIO

from fastapi import UploadFile
from google import genai
from pypdf import PdfReader

from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------------------------------------------------
# EXTRACT TEXT FROM PDF
# ---------------------------------------------------------

async def extract_resume_text(resume: UploadFile) -> str:

    if not resume.filename:
        raise ValueError("Resume file is required")

    if not resume.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF resume files are supported")

    try:
        file_bytes = await resume.read()

        if not file_bytes:
            raise ValueError("Uploaded resume file is empty")

        reader = PdfReader(BytesIO(file_bytes))

        resume_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                resume_text += page_text + "\n"

        resume_text = resume_text.strip()

        if not resume_text:
            raise ValueError(
                "Could not extract text from the PDF resume"
            )

        # Reset pointer so file can be read again if required
        await resume.seek(0)

        return resume_text

    except ValueError:
        await resume.seek(0)
        raise

    except Exception as e:
        await resume.seek(0)

        raise ValueError(
            f"Failed to process resume PDF: {str(e)}"
        )


# ---------------------------------------------------------
# GEMINI RESUME SCREENING
# ---------------------------------------------------------

def screen_resume(
    resume_text: str,
    job_description: str
) -> dict:

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty")

    prompt = f"""
You are an AI assistant that compares a candidate resume against a job description.

IMPORTANT:
The text between <JOB_DESCRIPTION> tags is the job description.
It is valid input even if it is only one sentence.
Do not reject or call the job description invalid because it is short.

<JOB_DESCRIPTION>
{job_description.strip()}
</JOB_DESCRIPTION>

<RESUME>
{resume_text.strip()}
</RESUME>

Evaluate how well the resume matches the job description.

Return ONLY valid JSON:

{{
  "matchScore": 0,
  "matchedSkills": [],
  "missingSkills": [],
  "recommendation": "REVIEW",
  "summary": ""
}}

Rules:
- matchScore must be an integer from 0 to 100.
- matchedSkills: skills required by the job description that appear in the resume.
- missingSkills: important skills required by the job description that are not found in the resume.
- recommendation must be exactly SHORTLIST, REVIEW, or REJECT.
- SHORTLIST: strong match.
- REVIEW: partial/moderate match.
- REJECT: weak match.
- Base the result only on job-related skills and experience.
- Do not use personal information such as name, phone number, email, address, gender, age, religion, caste, ethnicity, or other protected characteristics.
- Do not say the job description is invalid merely because it is short.
- Do not output markdown.
- Do not output anything outside the JSON object.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response")

        response_text = response.text.strip()

        # Remove markdown code block if Gemini adds one
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            result = json.loads(response_text)

        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned an invalid JSON response"
            )

        # Validate required fields
        required_fields = {
            "matchScore",
            "matchedSkills",
            "missingSkills",
            "recommendation",
            "summary"
        }

        missing_fields = required_fields - result.keys()

        if missing_fields:
            raise ValueError(
                f"Gemini response missing fields: "
                f"{', '.join(missing_fields)}"
            )

        # Validate match score
        try:
            result["matchScore"] = int(result["matchScore"])
        except (ValueError, TypeError):
            raise ValueError("Invalid matchScore returned by Gemini")

        result["matchScore"] = max(
            0,
            min(100, result["matchScore"])
        )

        # Validate recommendation
        recommendation = str(
            result["recommendation"]
        ).strip().upper()

        allowed_recommendations = {
            "SHORTLIST",
            "REVIEW",
            "REJECT"
        }

        if recommendation not in allowed_recommendations:
            recommendation = "REVIEW"

        result["recommendation"] = recommendation

        # Ensure skills are lists
        if not isinstance(result["matchedSkills"], list):
            result["matchedSkills"] = []

        if not isinstance(result["missingSkills"], list):
            result["missingSkills"] = []

        result["summary"] = str(
            result["summary"]
        ).strip()

        return result

    except ValueError:
        raise

    except Exception as e:
        print("GEMINI RESUME ERROR:", repr(e))

        raise RuntimeError(
            "AI resume screening service failed"
        )


# ---------------------------------------------------------
# COMPLETE RESUME ANALYSIS
# ---------------------------------------------------------

async def analyze_resume(
    resume: UploadFile,
    job_description: str
) -> dict:

    if not job_description.strip():
        raise ValueError("Job description is required")

    # Extract PDF text
    resume_text = await extract_resume_text(resume)

    # Send extracted text to Gemini
    result = screen_resume(
        resume_text=resume_text,
        job_description=job_description.strip()
    )

    return result