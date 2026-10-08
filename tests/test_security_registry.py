from tools.security_registry import SecurityToolRegistry


def test_registry_lists_security_tools():
    registry = SecurityToolRegistry()
    names = {tool["name"] for tool in registry.list_tools()}
    assert {"nmap", "whatweb", "nikto", "nuclei", "sqlmap", "gobuster", "ffuf"} <= names


def test_registry_detects_installed_status():
    registry = SecurityToolRegistry()
    for tool in registry.list_tools():
        assert isinstance(tool["installed"], bool)


def test_recommendation_does_not_execute_tools():
    registry = SecurityToolRegistry()
    result = registry.recommend("Check network ports")
    assert result["status"] == "recommendations_only"
    assert result["executed"] is False
    assert result["requires_authorization"] is True
    assert any(tool["name"] == "nmap" for tool in result["tools"])


def test_recommendation_matches_sql_injection():
    result = SecurityToolRegistry().recommend("Test for SQL injection")
    assert any(tool["name"] == "sqlmap" for tool in result["tools"])
    assert result["executed"] is False


def test_unknown_tool_returns_none():
    assert SecurityToolRegistry().get_tool("unknown-tool") is None


def test_empty_goal_is_rejected():
    try:
        SecurityToolRegistry().recommend(" ")
    except ValueError:
        pass
    else:
        raise AssertionError("Empty goal should be rejected")
