from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from app.models.domain_models import UploadMetadata, SummaryStyle, JobStatus, JobState
from app.models.api_models import UploadResponse
from app.config.config import SUPPORTED_CONTENT_TYPES
from app.orchestrator.service_orchestrator import Orchestrator
from app.storage.redis_client import redis_client

router = APIRouter(prefix = "/upload")
orchestrator = Orchestrator()

@router.post("/", response_model = UploadResponse)
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...), selected_models: list[str] = Form(...), summary_style: SummaryStyle = Form(...)):
    
    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(status_code = 400, detail = "Unsupported file format.")
    
    selected_models = [model.strip() for value in selected_models for model in value.split(",") if model.strip()]
    job_id = str(uuid4())
    metadata = UploadMetadata(selected_models = selected_models, summary_style = summary_style)

    await redis_client.save_job(f"job:{job_id}", JobState(job_id = job_id, status = JobStatus.PENDING, progress = 0).model_dump_json())
    background_tasks.add_task(orchestrator.process_document, job_id, file, metadata)

    return UploadResponse(job_id = job_id)