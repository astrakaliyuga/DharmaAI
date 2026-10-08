from pathlib import Path

# DharmaAI root directory
DharmaAI_ROOT = Path("/mnt/kaliyuga/DharmaAI")

# Main directories
MODELS_DIR = DharmaAI_ROOT / "models"
DATA_DIR = DharmaAI_ROOT / "data"
MEMORY_DIR = DharmaAI_ROOT / "memory"
PROJECTS_DIR = DharmaAI_ROOT / "projects"
BACKUPS_DIR = DharmaAI_ROOT / "backups"
LOGS_DIR = DharmaAI_ROOT / "logs"
TOOLS_DIR = DharmaAI_ROOT / "tools"
WORKSPACE_DIR = DharmaAI_ROOT / "workspace"

# AI model/cache directories
HUGGINGFACE_DIR = MODELS_DIR / "huggingface"
OLLAMA_DIR = MODELS_DIR / "ollama"

# Create directories if they don't exist
for directory in (
    MODELS_DIR,
    DATA_DIR,
    MEMORY_DIR,
    PROJECTS_DIR,
    BACKUPS_DIR,
    LOGS_DIR,
    TOOLS_DIR,
    WORKSPACE_DIR,
    HUGGINGFACE_DIR,
    OLLAMA_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# Local LLM configuration
OLLAMA_HOST = "http://127.0.0.1:11434"

DEFAULT_LLM_MODEL = "qwen2.5:1.5b"

AVAILABLE_LLM_MODELS = (
    "qwen2.5:1.5b",
    "qwen2.5:7b",
    "gemma2:9b",
)
