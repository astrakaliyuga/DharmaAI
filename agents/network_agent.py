import subprocess
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.network")

class NetworkAgent(BaseAgent):
    """Network tools agent"""
    
    def __init__(self):
        super().__init__("NetworkAgent", "Network tools: ping, curl, whois, dig")
        self.allowed = ["ping", "curl", "whois", "dig", "nslookup", "traceroute", "host"]
    
    def can_handle(self, task: str) -> bool:
        keywords = ["ping", "curl", "whois", "dig", "nslookup", "network"]
        return any(kw in task.lower() for kw in keywords)
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=2)
        if len(parts) < 2:
            return "Usage: ping <host>, curl <url>, whois <domain>"
        
        cmd = parts[0].lower()
        if cmd not in self.allowed:
            return f"Command not allowed: {cmd}\nAllowed: {', '.join(self.allowed)}"
        
        args = " ".join(parts[1:])
        try:
            result = subprocess.run(f"{cmd} {args}", shell=True, capture_output=True, text=True, timeout=30)
            output = (result.stdout + result.stderr).strip()
            return output[:2000] if output else "(no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out (30s)"
        except Exception as e:
            return f"Error: {e}"
