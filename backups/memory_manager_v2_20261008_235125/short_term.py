from collections import deque
from datetime import datetime
from config.settings import MEMORY_DIR
import json

class ShortTermMemory:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.memory = deque(maxlen=max_size)
    
    def add(self, content: str, metadata: dict = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "metadata": metadata or {}
        }
        self.memory.append(entry)
        return entry
    
    def get_recent(self, n: int = 10):
        return list(self.memory)[-n:]
    
    def clear(self):
        self.memory.clear()
    
    def save(self, filename: str = "short_term.json"):
        path = MEMORY_DIR / filename
        with open(path, 'w') as f:
            json.dump(list(self.memory), f, indent=2)
        return path
    
    def load(self, filename: str = "short_term.json"):
        path = MEMORY_DIR / filename
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                self.memory = deque(data, maxlen=self.max_size)
        return self.memory
