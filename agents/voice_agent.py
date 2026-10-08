import subprocess
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.voice")

class VoiceAgent(BaseAgent):
    """Voice agent — Whisper (speech-to-text) + Piper (text-to-speech)"""
    
    def __init__(self):
        super().__init__("VoiceAgent", "Speech-to-text and text-to-speech")
        self.workspace = Path("/mnt/kaliyuga/DharmaAI/workspace/voice")
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.piper_model = "/mnt/kaliyuga/DharmaAI/models/piper/en_US-lessac-medium.onnx"
    
    def can_handle(self, task: str) -> bool:
        keywords = ["voice", "speak", "listen", "transcribe", "tts", "stt"]
        return any(kw in task.lower() for kw in keywords)
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "No task provided. Use: 'speak <text>' or 'transcribe <audio>'"
        
        action = parts[0].lower()
        content = parts[1].strip()
        
        if action == "speak":
            return self._speak(content)
        elif action == "transcribe":
            return self._transcribe(content)
        else:
            return f"Unknown action: {action}"
    
    def _speak(self, text: str) -> str:
        """Text → speech (Piper)"""
        try:
            output_file = self.workspace / "output.wav"
            cmd = f'echo "{text}" | piper --model {self.piper_model} --output_file {output_file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return f"Spoken: {text[:50]}... → {output_file}"
            return f"Piper error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"
    
    def _transcribe(self, audio_file: str) -> str:
        """Audio → text (Whisper)"""
        try:
            if not Path(audio_file).exists():
                return f"File not found: {audio_file}"
            
            cmd = f'whisper "{audio_file}" --model tiny --output_dir {self.workspace} --output_format txt'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                txt_file = self.workspace / f"{Path(audio_file).stem}.txt"
                if txt_file.exists():
                    return txt_file.read_text()
            return f"Whisper error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"
