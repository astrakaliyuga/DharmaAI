from pathlib import Path
from datetime import datetime
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.file_watcher")

class FileWatcherAgent(BaseAgent):
    """File watcher agent"""
    
    def __init__(self):
        super().__init__("FileWatcherAgent", "Monitor file changes")
        self.watch_dir = Path("/mnt/kaliyuga/DharmaAI/workspace")
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("watch ")
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: watch <directory>"
        
        dirpath = Path(parts[1].strip())
        if not dirpath.exists():
            return f"Directory not found: {dirpath}"
        
        files = sorted(dirpath.rglob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
        result = f"Recent files in {dirpath}:\n"
        for f in files[:10]:
            if f.is_file():
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                result += f"  {f.name} ({mtime})\n"
        return result
