import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from config.settings import MEMORY_DIR


class MemoryStore:
    """
    Persistent JSONL memory store for DharmaAI.

    Each memory is stored as one JSON object per line.
    """

    def __init__(self, filename="memories.jsonl"):
        self.path = Path(MEMORY_DIR) / filename
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def add(self, content, category="general", metadata=None):
        if not content or not content.strip():
            raise ValueError("Memory content cannot be empty")

        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "content": content.strip(),
            "metadata": metadata or {},
        }

        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(memory, ensure_ascii=False) + "\n")

        return memory

    def all(self):
        memories = []

        if not self.path.exists():
            return memories

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                memories.append(json.loads(line))

        return memories

    def search(self, query, limit=5):
        query_words = {
            word.lower()
            for word in query.split()
            if word.strip()
        }

        if not query_words:
            return []

        scored = []

        for memory in self.all():
            text = memory["content"].lower()

            score = sum(
                1
                for word in query_words
                if word in text
            )

            if score > 0:
                scored.append((score, memory))

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1]["timestamp"],
            )
        )

        return [
            memory
            for score, memory in scored[:limit]
        ]

    def count(self):
        return len(self.all())
