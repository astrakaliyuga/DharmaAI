import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from brain.router import BrainRouter


router = BrainRouter()

tests = [
    ("fast", "qwen2.5:1.5b"),
    ("normal", "qwen2.5:7b"),
    ("complex", "gemma2:9b"),
    ("unknown", "qwen2.5:1.5b"),
]

print("===== BRAIN ROUTER TEST =====")

for complexity, expected in tests:
    actual = router.select_model(complexity)

    print(
        f"COMPLEXITY: {complexity:<8} "
        f"MODEL: {actual}"
    )

    if actual != expected:
        raise SystemExit(
            f"FAIL: expected {expected}, got {actual}"
        )

print()
print("STATUS: PASS")
