import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from brain.ollama_client import OllamaClient


client = OllamaClient(model="qwen2.5:1.5b")

response = client.generate(
    "Reply with exactly: DHARMAAI_BRAIN_OK"
)

print("MODEL:", client.model)
print("RESPONSE:", response)

if response != "DHARMAAI_BRAIN_OK":
    raise SystemExit("FAIL: unexpected model response")

print("STATUS: PASS")
