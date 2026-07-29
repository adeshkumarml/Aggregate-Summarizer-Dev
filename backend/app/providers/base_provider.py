from abc import ABC, abstractmethod
from app.models.domain_models import DocumentChunk, ModelResult

class BaseProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
    
    @abstractmethod
    async def summarize(self, chunks: list[DocumentChunk]) -> ModelResult:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass


    