from pathlib import Path

# ----------------------------
# PROJECT PATHS
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
FEEDBACK_CSV = BASE_DIR / "feedback_report.csv"

# ----------------------------
# RETRIEVAL SETTINGS
# ----------------------------
TOP_K = 5                 # final chunks sent to LLM
RETRIEVE_K = 15           # initial retrieval before reranking

CHUNK_SIZE = 800          # characters per chunk
CHUNK_OVERLAP = 150       # overlap for context continuity

# ----------------------------
# EMBEDDING MODEL
# ----------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ----------------------------
# RERANKING MODEL
# ----------------------------
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ----------------------------
# LLM SETTINGS (Ollama recommended)
# ----------------------------
LLM_PROVIDER = "ollama"   # or "huggingface"

OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434"

# If you ever switch to HF again:
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

# ----------------------------
# GENERATION SETTINGS
# ----------------------------
MAX_NEW_TOKENS = 200
TEMPERATURE = 0.2

# ----------------------------
# APP SETTINGS
# ----------------------------
APP_NAME = "Custom AI Knowledge Assistant (PRO MODE)"
ENABLE_FEEDBACK = True
ENABLE_STATS = True