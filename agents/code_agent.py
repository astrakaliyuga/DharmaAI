import subprocess
import tempfile
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.code")

class CodeAgent(BaseAgent):
    """Python code execution agent"""
    
    def __init__(self):
        super().__init__("CodeAgent", "Run Python code safely")
        self.temp_dir = Path("/mnt/kaliyuga/DharmaAI/workspace/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def can_handle(self, task: str) -> bool:
        # Only if task starts with "python" or "code"
        task_lower = task.lower()
        return task_lower.startswith("python ") or task_lower.startswith("code ")
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "No code provided"
        
        code = parts[1].strip()
        temp_file = self.temp_dir / "temp_code.py"
        temp_file.write_text(code)
        
        try:
            result = subprocess.run(
                ["python3", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout + result.stderr
            return output.strip() or "(no output)"
        except subprocess.TimeoutExpired:
            return "Code execution timed out (15s)"
        except Exception as e:
            return f"Error: {e}"
