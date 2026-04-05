"""Processing jobs status endpoint."""
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{job_id}")
async def get_job(job_id: str) -> dict:
    from app.data_processing.storage import DataStorage
    storage = DataStorage()
    job = await storage.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return job
