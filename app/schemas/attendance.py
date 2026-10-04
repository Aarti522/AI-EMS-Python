from pydantic import BaseModel, Field
from typing import List, Optional


class AttendanceAnalysisRequest(BaseModel):
    employeeId: int
    role: str
    employeeName: str

    currentMonthAttendance: float = Field(..., ge=0, le=100)
    previousMonthAttendance: float = Field(..., ge=0, le=100)

    lateDays: int = Field(..., ge=0)
    absentDays: int = Field(..., ge=0)
    leaveDays: int = Field(..., ge=0)


class AttendanceData(BaseModel):
    employeeId: int
    riskLevel: str
    summary: str
    observations: List[str]
    recommendation: str


class AttendanceAnalysisResponse(BaseModel):
    success: bool
    data: Optional[AttendanceData] = None
    message: str