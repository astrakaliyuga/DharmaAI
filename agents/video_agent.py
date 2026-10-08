import subprocess
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.video")

class VideoAgent(BaseAgent):
    """Video creation agent — ffmpeg"""
    
    def __init__(self):
        super().__init__("VideoAgent", "Create videos from images + audio")
        self.workspace = Path("/mnt/kaliyuga/DharmaAI/workspace/videos")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        # Match: "create ...", "video ...", "make video ..."
        if task_lower.startswith("create "):
            return True
        if task_lower.startswith("video "):
            return True
        if "video" in task_lower:
            return True
        return False
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "No task provided. Use: 'create <image> <audio>'"
        
        content = parts[1].strip()
        
        # "create " prefix unte teesey
        if content.lower().startswith("create "):
            content = content[7:].strip()
        
        args = content.split()
        
        if len(args) < 2:
            return "Need: image file + audio file"
        
        image_file = args[0]
        audio_file = args[1]
        return self._create_video(image_file, audio_file)
    
    def _create_video(self, image_file: str, audio_file: str) -> str:
        """Image + Audio → Video"""
        try:
            if not Path(image_file).exists():
                return f"Image not found: {image_file}"
            if not Path(audio_file).exists():
                return f"Audio not found: {audio_file}"
            
            filename = f"video_{len(list(self.workspace.glob('*.mp4')))}.mp4"
            output_file = self.workspace / filename
            
            cmd = (
                f'ffmpeg -loop 1 -i "{image_file}" -i "{audio_file}" '
                f'-shortest -c:v libx264 -pix_fmt yuv420p -c:a aac "{output_file}" -y'
            )
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return f"Video created: {output_file}"
            return f"ffmpeg error: {result.stderr[:200]}"
        except Exception as e:
            return f"Error: {e}"
