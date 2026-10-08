from datetime import datetime, timezone
import uuid


class TaskPlanner:
    """
    Deterministic task planner.

    V1 accepts an explicit ordered list of steps.
    It does not invent or execute steps autonomously.
    """

    def plan(self, tasks):
        if isinstance(tasks, str):
            raise TypeError(
                "Provide an ordered list of task strings"
            )

        if not isinstance(tasks, (list, tuple)):
            raise TypeError(
                "Tasks must be a list or tuple"
            )

        if not tasks:
            raise ValueError(
                "A plan must contain at least one task"
            )

        normalized = []

        for task in tasks:
            if not isinstance(task, str) or not task.strip():
                raise ValueError(
                    "Every planned task must be a non-empty string"
                )
            normalized.append(task.strip())

        return {
            "plan_id": str(uuid.uuid4()),
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "status": "planned",
            "steps": [
                {
                    "step": index,
                    "task": task,
                    "status": "pending",
                }
                for index, task in enumerate(
                    normalized,
                    start=1,
                )
            ],
        }
