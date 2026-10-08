import chromadb
from chromadb.config import Settings
from datetime import datetime
from config.settings import MEMORY_DIR
from core.logger import get_logger

logger = get_logger("memory.long_term")

class LongTermMemory:
    def __init__(self, collection_name: str = "dharma_memory"):
        self.client = chromadb.PersistentClient(
            path=str(MEMORY_DIR / "chroma_db")
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        logger.info(f"LongTermMemory initialized: {collection_name}")
    
    def add(self, content: str, metadata: dict = None, doc_id: str = None):
        if doc_id is None:
            doc_id = f"mem_{datetime.now().timestamp()}"
        
        meta = metadata or {}
        meta["timestamp"] = datetime.now().isoformat()
        
        self.collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[doc_id]
        )
        logger.info(f"Added to long-term memory: {content[:50]}...")
        return doc_id
    
    def search(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def count(self):
        return self.collection.count()
    
    def clear(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name
        )
        logger.info("Long-term memory cleared")
