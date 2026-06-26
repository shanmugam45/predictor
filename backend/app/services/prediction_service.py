import json

from sqlalchemy.orm import Session

from app.db.models import Prediction
from app.ml.model_loader import model_loader
from app.schemas.prediction import BatchPredictionInput, PredictionInput


def _build_model_features(input_data: dict) -> dict:
    return {
        "attendance_percentage": input_data["attendance_percentage"],
        "study_hours_per_week": input_data["study_hours_per_week"],
        "previous_gpa": input_data["previous_gpa"],
        "midterm_score": (input_data["internal_mark_1"] + input_data["internal_mark_2"]) / 2,
        "assignment_score": input_data["assignment_score"],
        "lab_score": input_data.get("lab_score"),
        "participation_score": input_data.get("participation_score"),
    }


def run_prediction(db: Session, data: PredictionInput) -> Prediction:
    input_data = data.model_dump()
    model_features = _build_model_features(input_data)
    result = model_loader.predict(model_features)

    record = Prediction(
        input_features=json.dumps(input_data),
        predicted_mark=result["predicted_mark"],
        predicted_grade=result["predicted_grade"],
        confidence_score=result.get("confidence_score"),
        model_version=result.get("model_version"),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def run_batch_prediction(db: Session, data: BatchPredictionInput) -> list[Prediction]:
    input_records = [r.model_dump() for r in data.records]
    feature_list = [_build_model_features(r) for r in input_records]
    results = model_loader.predict_batch(feature_list)

    records = []
    for idx, (item, result) in enumerate(zip(data.records, results)):
        record = Prediction(
            input_features=json.dumps(input_records[idx]),
            predicted_mark=result["predicted_mark"],
            predicted_grade=result["predicted_grade"],
            confidence_score=result.get("confidence_score"),
            model_version=result.get("model_version"),
        )
        db.add(record)
        records.append(record)
    db.commit()
    for r in records:
        db.refresh(r)
    return records


def get_predictions(db: Session, page: int = 1, page_size: int = 20):
    query = db.query(Prediction)
    total = query.count()
    items = (
        query.order_by(Prediction.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items
