from pathlib import Path

from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.file")


class FileAgent(BaseAgent):
    """Workspace-confined file operations."""

    def __init__(
        self,
        workspace="/mnt/kaliyuga/DharmaAI/workspace",
    ):
        super().__init__(
            "FileAgent",
            "Workspace-confined file operations",
        )

        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def can_handle(self, task: str) -> bool:
        keywords = [
            "write", "read", "list", "delete", "create file"
        ]
        return any(word in task.lower() for word in keywords)

    def _safe_path(self, name):
        candidate = Path(name)

        if not candidate.is_absolute():
            candidate = self.workspace / candidate

        resolved = candidate.resolve()

        if not resolved.is_relative_to(self.workspace):
            raise ValueError(
                "Path is outside the permitted workspace"
            )

        return resolved

    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=2)

        if not parts:
            return "No task provided"

        action = parts[0].lower()

        if action == "list":
            try:
                files = sorted(
                    path.name
                    for path in self.workspace.iterdir()
                )
                return "\n".join(files) or "Empty workspace"
            except OSError as exc:
                return f"List failed: {exc}"

        if action not in {"read", "write", "delete"}:
            return f"Unknown action: {action}"

        if len(parts) < 2 or not parts[1].strip():
            return f"Missing filename for action: {action}"

        try:
            path = self._safe_path(parts[1])
        except (OSError, ValueError, RuntimeError) as exc:
            return f"Operation blocked: {exc}"

        try:
            if action == "read":
                if not path.is_file():
                    return f"File not found: {parts[1]}"
                return path.read_text(encoding="utf-8")

            if action == "write":
                if len(parts) < 3:
                    return "Missing content for write"

                if path.is_dir():
                    return "Write blocked: target is a directory"

                path.write_text(
                    parts[2],
                    encoding="utf-8",
                )
                return f"Written to {parts[1]}"

            if action == "delete":
                if not path.is_file():
                    return f"File not found: {parts[1]}"

                path.unlink()
                return f"Deleted {parts[1]}"

        except OSError as exc:
            logger.error("File operation failed: %s", exc)
            return f"File operation failed: {exc}"

        return f"Unknown action: {action}"
