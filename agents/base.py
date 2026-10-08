from core.logger import get_logger

logger = get_logger("agents.base")

class BaseAgent:
    """Base agent — anni agents ki parent class"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
    
    def run(self, task: str) -> str:
        raise NotImplementedError(f"{self.name} must implement run()")
    
    def can_handle(self, task: str) -> bool:
        return False
    
    def __repr__(self):
        return f"<{self.name}: {self.description}>"
