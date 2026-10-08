from pathlib import Path
from brain.rag import RAGBrain
from core.logger import get_logger
from config.settings import DATA_DIR

logger = get_logger("brain.rag_integration")

class RAGIntegration:
    """Load documents and add to RAG"""
    
    def __init__(self):
        self.rag = RAGBrain()
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info("RAGIntegration initialized")
    
    def load_text_file(self, filepath: str):
        """Text file load chey and RAG lo add chey"""
        path = Path(filepath)
        if not path.exists():
            return f"File not found: {filepath}"
        
        try:
            content = path.read_text()
            chunks = self._chunk_text(content, chunk_size=500)
            
            for i, chunk in enumerate(chunks):
                self.rag.add_document(
                    chunk,
                    metadata={"source": str(path), "chunk": i}
                )
            
            return f"Loaded {len(chunks)} chunks from {filepath}"
        except Exception as e:
            logger.error(f"Load error: {e}")
            return f"Error: {e}"
    
    def load_directory(self, dirpath: str):
        """Directory lo anni .txt files load chey"""
        path = Path(dirpath)
        if not path.exists():
            return f"Directory not found: {dirpath}"
        
        results = []
        for txt_file in path.glob("*.txt"):
            result = self.load_text_file(str(txt_file))
            results.append(f"{txt_file.name}: {result}")
        
        return "\n".join(results) if results else "No .txt files found"
    
    def _chunk_text(self, text: str, chunk_size: int = 500):
        """Text ni chunks ga split chey"""
        words = text.split()
        chunks = []
        current = []
        current_len = 0
        
        for word in words:
            current.append(word)
            current_len += len(word) + 1
            if current_len >= chunk_size:
                chunks.append(" ".join(current))
                current = []
                current_len = 0
        
        if current:
            chunks.append(" ".join(current))
        
        return chunks
    
    def query(self, question: str):
        """RAG query"""
        return self.rag.query(question)
    
    def count(self):
        """Total documents count"""
        return self.rag.count()

