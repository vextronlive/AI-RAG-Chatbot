import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# PROVIDER SELECTION
# =============================================================================

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

# =============================================================================
# GROQ CONFIG
# =============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Updated Groq models (2026 supported)
# Recommended models:
# llama-3.1-8b-instant (fast)
# llama-3.1-70b-versatile (better quality)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

# =============================================================================
# OLLAMA CONFIG
# =============================================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

# =============================================================================
# OPENAI CONFIG
# =============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-3.5-turbo"
)

# =============================================================================
# EMBEDDINGS
# =============================================================================

EMBEDDING_PROVIDER = os.getenv(
    "EMBEDDING_PROVIDER",
    "huggingface"
).lower()

HUGGINGFACE_EMBEDDING_MODEL = os.getenv(
    "HUGGINGFACE_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"

# =============================================================================
# VECTOR STORE
# =============================================================================

VECTOR_STORE_PATH = "data/vector_store.faiss"

TOP_K_RETRIEVAL = 3

# =============================================================================
# CHAT SETTINGS
# =============================================================================

MAX_HISTORY_LENGTH = 10

LLM_TEMPERATURE = 0.7

MAX_TOKENS = 500

# =============================================================================
# DOCUMENT PROCESSING
# =============================================================================

UPLOAD_DIR = "data/uploads"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_llm_config():

    if LLM_PROVIDER == "groq":

        return {
            "provider": "groq",
            "model": GROQ_MODEL,
            "api_key": GROQ_API_KEY,
            "base_url": None
        }

    elif LLM_PROVIDER == "ollama":

        return {
            "provider": "ollama",
            "model": OLLAMA_MODEL,
            "api_key": None,
            "base_url": OLLAMA_BASE_URL
        }

    elif LLM_PROVIDER == "openai":

        return {
            "provider": "openai",
            "model": OPENAI_MODEL,
            "api_key": OPENAI_API_KEY,
            "base_url": None
        }

    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def get_embedding_config():

    if EMBEDDING_PROVIDER == "huggingface":

        return {
            "provider": "huggingface",
            "model": HUGGINGFACE_EMBEDDING_MODEL
        }

    elif EMBEDDING_PROVIDER == "openai":

        return {
            "provider": "openai",
            "model": OPENAI_EMBEDDING_MODEL
        }

    else:
        raise ValueError(f"Unknown embedding provider: {EMBEDDING_PROVIDER}")


# =============================================================================
# VALIDATION
# =============================================================================


def validate_config():

    llm_config = get_llm_config()

    if llm_config["provider"] == "groq":

        if not llm_config["api_key"]:
            raise ValueError(
                "GROQ_API_KEY missing.\n"
                "Get free key: https://console.groq.com/keys\n"
                "Add to .env: GROQ_API_KEY=your_key"
            )

        print(f"✅ Using Groq model: {GROQ_MODEL}")

    elif llm_config["provider"] == "ollama":

        print(f"✅ Using Ollama model: {OLLAMA_MODEL}")
        print("Make sure Ollama is running: ollama serve")

    elif llm_config["provider"] == "openai":

        if not llm_config["api_key"]:
            raise ValueError("OPENAI_API_KEY missing")

        print(f"✅ Using OpenAI model: {OPENAI_MODEL}")

    embed_config = get_embedding_config()

    if embed_config["provider"] == "huggingface":

        print(f"✅ Using HuggingFace embeddings: {HUGGINGFACE_EMBEDDING_MODEL}")

    elif embed_config["provider"] == "openai":

        if not OPENAI_API_KEY:
            raise ValueError("OpenAI embeddings require OPENAI_API_KEY")

        print(f"✅ Using OpenAI embeddings: {OPENAI_EMBEDDING_MODEL}")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)

    print("✅ Configuration validated successfully")