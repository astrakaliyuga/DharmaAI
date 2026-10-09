import base64
import hashlib
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.encryption")

class EncryptionAgent(BaseAgent):
    """Encryption agent — base64, hash"""
    
    def __init__(self):
        super().__init__("EncryptionAgent", "Encryption, hashing")
    
    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return (
            task_lower.startswith("encrypt ") or
            task_lower.startswith("decrypt ") or
            task_lower.startswith("hash ")
        )
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=2)
        if len(parts) < 3:
            return "Usage: encrypt <text> | decrypt <base64> | hash <text>"
        
        action = parts[0].lower()
        content = parts[1] + (" " + parts[2] if len(parts) > 2 else "")
        
        if action == "encrypt":
            return base64.b64encode(content.encode()).decode()
        elif action == "decrypt":
            try:
                return base64.b64decode(content.encode()).decode()
            except Exception as e:
                return f"Decrypt error: {e}"
        elif action == "hash":
            return hashlib.sha256(content.encode()).hexdigest()
        return f"Unknown action: {action}"
