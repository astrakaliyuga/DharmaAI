from memory.long_term import LongTermMemory
from core.logger import get_logger
import ollama

logger = get_logger("brain.rag")

class RAGBrain:
    """RAG — Retrieval Augmented Generation"""
    
    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.model = model
        self.memory = LongTermMemory()
        logger.info(f"RAGBrain initialized with model: {model}")
    
    def add_document(self, content: str, metadata: dict = None):
        """Document ni knowledge base lo add chey"""
        doc_id = self.memory.add(content, metadata=metadata)
        logger.info(f"Document added: {content[:50]}...")
        return doc_id
    
    def query(self, question: str, n_results: int = 5) -> str:
        """Question ki answer — knowledge base nunchi"""
        results = self.memory.search(question, n_results=n_results)
        
        if not results['documents'] or not results['documents'][0]:
            logger.warning("No relevant documents found")
            return "I don't have any relevant information about that."
        
        context = "\n\n".join(results['documents'][0])
        
        prompt = f"""Answer the question based on the following context:

Context:
{context}

Question: {question}

Answer:"""
        
        logger.info(f"Querying with {len(results['documents'][0])} relevant docs")
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        answer = response['message']['content']
        logger.info(f"Answer: {answer[:50]}...")
        return answer
    
    def count(self):
        """Total documents chudu"""
        return self.memory.count()
