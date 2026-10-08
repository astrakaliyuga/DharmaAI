from config.settings import (
    DEFAULT_LLM_MODEL,
    AVAILABLE_LLM_MODELS,
)


class BrainRouter:
    """
    Selects a local LLM based on task complexity.
    This first version uses explicit complexity levels.
    """

    def __init__(self):
        self.default_model = DEFAULT_LLM_MODEL
        self.available_models = AVAILABLE_LLM_MODELS

    def select_model(self, complexity="normal"):
        complexity = complexity.lower().strip()

        if complexity == "fast":
            model = "qwen2.5:1.5b"

        elif complexity == "normal":
            model = "qwen2.5:7b"

        elif complexity == "complex":
            model = "gemma2:9b"

        else:
            model = self.default_model

        if model not in self.available_models:
            raise RuntimeError(
                f"Selected model is not configured: {model}"
            )

        return model
