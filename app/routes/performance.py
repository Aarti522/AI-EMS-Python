from fastapi import APIRouter

from app.schemas.performance import (
    PerformanceRequest,
    PerformanceResponse
)

from app.services.performance_service import predict_performance


router = APIRouter(
    prefix="/api/ai/performance",
    tags=["Performance Prediction"]
)


@router.post(
    "/predict",
    response_model=PerformanceResponse
)
def predict(data: PerformanceRequest):
    return predict_performance(data)