import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.schemas.model_schema import (
    ModelRunRegisterRequest,
    ModelRunResponse,
    ModelStatusResponse,
)
from app.services import model_service

router = APIRouter()


@router.get("/status", response_model=ModelStatusResponse)
def model_status(db: Session = Depends(get_db)):
    """Get the current model status and metrics."""
    return model_service.get_model_status(db)


@router.post("/reload")
def reload_model(db: Session = Depends(get_db)):
    """Reload the model from disk (call this after you deploy a new model file)."""
    success = model_service.reload_model(db)
    if not success:
        raise HTTPException(
            status_code=404, detail="Model file not found or failed to load"
        )
    return {"message": "Model reloaded successfully"}


@router.post("/upload")
async def upload_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a trained model file (.joblib or .pkl).
    The file will be saved as the active model and reloaded automatically.
    """
    allowed_extensions = {".joblib", ".pkl", ".pickle"}
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"Invalid file type. Allowed: {allowed_extensions}"
        )

    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    os.makedirs("./models", exist_ok=True)
    dest = "./models/trained_model.joblib"
    with open(dest, "wb") as f:
        f.write(content)

    success = model_service.reload_model(db)
    return {
        "message": "Model uploaded and loaded successfully"
        if success
        else "File saved but failed to load model",
        "filename": file.filename,
    }


@router.post("/register-run", response_model=ModelRunResponse)
def register_run(metrics: ModelRunRegisterRequest, db: Session = Depends(get_db)):
    """
    Register model training metrics. Call this from your training script after training.
    """
    return model_service.register_model_run(db, metrics.model_dump())


@router.get("/runs", response_model=list[ModelRunResponse])
def list_model_runs(db: Session = Depends(get_db)):
    """List all model training runs."""
    return model_service.get_model_runs(db)
