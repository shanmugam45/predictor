from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.prediction import (
    BatchPredictionInput,
    BatchPredictionResponse,
    PredictionInput,
    PredictionResponse,
)
from app.services import prediction_service

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse, status_code=201)
def predict_single(data: PredictionInput, db: Session = Depends(get_db)):
    """Predict the final mark."""
    return prediction_service.run_prediction(db, data)


@router.post("/predict/batch", response_model=BatchPredictionResponse, status_code=201)
def predict_batch(data: BatchPredictionInput, db: Session = Depends(get_db)):
    """Predict final marks for multiple records at once."""
    results = prediction_service.run_batch_prediction(db, data)
    return BatchPredictionResponse(total=len(results), results=results)


@router.get("/", response_model=dict)
def list_predictions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List prediction history."""
    total, items = prediction_service.get_predictions(db, page, page_size)
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": p.id,
                "predicted_mark": p.predicted_mark,
                "predicted_grade": p.predicted_grade,
                "confidence_score": p.confidence_score,
                "model_version": p.model_version,
                "created_at": p.created_at,
                "input_features": p.input_features,
            }
            for p in items
        ],
    }
