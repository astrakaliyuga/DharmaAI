import urllib.request
import urllib.parse
import json
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.web")

class WebAgent(BaseAgent):
    """Web search and fetch agent"""
    
    def __init__(self):
        super().__init__("WebAgent", "Web search and URL fetch")
    
    def can_handle(self, task: str) -> bool:
        keywords = ["search", "fetch", "url", "web", "http"]
        return any(kw in task.lower() for kw in keywords)
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "No task provided. Use: 'search <query>' or 'fetch <url>'"
        
        action = parts[0].lower()
        content = parts[1].strip()
        
        if action == "search":
            return self._search(content)
        elif action == "fetch":
            return self._fetch(content)
        else:
            return f"Unknown action: {action}\nUse: 'search <query>' or 'fetch <url>'"
    
    def _search(self, query: str) -> str:
        """DuckDuckGo search — free API"""
        try:
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            results = []
            if data.get('AbstractText'):
                results.append(f"Abstract: {data['AbstractText']}")
            
            if data.get('RelatedTopics'):
                for topic in data['RelatedTopics'][:5]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        results.append(f"- {topic['Text']}")
            
            return "\n".join(results) if results else "No results found"
        except Exception as e:
            logger.error(f"Search error: {e}")
            return f"Search error: {e}"
    
    def _fetch(self, url: str) -> str:
        """URL fetch — first 2000 chars"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            # Simple HTML strip
            import re
            content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()
            
            return content[:2000]
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return f"Fetch error: {e}"
