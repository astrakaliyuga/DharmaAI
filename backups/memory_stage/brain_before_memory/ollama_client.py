import json
import urllib.request
import urllib.error

from config.settings import OLLAMA_HOST, DEFAULT_LLM_MODEL


class OllamaClient:
    def __init__(self, model=DEFAULT_LLM_MODEL, timeout=120):
        self.model = model
        self.timeout = timeout

    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            f"{OLLAMA_HOST}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result.get("response", "").strip()

        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Cannot connect to Ollama: {exc}"
            ) from exc

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Ollama returned invalid JSON"
            ) from exc


