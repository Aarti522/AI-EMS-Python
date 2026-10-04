from pydantic import BaseModel, Field


class PerformanceRequest(BaseModel):
    employeeId: int
    attendancePercentage: float = Field(..., ge=0, le=100)
    experienceYears: float = Field(..., ge=0)
    projectsCompleted: int = Field(..., ge=0)
    tasksCompleted: int = Field(..., ge=0)
    previousRating: float = Field(..., ge=0, le=5)
    trainingCompleted: int = Field(..., ge=0)
    overtimeHours: float = Field(..., ge=0)
    leaveDays: int = Field(..., ge=0)


class PerformanceResponse(BaseModel):
    employeeId: int
    prediction: str
    score: float
    confidence: float