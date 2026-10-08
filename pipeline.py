import ollama
import re
from pathlib import Path
from agents.voice_agent import VoiceAgent
from agents.image_agent import ImageAgent
from agents.video_agent import VideoAgent
from core.logger import get_logger

logger = get_logger("pipeline")

class StoryVideoPipeline:
    """Story → Video pipeline"""
    
    def __init__(self):
        self.voice = VoiceAgent()
        self.image = ImageAgent()
        self.video = VideoAgent()
        self.workspace = Path("/mnt/kaliyuga/DharmaAI/workspace")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def run(self, story_prompt: str, num_scenes: int = 3):
        print(f"📝 Story: {story_prompt}")
        print(f"🎬 Scenes: {num_scenes}")
        print()
        
        # Step 1: Story generate
        print("1️⃣ Generating story...")
        story = self._generate_story(story_prompt, num_scenes)
        print(f"✅ Story generated ({len(story)} chars)")
        print()
        
        # Step 2: Voice generate
        print("2️⃣ Generating voice...")
        voice_result = self.voice.run(f"speak {story}")
        print(f"✅ {voice_result}")
        print()
        
        # Step 3: Images generate
        print("3️⃣ Generating images...")
        scenes = self._extract_scenes(story, num_scenes)
        images = []
        for i, scene in enumerate(scenes, 1):
            print(f"   Scene {i}: {scene[:60]}...")
            self.image.run(f"generate {scene}")
            img_path = f"/mnt/kaliyuga/DharmaAI/workspace/images/image_{i-1}.png"
            images.append(img_path)
        print()
        
        # Step 4: Videos create
        print("4️⃣ Creating videos...")
        videos = []
        voice_path = "/mnt/kaliyuga/DharmaAI/workspace/voice/output.wav"
        for i, img in enumerate(images, 1):
            if Path(img).exists():
                result = self.video.run(f"create {img} {voice_path}")
                videos.append(result)
                print(f"   Video {i}: {result}")
        print()
        
        return {
            "story": story,
            "voice": voice_result,
            "images": images,
            "videos": videos
        }
    
    def _generate_story(self, prompt: str, num_scenes: int):
        full_prompt = f"Write a {num_scenes}-scene story about: {prompt}. Each scene should have a vivid visual description for image generation. Format: Scene 1: ..., Scene 2: ..., Scene 3: ..."
        
        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response['message']['content']
    
    def _extract_scenes(self, story: str, num_scenes: int):
        scenes = re.findall(r'Scene \d+:(.*?)(?=Scene \d+:|$)', story, re.DOTALL)
        scenes = [s.strip() for s in scenes if s.strip()]
        return scenes[:num_scenes]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline.py '<story_prompt>' [num_scenes]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    num_scenes = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    pipeline = StoryVideoPipeline()
    result = pipeline.run(prompt, num_scenes)
    print()
    print("=" * 60)
    print("✅ Pipeline complete!")
    print("=" * 60)
