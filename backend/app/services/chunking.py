import re
import tiktoken
from app.models.domain_models import DocumentChunk

class Chunking:
    PAGE_PATTERN = r"~+\sPAGE\s+(\d+)\s*~+"

    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")


    def _estimate_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
    
    
    def _is_page_marker(self, text: str) -> bool:
        return bool(re.match(self.PAGE_PATTERN, text.strip()))
    
    
    def _extract_page_number(self, text: str) -> int:
        match = re.match(self.PAGE_PATTERN, text.strip())
        return int(match.group(1))
    

    def _split_sentences(self, text: str) -> list[str]:
        sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]
        return sentences


    def _split_words(self, text: str) -> list[str]:
        return text.split()


    def _split_paragraphs(self, text: str) -> list[str]:
        paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
        return paragraphs


    def _split_large_paragraph(self, paragraph: str, max_tokens: int = 1000) -> list[str]:
        sentences = self._split_sentences(paragraph)
        chunks = []
        current = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self._estimate_tokens(sentence)

            if current_tokens + sentence_tokens <= max_tokens:
                current.append(sentence)
                current_tokens += sentence_tokens 

            else:
                if current:
                    chunks.append(" ".join(current))

                if sentence_tokens > max_tokens:
                    words = (self._split_words(sentence))
                    current_words = []
                    current_word_tokens = 0

                    for word in words:
                        word_tokens = self._estimate_tokens(word)

                        if current_word_tokens + word_tokens <= max_tokens:
                            current_words.append(word)
                            current_word_tokens += word_tokens

                        else:
                            chunks.append(" ".join(current_words))
                            current_words = [word]
                            current_word_tokens = word_tokens
                    
                    if current_words:
                        chunks.append(" ".join(current_words))
                        
                    current = []
                    current_tokens = 0

                else:
                    current = [sentence]
                    current_tokens = sentence_tokens
        if current:
            chunks.append(" ".join(current))
            current =[]
            current_tokens = 0

        return chunks



    def chunk_text(self, text: str, max_tokens: int = 1000) -> list[DocumentChunk]:

        if not text.strip():
            return []

        paragraphs = self._split_paragraphs(text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        current_document_page = 1
        chunk_start_page = None
        chunk_end_page = None
        chunk_id = 1

        for paragraph in paragraphs:

            if self._is_page_marker(paragraph):
                current_document_page = self._extract_page_number(paragraph)
                continue

            paragraph_tokens = self._estimate_tokens(paragraph)
            
            if paragraph_tokens > max_tokens:
                if current_chunk:
                    chunks.append(DocumentChunk(chunk_id = chunk_id, text = "\n\n".join(current_chunk), estimated_tokens = current_tokens, 
                                                start_page = chunk_start_page, end_page = chunk_end_page))
                    chunk_id += 1
                
                current_chunk =[]
                current_tokens = 0
                chunk_start_page = None
                chunk_end_page = None

                subchunks = self._split_large_paragraph(paragraph, max_tokens)

                for subchunk in subchunks:        
                    chunks.append(DocumentChunk(chunk_id = chunk_id, text = subchunk, estimated_tokens = self._estimate_tokens(subchunk), 
                                                    start_page = current_document_page, end_page = current_document_page))
                    chunk_id += 1
                continue
                
            if current_tokens + paragraph_tokens <= max_tokens:
                if chunk_start_page is None:
                    chunk_start_page = current_document_page
                chunk_end_page = current_document_page
                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens
            
            else:
                if current_chunk:
                    chunks.append(DocumentChunk(chunk_id = chunk_id, text = "\n\n".join(current_chunk), estimated_tokens = current_tokens,
                                                start_page = chunk_start_page, end_page = chunk_end_page))
                    chunk_id += 1
                current_chunk = [paragraph]
                current_tokens = paragraph_tokens
                chunk_start_page = current_document_page
                chunk_end_page = current_document_page
                
        if current_chunk:
            chunks.append(DocumentChunk(chunk_id = chunk_id, text = "\n\n".join(current_chunk), estimated_tokens = current_tokens,
                                        start_page = chunk_start_page, end_page = chunk_end_page))
            chunk_id += 1

        return chunks