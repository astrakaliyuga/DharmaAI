from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.pdf")

class PDFAgent(BaseAgent):
    """PDF read agent"""
    
    def __init__(self):
        super().__init__("PDFAgent", "PDF read, extract text")
    
    def can_handle(self, task: str) -> bool:
        return "pdf" in task.lower()
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=2)
        if len(parts) < 3:
            return "Usage: pdf read <file.pdf>"
        return self._read_pdf(parts[2].strip())
    
    def _read_pdf(self, filepath: str) -> str:
        try:
            import PyPDF2
            path = Path(filepath)
            if not path.exists():
                return f"File not found: {filepath}"
            
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text[:5000]
        except ImportError:
            return "PyPDF2 not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF error: {e}"

