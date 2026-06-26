from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ModelStatusResponse(BaseModel):
    is_loaded: bool
    model_name: Optional[str]
    model_version: Optional[str]
    accuracy: Optional[float]
    mae: Optional[float]
    rmse: Optional[float]
    r2_score: Optional[float]
    training_samples: Optional[int]
    last_trained: Optional[datetime]
    message: str


class ModelRunRegisterRequest(BaseModel):
    model_name: str = Field(default="custom_model")
    model_version: str = Field(default="1.0.0")
    accuracy: Optional[float] = None
    mae: Optional[float] = None
    rmse: Optional[float] = None
    r2_score: Optional[float] = None
    training_samples: Optional[int] = None
    notes: Optional[str] = None


class ModelRunResponse(BaseModel):
    id: int
    model_name: str
    model_version: str
    accuracy: Optional[float]
    mae: Optional[float]
    rmse: Optional[float]
    r2_score: Optional[float]
    training_samples: Optional[int]
    is_active: bool
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
