from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.translate")

class TranslateAgent(BaseAgent):
    """Translation agent"""
    
    def __init__(self):
        super().__init__("TranslateAgent", "Multi-language translation")
    
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
        try:
            from deep_translator import GoogleTranslator
            result = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
            return result
        except Exception as e:
            return f"Translation error: {e}"
