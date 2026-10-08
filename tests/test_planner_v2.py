import pytest

from core.planner import TaskPlanner


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.last_prompt = None

    def generate(self, prompt):
        self.last_prompt = prompt
        return self.response


class FakeAgent:
    def __init__(self, name):
        self.name = name


class FakeAgentManager:
    def find_agent(self, task):
        if task.startswith("list "):
            return FakeAgent("FileAgent")
        if task.startswith("run "):
            return FakeAgent("ShellAgent")
        return None


def test_goal_generates_structured_plan():
    client = FakeClient(
        '{"steps":["list workspace","list workspace"]}'
    )
    planner = TaskPlanner(client=client)

    result = planner.plan_goal(
        "Inspect the project workspace"
    )

    assert result["source"] == "local_llm"
    assert result["status"] == "proposed"
    assert result["requires_review"] is True
    assert len(result["steps"]) == 2


def test_plan_rejects_malformed_json():
    planner = TaskPlanner(client=FakeClient("not JSON"))

    with pytest.raises(ValueError):
        planner.plan_goal("Inspect workspace")


def test_plan_rejects_too_many_steps():
    tasks = [
        "list workspace"
        for _ in range(TaskPlanner.MAX_STEPS + 1)
    ]
    planner = TaskPlanner(client=FakeClient(
        __import__("json").dumps({"steps": tasks})
    ))

    with pytest.raises(ValueError):
        planner.plan_goal("Inspect workspace")


def test_plan_rejects_unsupported_agent_task():
    planner = TaskPlanner(
        client=FakeClient('{"steps":["launch rocket"]}')
    )

    with pytest.raises(ValueError, match="Unsupported"):
        planner.plan_goal(
            "Do something",
            agent_manager=FakeAgentManager(),
        )


def test_shell_step_requires_approval():
    planner = TaskPlanner(
        client=FakeClient('{"steps":["run whoami"]}')
    )

    result = planner.plan_goal(
        "Check current user",
        agent_manager=FakeAgentManager(),
    )

    assert result["steps"][0]["approval_required"] is True


def test_empty_model_plan_is_rejected():
    planner = TaskPlanner(client=FakeClient('{"steps":[]}'))

    with pytest.raises(ValueError):
        planner.plan_goal("Do something")


def test_v1_api_remains_available():
    result = TaskPlanner().plan(["list workspace"])

    assert result["steps"][0]["task"] == "list workspace"
    assert result["source"] == "explicit"


def test_goal_length_is_bounded():
    planner = TaskPlanner(client=FakeClient('{"steps":["list workspace"]}'))

    with pytest.raises(ValueError):
        planner.plan_goal("x" * 2001)
