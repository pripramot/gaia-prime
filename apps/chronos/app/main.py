"""C.H.R.O.N.O.S. — Tactical Intelligence & Mobile Tracking Service."""
from app.api.router import router
from app.core.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="C.H.R.O.N.O.S.",
    description="Tactical Intelligence, Mobile Tracking, Sovereign Map",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
