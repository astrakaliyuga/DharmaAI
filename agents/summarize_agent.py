from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.summarize")

class SummarizeAgent(BaseAgent):
    """Text summarization agent"""
    
    def __init__(self):
        super().__init__("SummarizeAgent", "Text summarization")
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("summarize ")
    
    def run(self, task: str, **kwargs) -> str:
        text = task[10:].strip()
        if not text:
            return "Usage: summarize <text>"
        return self._summarize(text)
    
    def _summarize(self, text: str) -> str:
        try:
            import ollama
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[{"role": "user", "content": f"Summarize this in 2-3 sentences:\n\n{text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Summarize error: {e}"
