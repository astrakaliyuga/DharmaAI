import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agents.manager import AgentManager
from config.settings import LOGS_DIR
from core.logger import get_logger
from core.planner import TaskPlanner


logger = get_logger("core.orchestrator")


class AgentOrchestrator:
    """
    First-generation DharmaAI task orchestrator.

    Responsibilities:
      - inspect a task and identify its agent
      - create an explicit task plan
      - gate potentially risky operations
      - record execution outcomes
      - return a structured result

    This version does not perform autonomous multi-step planning.
    It deliberately executes at most one agent task per run.
    """

    RISK_PATTERNS = (
        r"\bdelete\b",
        r"\bremove\b",
        r"\boverwrite\b",
        r"\bwrite\b",
        r"\bexecute\b",
        r"\bshell\b",
        r"\bcommand\b",
        r"\bsudo\b",
        r"\binstall\b",
        r"\bformat\b",
        r"\bchmod\b",
        r"\bchown\b",
        r"\bpython\b",
        r"\bcode\b",
        r"\bfetch\b",
        r"\brun\b",
    )

    APPROVAL_AGENTS = {
        "ShellAgent",
        "CodeAgent",
    }

    def __init__(
        self,
        agent_manager=None,
        audit_path=None,
    ):
        self.agent_manager = (
            agent_manager or AgentManager()
        )

        self.audit_path = Path(
            audit_path
            if audit_path is not None
            else LOGS_DIR / "orchestrator.jsonl"
        )

        self.audit_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _now():
        return datetime.now(
            timezone.utc
        ).isoformat()

    @classmethod
    def _requires_approval(
        cls,
        task,
        agent_name,
    ):
        if agent_name in cls.APPROVAL_AGENTS:
            return True

        text = task.lower()

        return any(
            re.search(pattern, text)
            for pattern in cls.RISK_PATTERNS
        )

    def _audit(self, event):
        try:
            with self.audit_path.open(
                "a",
                encoding="utf-8",
            ) as file:
                file.write(
                    json.dumps(
                        event,
                        ensure_ascii=False,
                    ) + "\n"
                )
        except OSError:
            logger.exception(
                "Could not write orchestrator audit log"
            )

    def plan(self, task):
        if not isinstance(task, str) or not task.strip():
            raise ValueError(
                "Task must be a non-empty string"
            )

        task = task.strip()
        agent = self.agent_manager.find_agent(task)

        if agent is None:
            return {
                "task_id": str(uuid.uuid4()),
                "task": task,
                "status": "unroutable",
                "steps": [],
                "created_at": self._now(),
            }

        approval_required = self._requires_approval(
            task,
            agent.name,
        )

        return {
            "task_id": str(uuid.uuid4()),
            "task": task,
            "status": "planned",
            "created_at": self._now(),
            "steps": [
                {
                    "step": 1,
                    "agent": agent.name,
                    "description": task,
                    "status": "awaiting_approval"
                    if approval_required
                    else "ready",
                    "approval_required": approval_required,
                }
            ],
        }

    def run(self, task, approved=False):
        plan = self.plan(task)

        result = {
            **plan,
            "finished_at": self._now(),
            "output": None,
        }

        if plan["status"] == "unroutable":
            result["status"] = "unroutable"
            result["output"] = (
                f"No agent found for task: {task}"
            )
            self._audit(result)
            return result

        step = plan["steps"][0]

        if step["approval_required"] and not approved:
            result["status"] = "approval_required"
            result["steps"][0]["status"] = (
                "approval_required"
            )
            result["output"] = (
                "Execution blocked: explicit approval "
                "is required for this operation."
            )
            self._audit(result)
            return result

        try:
            output = self.agent_manager.run(
                plan["task"]
            )

            result["output"] = str(output)
            result["finished_at"] = self._now()

            if str(output).startswith("No agent found"):
                result["status"] = "failed"
                result["steps"][0]["status"] = "failed"
            else:
                result["status"] = "completed"
                result["steps"][0]["status"] = "completed"

        except Exception as exc:
            logger.exception(
                "Orchestrator task failed"
            )
            result["status"] = "failed"
            result["steps"][0]["status"] = "failed"
            result["output"] = (
                f"{type(exc).__name__}: {exc}"
            )
            result["finished_at"] = self._now()

        self._audit(result)
        return result


    @staticmethod
    def _output_indicates_failure(output):
        text = str(output or "").strip().lower()

        failure_prefixes = (
            "no agent found",
            "command not allowed:",
            "command rejected:",
            "operation blocked:",
            "write blocked:",
            "file operation failed:",
            "list failed:",
            "file not found:",
            "unknown action:",
            "no command provided",
            "no task provided",
            "execution blocked:",
        )

        return text.startswith(failure_prefixes)

    def plan_goal(self, goal):
        """Create a validated, non-executing local-LLM proposal."""
        planner = TaskPlanner()
        plan = planner.plan_goal(
            goal,
            agent_manager=self.agent_manager,
        )
        self._audit({
            "event": "goal_plan_proposed",
            "plan_id": plan["plan_id"],
            "goal": plan["goal"],
            "source": plan["source"],
            "status": plan["status"],
            "created_at": self._now(),
        })
        return plan

    def execute_plan(self, plan, approved_steps=None):
        """Execute a validated LLM proposal only after explicit review."""
        if not isinstance(plan, dict):
            raise TypeError("Plan must be a dictionary")
        if plan.get("source") != "local_llm":
            raise ValueError("Only local_llm proposals are accepted")
        if plan.get("status") != "proposed":
            raise ValueError("Plan must have proposed status")
        if plan.get("requires_review") is not True:
            raise ValueError("Plan must require review")

        steps = plan.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ValueError("Plan must contain steps")

        tasks = []
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                raise ValueError("Every step must be an object")
            if step.get("step") != index:
                raise ValueError("Plan step numbering is invalid")
            task = step.get("task")
            if not isinstance(task, str) or not task.strip():
                raise ValueError("Every step needs a task")
            agent = self.agent_manager.find_agent(task)
            if agent is None:
                raise ValueError("Unsupported planned task: " + task)
            tasks.append(task.strip())

        return self.run_plan(
            tasks,
            approved_steps=approved_steps,
        )

    def run_plan(self, tasks, approved_steps=None):
        """
        Execute an explicit ordered list of agent tasks.

        approved_steps contains 1-based step numbers approved
        by the caller. Execution stops at the first failed step
        or approval gate.
        """
        planner = TaskPlanner()
        plan = planner.plan(tasks)

        approvals = set(approved_steps or [])
        completed = 0
        plan["status"] = "running"

        for step in plan["steps"]:
            task = step["task"]
            agent = self.agent_manager.find_agent(task)

            step["started_at"] = self._now()

            if agent is None:
                step["status"] = "failed"
                step["error"] = "No agent can handle this task"
                plan["status"] = "failed"
                break

            step["agent"] = agent.name
            needs_approval = self._requires_approval(
                task,
                agent.name,
            )
            step["approval_required"] = needs_approval

            if needs_approval and step["step"] not in approvals:
                step["status"] = "approval_required"
                step["finished_at"] = self._now()
                plan["status"] = "approval_required"
                break

            try:
                output = self.agent_manager.run(task)
                step["output"] = str(output)
                step["finished_at"] = self._now()

                if self._output_indicates_failure(output):
                    step["status"] = "failed"
                    plan["status"] = "failed"
                    break

                step["status"] = "completed"
                completed += 1

            except Exception as exc:
                logger.exception(
                    "Planner step %s failed",
                    step["step"],
                )
                step["status"] = "failed"
                step["error"] = (
                    f"{type(exc).__name__}: {exc}"
                )
                step["finished_at"] = self._now()
                plan["status"] = "failed"
                break

        else:
            plan["status"] = "completed"

        plan["completed_steps"] = completed
        plan["total_steps"] = len(plan["steps"])
        plan["finished_at"] = self._now()

        self._audit(plan)
        return plan

