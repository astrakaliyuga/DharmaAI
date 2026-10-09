import psutil
import platform
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.system")

class SystemAgent(BaseAgent):
    """System information agent"""
    
    def __init__(self):
        super().__init__("SystemAgent", "System info, processes, resources")
    
    def can_handle(self, task: str) -> bool:
        keywords = ["system", "cpu", "ram", "memory", "disk", "process"]
        return any(kw in task.lower() for kw in keywords)
    
    def run(self, task: str, **kwargs) -> str:
        action = task.split()[0].lower() if task.split() else "info"
        
        if action in ["system", "info"]:
            return self._system_info()
        elif action == "cpu":
            return self._cpu_info()
        elif action in ["ram", "memory"]:
            return self._ram_info()
        elif action == "disk":
            return self._disk_info()
        elif action == "process":
            return self._process_info()
        return self._system_info()
    
    def _system_info(self) -> str:
        return f"""System: {platform.system()}
Node: {platform.node()}
Release: {platform.release()}
Machine: {platform.machine()}"""
    
    def _cpu_info(self) -> str:
        return f"CPU: {psutil.cpu_percent(interval=1)}% usage, {psutil.cpu_count()} cores"
    
    def _ram_info(self) -> str:
        mem = psutil.virtual_memory()
        return f"RAM: {mem.percent}% used ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)"
    
    def _disk_info(self) -> str:
        disk = psutil.disk_usage('/')
        return f"Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
    
    def _process_info(self) -> str:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                procs.append(p.info)
            except:
                pass
        procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        result = "Top 5 processes:\n"
        for p in procs[:5]:
            result += f"  PID {p['pid']}: {p['name']} ({p['cpu_percent']}%)\n"
        return result
