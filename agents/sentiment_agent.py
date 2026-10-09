from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.sentiment")

class SentimentAgent(BaseAgent):
    """Sentiment analysis agent"""
    
    def __init__(self):
        super().__init__("SentimentAgent", "Sentiment analysis")
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("sentiment ")
    
    def run(self, task: str, **kwargs) -> str:
        text = task[10:].strip()
        if not text:
            return "Usage: sentiment <text>"
        try:
            import ollama
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[{"role": "user", "content": f"Analyze sentiment (positive/negative/neutral) of:\n\n{text}\n\nReply in one line."}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Sentiment error: {e}"
