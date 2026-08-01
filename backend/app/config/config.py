from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


SUPPORTED_MODELS = {
    "openai": ["gpt-4o-mini"],
    "gemini": ["gemini-3.1-flash-lite"],
    "deepseek": ["deepseek-v4-flash"],
    "together": ["Qwen/Qwen3.5-9B", "meta-llama/Llama-3.3-70B-Instruct-Turbo", "MiniMax-M3"]
}

MAX_MODELS_PER_REQUEST = 3

MAX_FILE_SIZE = 10

MAX_CHUNK_TOKENS = 1000

PROMPT_BUFFER = 200

DEFAULT_TEMPERATURE = 0.2

DEFAULT_MAX_SUMMARY_TOKENS = 500

SUMMARY_TIMEOUT_SECS = 60

DIRECT_SUMMARIZATION_LIMIT = 15000

MAX_PARALLEL_REQS = 5

SIMILARITY_THRESHOLD = 0.7

ENABLE_COVERAGE_SCORING = False
# Coverage score calculation is very heavy and slow, constrained for production server, hence keeping this setting to false to disable this metric.

PROGRESS = {
    "PARSING": 15,
    "CHUNKING": 30,
    "SUMMARIZING": 60,
    "SCORING": 80,
    "CONSOLIDATING": 90,
    "COMPLETED": 100
}

SUMMARY_STYLE_CONFIG = {
    "concise": {
        "ratio": 0.20,
        "min_tokens": 150,
        "max_tokens": 500
    },

    "comprehensive": {
        "ratio": 0.35,
        "min_tokens": 300,
        "max_tokens": 1200
    },

    "detailed": {
        "ratio": 0.50,
        "min_tokens": 600,
        "max_tokens": 2000
    }
}

MODEL_COSTS = {
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60
    },

    "gemini-3.1-flash-lite": {
        "input": 0.25,
        "output": 1.50
    },

    "deepseek-v4-flash": {
        "input": 0.14,
        "output": 0.28
    },

    "Qwen/Qwen3.5-9B": {
        "input": 0.17,
        "output": 0.25
    },

    "meta-llama/Llama-3.3-70B-Instruct-Turbo": {
        "input": 1.04,
        "output": 1.04
    },

    "MiniMaxAI/MiniMax-M3": {
        "input": 0.30,
        "output": 1.20
    }
}


REDIS_TTL_SECS = 1800
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_SSL = os.getenv("REDIS_SSL", "false").lower() == "true"


SUPPORTED_CONTENT_TYPES = {
    "application/pdf", 
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
    "application/msword",
    "text/plain"
}