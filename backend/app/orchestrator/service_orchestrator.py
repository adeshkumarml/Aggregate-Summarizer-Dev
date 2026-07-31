from app.models.domain_models import UploadMetadata, JobStage, JobStatus, JobState

from app.services.parser import Parser
from app.services.chunking import Chunking
from app.services.scoring import Scoring
from app.services.consolidated import Consolidation
from app.providers.provider_factory import ProviderFactory

from app.config.config import PROGRESS
from app.storage.redis_client import redis_client
from fastapi import UploadFile

import asyncio

# temporary
import time


class Orchestrator:
    def __init__(self):
        self.parser = Parser()
        self.chunker = Chunking()
        self.scoring = Scoring()
        self.consolidator = Consolidation()


    async def process_document(self, job_id: str, file: UploadFile, metadata: UploadMetadata):
        await self._update_job(JobState(job_id = job_id, status = JobStatus.PENDING, progress = 0))
        
        try:
            await self._update_job(JobState(job_id = job_id, status = JobStatus.PROCESSING, stage = JobStage.PARSING, progress = PROGRESS["PARSING"]))    
            document_text = await self.parser.extract_text(file)
            
            await self._update_job(JobState(job_id = job_id, status = JobStatus.PROCESSING, stage = JobStage.CHUNKING, progress = PROGRESS["CHUNKING"]))
            chunks = self.chunker.chunk_text(document_text)
            
            await self._update_job(JobState(job_id = job_id, status = JobStatus.PROCESSING, stage = JobStage.SUMMARIZING, progress = PROGRESS["SUMMARIZING"]))

            #temporary
            print("Before provider gatherer", time.time())

            providers = []
            for selected_model in metadata.selected_models:
                provider_name = self._get_provider_name(selected_model)
                providers.append(ProviderFactory.get_provider(provider_name = provider_name, model_name = selected_model))

            provider_results = await asyncio.gather(*[provider.summarize(chunks, metadata.summary_style) for provider in providers], return_exceptions = True)

            #temporary
            print("After provider gatherer", time.time())

            successful_results = [result for result in provider_results if not isinstance(result, Exception)]
            if not successful_results:
                raise RuntimeError("All models failed!")
            
            await self._update_job(JobState(job_id = job_id, status = JobStatus.PROCESSING, stage = JobStage.SCORING, progress = PROGRESS["SCORING"]))
            evaluations = self.scoring.evaluate(document_text, successful_results)

            await self._update_job(JobState(job_id = job_id, status = JobStatus.PROCESSING, stage = JobStage.CONSOLIDATING, progress = PROGRESS["CONSOLIDATING"]))
            consolidated_output = await self.consolidator.consolidate(successful_results, evaluations, metadata.summary_style)

            await self._update_job(JobState(job_id = job_id, status = JobStatus.COMPLETED, stage = JobStage.COMPLETED, progress = PROGRESS["COMPLETED"],
                                            result = {
                                                "filename": file.filename,
                                                "model_results": [r.model_dump() for r in successful_results],
                                                "evaluations": {
                                                    k: v.model_dump() for k,v in evaluations.items()
                                                },
                                                "consolidated": consolidated_output.model_dump()
                                            }
                                        ))
        
        except Exception as e:
            await self._update_job(JobState(job_id = job_id, status = JobStatus.FAILED, progress = 100, error = str(e)))


    async def _update_job(self, state: JobState):

        #temporary
        print(f"{state.stage} | {state.progress} | {state.status}")
        
        await redis_client.save_job(f"job:{state.job_id}", state.model_dump_json())

    
    def _get_provider_name(self, model_name: str) -> str:
        mapping = {
            "gpt-4o-mini": "openai",
            "gemini-3.1-flash-lite": "gemini",
            "deepseek-v4-flash": "deepseek",
            "Qwen/Qwen3.5-9B": "together",
            "meta-llama/Llama-3.3-70B-Instruct-Turbo": "together",
            "MiniMaxAI/MiniMax-M3": "together"
        }
        return mapping[model_name]
            