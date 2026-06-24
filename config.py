from pathlib import Path

# ----------------------------
# APP INFO
# ----------------------------
APP_NAME = "AI Assistant Pro Mode"

# ----------------------------
# PATHS
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
FEEDBACK_CSV = BASE_DIR / "feedback_report.csv"

# ----------------------------
# RETRIEVAL
# ----------------------------
TOP_K = 3
RETRIEVE_K = 15

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

MAX_CONTEXT_CHUNKS = TOP_K
MIN_CONTEXT_CHUNKS = 1

# ----------------------------
# MODELS
# ----------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

# ----------------------------
# LLM (OLLAMA ONLY — FIXED)
# ----------------------------
LLM_PROVIDER = "ollama"

OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434"

# fallback only
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

# ----------------------------
# GENERATION
# ----------------------------
MAX_NEW_TOKENS = 200
TEMPERATURE = 0.2