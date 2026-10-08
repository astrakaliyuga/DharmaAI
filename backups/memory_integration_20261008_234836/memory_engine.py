from brain.engine import BrainEngine
from memory.store import MemoryStore
from memory.context import MemoryContext


class MemoryAwareBrain:
    """
    DharmaAI brain with persistent memory retrieval.

    Flow:
        Task
          -> Memory Retrieval
          -> Context
          -> BrainEngine
          -> Ollama
    """

    def __init__(self, memory_store=None):
        self.brain = BrainEngine()
        self.memory_store = memory_store or MemoryStore()
        self.memory_context = MemoryContext(self.memory_store)

    def run(self, prompt, complexity="normal", memory_limit=5):
        context = self.memory_context.build_context(
            prompt,
            limit=memory_limit,
        )

        if context:
            final_prompt = (
                f"{context}\n\n"
                f"Current task:\n{prompt}"
            )
        else:
            final_prompt = prompt

        result = self.brain.run(
            final_prompt,
            complexity=complexity,
        )

        result["memory_context"] = context
        result["memory_used"] = bool(context)

        return result
