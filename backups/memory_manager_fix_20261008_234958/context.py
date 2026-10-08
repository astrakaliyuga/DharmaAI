from memory.store import MemoryStore


class MemoryContext:
    """
    Converts stored memories into context text
    that can later be supplied to the Brain.
    """

    def __init__(self, store=None):
        self.store = store or MemoryStore()

    def retrieve(self, query, limit=5):
        return self.store.search(query, limit=limit)

    def build_context(self, query, limit=5):
        memories = self.retrieve(query, limit=limit)

        if not memories:
            return ""

        lines = [
            "Relevant DharmaAI memory:"
        ]

        for memory in memories:
            lines.append(
                f"- [{memory['category']}] "
                f"{memory['content']}"
            )

        return "\n".join(lines)
