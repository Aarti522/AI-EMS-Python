import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.performance import router as performance_router
from app.routes.attrition import router as attrition_router
from app.routes.resume import router as resume_router
from app.routes.chatbot import router as chatbot_router
from app.routes.attendance import router as attendance_router


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AI-EMS Python Service",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

# For local development:
# FRONTEND_URL is not required.
# http://localhost:5173 will be used automatically.
#
# For deployment:
# Set FRONTEND_URL in the hosting platform's
# environment variables to your deployed React URL.

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "AI-EMS Python Service is running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/ai/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-EMS Python Service"
    }


# ==========================================
# AI ROUTES
# ==========================================

# Performance AI
app.include_router(performance_router)

# Attrition AI
app.include_router(attrition_router)

# Resume AI
app.include_router(resume_router)

# Chatbot AI
app.include_router(chatbot_router)

# Attendance AI
app.include_router(attendance_router)