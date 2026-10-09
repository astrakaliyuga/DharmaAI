import ollama
from core.logger import get_logger
from core.language import LanguageHandler
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from datetime import datetime

logger = get_logger("brain.llm")

class LLMBrain:
    def __init__(self, model: str = "qwen2.5:0.5b", memory_size: int = 50):
        self.model = model
        self.conversation = []
        self.memory = ShortTermMemory(max_size=memory_size)
        self.long_term = LongTermMemory()
        self.language = LanguageHandler()
        logger.info(f"LLMBrain initialized with model: {model}")
    
    def think(self, prompt: str, telugu_mode: bool = False) -> str:
        is_telugu_unicode = self.language.detect_telugu(prompt)
        is_romanized = self.language.is_romanized_telugu(prompt)
        original_prompt = prompt
        
        # Telugu handling
        if is_romanized and not is_telugu_unicode:
            prompt_for_llm = prompt
        elif is_telugu_unicode and telugu_mode:
            prompt_for_llm = self.language.to_english(prompt)
        else:
            prompt_for_llm = prompt
        
        # Long-term memory search (optional — fast)
        relevant = self.long_term.search(prompt_for_llm, n_results=2)
        context = ""
        if relevant['documents'] and relevant['documents'][0]:
            context = "\n\nRelevant context from memory:\n"
            for doc in relevant['documents'][0]:
                context += f"- {doc}\n"
        
        # Short-term memory save
        self.memory.add(
            content=original_prompt,
            metadata={"type": "user_input", "language": "te" if (is_telugu_unicode or is_romanized) else "en"}
        )
        
        self.conversation.append({"role": "user", "content": prompt_for_llm})
        
        # Context tho LLM ki pampu
        if context:
            full_prompt = f"{context}\n\nUser: {prompt_for_llm}"
            messages = self.conversation[:-1] + [{"role": "user", "content": full_prompt}]
        else:
            messages = self.conversation
        
        logger.info(f"Thinking about: {prompt_for_llm[:50]}...")
        
        response = ollama.chat(
            model=self.model,
            messages=messages
        )
        
        reply = response['message']['content']
        
        self.conversation.append({"role": "assistant", "content": reply})
        self.memory.add(content=reply, metadata={"type": "assistant_response"})
        
        logger.info(f"Response: {reply[:50]}...")
        return reply
    
    def recall(self, n: int = 10):
        return self.memory.get_recent(n)
    
    def remember(self, content: str):
        self.long_term.add(content)
        logger.info(f"Remembered: {content[:50]}...")
    
    def search_memory(self, query: str, n: int = 5):
        return self.long_term.search(query, n_results=n)
    
    def reset(self):
        self.conversation = []
        logger.info("Conversation reset")
    
    def save_memory(self):
        path = self.memory.save()
        logger.info(f"Memory saved to {path}")
        return path
    
    def load_memory(self):
        self.memory.load()
        logger.info("Memory loaded")
