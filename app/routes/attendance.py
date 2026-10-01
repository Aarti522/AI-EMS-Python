from fastapi import APIRouter, HTTPException

from app.schemas.attendance import (
    AttendanceAnalysisRequest,
    AttendanceAnalysisResponse
)

from app.services.attendance_service import analyze_attendance
from app.utils.role_utils import validate_role


router = APIRouter(
    prefix="/api/ai/attendance",
    tags=["Attendance AI Insights"]
)


@router.post(
    "/analyze",
    response_model=AttendanceAnalysisResponse
)
def attendance_analysis(data: AttendanceAnalysisRequest):

    validate_role(data.role)

    try:
        result = analyze_attendance(data)

        return {
            "success": True,
            "data": result,
            "message": "Attendance analysis completed successfully"
        }

    except Exception as e:
        print("ATTENDANCE ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "data": None,
                "message": "Attendance analysis failed"
            }
        )