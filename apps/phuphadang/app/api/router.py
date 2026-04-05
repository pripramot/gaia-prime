"""Phuphadang API router."""
from app.api.endpoints import forensics, health
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(forensics.router, prefix="/forensics", tags=["forensics"])
