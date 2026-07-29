from app.config.config import TOGETHER_API_KEY, DEFAULT_TEMPERATURE, DIRECT_SUMMARIZATION_LIMIT, SUMMARY_STYLE_CONFIG, MAX_PARALLEL_REQS
from app.config.prompts import SYSTEM_PROMPT, STYLE_PROMPTS
from app.models.domain_models import DocumentChunk, ModelResult, SummaryStyle
from app.providers.base_provider import BaseProvider
from app.utils.cost import estimate_cost
from openai import AsyncOpenAI
import tiktoken
import asyncio
import time

class TogetherProvider(BaseProvider):
    def __init__(self, model_name: str):
        self._provider_name = "together"
        self._model_name = model_name
        self.client = AsyncOpenAI(api_key = TOGETHER_API_KEY, base_url = "https://api.together.ai/")
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    @property
    def provider_name(self):
        return self._provider_name
    
    @property
    def model_name(self):
        return self._model_name
    

    async def summarize(self, chunks: list[DocumentChunk], style: SummaryStyle) -> ModelResult:
        total_tokens = sum(chunk.estimated_tokens for chunk in chunks)
        if total_tokens <= DIRECT_SUMMARIZATION_LIMIT:
            return await self._summarize_document(chunks, style)
        
        return await self._hierarchical_summarize(chunks, style)
    
    
    async def _summarize_document(self, chunks: list[DocumentChunk], style: SummaryStyle) -> ModelResult:
        document = "\n\n".join(chunk.text for chunk in chunks)
        
        return await self._generate_summary(document, style)
    

    async def _hierarchical_summarize(self, chunks: list[DocumentChunk], style: SummaryStyle) -> ModelResult:
        semaphore = asyncio.Semaphore(MAX_PARALLEL_REQS)
        
        async def summarize_chunk(chunk: DocumentChunk):
            async with semaphore:
                return await self._generate_summary(chunk.text, style)
            
        async_summaries = await asyncio.gather(*[summarize_chunk(chunk) for chunk in chunks], return_exceptions = True)
        successful_summaries = [summary for summary in async_summaries if isinstance(summary, ModelResult)]

        if not successful_summaries:
            raise RuntimeError("All chunk summaries failed!")

        intermediate_summaries = [item.summary for item in successful_summaries]
        consolidated_document = "\n\n".join(intermediate_summaries)

        return await self._generate_summary(consolidated_document, style)
    

    async def _generate_summary(self, document: str, style: SummaryStyle) -> ModelResult:        
        start = time.perf_counter()

        for attempt in range(3):
            try:
                prompt_text = f"{SYSTEM_PROMPT}\n{STYLE_PROMPTS[style.value]}\n\nDocument:\n{document}"
                est_input_tokens = len(self.tokenizer.encode(prompt_text))
                config = SUMMARY_STYLE_CONFIG[style.value]
                max_output_tokens = int(est_input_tokens * config["ratio"])
                max_output_tokens = max(config["min_tokens"], max_output_tokens)
                max_output_tokens = min(config["max_tokens"], max_output_tokens)

                kwargs ={}
                if "Qwen/Qwen3.5-9B" in self.model_name:
                    kwargs["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}

                response = await self.client.chat.completions.create(
                    model = self.model_name,
                    temperature = DEFAULT_TEMPERATURE,
                    max_completion_tokens = max_output_tokens,
                    messages = [
                        {
                            "role": "system",
                            "content": f"{SYSTEM_PROMPT} {STYLE_PROMPTS[style.value]}"
                        },
                        {
                            "role": "user",
                            "content":
                            f"""DOCUMENT:
                            {document}"""
                        }         
                    ],
                    **kwargs
                )
                break
            
            except Exception:
                if attempt == 2:
                    raise 
                await asyncio.sleep(attempt + 1)
        
        latency = time.perf_counter() - start
        usage = response.usage

        return ModelResult(
            provider_name = self.provider_name,
            model_name = self.model_name,
            summary = response.choices[0].message.content,
            latency_secs = latency,
            total_tokens = usage.total_tokens,
            estimated_cost_usd = estimate_cost(self.model_name, usage.prompt_tokens, usage.completion_tokens)
        )
    

    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False