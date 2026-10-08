from memory.long_term import LongTermMemory
from memory.short_term import ShortTermMemory
from memory.store import MemoryStore


class MemoryManager:
    """
    Unified DharmaAI memory interface.

    Memory layers:

        1. Short-term memory
        2. ChromaDB long-term semantic memory
        3. JSONL structured memory

    ChromaDB is the primary knowledge retrieval layer.
    """

    def __init__(
        self,
        long_term=None,
        short_term=None,
        structured_store=None,
    ):
        self.long_term = long_term or LongTermMemory()
        self.short_term = short_term or ShortTermMemory()
        self.structured_store = (
            structured_store or MemoryStore()
        )

    def remember_short_term(self, content):
        """
        Add a memory to the active short-term context.
        """
        if not content or not content.strip():
            raise ValueError(
                "Short-term memory content cannot be empty"
            )

        return self.short_term.add(content.strip())

    def remember_long_term(
        self,
        content,
        category="general",
        metadata=None,
        doc_id=None,
    ):
        """
        Add persistent semantic memory to ChromaDB.
        """
        metadata = dict(metadata or {})
        metadata["category"] = category

        return self.long_term.add(
            content=content,
            metadata=metadata,
            doc_id=doc_id,
        )

    def remember_structured(
        self,
        content,
        category="general",
        metadata=None,
    ):
        """
        Add persistent structured JSONL memory.
        """
        return self.structured_store.add(
            content=content,
            category=category,
            metadata=metadata,
        )

    def retrieve(
        self,
        query,
        limit=5,
    ):
        """
        Retrieve unified memory.

        Priority:
            1. ChromaDB long-term semantic memory
            2. Short-term active memory
            3. JSONL structured memory
        """

        if not query or not query.strip():
            return []

        memories = []
        seen = set()

        # --------------------------------------------------
        # 1. Long-term ChromaDB
        # --------------------------------------------------

        result = self.long_term.search(
            query,
            n_results=limit,
        )

        documents = result.get(
            "documents",
            [[]],
        )[0]

        ids = result.get(
            "ids",
            [[]],
        )[0]

        metadatas = result.get(
            "metadatas",
            [[]],
        )[0]

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
                    "id": (
                        ids[i]
                        if i < len(ids)
                        else None
                    ),
                    "category": metadata.get(
                        "category",
                        metadata.get(
                            "type",
                            "long_term",
                        ),
                    ),
                    "content": document,
                    "metadata": metadata,
                    "source": "chroma",
                }
            )

        # --------------------------------------------------
        # 2. Short-term memory
        # --------------------------------------------------

        try:
            short_items = self.short_term.get_all()
        except AttributeError:
            short_items = []

        for item in short_items:
            if isinstance(item, dict):
                document = str(
                    item.get("content", "")
                ).strip()
            else:
                document = str(item).strip()

            if not document or document in seen:
                continue

            seen.add(document)

            memories.append(
                {
                    "id": None,
                    "category": "short_term",
                    "content": document,
                    "metadata": {},
                    "source": "short_term",
                }
            )

        # --------------------------------------------------
        # 3. Structured JSONL memory
        # --------------------------------------------------

        structured = self.structured_store.search(
            query,
            limit=limit,
        )

        for memory in structured:
            document = (
                memory["content"]
                .strip()
            )

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

    def build_context(
        self,
        query,
        limit=5,
    ):
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
                f"- [{memory['source']}] "
                f"[{memory['category']}] "
                f"{memory['content']}"
            )

        return "\n".join(lines)

    def count_long_term(self):
        return self.long_term.count()

    def count_short_term(self):
        try:
            return len(
                self.short_term.get_all()
            )
        except AttributeError:
            return 0

    def count_structured(self):
        return self.structured_store.count()
