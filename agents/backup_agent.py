import subprocess
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.backup")

class BackupAgent(BaseAgent):
    """Backup agent"""
    
    def __init__(self):
        super().__init__("BackupAgent", "Backup and restore")
        self.backup_dir = Path("/mnt/kaliyuga/backups/DharmaAI")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("backup")
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split()
        # "backup list" → action = "list"
        # "backup run"  → action = "run"
        if len(parts) >= 2:
            action = parts[1].lower()
        else:
            action = "list"
        
        if action == "run":
            return self._run_backup()
        else:
            return self._list_backups()
    
    def _run_backup(self) -> str:
        try:
            result = subprocess.run(
                "/mnt/kaliyuga/DharmaAI/backup.sh",
                shell=True, capture_output=True, text=True, timeout=120
            )
            return "Backup completed" if result.returncode == 0 else f"Failed: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"
    
    def _list_backups(self) -> str:
        backups = sorted(self.backup_dir.glob("*.tar.gz"), reverse=True)
        if not backups:
            return "No backups found"
        result = "Backups:\n"
        for b in backups[:10]:
            result += f"  {b.name} ({b.stat().st_size // 1024} KB)\n"
        return result
