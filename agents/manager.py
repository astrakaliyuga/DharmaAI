from agents.file_agent import FileAgent
from agents.shell_agent import ShellAgent
from agents.code_agent import CodeAgent
from agents.web_agent import WebAgent
from agents.voice_agent import VoiceAgent
from agents.image_agent import ImageAgent
from agents.video_agent import VideoAgent
from core.logger import get_logger
from tools.security_registry import SecurityToolRegistry

logger = get_logger("agents.manager")

class AgentManager:
    """Agent manager — anni agents ni manage chey"""
    
    def __init__(self):
        self.agents = [
            WebAgent(),
            VoiceAgent(),
            ImageAgent(),
            VideoAgent(),
            FileAgent(),
            ShellAgent(),
            CodeAgent(),
        ]

        self.security_registry = SecurityToolRegistry()

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
            logger.info(f"Routing to {agent.name}: {task[:50]}")
            return agent.run(task)
        return f"No agent found for task: {task}"
    
    def list_security_tools(self):
        """List registered security tools and installation status."""
        return self.security_registry.list_tools()
    
    def recommend_security_tools(self, goal: str):
        """Recommend security tools without executing scans."""
        return self.security_registry.recommend(goal)
