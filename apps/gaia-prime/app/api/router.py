"""API router — aggregates all sub-routers."""
from app.api.endpoints import data, health, jobs
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(data.router, prefix="/data", tags=["data"])
router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
