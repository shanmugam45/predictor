import os

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import ModelRun
from app.ml.model_loader import model_loader


def get_model_status(db: Session) -> dict:
    active_run = db.query(ModelRun).filter(ModelRun.is_active == True).first()
    return {
        "is_loaded": model_loader.is_loaded,
        "model_name": model_loader.model_name,
        "model_version": model_loader.model_version,
        "accuracy": active_run.accuracy if active_run else None,
        "mae": active_run.mae if active_run else None,
        "rmse": active_run.rmse if active_run else None,
        "r2_score": active_run.r2_score if active_run else None,
        "training_samples": active_run.training_samples if active_run else None,
        "last_trained": active_run.created_at if active_run else None,
        "message": "Model is ready"
        if model_loader.is_loaded
        else "No model loaded — using fallback heuristic",
    }


def reload_model(db: Session) -> bool:
    success = model_loader.load(settings.MODEL_PATH)
    return success


def register_model_run(db: Session, metrics: dict) -> ModelRun:
    # Deactivate previous runs
    db.query(ModelRun).filter(ModelRun.is_active == True).update({"is_active": False})
    run = ModelRun(
        model_name=metrics.get("model_name", "custom_model"),
        model_version=metrics.get("model_version", "1.0.0"),
        accuracy=metrics.get("accuracy"),
        mae=metrics.get("mae"),
        rmse=metrics.get("rmse"),
        r2_score=metrics.get("r2_score"),
        training_samples=metrics.get("training_samples"),
        is_active=True,
        notes=metrics.get("notes"),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_model_runs(db: Session) -> list[ModelRun]:
    return db.query(ModelRun).order_by(ModelRun.created_at.desc()).all()
