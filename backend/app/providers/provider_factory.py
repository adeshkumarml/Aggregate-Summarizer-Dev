from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.deepseek_provider import DeepseekProvider
from app.providers.together_provider import TogetherProvider

class ProviderFactory:

    @staticmethod
    def get_provider(provider_name: str, model_name: str):
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            return OpenAIProvider(model_name = model_name)
         
        elif provider_name == "gemini":
            return GeminiProvider(model_name = model_name)
        
        elif provider_name == "deepseek":
            return DeepseekProvider(model_name = model_name)
        
        elif provider_name == "together":
            return TogetherProvider(model_name = model_name)
        
        raise ValueError(f"Unknown provider: {provider_name}")

