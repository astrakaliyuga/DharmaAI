import re
import shlex
import subprocess
from pathlib import Path

from agents.base import BaseAgent
from core.logger import get_logger

logger = get_logger("agents.shell")


class ShellAgent(BaseAgent):
    """Restricted shell-command agent; never invokes a shell interpreter."""

    ALLOWED_COMMANDS = {
        "ls", "pwd", "echo", "cat", "date",
        "whoami", "df", "free", "uptime", "uname",
    }

    # Shell operators and control characters are not part of this
    # agent's command language. subprocess also uses shell=False.
    FORBIDDEN = re.compile(r"[;&|><`$\n\r]")

    def __init__(self):
        super().__init__("ShellAgent", "Restricted shell commands")
        self.workspace = Path(
            "/mnt/kaliyuga/DharmaAI/workspace"
        ).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def can_handle(self, task: str) -> bool:
        keywords = ["run", "execute", "shell", "command"]
        return any(word in task.lower() for word in keywords)

    def _safe_workspace_path(self, value):
        candidate = Path(value)

        if not candidate.is_absolute():
            candidate = self.workspace / candidate

        resolved = candidate.resolve()

        if not resolved.is_relative_to(self.workspace):
            raise ValueError(
                "File access outside the DharmaAI workspace is blocked"
            )

        return str(resolved)

    def run(self, task: str, **kwargs) -> str:
        parts = task.split(maxsplit=1)

        if len(parts) < 2:
            return "No command provided"

        command_text = parts[1].strip()

        if not command_text:
            return "No command provided"

        if self.FORBIDDEN.search(command_text):
            return "Command rejected: shell operators are not allowed"

        try:
            argv = shlex.split(command_text, posix=True)
        except ValueError:
            return "Command rejected: invalid quoting"

        if not argv:
            return "No command provided"

        cmd_name = argv[0]

        if cmd_name not in self.ALLOWED_COMMANDS:
            return (
                f"Command not allowed: {cmd_name}\n"
                f"Allowed: {', '.join(sorted(self.ALLOWED_COMMANDS))}"
            )

        # cat may read files only from the project workspace.
        if cmd_name == "cat":
            if len(argv) < 2:
                return "Command rejected: cat requires a workspace file"

            try:
                safe_paths = [
                    self._safe_workspace_path(arg)
                    for arg in argv[1:]
                ]
            except (OSError, ValueError, RuntimeError) as exc:
                return f"Command rejected: {exc}"

            argv = [cmd_name, *safe_paths]

        # ls may list workspace paths only, while still allowing flags.
        if cmd_name == "ls":
            safe_args = []

            try:
                for arg in argv[1:]:
                    if arg.startswith("-"):
                        safe_args.append(arg)
                    else:
                        safe_args.append(
                            self._safe_workspace_path(arg)
                        )
            except (OSError, ValueError, RuntimeError) as exc:
                return f"Command rejected: {exc}"

            argv = [cmd_name, *safe_args]

        try:
            result = subprocess.run(
                argv,
                shell=False,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = (
                result.stdout + result.stderr
            ).strip()

            if result.returncode != 0:
                logger.warning(
                    "Restricted command exited with status %s",
                    result.returncode,
                )

            return output or (
                f"(no output; exit code {result.returncode})"
            )

        except subprocess.TimeoutExpired:
            return "Command timed out (10s)"
        except OSError as exc:
            logger.error("Command execution failed: %s", exc)
            return f"Command execution failed: {exc}"
