import json

import pytest

from core.planner import TaskPlanner
from core.orchestrator import AgentOrchestrator


class FakeAgent:
    def __init__(self, name="FileAgent"):
        self.name = name


class FakeManager:
    def __init__(self, outputs=None):
        self.outputs = list(outputs or [])
        self.calls = []

    def find_agent(self, task):
        if task.startswith("unknown "):
            return None
        if task.startswith("run "):
            return FakeAgent("ShellAgent")
        return FakeAgent("FileAgent")

    def run(self, task):
        self.calls.append(task)
        if self.outputs:
            value = self.outputs.pop(0)
            if isinstance(value, Exception):
                raise value
            return value
        return "OK"


def test_planner_preserves_order():
    plan = TaskPlanner().plan([
        "list workspace",
        "read notes.txt",
    ])

    assert plan["status"] == "planned"
    assert [step["task"] for step in plan["steps"]] == [
        "list workspace",
        "read notes.txt",
    ]


def test_planner_rejects_empty_plan():
    with pytest.raises(ValueError):
        TaskPlanner().plan([])


def test_planner_rejects_string_instead_of_list():
    with pytest.raises(TypeError):
        TaskPlanner().plan("list workspace")


def test_orchestrator_runs_steps_in_order(tmp_path):
    manager = FakeManager(["first output", "second output"])
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run_plan([
        "list workspace",
        "read notes.txt",
    ])

    assert result["status"] == "completed"
    assert result["completed_steps"] == 2
    assert manager.calls == [
        "list workspace",
        "read notes.txt",
    ]
    assert all(
        step["status"] == "completed"
        for step in result["steps"]
    )


def test_plan_stops_at_approval_gate(tmp_path):
    manager = FakeManager(["listed"])
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run_plan([
        "list workspace",
        "run whoami",
        "list workspace",
    ])

    assert result["status"] == "approval_required"
    assert result["steps"][0]["status"] == "completed"
    assert result["steps"][1]["status"] == "approval_required"
    assert len(manager.calls) == 1


def test_plan_stops_after_failure(tmp_path):
    manager = FakeManager([
        "list output",
        "File not found: missing.txt",
        "third output",
    ])
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run_plan([
        "list workspace",
        "read missing.txt",
        "list workspace",
    ])

    assert result["status"] == "failed"
    assert result["steps"][1]["status"] == "failed"
    assert len(manager.calls) == 2


def test_plan_records_audit(tmp_path):
    audit = tmp_path / "audit.jsonl"
    orchestrator = AgentOrchestrator(
        FakeManager(["OK"]),
        audit,
    )

    result = orchestrator.run_plan(["list workspace"])

    record = json.loads(audit.read_text().splitlines()[-1])
    assert record["plan_id"] == result["plan_id"]
    assert record["status"] == "completed"


def test_approved_risky_step_can_continue(tmp_path):
    manager = FakeManager(["identity"])
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run_plan(
        ["run whoami"],
        approved_steps=[1],
    )

    assert result["status"] == "completed"
    assert result["completed_steps"] == 1
