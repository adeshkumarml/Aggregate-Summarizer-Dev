from sentence_transformers import SentenceTransformer
import numpy as np

class Embedding:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    def embed_text_single(self, text: str) -> np.ndarray:
        if not text.strip():
            raise ValueError("Cannot embed empty text.")
        
        return self.model.encode(text, convert_to_numpy = True, normalize_embeddings = True)
    
    
    def embed_text_batch(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        
        return self.model.encode(texts, convert_to_numpy = True, normalize_embeddings = True)


