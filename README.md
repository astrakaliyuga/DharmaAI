# 🧠 DharmaAI

**Personal AI Assistant with 20 Agents**

Built from scratch on Kali Linux using local models.

## 🚀 Features

- **20 Agents**: File, Shell, Code, Web, Voice, Image, Video, System, Network, Database, PDF, Backup, Email, Scheduler, Encryption, FileWatcher, API, Translate, Summarize, Sentiment
- **Multi-Command**: Use `,` to separate commands
- **Personal Commands**: `/morning`, `/me`, `/work`
- **Memory**: Short-term + Long-term (ChromaDB)
- **RAG**: Retrieval Augmented Generation
- **Security Registry**: 7 security tools (recommendations only)
- **Planner + Orchestrator**: Task planning and execution
- **38 Tests**: All passing
- **Automatic Backup**: Daily 2 AM via cron
- **Docker**: Containerized
- **CI/CD**: GitHub Actions

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Ollama (qwen2.5:0.5b) |
| Image | Stable Diffusion v1.5 |
| Voice | Piper |
| STT | Whisper |
| Vector DB | ChromaDB |
| Framework | LangChain |
| Video | ffmpeg |

## ⚡ Quick Start

```bash
# Clone repo
git clone https://github.com/astrakaliyuga/DharmaAI.git
cd DharmaAI

# Activate venv
source ~/ai-lab/venv/bin/activate

# Run chat
python3 chat.py

# Run web UI
python3 web_ui.py
# Browser: http://localhost:5000
