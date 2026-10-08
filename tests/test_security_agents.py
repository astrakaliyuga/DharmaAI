from pathlib import Path

from agents.file_agent import FileAgent
from agents.shell_agent import ShellAgent


def test_shell_operator_is_rejected(tmp_path):
    agent = ShellAgent()
    marker = tmp_path / "should_not_exist"

    result = agent.run(
        f"run whoami; touch {marker}"
    )

    assert "rejected" in result.lower()
    assert not marker.exists()


def test_shell_command_uses_restricted_allowlist():
    agent = ShellAgent()

    result = agent.run("run id")

    assert "not allowed" in result.lower()


def test_shell_cat_cannot_read_outside_workspace(tmp_path):
    agent = ShellAgent()
    secret = tmp_path / "outside.txt"
    secret.write_text("NOT_FOR_AGENT")

    result = agent.run(f"run cat {secret}")

    assert "rejected" in result.lower()
    assert "NOT_FOR_AGENT" not in result


def test_file_agent_blocks_parent_traversal(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    agent = FileAgent(str(workspace))

    result = agent.run("write ../escaped.txt blocked")

    assert "blocked" in result.lower()
    assert not (tmp_path / "escaped.txt").exists()


def test_file_agent_normal_operations_work(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    agent = FileAgent(str(workspace))

    assert "Written" in agent.run(
        "write sample.txt hello world"
    )
    assert agent.run("read sample.txt") == "hello world"
    assert "Deleted" in agent.run("delete sample.txt")
    assert not (workspace / "sample.txt").exists()


def test_file_agent_blocks_symlink_escape(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside = tmp_path / "outside"
    outside.mkdir()
    secret = outside / "secret.txt"
    secret.write_text("PRIVATE")

    link = workspace / "shortcut"
    link.symlink_to(outside, target_is_directory=True)

    agent = FileAgent(str(workspace))
    result = agent.run("read shortcut/secret.txt")

    assert "blocked" in result.lower()
    assert "PRIVATE" not in result
