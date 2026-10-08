import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from memory.store import MemoryStore
from brain.memory_engine import MemoryAwareBrain


TEST_FILE = "memory_engine_test.jsonl"

store = MemoryStore(filename=TEST_FILE)

# Clean test storage.
store.path.unlink(missing_ok=True)
store.path.touch(exist_ok=True)

print("===== MEMORY-AWARE BRAIN TEST =====")

store.add(
    "DharmaAI uses Ollama for local LLM inference.",
    category="architecture",
)

store.add(
    "DharmaAI stores its project data on the external SSD.",
    category="storage",
)

store.add(
    "The Brain Router selects models according to task complexity.",
    category="brain",
)

print("TEST MEMORIES:", store.count())

brain = MemoryAwareBrain(memory_store=store)

# The task deliberately contains words that exist
# in the stored memory so retrieval can be verified.
result = brain.run(
    "What local inference system does DharmaAI use?",
    complexity="fast",
)

print("MODEL:", result["model"])
print("MEMORY USED:", result["memory_used"])
print("RESPONSE:", result["response"])

print()
print("===== RETRIEVED CONTEXT =====")
print(result["memory_context"])

if result["model"] != "qwen2.5:1.5b":
    raise SystemExit(
        "FAIL: fast task selected wrong model"
    )

if not result["response"]:
    raise SystemExit(
        "FAIL: model returned empty response"
    )

if not result["memory_used"]:
    raise SystemExit(
        "FAIL: expected memory context to be used"
    )

if "Ollama" not in result["memory_context"]:
    raise SystemExit(
        "FAIL: expected Ollama memory was not retrieved"
    )

print()
print("MEMORY RETRIEVAL: PASS")
print("BRAIN RESPONSE: PASS")
print("STATUS: PASS")
