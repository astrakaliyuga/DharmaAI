from memory.manager import MemoryManager


class MemoryContext:
    """
    DharmaAI memory context builder.

    Uses the unified MemoryManager.

    Backward compatibility:
        Older callers may pass a MemoryStore directly.
        In that case it becomes the structured memory layer
        of a MemoryManager.
    """

    def __init__(self, manager=None):
        if isinstance(manager, MemoryManager):
            self.manager = manager
        elif manager is not None:
            # Compatibility with the older API:
            # MemoryContext(MemoryStore(...))
            self.manager = MemoryManager(
                structured_store=manager
            )
        else:
            self.manager = MemoryManager()

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
