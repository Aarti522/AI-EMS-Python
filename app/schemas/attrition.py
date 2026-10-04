from pydantic import BaseModel, Field


class AttritionRequest(BaseModel):
    employeeId: int

    age: int = Field(..., ge=18)
    experienceYears: float = Field(..., ge=0)
    monthlyIncome: float = Field(..., ge=0)
    jobSatisfaction: int = Field(..., ge=1, le=5)
    workLifeBalance: int = Field(..., ge=1, le=5)
    overtimeHours: float = Field(..., ge=0)
    yearsAtCompany: float = Field(..., ge=0)
    promotionYearsAgo: float = Field(..., ge=0)
    leaveDays: int = Field(..., ge=0)


class AttritionResponse(BaseModel):
    employeeId: int
    prediction: str
    score: float
    confidence: float