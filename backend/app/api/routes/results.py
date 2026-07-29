from app.models.domain_models import JobState, JobStatus
from app.models.api_models import ResultsResponse, ScoreResponse
from fastapi import APIRouter, HTTPException
from app.storage.redis_client import redis_client


router = APIRouter(prefix = "/results")

@router.get("/{job_id}", response_model = ResultsResponse)
async def get_results(job_id: str):
    job = await redis_client.get_job(f"job:{job_id}")
    if job is None:
        raise HTTPException(status_code = 404, detail = "Job not found.")
    
    state = JobState.model_validate(job)
    if state.status != JobStatus.COMPLETED:
        raise HTTPException(status_code = 400, detail = "Job not completed.")
    
    summaries = {
        result["model_name"]: result["summary"] for result in state.result["model_results"]
    }

    scores ={}
    for result in state.result["model_results"]:
        evaluation = state.result["evaluations"][result["model_name"]]
        scores[result["model_name"]] = ScoreResponse(
            semantic_sim = evaluation["semantic_sim"],
            coverage_score = evaluation["coverage_score"],
            compression_ratio = evaluation["compression_ratio"],
            latency_secs = result["latency_secs"],
            total_tokens = result["total_tokens"],
            estimated_cost = result["estimated_cost_usd"] 
        )

    return ResultsResponse(job_id = job_id, summaries = summaries, scores = scores, consolidated_summary = state.result["consolidated"]["summary"], agreement_score = state.result["consolidated"]["agreement_score"])