from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from app.services.resume_service import (
    extract_resume_text,
    analyze_resume,
)
from app.schemas.resume import ResumeResponse
from app.utils.role_utils import require_role


router = APIRouter(
    prefix="/api/ai/resume",
    tags=["Resume Screening"],
)

# ---------------------------------------------------------
# TEST RESUME PDF UPLOAD
# ---------------------------------------------------------
@router.post("/test-upload")
async def test_resume_upload(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    """
    Test endpoint for checking:
    - PDF upload
    - PDF text extraction
    - Job description form input
    """

    try:
        # Basic validation
        if not resume.filename:
            raise ValueError("Resume file is required")

        if not job_description.strip():
            raise ValueError("Job description is required")

        # Extract resume text
        resume_text = await extract_resume_text(resume)

        return {
            "success": True,
            "filename": resume.filename,
            "jobDescription": job_description,
            "textExtracted": bool(resume_text),
            "textLength": len(resume_text),
            "preview": resume_text[:500],
            "message": "Resume uploaded and text extracted successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": str(e),
            },
        )

    except Exception as e:
        print("RESUME TEST UPLOAD ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": "Resume processing failed",
            },
        )


# ---------------------------------------------------------
# AI RESUME SCREENING
# ---------------------------------------------------------

@router.post(
    "/screen",
    response_model=ResumeResponse,
)
async def screen_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    role: str = Form(...),
):
    """
## AI Resume Screening

Screen a resume against a job description using AI.

### Allowed Roles

- **ADMIN**
- **HR**

### Access Denied

- **MANAGER**
- **EMPLOYEE**
"""

    try:
        # Normalize role
        normalized_role = role.strip().upper()

        # Role authorization
        require_role(
            normalized_role,
            {"ADMIN", "HR"},
        )

        # Validate resume
        if not resume.filename:
            raise ValueError("Resume file is required")

        # Validate job description
        if not job_description.strip():
            raise ValueError("Job description is required")

        # AI analysis
        result = await analyze_resume(
            resume,
            job_description.strip(),
        )

        return {
            "success": True,
            "data": result,
            "message": "Resume screening completed successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "data": None,
                "message": str(e),
            },
        )

    except HTTPException:
        raise

    except Exception as e:
        print("RESUME SCREENING ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "data": None,
                "message": "Resume screening failed",
            },
        )