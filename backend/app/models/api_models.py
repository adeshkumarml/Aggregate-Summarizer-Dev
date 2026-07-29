from pydantic import BaseModel

class UploadResponse(BaseModel):
    job_id: str 

class StatusResponse(BaseModel):
    job_id: str
    status: str
    stage: str | None = None
    progress: int
    current_model: str | None = None

class ScoreResponse(BaseModel):
    semantic_sim: float
    coverage_score: float
    compression_ratio: float
    latency_secs: float
    total_tokens: int
    estimated_cost: float

class ResultsResponse(BaseModel):
    job_id: str
    summaries: dict[str, str]
    scores: dict[str, ScoreResponse]
    consolidated_summary: str
    agreement_score: float