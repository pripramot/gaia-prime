"""C.H.R.O.N.O.S. API router."""
from app.api.endpoints import health, tracking
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(tracking.router, prefix="/tracking", tags=["tracking"])
