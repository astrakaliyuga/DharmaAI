import sqlite3
from pathlib import Path
from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.database")

class DatabaseAgent(BaseAgent):
    """SQLite database agent"""
    
    def __init__(self):
        super().__init__("DatabaseAgent", "SQLite database operations")
        self.db_path = Path("/mnt/kaliyuga/DharmaAI/data/dharma.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def can_handle(self, task: str) -> bool:
        keywords = ["database", "sql", "sqlite", "query"]
        return any(kw in task.lower() for kw in keywords)
    
    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: database <sql_query>"
        return self._execute(parts[1].strip())
    
    def _execute(self, query: str) -> str:
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                result = "\n".join([str(row) for row in rows]) if rows else "(no rows)"
            else:
                conn.commit()
                result = f"Rows affected: {cursor.rowcount}"
            conn.close()
            return result
        except Exception as e:
            return f"Database error: {e}"
