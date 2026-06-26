from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    attendance_percentage: float = Field(..., ge=0.0, le=100.0)
    study_hours_per_week: float = Field(..., ge=0.0, le=168.0)
    previous_gpa: float = Field(..., ge=0.0, le=10.0)
    internal_mark_1: float = Field(..., ge=0.0, le=100.0)
    internal_mark_2: float = Field(..., ge=0.0, le=100.0)
    assignment_score: float = Field(..., ge=0.0, le=100.0)
    lab_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    participation_score: Optional[float] = Field(None, ge=0.0, le=100.0)


class BatchPredictionInput(BaseModel):
    records: list[PredictionInput] = Field(..., min_length=1, max_length=500)


class PredictionResponse(BaseModel):
    id: int
    predicted_mark: float
    predicted_grade: str
    confidence_score: Optional[float]
    model_version: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class BatchPredictionResponse(BaseModel):
    total: int
    results: list[PredictionResponse]
