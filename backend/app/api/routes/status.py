from app.models.domain_models import JobState
from app.models.api_models import StatusResponse
from fastapi import APIRouter, HTTPException
from app.storage.redis_client import redis_client

router = APIRouter(prefix = "/status")

@router.get("/{job_id}", response_model = StatusResponse)
async def get_status(job_id: str):
    
    job = await redis_client.get_job(f"job:{job_id}")
    if job is None:
        raise HTTPException(status_code = 400, detail = "Job not found.")
    state = JobState.model_validate(job)

    return StatusResponse(
        job_id = job_id, 
        status = (state.status.value if state.status else ""),
        progress = state.progress, 
        current_model = state.current_model)
 