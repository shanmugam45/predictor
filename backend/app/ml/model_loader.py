"""
ML Model Loader
===============
Singleton that loads a trained model (joblib/pickle) and exposes predict/predict_batch.
Falls back to a weighted heuristic when no model file is found.
"""

import logging
import os
import pickle
from typing import Any, Optional

import joblib
import numpy as np
import pandas as pd

from app.core.config import settings

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = [
    "attendance_percentage",
    "study_hours_per_week",
    "previous_gpa",
    "midterm_score",
    "assignment_score",
    "lab_score",
    "participation_score",
]


def _mark_to_grade(mark: float) -> str:
    if mark >= 90:
        return "O"
    if mark >= 80:
        return "A+"
    if mark >= 75:
        return "A"
    if mark >= 70:
        return "B+"
    if mark >= 65:
        return "B"
    if mark >= 60:
        return "C+"
    if mark >= 50:
        return "C"
    return "F"


def _fallback_predict(features: dict) -> dict:
    score = (
        features.get("midterm_score", 0) * 0.35
        + features.get("assignment_score", 0) * 0.20
        + features.get("attendance_percentage", 0) * 0.15
        + features.get("previous_gpa", 0) * 10 * 0.15
        + features.get("study_hours_per_week", 0) / 40 * 100 * 0.10
        + (features.get("lab_score") or 0) * 0.03
        + (features.get("participation_score") or 0) * 0.02
    )
    score = min(max(score, 0), 100)
    return {
        "predicted_mark": round(score, 2),
        "predicted_grade": _mark_to_grade(score),
        "confidence_score": None,
        "model_version": "fallback-heuristic",
    }


class ModelLoader:
    def __init__(self):
        self.model: Optional[Any] = None
        self.is_loaded: bool = False
        self.model_name: str = "Not loaded"
        self.model_version: str = "N/A"

    @property
    def candidates(self) -> list[str]:
        return [
            p for p in [
                getattr(settings, "MODEL_PATH", None),
                "./models/trained_model.joblib",
                "./marks_model.pkl",
                "./marks_model.joblib",
            ] if p
        ]

    def load(self, path: Optional[str] = None) -> bool:
        """Attempt to load a model. Returns True on success."""
        to_try = [path] + self.candidates if path else self.candidates
        for p in to_try:
            if not p or not os.path.exists(p):
                continue
            try:
                try:
                    m = joblib.load(p)
                except Exception:
                    with open(p, "rb") as f:
                        m = pickle.load(f)
                self.model = m
                self.is_loaded = True
                self.model_name = m.__class__.__name__ if isinstance(m, type) or hasattr(m, "__class__") else type(m).__name__
                self.model_version = getattr(m, "version", "1.0.0")
                logger.info(f"Model loaded from {p}")
                return True
            except Exception as e:
                logger.warning(f"Failed to load model from {p}: {e}")
                continue
        logger.warning("No model file found, using fallback heuristic")
        return False

    @staticmethod
    def _build_feature_array(features: dict) -> np.ndarray:
        row = [float(features.get(col, 0.0) or 0.0) for col in FEATURE_COLUMNS]
        return np.array([row])

    def predict(self, features: dict) -> dict:
        if not self.is_loaded:
            return _fallback_predict(features)

        df = pd.DataFrame([features])
        for c in df.columns:
            try:
                df[c] = pd.to_numeric(df[c])
            except Exception:
                pass

        try:
            y_pred = self.model.predict(df)
            pred_mark = float(np.clip(y_pred[0], 0, 100))
            confidence = None
            try:
                proba = self.model.predict_proba(df)
                confidence = float(np.max(proba))
            except (AttributeError, Exception):
                pass
            return {
                "predicted_mark": round(pred_mark, 2),
                "predicted_grade": _mark_to_grade(pred_mark),
                "confidence_score": confidence,
                "model_version": self.model_version,
            }
        except Exception as e:
            logger.warning(f"Model predict failed, using fallback: {e}")
            return _fallback_predict(features)

    def predict_batch(self, feature_list: list[dict]) -> list[dict]:
        if not self.is_loaded:
            return [_fallback_predict(f) for f in feature_list]

        df = pd.DataFrame(feature_list)
        for c in df.columns:
            try:
                df[c] = pd.to_numeric(df[c])
            except Exception:
                pass

        try:
            y_pred = np.clip(self.model.predict(df), 0, 100)
            out = []
            for mark in y_pred:
                out.append({
                    "predicted_mark": round(float(mark), 2),
                    "predicted_grade": _mark_to_grade(float(mark)),
                    "confidence_score": None,
                    "model_version": self.model_version,
                })
            return out
        except Exception as e:
            logger.warning(f"Batch predict failed, using fallback: {e}")
            return [_fallback_predict(f) for f in feature_list]


model_loader = ModelLoader()
