from fastapi import APIRouter, HTTPException

from app.schemas.chatbot import (
    ChatRequest,
    ChatResponse
)

from app.services.chatbot_service import generate_chat_response


router = APIRouter(
    prefix="/api/ai/chatbot",
    tags=["AI HR Chatbot"]
)


# All valid AI-EMS roles
ALLOWED_ROLES = {
    "ADMIN",
    "HR",
    "MANAGER",
    "EMPLOYEE"
}


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chatbot(request: ChatRequest):

    # Safely normalize role
    role = str(request.role).strip().upper()

    # Validate role
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "data": None,
                "message": f"Invalid role: {role}"
            }
        )

    try:
        ai_response = generate_chat_response(
            message=request.message,
            role=role,
            employeeId=request.employeeId,
            context=request.context
        )

        return ChatResponse(
            success=True,
            data={
                "employeeId": request.employeeId,
                "response": ai_response
            },
            message="Chatbot response generated successfully"
        )

    except Exception as e:
        print("CHATBOT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "data": None,
                "message": "Chatbot request failed"
            }
        )