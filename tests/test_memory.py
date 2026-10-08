import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from memory.store import MemoryStore
from memory.context import MemoryContext


TEST_FILE = "memory_test.jsonl"

store = MemoryStore(filename=TEST_FILE)

# Start this test with a clean test file.
store.path.unlink(missing_ok=True)
store.path.touch(exist_ok=True)

print("===== MEMORY STORE TEST =====")

first = store.add(
    "DharmaAI uses Ollama for local model inference.",
    category="architecture",
)

second = store.add(
    "DharmaAI project data is stored on the external SSD.",
    category="storage",
)

third = store.add(
    "Brain Router selects models based on task complexity.",
    category="brain",
)

print("ADDED:", first["id"])
print("ADDED:", second["id"])
print("ADDED:", third["id"])

if store.count() != 3:
    raise SystemExit(
        f"FAIL: expected 3 memories, got {store.count()}"
    )

print("COUNT:", store.count())

print()
print("===== MEMORY SEARCH TEST =====")

results = store.search("Ollama local model", limit=5)

print("RESULTS:", len(results))

if not results:
    raise SystemExit(
        "FAIL: memory search returned no results"
    )

print("TOP RESULT:", results[0]["content"])

if "Ollama" not in results[0]["content"]:
    raise SystemExit(
        "FAIL: incorrect memory search result"
    )

print("SEARCH: PASS")

print()
print("===== MEMORY CONTEXT TEST =====")

context = MemoryContext(store).build_context(
    "external SSD project storage"
)

print(context)

if "external SSD" not in context:
    raise SystemExit(
        "FAIL: memory context missing expected result"
    )

print("CONTEXT: PASS")

print()
print("STATUS: PASS")
