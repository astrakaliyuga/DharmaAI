from brain.router import BrainRouter
from brain.ollama_client import OllamaClient


class BrainEngine:
    """
    Main DharmaAI brain pipeline.

    Task
      -> Router
      -> Model
      -> Ollama
      -> Response
    """

    def __init__(self):
        self.router = BrainRouter()

    def run(self, prompt, complexity="normal"):
        model = self.router.select_model(complexity)

        client = OllamaClient(model=model)

        response = client.generate(prompt)

        return {
            "prompt": prompt,
            "complexity": complexity,
            "model": model,
            "response": response,
        }
