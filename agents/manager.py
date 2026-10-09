from agents.file_agent import FileAgent
from agents.shell_agent import ShellAgent
from agents.code_agent import CodeAgent
from agents.web_agent import WebAgent
from agents.voice_agent import VoiceAgent
from agents.image_agent import ImageAgent
from agents.video_agent import VideoAgent
from agents.system_agent import SystemAgent
from agents.network_agent import NetworkAgent
from agents.database_agent import DatabaseAgent
from agents.pdf_agent import PDFAgent
from agents.backup_agent import BackupAgent
from core.logger import get_logger

logger = get_logger("agents.manager")

class AgentManager:
    def __init__(self):
        self.agents = [
            WebAgent(), VoiceAgent(), ImageAgent(), VideoAgent(),
            FileAgent(), ShellAgent(), CodeAgent(),
            SystemAgent(), NetworkAgent(), DatabaseAgent(),
            PDFAgent(), BackupAgent(),
        ]
        logger.info(f"AgentManager initialized with {len(self.agents)} agents")
    
    def list_agents(self):
        return [(a.name, a.description) for a in self.agents]
    
    def find_agent(self, task: str):
        for agent in self.agents:
            if agent.can_handle(task):
                return agent
        return None
    
    def run(self, task: str) -> str:
        agent = self.find_agent(task)
        if agent:
            return agent.run(task)
        return f"No agent found for task: {task}"
