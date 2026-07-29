from enum import Enum
from pydantic import BaseModel

class SummaryStyle(str, Enum):
    CONCISE = "concise"
    COMPREHENSIVE = "comprehensive"
    DETAILED = "detailed"    

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobStage(str, Enum):
    PARSING = "Parsing document"
    CHUNKING = "Chunking document"
    SUMMARIZING = "Generating summaries"
    SCORING = "Computing metrics"
    CONSOLIDATING = "Consolidating"
    COMPLETED = "Completed"

class UploadMetadata(BaseModel):
    selected_models: list[str]
    summary_style: SummaryStyle

class DocumentChunk(BaseModel):
    chunk_id: int
    text: str
    estimated_tokens: int
    start_page: int | None = None
    end_page: int | None = None
    
class ModelResult(BaseModel):
    provider_name: str
    model_name: str
    summary: str
    latency_secs: float
    total_tokens: int
    estimated_cost_usd: float

class ConsolidatedResult(BaseModel):
    summary: str
    participating_models: list[str]
    agreement_score: float

class EvaluationResult(BaseModel):
    semantic_sim: float
    coverage_score: float
    compression_ratio: float
    latency_rank: int
    cost_rank: int

class JobState(BaseModel):
    job_id: str
    status: JobStatus
    stage: JobStage | None = None
    progress: int
    current_model: str | None = None
    result: dict | None = None
    error: str | None = None

