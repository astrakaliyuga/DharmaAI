from brain.engine import BrainEngine
from memory.manager import MemoryManager
from memory.context import MemoryContext


class MemoryAwareBrain:
    """
    DharmaAI brain with unified persistent memory.

    Flow:
        Task
          -> MemoryManager
          -> MemoryContext
          -> BrainEngine
          -> Router
          -> Ollama
          -> Response

    Backward compatibility:
        memory_store=... is accepted as an alias for the
        structured JSONL memory layer.
    """

    def __init__(
        self,
        memory_manager=None,
        memory_store=None,
    ):
        self.brain = BrainEngine()

        # New API takes priority.
        if memory_manager is not None:
            self.memory_manager = memory_manager

        # Compatibility with the previous API:
        # MemoryAwareBrain(memory_store=store)
        elif memory_store is not None:
            self.memory_manager = MemoryManager(
                structured_store=memory_store
            )

        else:
            self.memory_manager = MemoryManager()

        self.memory_context = MemoryContext(
            self.memory_manager
        )

    def run(
        self,
        prompt,
        complexity="normal",
        memory_limit=5,
    ):
        context = self.memory_context.build_context(
            prompt,
            limit=memory_limit,
        )

        if context:
            final_prompt = (
                "You are DharmaAI, a local personal AI system.\n"
                "Use the provided memory as authoritative context "
                "about the DharmaAI project.\n"
                "Do not invent project facts that contradict the memory.\n\n"
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
