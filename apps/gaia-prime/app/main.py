"""GAIA PRIME — Master Orchestrator (Ring-Forge)."""
from app.api.router import router
from app.core.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="GAIA PRIME Master Orchestrator",
    description="Ring-Forge — Local-first AI Orchestration Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
