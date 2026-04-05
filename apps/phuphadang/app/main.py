"""Phuphadang — Core AI & Digital Forensics Service."""
from app.api.router import router
from app.core.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="Phuphadang",
    description="Core AI & Digital Forensics — ภูผาแดง",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
