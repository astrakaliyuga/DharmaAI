import subprocess
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.scheduler")

class SchedulerAgent(BaseAgent):
    """Cron job scheduler agent"""
    
    def __init__(self):
        super().__init__("SchedulerAgent", "Cron jobs, scheduled tasks")
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("schedule ") or task.lower().startswith("cron ")
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=2)
        if len(parts) < 2:
            return "Usage: schedule list | schedule add <cron> <command>"
        
        action = parts[1].lower()
        
        if action == "list":
            return self._list_cron()
        elif action == "add" and len(parts) >= 3:
            return self._add_cron(parts[2])
        return f"Unknown action: {action}"
    
    def _list_cron(self) -> str:
        try:
            result = subprocess.run("crontab -l", shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout.strip() or "No cron jobs"
        except Exception as e:
            return f"Error: {e}"
    
    def _add_cron(self, cron_spec: str) -> str:
        return f"To add: (crontab -l; echo '{cron_spec}') | crontab -"
