from memory.long_term import LongTermMemory
from memory.store import MemoryStore


class MemoryManager:
    """
    Unified DharmaAI memory interface.

    Sources:
        - ChromaDB long-term semantic memory
        - JSONL structured memory

    Retrieval:
        - Long-term ChromaDB is the primary source.
        - JSONL memories are included when available.
        - Duplicate documents are removed.
    """

    def __init__(
        self,
        long_term=None,
        structured_store=None,
    ):
        self.long_term = long_term or LongTermMemory()
        self.structured_store = structured_store or MemoryStore()

    def retrieve(self, query, limit=5):
        if not query or not query.strip():
            return []

        memories = []
        seen = set()

        # Primary retrieval: ChromaDB semantic + lexical hybrid search.
        result = self.long_term.search(
            query,
            n_results=limit,
        )

        documents = result.get("documents", [[]])[0]
        ids = result.get("ids", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        for i, document in enumerate(documents):
            document = (document or "").strip()

            if not document or document in seen:
                continue

            seen.add(document)

            metadata = (
                metadatas[i]
                if i < len(metadatas)
                else {}
            )

            memories.append(
                {
                    "id": ids[i] if i < len(ids) else None,
                    "category": metadata.get(
                        "category",
                        metadata.get("type", "long_term"),
                    ),
                    "content": document,
                    "metadata": metadata,
                    "source": "chroma",
                }
            )

        # Secondary retrieval: structured JSONL memory.
        structured = self.structured_store.search(
            query,
            limit=limit,
        )

        for memory in structured:
            document = memory["content"].strip()

            if not document or document in seen:
                continue

            seen.add(document)

            memories.append(
                {
                    "id": memory.get("id"),
                    "category": memory.get(
                        "category",
                        "structured",
                    ),
                    "content": document,
                    "metadata": memory.get(
                        "metadata",
                        {},
                    ),
                    "source": "jsonl",
                }
            )

        return memories[:limit]

    def build_context(self, query, limit=5):
        memories = self.retrieve(
            query,
            limit=limit,
        )

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

    def count_long_term(self):
        return self.long_term.count()

    def count_structured(self):
        return self.structured_store.count()
