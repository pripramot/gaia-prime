"""Unicorn API router."""
from app.api.endpoints import alerts, health
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
