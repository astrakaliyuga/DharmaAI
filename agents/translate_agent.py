import time
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.translate")

class TranslateAgent(BaseAgent):
    """Translation agent — fast fail"""
    
    def __init__(self):
        super().__init__("TranslateAgent", "Multi-language translation")
        self.last_request_time = 0
        self.min_interval = 1.5
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("translate ")
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=3)
        if len(parts) < 4:
            return "Usage: translate <from> <to> <text>"
        
        from_lang = parts[1]
        to_lang = parts[2]
        text = parts[3]
        return self._translate(from_lang, to_lang, text)
    
    def _translate(self, from_lang: str, to_lang: str, text: str) -> str:
        # Rate limit — wait
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
        
        try:
            from deep_translator import GoogleTranslator
            return GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        except Exception as e:
            error_msg = str(e).lower()
            if "too many requests" in error_msg:
                return "Rate limit — wait 1 min and try again"
            return f"Translation error: {str(e)[:100]}"
