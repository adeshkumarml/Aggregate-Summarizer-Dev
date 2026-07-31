from app.models.domain_models import ModelResult, EvaluationResult
from app.services.embedding import Embedding
import numpy as np
import tiktoken
import re

#temp
import time

class Scoring:
    def __init__(self):
        self.embedding = Embedding()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")


    def _semantic_similarity_scores(self, model_results: list[ModelResult]) -> dict[str, float]:
        summaries = [result.summary for result in model_results]
        #temporary
        t = time.perf_counter()
        embeddings = self.embedding.embed_text_batch(summaries)
        #temporary
        print(f"Semantic embedding: {time.perf_counter()-t:.2f}s")

        scores = {}
        for i, result in enumerate(model_results):
            similarities = []

            for j in range (len(model_results)):
                if i == j:
                    continue
                similarity = np.dot(embeddings[i], embeddings[j])
                similarities.append(similarity)
            
            if similarities:
                scores[result.model_name] = float(np.mean(similarities))
            else:
                scores[result.model_name] = 1.0

        return scores


    def _split_sentences(self, text: str) -> list[str]:
        sentences = [sentence.strip() for sentence in re.split(r'(?<=[.!?。！？؟۔։።፧।॥။៕᱾])\s+', text) if sentence.strip()]
        return sentences


    def _coverage_scores(self, source_document: str, model_results: list[ModelResult], similarity_threshold: float = 0.7) -> dict[str, float]:
        document_sentences = self._split_sentences(source_document)

        if not document_sentences:
            return {
                result.model_name: 0.0 for result in model_results
            }

        #temporary
        t = time.perf_counter()
        print(len(document_sentences)) # temp, remove this line later
        document_embeddings = self.embedding.embed_text_batch(document_sentences)
        #temporary
        print(f"Document embedding: {time.perf_counter()-t:.2f}s")

        scores = {}

        for result in model_results:
            summary_sentences = self._split_sentences(result.summary)
            
            if not summary_sentences:
                scores[result.model_name] = 0.0
                continue

            #temporary
            t = time.perf_counter()
            print(len(summary_sentences)) # temporary, remove later    
            summary_embeddings = self.embedding.embed_text_batch(summary_sentences)
            #temporary
            print(f"{result.model_name}: summary embedding {time.perf_counter()-t:.2f}s")

            covered_sentences = 0

            for document_emb in document_embeddings:
                #temp
                t = time.perf_counter()
                similarities = [np.dot(document_emb, summary_emb) for summary_emb in summary_embeddings]
                max_sim = max(similarities)
                if max_sim >= similarity_threshold:
                    covered_sentences += 1

            #temp
            print(f"{result.model_name}: similarity loop {time.perf_counter()-t:.2f}s")

            scores[result.model_name] = covered_sentences / len(document_sentences)

        return scores


    def _compression_ratio(self, document: str, summary: str) -> float:
        document_tokens = max(1, len(self.tokenizer.encode(document)))
        summary_tokens = max(1, len(self.tokenizer.encode(summary)))

        return document_tokens / summary_tokens
    

    def _latency_ranks(self, model_results: list[ModelResult])-> dict[str, int]:
        ordered = sorted(model_results, key=lambda x: x.latency_secs)

        return {
            result.model_name: index for index, result in enumerate(ordered, 1)
        }
    

    def _cost_ranks(self, model_results: list[ModelResult]) -> dict[str, int]:
        ordered = sorted(model_results, key=lambda x: x.estimated_cost_usd)

        return {
            result.model_name: index for index, result in enumerate(ordered, 1)
        }



    def evaluate(self, source_document: str, model_results: list[ModelResult]) -> dict[str, EvaluationResult]:
        semantic_scores = self._semantic_similarity_scores(model_results)
        coverage_scores = self._coverage_scores(source_document, model_results)
        latency_ranks = self._latency_ranks(model_results)
        cost_ranks = self._cost_ranks(model_results)
        evaluations = {}

        for result in model_results:
            evaluations[result.model_name] = EvaluationResult(
                semantic_sim = semantic_scores[result.model_name],
                coverage_score= coverage_scores[result.model_name],
                compression_ratio = self._compression_ratio(source_document, result.summary),
                latency_rank = latency_ranks[result.model_name],
                cost_rank = cost_ranks[result.model_name]
            )

        return evaluations
    
