import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.email")

class EmailAgent(BaseAgent):
    """Email send agent"""
    
    def __init__(self):
        super().__init__("EmailAgent", "Send emails via SMTP")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def can_handle(self, task: str) -> bool:
        return task.lower().startswith("email ")
    
    def run(self, task: str, **kwargs) -> str:
        # Usage: email send <to> <subject> <body>
        parts = task.split(maxsplit=4)
        if len(parts) < 5:
            return "Usage: email send <to> <subject> <body>"
        
        action = parts[1].lower()
        if action == "send":
            to = parts[2]
            subject = parts[3]
            body = parts[4]
            return self._send(to, subject, body)
        return f"Unknown action: {action}"
    
    def _send(self, to: str, subject: str, body: str) -> str:
        return f"Email would be sent to {to}: {subject} — (SMTP credentials not configured)"

