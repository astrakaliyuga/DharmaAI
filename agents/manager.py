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
from agents.email_agent import EmailAgent
from agents.scheduler_agent import SchedulerAgent
from agents.encryption_agent import EncryptionAgent
from agents.file_watcher_agent import FileWatcherAgent
from agents.api_agent import APIAgent
from agents.translate_agent import TranslateAgent
from agents.summarize_agent import SummarizeAgent
from agents.sentiment_agent import SentimentAgent
from core.logger import get_logger

logger = get_logger("agents.manager")

class AgentManager:
    def __init__(self):
        self.agents = [
            BackupAgent(), PDFAgent(), DatabaseAgent(), NetworkAgent(),
            SystemAgent(), EmailAgent(), SchedulerAgent(), EncryptionAgent(),
            FileWatcherAgent(), APIAgent(), TranslateAgent(), SummarizeAgent(),
            SentimentAgent(), WebAgent(), VoiceAgent(), ImageAgent(),
            VideoAgent(), FileAgent(), ShellAgent(), CodeAgent(),
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
