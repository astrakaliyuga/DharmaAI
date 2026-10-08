import json

import pytest

from core.orchestrator import AgentOrchestrator


class FakeAgent:
    def __init__(self, name):
        self.name = name


class FakeAgentManager:
    def __init__(self, agent=None, output="FAKE_AGENT_OK"):
        self.agent = agent
        self.output = output
        self.calls = 0

    def find_agent(self, task):
        return self.agent

    def run(self, task):
        self.calls += 1
        return self.output


def test_plan_selects_agent(tmp_path):
    manager = FakeAgentManager(FakeAgent("FileAgent"))
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    plan = orchestrator.plan("list workspace")

    assert plan["status"] == "planned"
    assert plan["steps"][0]["agent"] == "FileAgent"
    assert plan["steps"][0]["status"] == "ready"


def test_risky_task_requires_approval(tmp_path):
    manager = FakeAgentManager(FakeAgent("ShellAgent"))
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run("run whoami")

    assert result["status"] == "approval_required"
    assert manager.calls == 0


def test_approved_task_runs_and_is_audited(tmp_path):
    audit = tmp_path / "audit.jsonl"
    manager = FakeAgentManager(FakeAgent("ShellAgent"))
    orchestrator = AgentOrchestrator(manager, audit)

    result = orchestrator.run(
        "run whoami",
        approved=True,
    )

    assert result["status"] == "completed"
    assert result["output"] == "FAKE_AGENT_OK"
    assert manager.calls == 1

    records = [
        json.loads(line)
        for line in audit.read_text().splitlines()
    ]
    assert len(records) == 1
    assert records[0]["status"] == "completed"


def test_unknown_task_does_not_execute(tmp_path):
    manager = FakeAgentManager()
    orchestrator = AgentOrchestrator(
        manager,
        tmp_path / "audit.jsonl",
    )

    result = orchestrator.run("unrecognized request")

    assert result["status"] == "unroutable"
    assert manager.calls == 0


def test_empty_task_is_rejected(tmp_path):
    orchestrator = AgentOrchestrator(
        FakeAgentManager(),
        tmp_path / "audit.jsonl",
    )

    with pytest.raises(ValueError):
        orchestrator.plan("   ")


def test_agent_exception_is_recorded(tmp_path):
    class BrokenManager(FakeAgentManager):
        def run(self, task):
            raise RuntimeError("controlled test failure")

    audit = tmp_path / "audit.jsonl"
    manager = BrokenManager(FakeAgent("FileAgent"))
    orchestrator = AgentOrchestrator(manager, audit)

    result = orchestrator.run("list workspace")

    assert result["status"] == "failed"
    assert "controlled test failure" in result["output"]
    assert audit.exists()
