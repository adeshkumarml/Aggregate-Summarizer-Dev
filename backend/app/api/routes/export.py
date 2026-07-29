from app.models.domain_models import JobState, JobStatus, ModelResult, ConsolidatedResult
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.storage.redis_client import redis_client
from app.services.export import Export


router = APIRouter(prefix = "/export")
export_service = Export()


@router.get("/{job_id}")
async def export_results(job_id: str, format: str):
    if format not in ("pdf", "docx"):
        raise HTTPException(status_code = 400, detail = "Format must be pdf or docx.")

    job = await redis_client.get_job(f"job:{job_id}")
    if job is None:
        raise HTTPException(status_code = 404, detail = "Job not found.")

    state = JobState.model_validate(job)
    if state.status != JobStatus.COMPLETED:
        raise HTTPException(status_code = 400, detail = "Job not completed yet.")

    if not state.result:
        raise HTTPException(status_code = 400, detail = "No exportable result found.")
    
    result = state.result
    filename = result.get("filename", "document")
    model_results = [ModelResult.model_validate(item) for item in result["model_results"]]
    consolidated = ConsolidatedResult.model_validate(result["consolidated"])

    if format == "pdf":
        buffer, output_filename = export_service.export_pdf(
            original_filename = filename,
            consolidated = consolidated,
            model_results = model_results
        )
        media_type = "application/pdf"
    else:
        buffer, output_filename = export_service.export_docx(
            original_filename = filename,
            consolidated = consolidated,
            model_results = model_results
        )
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return StreamingResponse(buffer, media_type = media_type, headers = {"Content-Disposition": f'attachment; filename="{output_filename}"'})