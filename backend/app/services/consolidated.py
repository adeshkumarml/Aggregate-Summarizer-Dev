from app.config.config import GEMINI_API_KEY, DEFAULT_TEMPERATURE, CONSOLIDATION_STYLE_CONFIG
from app.config.prompts import CONSOLIDATION_PROMPT, STYLE_PROMPTS
from app.models.domain_models import ModelResult, EvaluationResult, ConsolidatedResult, SummaryStyle
from google import genai
import tiktoken

class Consolidation:
    def __init__(self):
        self.client = genai.Client(api_key = GEMINI_API_KEY)
        self.model_name = "gemini-3.1-flash-lite"
        self.tokenizer = tiktoken.get_encoding("cl100k_base")


    def _build_prompt(self, model_results: list[ModelResult], evaluations: dict[str, EvaluationResult], style: SummaryStyle) -> str:
        prompt = f"""{CONSOLIDATION_PROMPT}
            {STYLE_PROMPTS[style.value]}
            """
        
        for result in model_results:
            eval = evaluations[result.model_name]
            prompt += f"""MODEL: {result.model_name}
                SEMANTIC AGREEEMENT: {eval.semantic_sim:.2f}"""
            if eval.coverage_score is not None:
                prompt += f"COVERAGE SCORE: {eval.coverage_score:.2f}\n"
            prompt += f"SUMMARY: {result.summary}"
                
        return prompt


    async def consolidate(self, model_results: list[ModelResult], evaluations: dict[str, EvaluationResult], style: SummaryStyle) -> ConsolidatedResult:
        if len(model_results) == 1:
            return ConsolidatedResult(
            summary = model_results[0].summary,
            participating_models = [model_results[0].model_name],
            agreement_score = 1.0
        )

        prompt = self._build_prompt(model_results, evaluations, style)
        est_input_tokens = len(self.tokenizer.encode(prompt))
        config = CONSOLIDATION_PROMPT[style.value]
        max_output_tokens = int(est_input_tokens * config["ratio"]) + 100
        max_output_tokens = max(config["min_tokens"], max_output_tokens)
        max_output_tokens = min(config["max_tokens"], max_output_tokens)

        response = await self.client.aio.models.generate_content(
            model = self.model_name,
            contents = prompt,
            config = {
                "temperature": DEFAULT_TEMPERATURE,
                "max_output_tokens": max_output_tokens
            }
        )
        agreement_score = sum(evaluations[result.model_name].semantic_sim for result in model_results) / len(model_results)

        return ConsolidatedResult(
            summary = response.text,
            participating_models = [result.model_name for result in model_results],
            agreement_score = agreement_score
        )