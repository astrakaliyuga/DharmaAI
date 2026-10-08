from memory.manager import MemoryManager


class MemoryContext:
    """
    DharmaAI memory context builder.

    Uses the unified MemoryManager instead of directly
    querying the JSONL store.
    """

    def __init__(self, manager=None):
        self.manager = manager or MemoryManager()

    def retrieve(self, query, limit=5):
        return self.manager.retrieve(
            query,
            limit=limit,
        )

    def build_context(self, query, limit=5):
        return self.manager.build_context(
            query,
            limit=limit,
        )
