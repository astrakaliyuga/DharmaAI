import urllib.request
import urllib.parse
import json
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.api")

class APIAgent(BaseAgent):
    """REST API agent"""
    
    def __init__(self):
        super().__init__("APIAgent", "REST API calls")
    
    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return (
            task_lower.startswith("api get ") or
            task_lower.startswith("api post ")
        )
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=3)
        if len(parts) < 3:
            return "Usage: api get <url> | api post <url> <data>"
        
        method = parts[1].lower()
        url = parts[2]
        
        if method == "get":
            return self._get(url)
        elif method == "post" and len(parts) >= 4:
            return self._post(url, parts[3])
        return f"Unknown method: {method}"
    
    def _get(self, url: str) -> str:
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            req = urllib.request.Request(url, headers={'User-Agent': 'DharmaAI/1.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8', errors='ignore')[:2000]
        except Exception as e:
            return f"API error: {e}"
    
    def _post(self, url: str, data: str) -> str:
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            req = urllib.request.Request(
                url,
                data=data.encode(),
                headers={'Content-Type': 'application/json', 'User-Agent': 'DharmaAI/1.0'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8', errors='ignore')[:2000]
        except Exception as e:
            return f"API error: {e}"
