from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.db.database import create_tables
from app.api.routes import predictions, model
from app.services import model_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Mark Prediction API...")
    create_tables()
    logger.info("Database tables created/verified.")
    # Attempt to load the ML model (if present) so API is ready to serve predictions
    try:
        model_service.reload_model(None)
        logger.info("Model loader attempted startup reload.")
    except Exception:
        logger.exception("Model reload failed during startup.")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Mark Prediction API",
    description="API for predicting marks using ML models",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# ── Security Middleware ────────────────────────────────────────────────────────
# Only redirect to HTTPS in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "X-Requested-With"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["Predictions"])
app.include_router(model.router,    prefix="/api/v1/model",   tags=["Model"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
