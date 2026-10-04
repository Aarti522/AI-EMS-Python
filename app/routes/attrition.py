from fastapi import APIRouter

from app.schemas.attrition import (
    AttritionRequest,
    AttritionResponse
)

from app.services.attrition_service import predict_attrition


router = APIRouter(
    prefix="/api/ai/attrition",
    tags=["Attrition Prediction"]
)


@router.post(
    "/predict",
    response_model=AttritionResponse
)
def predict(data: AttritionRequest):
    return predict_attrition(data)