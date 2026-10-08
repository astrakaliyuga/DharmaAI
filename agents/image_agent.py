from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.image")

class ImageAgent(BaseAgent):
    """Image generation agent — Stable Diffusion"""
    
    def __init__(self):
        super().__init__("ImageAgent", "Generate images from text (Stable Diffusion)")
        self.workspace = Path("/mnt/kaliyuga/DharmaAI/workspace/images")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        # Match ONLY if task starts with generate/draw/image
        if task_lower.startswith("generate "):
            return True
        if task_lower.startswith("draw "):
            return True
        if task_lower.startswith("image "):
            return True
        return False
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "No prompt provided. Use: 'generate <prompt>'"
        
        prompt = parts[1].strip()
        return self._generate(prompt)
    
    def _generate(self, prompt: str) -> str:
        """Text → image (Stable Diffusion)"""
        try:
            import torch
            from diffusers import StableDiffusionPipeline
            
            logger.info(f"Generating image: {prompt[:50]}")
            
            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float32
            ).to("cpu")
            
            image = pipe(prompt, num_inference_steps=20).images[0]
            
            # Save
            filename = f"image_{len(list(self.workspace.glob('*.png')))}.png"
            filepath = self.workspace / filename
            image.save(filepath)
            
            return f"Generated: {filepath}"
        except Exception as e:
            logger.error(f"Image error: {e}")
            return f"Error: {e}"
