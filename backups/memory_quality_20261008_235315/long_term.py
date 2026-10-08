import re

import chromadb
from datetime import datetime

from config.settings import MEMORY_DIR
from core.logger import get_logger


logger = get_logger("memory.long_term")


class LongTermMemory:
    """
    Persistent long-term memory using ChromaDB.

    Retrieval strategy:
        1. Chroma semantic search
        2. Exact/token lexical matching
        3. Combined reranking

    The existing Chroma collection and records are preserved.
    """

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "does",
        "for",
        "how",
        "in",
        "is",
        "of",
        "on",
        "the",
        "to",
        "what",
        "which",
        "where",
        "who",
        "with",
    }

    def __init__(self, collection_name: str = "dharma_memory"):
        self.client = chromadb.PersistentClient(
            path=str(MEMORY_DIR / "chroma_db")
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

        logger.info(
            f"LongTermMemory initialized: {collection_name}"
        )

    def add(
        self,
        content: str,
        metadata: dict = None,
        doc_id: str = None,
    ):
        if not content or not content.strip():
            raise ValueError("Memory content cannot be empty")

        if doc_id is None:
            doc_id = f"mem_{datetime.now().timestamp()}"

        meta = dict(metadata or {})
        meta["timestamp"] = datetime.now().isoformat()

        self.collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[doc_id],
        )

        logger.info(
            f"Added to long-term memory: {content[:50]}..."
        )

        return doc_id

    @staticmethod
    def _tokens(text: str):
        """
        Convert text into normalized searchable tokens.
        """
        return {
            token
            for token in re.findall(
                r"[a-zA-Z0-9_./:-]+",
                text.lower(),
            )
            if token not in LongTermMemory.STOPWORDS
        }

    @staticmethod
    def _lexical_score(query: str, document: str):
        """
        Score direct token overlap.

        Stronger matches are given to:
        - exact token matches
        - multi-token overlap
        - query terms appearing in the document
        """
        query_tokens = LongTermMemory._tokens(query)
        document_tokens = LongTermMemory._tokens(document)

        if not query_tokens or not document_tokens:
            return 0.0

        overlap = query_tokens & document_tokens

        if not overlap:
            return 0.0

        coverage = len(overlap) / len(query_tokens)

        # Small bonus for multiple matching query terms.
        multi_token_bonus = min(
            len(overlap) * 0.10,
            0.50,
        )

        return coverage + multi_token_bonus

    def search(
        self,
        query: str,
        n_results: int = 5,
    ):
        """
        Hybrid memory retrieval.

        Chroma provides semantic candidates.
        Lexical matching reranks them using direct token overlap.

        The returned structure remains compatible with the
        existing memory/context code.
        """
        if not query or not query.strip():
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        total = self.collection.count()

        if total == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        candidate_count = min(
            max(n_results * 3, 10),
            total,
        )

        semantic = self.collection.query(
            query_texts=[query],
            n_results=candidate_count,
        )

        ids = semantic.get("ids", [[]])[0]
        documents = semantic.get("documents", [[]])[0]
        metadatas = semantic.get("metadatas", [[]])[0]
        distances = semantic.get("distances", [[]])[0]

        candidates = []

        for i, doc_id in enumerate(ids):
            document = documents[i] or ""
            distance = distances[i]

            lexical = self._lexical_score(
                query,
                document,
            )

            # Lower Chroma distance is better.
            #
            # Normalize semantic contribution into a
            # bounded score where higher is better.
            semantic_score = 1.0 / (1.0 + distance)

            combined_score = (
                (semantic_score * 0.35)
                + (lexical * 0.65)
            )

            candidates.append(
                {
                    "id": doc_id,
                    "document": document,
                    "metadata": metadatas[i],
                    "distance": distance,
                    "lexical_score": lexical,
                    "semantic_score": semantic_score,
                    "combined_score": combined_score,
                }
            )

        candidates.sort(
            key=lambda item: (
                -item["combined_score"],
                item["distance"],
            )
        )

        selected = candidates[:n_results]

        return {
            "ids": [[item["id"] for item in selected]],
            "documents": [
                [item["document"] for item in selected]
            ],
            "metadatas": [
                [item["metadata"] for item in selected]
            ],
            "distances": [
                [item["distance"] for item in selected]
            ],
        }

    def count(self):
        return self.collection.count()

    def clear(self):
        self.client.delete_collection(
            self.collection.name
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection.name
            )
        )

        logger.info("Long-term memory cleared")
