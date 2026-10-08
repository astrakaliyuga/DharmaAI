import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from brain.engine import BrainEngine


engine = BrainEngine()

print("===== BRAIN ENGINE TEST =====")

result = engine.run(
    "Reply with exactly: DHARMAAI_ENGINE_OK",
    complexity="fast",
)

print("PROMPT:", result["prompt"])
print("COMPLEXITY:", result["complexity"])
print("MODEL:", result["model"])
print("RESPONSE:", result["response"])

if result["model"] != "qwen2.5:1.5b":
    raise SystemExit(
        "FAIL: fast task selected wrong model"
    )

if result["response"] != "DHARMAAI_ENGINE_OK":
    raise SystemExit(
        "FAIL: unexpected model response"
    )

print("STATUS: PASS")
