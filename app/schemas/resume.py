from typing import List, Optional
from pydantic import BaseModel, Field


class ResumeScreeningResult(BaseModel):
    matchScore: int = Field(..., ge=0, le=100)
    matchedSkills: List[str]
    missingSkills: List[str]
    recommendation: str
    summary: str


class ResumeResponse(BaseModel):
    success: bool
    data: Optional[ResumeScreeningResult] = None
    message: str