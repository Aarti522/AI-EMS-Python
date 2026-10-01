from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    role: str
    employeeId: int
    context: Optional[Dict[str, Any]] = None


class ChatData(BaseModel):
    employeeId: int
    response: str


class ChatResponse(BaseModel):
    success: bool
    data: Optional[ChatData] = None
    message: str